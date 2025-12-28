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

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, validators, PasswordField
import config
from extensions import db

#initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

#initialize SQLAlchemy
db.init_app(app)
# Import models after initializing db to avoid circular imports
import models

with app.app_context():
    db.create_all()  # Create database tables if they don't exist

# define forms
class PatientForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    dob = DateField('Date of Birth', [validators.InputRequired()], format='%Y-%m-%d')

class add_PatientForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    dob = DateField('Date of Birth', [validators.InputRequired()], format='%Y-%m-%d')
    status_id = IntegerField('Status', [validators.InputRequired()])

@app.route('/')
# Implement login functionality later
def home():
    from models import PatientFile, Status

    out_files = PatientFile.query.join(Status).filter(Status.status_name == "Checked Out").all() # Assuming status_id=1 corresponds to "Out"
    return render_template('home.html', out_files = out_files) # Render the home page template. Pass required data later.

@app.route('/patients', methods=['GET', 'POST'])
# Implement login functionality later
def patients():

    if request.method == 'GET':
        # Handle search query
        form = PatientForm()

        search_name = request.args.get('search')

        if search_name:

            # Perform search in the database
            results = models.PatientFile.query.filter(models.PatientFile.patient_name == search_name).all()

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
def add_patient():
    
    form = add_PatientForm()
    
    return render_template('add_patients.html', form=form, statuses=models.Status.query.all())

# Implement modify_staff route later

#Functions Section - To be decided if they should be here or in a separate file
# Function to add a new patient file
def add_patient_file(name, new_dob, status):
    # In the workflow, the user will have determined that a new patient file is required

    from models import PatientFile

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
        return f"Error adding patient file: {str(e)}, please try again."



if __name__ == '__main__':
    app.run(debug=True)