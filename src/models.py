from src.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(50), nullable=False, unique=True) # e.g., Radiology, Cardiology etc.

    #Relationships
    staff_members = db.relationship('Staff', back_populates='department') 

    def __repr__(self):
        return f"<Department {self.department_name}>"

class Staff(db.Model, UserMixin):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False) # e.g., Radiology, Cardiology etc. Will be programmed to only allow certain values
    permissions = db.Column(db.String(100), nullable=False) # e.g., Super-user, Standard User etc. Will be programmed to only allow certain values

    #implement login capabilities
    username = db.Column(db.String(100), nullable = False, unique = True)
    password_hash = db.Column(db.String(255), nullable = False)

    #Relationships
    department = db.relationship('Department', back_populates='staff_members') # Assume staff members belong to one department

    # Password methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.staff_id)




    __table_args__ = (
        db.CheckConstraint("permissions IN ('Super-user', 'Standard User','Special User')",
        name = "check_permissions"),
    )

    def __repr__(self):
        return f"<Staff {self.name} - {self.department_id}>"
class Status(db.Model):
    __tablename__ = 'statuses'
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(50), nullable=False, unique=True) # e.g., In Transit, At Department, With Staff etc.

    #Relationships
    patient_files = db.relationship('PatientFile', back_populates='status')

    def __repr__(self):
        return f"<Status {self.status_name}>"

class PatientFile(db.Model):
    __tablename__ = 'patient_files'
    file_no = db.Column(db.Integer, primary_key=True, autoincrement=True) # Unique file number for each patient file
    patient_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False) # Date of Birth to help distinguish patients with similar names
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.status_id'), nullable=False) # Current status of the file

    #Relationships
    status = db.relationship('Status', back_populates='patient_files')

    def __repr__(self):
        return f"<PatientFile {self.patient_name} - {self.dob}>"

class FileLog(db.Model):
    __tablename__ = 'file_logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_no = db.Column(db.Integer, db.ForeignKey('patient_files.file_no'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc) ) # Timestamp of the log entry
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.status_id'), nullable=False) # Status of the file after this log entry

    # Relationships to be implemented later if needed

    def __repr__(self):
        return f"<FileLog File No: {self.file_no} - Status: {self.status_id}>"