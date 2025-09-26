from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'railway_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StationDrawing(db.Model):
    __tablename__ = 'station_drawing'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    checksum = db.Column(db.String(100))
    station_id = db.Column(db.String(100))  # Changed to String to match xlsx
    diagram_name = db.Column(db.String(200))
    station_name = db.Column(db.String(200))
    station_code = db.Column(db.String(50))
    version = db.Column(db.String(50))
    date = db.Column(db.String(100))
    drawn_by = db.Column(db.String(200))
    checked_by = db.Column(db.String(200))
    division = db.Column(db.String(200))
    zone = db.Column(db.String(200))
    total_sheet = db.Column(db.String(50))
    designation1 = db.Column(db.String(200))
    designation2 = db.Column(db.String(200))
    designation3 = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class JunctionBox(db.Model):
    __tablename__ = 'junction_box'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    station_id = db.Column(db.String(100))
    junction_id = db.Column(db.String(100))
    junction_name = db.Column(db.String(200))
    latitude = db.Column(db.String(100))  # Keep as String to handle empty values
    longitude = db.Column(db.String(100))
    junction_size = db.Column(db.String(100))
    junction_row = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Circuit(db.Model):
    __tablename__ = 'circuit'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    circuit_id = db.Column(db.String(100))
    circuit_name = db.Column(db.String(200))
    junction_box = db.Column(db.String(200))
    junction_name = db.Column(db.String(200))
    row = db.Column(db.String(50))
    position = db.Column(db.String(50))
    terminal = db.Column(db.String(100))
    start_no = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Terminal(db.Model):
    __tablename__ = 'terminal'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    circuit_id = db.Column(db.String(100))
    terminal_id = db.Column(db.String(100))
    terminal_name = db.Column(db.String(200))
    symbol = db.Column(db.String(100))
    input_left = db.Column(db.String(200))
    input_right = db.Column(db.String(200))
    spare = db.Column(db.String(50))
    input_connected = db.Column(db.String(200))
    output_connected = db.Column(db.String(200))
    output_left = db.Column(db.String(200))
    output_right = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Group(db.Model):
    __tablename__ = 'group_table'  # 'group' is reserved in PostgreSQL
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    circuit_id = db.Column(db.String(100))
    group_id = db.Column(db.String(100))
    terminal_no = db.Column(db.String(100))
    input_output = db.Column(db.String(100))
    text = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class TerminalHeader(db.Model):
    __tablename__ = 'terminal_header'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    circuit_id = db.Column(db.String(100))
    header_type = db.Column(db.String(100))
    terminal_start = db.Column(db.String(100))
    terminal_end = db.Column(db.String(100))
    input_output = db.Column(db.String(100))
    text = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class ChokeTable(db.Model):
    __tablename__ = 'choke_table'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    circuit_id = db.Column(db.String(100))
    choke_id = db.Column(db.String(100))
    input_terminal = db.Column(db.String(100))
    output_terminal = db.Column(db.String(100))
    terminal_name = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class ResistorTable(db.Model):
    __tablename__ = 'resistor_table'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('railway_projects.id'), nullable=False)
    circuit_id = db.Column(db.String(100))
    resistor_id = db.Column(db.String(100))
    input_terminal = db.Column(db.String(100))
    output_terminal = db.Column(db.String(100))
    resistor_name = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
