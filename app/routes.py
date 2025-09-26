import io
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash, session
from openpyxl import Workbook
from .models import (db, Project, StationDrawing, JunctionBox, Circuit, 
                     Terminal, Group, TerminalHeader, ChokeTable, ResistorTable)
from .schemas import SHEETS, HEADER_HINTS

bp = Blueprint("main", __name__)

# Model mapping for dynamic access based on sheet names
MODEL_MAP = {
    "StationDrawing": StationDrawing,
    "junction_box": JunctionBox,
    "circuit": Circuit,
    "terminal": Terminal,
    "group": Group,
    "terminal_header": TerminalHeader,
    "choketable": ChokeTable,
    "resistortable": ResistorTable,
}

def get_current_project():
    """Get or create current project in session"""
    if 'project_id' not in session:
        # Create new project
        project = Project(
            name=f"RailwayProject_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description="Generated from Flask XLSX Builder"
        )
        db.session.add(project)
        db.session.commit()
        session['project_id'] = project.id
        flash(f"Created new project: {project.name} (ID: {project.id})")
    return session['project_id']

@bp.route("/")
def index():
    """Main page showing all sheets with row counts"""
    project_id = get_current_project()
    current_project = Project.query.get(project_id)
    
    # Get row counts for each sheet
    table_counts = {}
    total_rows = 0
    for sheet_name, model in MODEL_MAP.items():
        count = model.query.filter_by(project_id=project_id).count()
        table_counts[sheet_name] = count
        total_rows += count
    
    return render_template("index.html", 
                         tables=table_counts, 
                         current_project=current_project,
                         total_rows=total_rows)

@bp.route("/sheet/<name>", methods=["GET", "POST"])
def sheet_form(name):
    """Handle form for individual sheets - add/edit/display"""
    if name not in SHEETS:
        flash(f"Unknown sheet: {name}")
        return redirect(url_for("main.index"))
    
    project_id = get_current_project()
    current_project = Project.query.get(project_id)
    model = MODEL_MAP[name]
    columns = SHEETS[name]
    
    # Check if editing existing row
    edit_id = request.args.get('edit', type=int)
    edit_row = None
    if edit_id:
        edit_row = model.query.filter_by(id=edit_id, project_id=project_id).first()
        if not edit_row:
            flash("Row not found")
            return redirect(url_for("main.sheet_form", name=name))
    
    if request.method == "POST":
        # Collect form data
        data = {}
        for col in columns:
            value = request.form.get(col, "").strip()
            data[col] = value if value else None
        
        # Check if at least one field has data
        if any(data.values()):
            data['project_id'] = project_id
            
            if edit_id and edit_row:
                # Update existing row
                for col, val in data.items():
                    if hasattr(edit_row, col):
                        setattr(edit_row, col, val)
                flash(f"Row updated in {name} for Project ID {project_id}")
            else:
                # Create new row
                try:
                    new_record = model(**data)
                    db.session.add(new_record)
                    flash(f"Row added to {name} for Project ID {project_id}")
                except Exception as e:
                    flash(f"Error adding row: {str(e)}")
                    db.session.rollback()
                    return redirect(url_for("main.sheet_form", name=name))
            
            db.session.commit()
        else:
            flash("Please fill at least one field")
            
        return redirect(url_for("main.sheet_form", name=name))
    
    # GET request - display form and existing data
    rows = model.query.filter_by(project_id=project_id).order_by(model.id).all()
    
    # Convert SQLAlchemy objects to dictionaries for easier template access
    rows_data = []
    for row in rows:
        row_dict = {}
        for col in columns:
            row_dict[col] = getattr(row, col, '')
        row_dict['id'] = row.id  # Keep the ID for edit/delete
        rows_data.append(row_dict)
    
    # Convert edit_row to dictionary if exists
    edit_row_dict = None
    if edit_row:
        edit_row_dict = {}
        for col in columns:
            edit_row_dict[col] = getattr(edit_row, col, '')
    
    return render_template("sheet_form.html",
                         sheet=name, 
                         columns=columns, 
                         rows=rows_data,
                         hint=HEADER_HINTS.get(name, ""),
                         edit_id=edit_id,
                         edit_row=edit_row_dict,
                         current_project=current_project)

@bp.route("/sheet/<name>/delete/<int:row_id>", methods=["POST"])
def delete_row(name, row_id):
    """Delete a specific row from database"""
    if name not in MODEL_MAP:
        flash("Invalid sheet name")
        return redirect(url_for("main.index"))
    
    project_id = get_current_project()
    model = MODEL_MAP[name]
    
    record = model.query.filter_by(id=row_id, project_id=project_id).first()
    if record:
        try:
            db.session.delete(record)
            db.session.commit()
            flash(f"Row deleted successfully from {name} (Project ID: {project_id})")
        except Exception as e:
            flash(f"Error deleting row: {str(e)}")
            db.session.rollback()
    else:
        flash("Row not found")
    
    return redirect(url_for("main.sheet_form", name=name))

@bp.route("/sheet/<name>/edit/<int:row_id>")
def edit_row(name, row_id):
    """Redirect to sheet form with edit parameter"""
    return redirect(url_for("main.sheet_form", name=name, edit=row_id))

@bp.route("/preview")
def preview():
    """Preview all data before download"""
    project_id = get_current_project()
    current_project = Project.query.get(project_id)
    
    table_data = {}
    total_records = 0
    for sheet_name, model in MODEL_MAP.items():
        records = model.query.filter_by(project_id=project_id).order_by(model.id).all()
        # Convert to dictionaries
        records_data = []
        for record in records:
            record_dict = {}
            for col in SHEETS[sheet_name]:
                record_dict[col] = getattr(record, col, '')
            records_data.append(record_dict)
        
        table_data[sheet_name] = records_data
        total_records += len(records_data)
    
    return render_template("preview.html", 
                         sheets=SHEETS, 
                         tables=table_data,
                         current_project=current_project,
                         total_records=total_records)

@bp.route("/download")
def download():
    """Generate and download XLSX file"""
    project_id = get_current_project()
    current_project = Project.query.get(project_id)
    
    # Create workbook
    wb = Workbook()
    default = wb.active
    wb.remove(default)

    total_records = 0
    # Add each sheet with data
    for sheet_name, columns in SHEETS.items():
        ws = wb.create_sheet(title=sheet_name)
        
        # Add headers
        ws.append(columns)
        
        # Add data from database
        model = MODEL_MAP[sheet_name]
        records = model.query.filter_by(project_id=project_id).order_by(model.id).all()
        
        for record in records:
            row = []
            for col in columns:
                # Get attribute value, default to empty string
                value = getattr(record, col, "")
                row.append(str(value) if value is not None else "")
            ws.append(row)
            total_records += 1

    # Save to memory and send
    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)
    
    filename = f"RAILWAYPROJECT_ID{project_id}_{current_project.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    flash(f"Downloaded {total_records} records from Project ID {project_id}")
    
    return send_file(
        bio,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@bp.route("/projects")
def list_projects():
    """List all projects with their IDs and row counts"""
    projects = Project.query.order_by(Project.created_date.desc()).all()
    
    # Get row counts for each project
    projects_data = []
    for project in projects:
        total_rows = 0
        sheet_counts = {}
        for sheet_name, model in MODEL_MAP.items():
            count = model.query.filter_by(project_id=project.id).count()
            sheet_counts[sheet_name] = count
            total_rows += count
        
        projects_data.append({
            'project': project,
            'total_rows': total_rows,
            'sheet_counts': sheet_counts
        })
    
    return render_template("projects.html", projects_data=projects_data)

@bp.route("/project/<int:project_id>/switch")
def switch_project(project_id):
    """Switch to different project"""
    project = Project.query.get_or_404(project_id)
    session['project_id'] = project.id
    flash(f"Switched to Project ID {project.id}: {project.name}")
    return redirect(url_for("main.index"))

@bp.route("/new_project", methods=["GET", "POST"])
def new_project():
    """Create new project"""
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if name:
            project = Project(name=name, description=description)
            db.session.add(project)
            db.session.commit()
            session['project_id'] = project.id
            flash(f"Created new Project ID {project.id}: {project.name}")
            return redirect(url_for("main.index"))
        else:
            flash("Project name is required")
    
    return render_template("new_project.html")

@bp.route("/project/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    """Delete entire project and all its data"""
    if project_id == session.get('project_id'):
        flash("Cannot delete current project. Switch to another project first.")
        return redirect(url_for("main.list_projects"))
    
    project = Project.query.get_or_404(project_id)
    
    try:
        # Count total records before deletion
        total_deleted = 0
        # Delete all related data
        for model in MODEL_MAP.values():
            count = model.query.filter_by(project_id=project_id).count()
            model.query.filter_by(project_id=project_id).delete()
            total_deleted += count
        
        # Delete project
        project_name = project.name
        db.session.delete(project)
        db.session.commit()
        flash(f"Project ID {project_id} '{project_name}' deleted successfully (Deleted {total_deleted} records)")
    except Exception as e:
        flash(f"Error deleting project: {str(e)}")
        db.session.rollback()
    
    return redirect(url_for("main.list_projects"))

@bp.route("/clear_current_project", methods=["POST"])
def clear_current_project():
    """Clear all data from current project but keep project"""
    project_id = get_current_project()
    
    try:
        total_deleted = 0
        # Delete all data for current project
        for model in MODEL_MAP.values():
            count = model.query.filter_by(project_id=project_id).count()
            model.query.filter_by(project_id=project_id).delete()
            total_deleted += count
        
        db.session.commit()
        flash(f"All data cleared from Project ID {project_id} (Deleted {total_deleted} records)")
    except Exception as e:
        flash(f"Error clearing project data: {str(e)}")
        db.session.rollback()
    
    return redirect(url_for("main.index"))
