# Copyright (c) 2025 Joy_M
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from src import create_app, db, models
from flask import render_template, request, redirect, url_for, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, validators, PasswordField, SubmitField
from functools import wraps
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from src.models import PatientFile,Status, FileLog
from src.config import Config
from flask_login import(
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
    UserMixin  
)

app = create_app(Config)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# define forms
class PatientForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    dob = DateField('Date of Birth', [validators.InputRequired()], format='%Y-%m-%d')

class add_PatientForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    dob = DateField('Date of Birth', [validators.InputRequired()], format='%Y-%m-%d')
    status_id = IntegerField('Status', [validators.InputRequired()])

class login_form(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Submit')


@login_manager.user_loader
def load_user(staff_id):
    return db.session.get(models.Staff, int(staff_id))

# Authorization decorator
def Role_Required(*role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args,**kwargs):
            if not current_user.permissions in role:
                abort(403)
            return fn(*args, *kwargs)
        return decorated_view
    return wrapper

@app.route('/login', methods = ['GET', 'POST']) #Login Screen route
def login():

    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page or url_for('home'))

    form = login_form()

    if request.method == "POST":

        if form.validate_on_submit():

            user = models.Staff.query.filter_by(username = form.username.data).first()

            if user and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')

                return redirect(next_page or url_for('home'))
            else:
                flash("Invalid username and password.", 'danger')

    return render_template("login.html", form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/update_login', methods=['GET','POST'])
def update_login():
    return render_template("")

# To be implemented later
@app.route('/add_staff', methods = ["GET","POST"])
@login_required
@Role_Required("Super-user")
def add_staff():
    return render_template("")

# Global Variable for overdue interval
OVERDUE_INTERVAL = 24*60*60# Takes only seconds. All other units must be converted. Currently 24hrs


@app.route('/')
# Implement login functionality later
def home():
    #from src.models import PatientFile, Status

    # Subquery to return the latest timestamp of all files to be used to extract the latest timestamp of checked out files
    latest_log_subq = db.session.query(models.FileLog.file_no,
                                       func.max(models.FileLog.timestamp).label("latest_timestamp")
                                       ).group_by(models.FileLog.file_no).subquery()
    
    # Join above subquery to PatientFile entries filtered for "checked out" statuses
    query = (db.session.query(PatientFile, latest_log_subq.c.latest_timestamp)
                 .join(Status)
                 .join(latest_log_subq, PatientFile.file_no==latest_log_subq.c.file_no)
                 .filter(Status.status_name=="Checked Out"))


    out_files = query.all() # Checked out files view

    # Overdue files
    overdue_files = []
    due_date = []

    for file in out_files:

        if is_overdue(file[1]):
            overdue_date = file[1] + timedelta(seconds = OVERDUE_INTERVAL)
            overdue_by = datetime.now().replace(tzinfo=None) - overdue_date

            due_date.append((overdue_date, overdue_by.days))
            overdue_files.append(file)

    return render_template('home.html', out_files = out_files, overdue_files=zip(overdue_files, due_date)) # Render the home page template. Pass required data later.

@app.route('/patients', methods=['GET', 'POST'])
@login_required # Login implementation
def patients():

    if request.method == 'GET':
        # Handle search query
        form = PatientForm()

        search_name = request.args.get('search')

        if search_name:

            # Perform search in the database
            results = models.PatientFile.query.filter(models.PatientFile.patient_name.ilike(f"%{search_name}%") ).all()

            if results:
                return render_template('patients.html', form=form, patients=results)
            else:
                return render_template('patients.html', form=form, patients = None, search=search_name)

        return render_template('patients.html',form = form)
    elif request.method == 'POST':
        # Handle adding new patient and mark patient file as "out"
        form = add_PatientForm(request.form)
        message = "" # Placeholder for user feedback messages

        print(request.form)

        if form.validate_on_submit():
            name = form.name.data
            dob = form.dob.data
            status = form.status_id.data
            message = add_patient_file(name, dob, status)
        
        return render_template('add_patients.html', form=form, message=message, statuses=models.Status.query.all())
    return redirect(url_for('home')) # Not sure if this is needed

@app.route('/add_patient')
@login_required #login implementation
@Role_Required("Super-user","Special User")
def add_patient():
    
    form = add_PatientForm()
    
    return render_template('add_patients.html', form=form, statuses=models.Status.query.all())

@app.route('/change_status/<int:file_no>', methods=['POST'])
@login_required
def change_status(file_no):

    # retrieve the patient file by file_no
    #from src.models import PatientFile, Status

    patient_file = PatientFile.query.get(file_no)

    if not patient_file:
        return "Patient file not found.", 404

    if patient_file.status_id == 1:  # Assuming status_id=1 corresponds to "Checked In"
        patient_file.status_id = 2  # Assuming status_id=2 corresponds to "Checked Out"
    else:
        patient_file.status_id = 1  # Change back to "Checked In"
    
    db.session.commit()

    add_file_log(file_no, current_user.staff_id, patient_file.status_id)

    #debug
    #logs = FileLog.query.filter_by(file_no=file_no).all()
    #print(logs[-1])

    return redirect(url_for('patients'))

# Implement modify_staff route later

#Functions Section - To be decided if they should be here or in a separate file
# Function to add a new patient file
def add_patient_file(name, new_dob, status):
    # In the workflow, the user will have determined that a new patient file is required

    #from src.models import PatientFile

    try:
        new_file = PatientFile(
            patient_name=name, # type: ignore
            dob=new_dob, # type: ignore
            status_id=status  # type: ignore
        )

        db.session.add(new_file)
        db.session.commit()
        return "Patient file added successfully."
    
    except Exception as e:
        db.session.rollback()
        return f"Error adding patient file, please try again."

def add_file_log(file_no, staff_id, status_id):
    #from models import FileLog

    try:
        new_log = FileLog(
            file_no=file_no, # type: ignore
            staff_id=staff_id, # type: ignore
            status_id=status_id, # type: ignore
            #timestamp=timestamp # No longer necessary. A default time now will be captured in the utc timezone
        )

        db.session.add(new_log)
        db.session.commit()
        return "File log added successfully."
    
    except Exception as e:
        db.session.rollback()
        return f"Error adding file log, please try again."

def is_overdue(dt):
    # Function determines if a file is overdue and returns True or False

    

    now = datetime.now(timezone.utc)

    # For difference calculation, make both dates timezone naive, since they are both consistently UTC. 
    # Even though this may not be the timezone of the user, it is irrelevant when calculating the difference

    now_naive = now.replace(tzinfo = None)
    dt_naive = dt.replace(tzinfo = None)


    diff = now_naive-dt_naive

    if diff.total_seconds()>=OVERDUE_INTERVAL: # Fix this line when
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)