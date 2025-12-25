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

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
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


@app.route('/')
# Implement login functionality later
def home():
    return render_template('home.html') # Render the home page template. Pass required data later.

@app.route('/patients', methods=['GET', 'POST'])
# Implement login functionality later
def patients():

    if request.method == 'GET':
        # Handle search query
        pass
    elif request.method == 'POST':
        # Handle adding new patient and mark patient file as "out"
        pass
    return render_template('patients.html') # Render the patients page template. Pass required data later.

# Implement modify_staff route later
if __name__ == '__main__':
    app.run(debug=True)