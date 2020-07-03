# Eye-tracking-device
## Eye-tracking WebApp
Integrate WebGazer.js into a Flask Framework.

### Currently Working on:
* Save coordinates to models.py
* Phase 2


## Goals
### Phase 1: Get webgaze.js working
* Integrate webgazer.js into the flask webapp (single page)
* start webgazer, which starts collecting points in which and transmitting the data to the backend
* upon ending (have a button that ends the process), stop the webgazer (webgazer.end();) and stop transmitting data
* save the coordinates to models py (Revision: Save to session, we will not store the images and their respective data)

### Phase 2: Upload functions
* allow users to upload a design
* when the design is shown, webgzer begins 
* after the process is ended (user ends the detection process), the detection is saved
* the positions are evaluated, outputting a heatmap of where the user looks at on the design (make sure that the gaze coordinates that were outside of the boundaries of the uploaded designs are filtered out)

### Phase 3: Completion
* add complementary features to make the process easier
* add calibration so that eyetracking could be better (webgazer does not require calibration but relies on user's interaction with the interface, the more the user interacts with the webpage, the more accurate webgazer is, therefore, having an initial interaction where we induce users to click on stuff could improve the accuracy of the webgazer when they user views the designs)

## Set up Project
### Create a Virtual Environment

```bash
$ python3 -m virtualenv venv
```
To activate the virtual environment, run:

```bash
$ source venv/bin/activate
```

## Installing Dependencies
To successfully run the application, dependencies are required, please run:

```bash
$ pip3 install -r requirements.txt 
```

## Setting up a database:
We use a sqlite database in this project, to set up the database, go to the terminal and enter:

```bash
$ python3
```

Once your on the python console, enter the following commands:

```bash
$ from EyeTracking import db
$ db.drop_all()
$ db.create_all()
```

## Running the application
Once you installed everything necessary, go to the root directory of the project and run:

```bash
$ python3 app.py
```

## Run on HTTPS
Refer to [this link](https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/) to generate SSL keys (using method 2)<br>
Make directory:
```bash
$ mkdir cert 
$ cd cert 
```
Make sure to install ```pyopenssl```
```bash
$ pip intsall pyopenssl
```
Run the following to create the needed certificates in the ```cert``` folder
```bash
$ openssl genrsa -des3 -out server.key 1024
$ # fill in some info
$ openssl req -new -key server.key -out server.csr
$ # fill in more info with the same key as server.key
$ cp server.key server.key.org 
$ openssl rsa -in server.key.org -out server.key
$ openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

