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
from wtforms import Form, StringField, DateField, validators, PasswordField
import config

#initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

#initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models after initializing db to avoid circular imports
import models

with app.app_context():
    db.create_all()  # Create database tables if they don't exist

# define forms
class PatientForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    dob = DateField('Date of Birth', [validators.InputRequired()], format='%Y-%m-%d')


@app.route('/')
# Implement login functionality later
def home():
    return render_template('home.html') # Render the home page template. Pass required data later.

@app.route('/patients', methods=['GET', 'POST'])
# Implement login functionality later
def patients():

    if request.method == 'GET':
        # Handle search query
        form = PatientForm()

        return render_template('patients.html',form = form)
    elif request.method == 'POST':
        # Handle adding new patient and mark patient file as "out"
        form = PatientForm(request.form)
        message = "" # Placeholder for user feedback messages

        if form.validate():
            name = form.name.data
            dob = form.dob.data
            message = add_patient_file(name, dob)
        pass
    return redirect(url_for('home')) # Not sure if this is needed

# Implement modify_staff route later

#Functions Section - To be decided if they should be here or in a separate file
# Function to add a new patient file
def add_patient_file(name, new_dob):
    # In the workflow, the user will have determined that a new patient file is required

    from models import PatientFile

    try:
        new_file = PatientFile(
            patient_name=name,
            dob=new_dob,
            status_id=1  # Assuming '1' corresponds to the "file out" status in the statuses table
        )

        db.session.add(new_file)
        db.session.commit()
        return "Patient file added successfully."
    
    except Exception as e:
        db.session.rollback()
        return f"Error adding patient file: {str(e)}, please try again."



if __name__ == '__main__':
    app.run(debug=True)