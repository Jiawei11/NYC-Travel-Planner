#  Template

Build using Flask, see https://flask.palletsprojects.com/en/2.2.x/
The Flask html template is located in "app" folder, all the html templated are used
for this project

## Data preparation
All the required cleaned data files are stored in "database" folder
"transfer_zip.ipynb" is to transfer latitude and longitude into matched zipcodes
"data_cleaning.ipynb" is for data cleaning
The data files are already cleaned so you don't have to run above two files

## Inital DB
  1. You will need to create a databse with following using PostgreSQL
		host="localhost", 
    database="postgres",
    user="postgres",
    password="123"

  2. You will need to create table and insert value into databse by running "database.ipynb"

## Build and Running Instruction

  1. (Optional, you don't have to do this) Create a new virtual env
     ```python -m venv env```

	 Remember to activate the Env when you go to use it
	  
	 ```
	 source env/bin/activate
	 ```
     
  2. (Optional if you have everything already installed) Install Requirements
		every required packages are listed in REQUIREMENTS.txt

     ```
	 python -m pip install -r REQUIREMENTS.txt
	 ```

	 	you can also install those packages manually
	
  3. Run
	1. first direct to the directory to "app" folder, or where "views.py" located at
	 ```
	 cd C:\[file_directory]
	 ```
	2. next execute the statement below
     ```
	 python -m flask --app app/ --debug run
	 ```

The site should now be visible on 127.0.0.1:5000
If you are not able to exetute those statements above, simply add "app.run()"
at the end of "views.py" and run it in jupyter notebook.






	 

## Files

Some Supporting files

  - schema.sql
  
    Basic database schema to get you started
	
	You can build this by visiting the ```/initdb``` url

