# How to run

To run the Application:
1. clone the repository using `git clone https://github.com/adityaa-chandramohan/ReactApp.git` command. Then navigate to ReactApp folder in CLI.

2. run `docker build -t server backend/.`  to create docker image (the backend - Flask + Postgres).

3. run `docker buiild -t ui frontend/.`    to create docker image (the frontend - React APP)

4. run `docker-compose up` to run the container. 

Wait for few mins for the containers to start and UI will be up [`http://localhost:3000/`]

# Description (Features)

1. Register as new user.
   - There are some validations done in UI and backend to avoid input of malicious character. 
   - Password length must be between 8 and 32
   - Password is stored encrypted in database using bcrypt.
   - sample entry E.g: Name - TestUser , Email - TestUser@gmail.com , Password - T3stUs3r?11

2. Landing page. 
   - The login date time and the ip from which current user logged in are displayed.
   - Every login attempt will be stored in the database , but only the current successful login will be displayed. If there is a           new version of this app in future, will include logic to show the number of failed attempts before the current successful login attempt.
   - Currently the upload image feature is not available. This will be handled in future version.
   
3. Login as user.
   - Once user is registered successfully, user can login with email id and password. 
   - Multiple users with same email address is not allowed to register in the app. 
      
