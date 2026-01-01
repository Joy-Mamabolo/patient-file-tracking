from src import create_app
from src.extensions import db
import src.models as models
from flask_migrate import upgrade,migrate,init
import datetime

app = create_app("src.config.Config")

def setup_database():
    with app.app_context():

        try:
            init()
        except:
            # /migrations folder has already been created.
            pass

        migrate(message="Initial schema")
        upgrade()

        # Add sample data
        # Department table

        if not models.Department.query.first():
            db.session.add(models.Department(department_name = "Records")) # type:ignore 
            db.session.add(models.Department(department_name = "Cardiology")) # type:ignore
            db.session.add(models.Department(department_name = "Maternity")) # type:ignore
            db.session.add(models.Department(department_name = "Radiology")) # type:ignore
            db.session.commit()
        
        # Add staff table
        if not models.Staff.query.first():
            db.session.add(models.Staff(name = "John Smith", department_id = 1, permissions = "Super-user")) # type:ignore
            db.session.add(models.Staff(name = "Jane Doe", department_id = 4, permissions = "Standard User")) # type:ignore
            db.session.add(models.Staff(name = "Bob Johnson", department_id = 1, permissions = "Special User")) # type:ignore
            db.session.add(models.Staff(name = "Alice Williams", department_id = 3, permissions = "Standard User")) # type:ignore
            db.session.add(models.Staff(name = "Charlie Brown", department_id = 2, permissions = "Standard User")) # type:ignore
            db.session.commit()

        # Status table
        if not models.Status.query.first():
            db.session.add(models.Status(status_name = "Checked In")) # type:ignore
            db.session.add(models.Status(status_name = "Checked Out")) # type:ignore
            db.session.add(models.Status(status_name = "Admitted")) # type:ignore
            db.session.commit()
        # Patient file table
        if not models.PatientFile.query.first():
            db.session.add(models.PatientFile(patient_name = "Emily Davis", dob = datetime.date(1985,4,12), status_id = 1)) # type:ignore
            db.session.add(models.PatientFile(patient_name = "Michael Wilson", dob = datetime.date(1990,9,23), status_id = 2)) # type:ignore
            db.session.add(models.PatientFile(patient_name = "Sarah Miller", dob = datetime.date(1978,11,5), status_id = 3)) # type:ignore
            db.session.add(models.PatientFile(patient_name = "David Anderson", dob = datetime.date(1965,2,17), status_id = 1)) # type:ignore
            db.session.add(models.PatientFile(patient_name = "Laura Thomas", dob = datetime.date(2000,7,30), status_id = 2)) # type:ignore
            db.session.commit()

if __name__ == "__main__":
    setup_database()
    print("Database setup complete with latest schema and sample data.")
