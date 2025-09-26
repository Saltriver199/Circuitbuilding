# Complete column schemas extracted from RAILWAYPROJECT.xlsx - all 8 sheets
SHEETS = {
    "StationDrawing": [
        "checksum", "Station ID", "diagram_name", "station_name", "station_code",
        "version", "date", "drawn_by", "checked_by", "division", "zone",
        "total_sheet", "designation1", "designation2", "designation3"
    ],
    "junction_box": [
        "station_id", "junction_id", "junction_name", "latitude", "longitude",
        "junction_size", "junction_row"
    ],
    "circuit": [
        "circuit_id", "circuit_name", "junction_box", "junction_name", "row",
        "position", "terminal", "start_no"
    ],
    "terminal": [
        "circuit_id", "terminal_id", "terminal_name", "symbol", "input_left",
        "input_right", "spare", "input_connected", "output_connected",
        "output_left", "output_right"
    ],
    "group": [
        "circuit_id", "group_id", "terminal_no", "input_output", "text"
    ],
    "terminal_header": [
        "circuit_id", "header_type", "terminal_start", "terminal_end", "input_output", "text"
    ],
    "choketable": [
        "circuit_id", "choke_id", "input_terminal", "output_terminal", "terminal_name"
    ],
    "resistortable": [
        "circuit_id", "resistor_id", "input_terminal", "output_terminal", "resistor_name"
    ]
}

HEADER_HINTS = {
    "StationDrawing": "Enter station metadata (checksum, IDs, names, zone, totals, designations).",
    "junction_box": "Enter each junction box with coordinates and size/rows if available.",
    "circuit": "Define each circuit: names, junctions, row/position, terminal count, start number.",
    "terminal": "Define terminal details: symbols, connections, spare status, inputs/outputs.",
    "group": "Group terminals by circuit with terminal numbers and input/output descriptions.",
    "terminal_header": "Define headers (WIREFROM/WIRETO/RELAY), terminal ranges, and connection notes.",
    "choketable": "Define choke components with input/output connections for circuit filtering.",
    "resistortable": "Define resistor components with input/output terminals and resistance values.",
}
