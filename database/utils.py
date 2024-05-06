from sqlalchemy.orm import Session
from sqlalchemy import update
from database.session import get_session

def update_record(model, record_id, field_name, new_value):
    """
    Update a field of a record in the database.
    
    Parameters:
        session (Session): The SQLAlchemy session.
        model (Base): The SQLAlchemy model class of the table.
        record_id (int): The ID of the record to update.
        field_name (str): The name of the column to update.
        new_value (any): The new value for the column.
    """
    # Access the model's field using Python's `getattr`
    if hasattr(model, field_name):
        # Perform the update
        with get_session() as session:
            session.query(model).filter(model.id == record_id).update({getattr(model, field_name): new_value})
            session.commit()
    else:
        raise ValueError(f"No such field {field_name} in the model {model.__name__}.")