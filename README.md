# patient-file-tracking Overview
## Aim:
Develop a python based tool that helps hospitals using paper-based patient files to track file locations. The aim is to help hospital staff avoid losing patient files, which can have dire consequences for the patient and the hospital. The ultimate solution is, of course, complete digitization of patient files, however, that process can take years to implement due to project cost, complexity and regulatory hurdles. This tool is meant to be a low cost and low complexity interim solution.

## Problem description
The current problem with locating patient files is that clerks cannot confirm if a file has not been returned - i.e. held by a health practioner - or if it has been mis-filed (not placed according to filing convention). This uncertainty means that if a file is not found in the place it should be, then more time is required to locate said file. Depending on the number of files and the size of the hospital, the time it takes to find the file may not be practical for a patient waiting to see a health practioner. Consequently, patients have new files opened which are then later included with the original file if it is finally located. This, unfortunately, means that the health practioner may not have the patient history the hospital has built, and would need to rely on the patient's memory. This puts the patient at risk if the health practioner misses something from the patient's history, and could, thus, place the hospital at risk of litigation.

## Solution description
This tool will allow clerks to scan a barcode attached to the file when issueing the files and scan again when the file is returned. This will allow clerks to eliminate either the possibility of mis-filing or the patient's file not being returned. Whenever a file is scanned out, a timestamp will be logged against that file number. If a patient's file has not been returned within 24 hours, and the patient has not been admitted, the file will be flagged. The list of flagged files can be discussed in daily staff meetings to ensure that the file is retrieved timeously.
The tool, depending on its implementation, also has the potential to collect data that can be used to analyze patient waiting times and identify bottle-necks in the different departments of the hospital. This is possible if each health practioner that receives the file, also scans the file to mark it as "received" and "transferred" after the patient consult. Since everytime this is done, a timestamp will be logged, it is possible to extract data on how long a patient spent in a certain department, between departments and how long it took before the patient could leave the hospital. An added benefit to this implementation is the file exchange log that will also be kept. This means that if a file is marked as overdue, the system can be checked to identify the last department to receive and/or transfer the file. This will help narrow down the search for the file. It will also promote accountability among hospital staff, as management can identify staff members that consistently neglect hospital file-keeping standards. 

# Roll-out plan
The project will be developed and rolled-out in stages. Stage 1, the proof of concept, will only involve the clerks. This will then, hopefully,
be tested in a real hospital setting and feedback incorporated in future versions. Stage 1 will include the following features: 
> adding of new patient;
> searching for patient in database;
> changing file status (in-storage or out)
> marking a patient as admitted
> display a list of files that are currently out and highlight files that are overdue
Stage 2 will introduce the roles of super-user and general staff. Super-user is critical, however the general staff access will be workshopped with the clients for final inclusion decision. The following are stage2 deliverables:
> Generate daily report with a list of overdue files and other metrics (TBC with client)
> Program Super-user functionality
> Program General-staff access (if approved)
If the General-staff access is approved, then stage 3 will include data analytics that can indicate patient wait times within the hospital as a whole and/or between departments. Otherwise, stage 3 may only include suggested new features from clients and bug fixes. 


# License

This project is licensed under the Apache License 2.0.

You are free to use, modify, and distribute this software, including in commercial
and institutional settings, provided that you include the original copyright notice
and license text in any copies or substantial portions of the software.

The Apache 2.0 license also provides explicit patent protection and liability disclaimers,
which makes it suitable for enterprise and healthcare environments where compliance
and risk management are critical.

For the full license text, see the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).


# Setup
---To be updated ---

# Database Design
The database consists of 3 tables with the given columns:

1. staff (Staff_ID; Staff_Name; Department; Permissions)
2. patient_file (File_No, Patient_Name, DOB, File_Status)
3. logs (File_No, File_Status, Staff_ID, Timestamp)

The staff table stores the staff_ID - set up currently as a autoincrement primary key, but can later be changed to match actual staff ids if they exist. 
The staff table also has a Permissions column that gives staff members different permissions in the system as follows:
a) Super-user: Has the rights to add/delete staff members to/from the database, and to assign/revoke user permissions.
b) General_staff: Has permission to change status of patient_file and to indicate if patient has been admitted.
c) Clerk: Has rights to add new patients in addition to General_staff permissions.
