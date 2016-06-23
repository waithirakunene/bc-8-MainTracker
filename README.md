# bc-8-MainTracker
 MaintenanceTrackorSystem
Maintenance Tracker is system to allow reporting of maintenance/repairs request by users on certain facilities, An admin keeps track of requests and can respond or reject them. The system will facilitate  maintenance process and escalate unusual delays.
##### Features
1. The admin for this app will be the person in charge of Facilities
As admin, I should be able to view all maintenance / repairs requests
2. As admin, I should be able to add names and contacts (phone number) for the people doing maintenance.
3. As admin, once maintenance is done, I should be able to mark it as resolved
4. As admin, I should be able to approve/reject a repair/maintenance request, and provide comments.
5. The app should be able to automatically send an SMS notification to the person that is to do maintenance. 
6. As a staff member, I should be able to report a maintenance or repair case (and upload a photo if necessary)
7. As a staff member, I should be able to get a notification (web), once the request has been approved/rejected by the adminFeatures

####Configurations.
While deploying the system the configuration variables inside the config.py will be expected.
+ MAINTRACTOR_ADMIN - A system admin is automatically assigned the admin role once signed up to the system.
+ MAIL_USERNAME  - the users username will be the email address.
+ MAIL_PASSWORD - this is the password the user sets.(maps to the MAIL_USERNAME).
+ SECRET_KEY - this automatically generates the authentication tokens and csrf tokens.

###How To Install The System.
* Clone the repository to your local machine.
<url>
* Install project dependencies using pip while inside a virtual enviroment.
* Initialize the database.
<command>
* Create the database and migrate its models.
<command>
* Run the server.
<command>
N/B View a live demo on heroku.com
<link>

####How The System Works.
A user who is an admin or a staff member is expected to sign up(register) after which an email is sent to him/her for confirmation.After a successful confirmation a user can now login.
The Admin and normal user(a staff member or a fellow) have different levels of authentication.
An admin can add the names and phone numbers for people,doing maintainance, can reject or approve a requests for repairs,can mark whether a task is resolved or its progress,and can view notifications for new request made.On the other hand a normal user can send requests for maintainace/repair and view its progress.
A normal user makes a request for maintainance and can view notifications after admin has approved.
A person in charge of maintainance can view new assignment to tasks,can view the task and update its progress.

###Bugs
Sometimes routes redirects breaks or page not found(error 400)



###Conclusions.
This app is build using Flask micro framework for python.
It has helped me master several skills on software backend and frontend development.
I have attained skills on:
* using Jinja boostrap
* How Client server requests works.
* Using SQLalchemy database
* Authenticating user logins.
* How to manage User Interface.
