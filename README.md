# facial-recognition-flask-app
This app uses the face-recognition and opencv python libraries to display the user on a live video feed with a red box over their face displaying their name.<br>
The app also displays a percentage level of confidence 

Utilises Flask and SocketIO as well as waitress to allow multiple clients to connect to the server.

In order to launch the application you need to install the packages from requirements.txt<br>
`pip install requirements.txt`

Start the Flask app with:<br>
`python3 server.py`<br>
The app should launch at http://localhost:8080 or http://local_ip:8080 <br>

You can get your computers ip address via the ipconfig command on Windows or ifconfig on Linux and Mac OS


![Image](images/face-image.png)
