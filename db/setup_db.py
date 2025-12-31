from src import create_app
from src.extensions import db
import src.models as models
from flask_migrate import upgrade

app = create_app("src.config.Config")

def setup_database():
    with app.app_context():
        upgrade()

        # Add sample data
        # Department table

        if not models.Department.query().first():
            db.session.add(models.Department(department_name = "Records"))
            db.session.add(models.Department(department_name = "Cardiology"))
            db.session.add(models.Department(department_name = "Maternity"))
            db.session.add(models.Department(department_name = "Radiology"))
        
        # Add staff table
        if not models.Staff.query().first():
            db.session.add(models.Staff(name = "John Smith", department_id = 1, permissions = "Super-user"))
            db.session.add(models.Staff(name = "Jane Doe", department_id = 4, permissions = "Standard User"))
            db.session.add(models.Staff(name = "Bob Johnson", department_id = 1, permissions = "Special User"))
            db.session.add(models.Staff(name = "Alice Williams", department_id = 3, permissions = "Standard User"))
            db.session.add(models.Staff(name = "Charlie Brown", department_id = 2, permissions = "Standard User"))
        

        # Status table
        if not models.Status.query().first():
            db.session.add(models.Status(status_name = "Checked In"))
            db.session.add(models.Status(status_name = "Checked Out"))
            db.session.add(models.Status(status_name = "Admitted"))
        
        # Patient file table
        if not models.PatientFile.query().first():
            db.sessions.add(models.PatientFile(patient_name = "Emily Davis", dob = "1985-04-12", status_id = 1))
            db.sessions.add(models.PatientFile(patient_name = "Michael Wilson", dob = "1990-09-23", status_id = 2))
            db.sessions.add(models.PatientFile(patient_name = "Sarah Miller", dob = "1978-11-05", status_id = 3))
            db.sessions.add(models.PatientFile(patient_name = "David Anderson", dob = "1965-02-17", status_id = 1))
            db.sessions.add(models.PatientFile(patient_name = "Laura Thomas", dob = "2000-07-30", status_id = 2))

if __name__ == "__main__":
    setup_database()
    print("Database setup complete with latest schema and sample data.")
