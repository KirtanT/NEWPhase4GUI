Read Me: CS 4400 Phase IV Simple Airline Management System (SAMS)

Instructions to set up application: 
  Clone or download this repository to your computer.
  Create Python Virtual Environment
  Install Python dependencies:
    pip install Flask
    pip install mysql-connector-python

Instructions to run application: 
  Open a terminal inside the project directory.
  Run python app.py
  Open server URL.

Technologies Used:
  Flask: Python web framework used to build the web server and backend.
  HTML & Java Script: Used to render the homepage and structure the front end.
  MySQL: Used as the relational database system.

We built a Flask web application (with app.py as the file) that connects to a relational database. We wrote a db_config.py file that handles database connections using a function get_db_connection(). 
Furthermore, we defined multiple POST routes to allow inserting or updating information via stored procedures using input parameters. Moreover, we defined multiple GET routes to fetch summarized data from views. 
The application handles requests, manages database connections, and returns data in JSON format for easy interaction.


