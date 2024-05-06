import os

def ensure_directory_for_sqlite(db_url):
    if db_url.startswith('sqlite:///'):
        db_path = db_url.replace('sqlite:///', '')
        
        if os.path.isabs(db_path):
            full_db_path = db_path
        else:
            project_root = find_project_root(os.path.abspath(__file__))
            full_db_path = os.path.join(project_root, db_path)
        
        db_dir = os.path.dirname(full_db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

def find_project_root(current_path):
    root_marker = '.git'
    while current_path != os.path.dirname(current_path):
        if os.path.exists(os.path.join(current_path, root_marker)):
            return current_path
        current_path = os.path.dirname(current_path)
    raise FileNotFoundError("Project root not found.")
