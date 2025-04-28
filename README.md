Instructions to Set Up Application
Clone or download this repository to your computer.

Create a Python Virtual Environment.

Install Python dependencies:

pip install Flask

pip install mysql-connector-python

Instructions to Run Application
Open a terminal inside the project directory.

Run python app.py.

Open the server URL.

Technologies Used
Flask: Python web framework used to build the web server and backend.

HTML & JavaScript: Used to render the homepage and structure the front end.

MySQL: Used as the relational database system.

Project Description
We built a Flask web application (app.py) that connects to a relational database.
A db_config.py file was created to handle database connections using the function get_db_connection().

We defined multiple POST routes to insert or update information via stored procedures using input parameters.
We also defined multiple GET routes to fetch summarized data from views.

The application:

Handles HTTP requests,

Manages database connections,

Returns data in JSON format for easy interaction.
