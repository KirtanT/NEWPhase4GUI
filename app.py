from flask import Flask, request, jsonify, render_template
from db_config import get_db_connection
import datetime

app = Flask(__name__)

# linking flask to html site
@app.route('/')
def index():
    return render_template('index.html')

# route the procedure call back to the html doc
@app.route('/procedure', methods=['POST'])
def prun():
    data = request.get_json()
    procedure_name = data.get('procedure_name')     #grabbing the procedure inputs to input into DB
    inputs = data.get('inputs', [])
    try:
        results = pcall(procedure_name, inputs)
        return jsonify(results)
    except KeyError as key:
        return jsonify({'error': 'Primary key cannot be null: ' + str(key)}), 400
    except ValueError as value:
        return jsonify({'error': {str(value)}}), 400
    except Exception as exc:
        return jsonify({"Error calling" + str(procedure_name) + ':' + str(exc)}), 500
    
# create funciton for stored procedures by accessing flight tracking DB
def pcall(procedure_name, inputs):
    connection = get_db_connection()    # linking inputs to the DB in db_config.py
    cursor = connection.cursor()
    try:
        cursor.callproc(procedure_name, inputs)
        results = []
        for result in cursor.stored_results():
            cols = [d[0] for d in result.description]
            for row in result.fetchall():
                results.append(dict(zip(cols, row)))
        connection.commit()
        return results
    finally:
        cursor.close()
        connection.close()

@app.route('/view/<view>', methods=['GET'])
def vrun(view):
    if view not in ['flights_in_the_air', 'flights_on_the_ground', 'people_in_the_air', 'people_on_the_ground', 'route_summary', 'alternative_airports']:
        return 'View not found', 404
    try:
        data = vcall(view)
        return jsonify(data)
    except ValueError as value:
        return jsonify({f"Bad request on {view}: {value}"}), 400
    except Exception as exc:
        return jsonify({f"Server Error fetching {view}: {exc}"}), 500
    
# create function for view call using input from vrun
def vcall(view):
    connection = get_db_connection()    # linking inputs to the DB in db_config.py
    cursor = connection.cursor()
    try:
        cursor.execute(f"select * from {view}")
        cols = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        output = []
        # turning the DB table into dict format
        for row in rows:
            rec = {}
            for col, val in zip(cols, row):
                if isinstance(val, datetime.timedelta):    # making sure to avoid unserializable object in JSON
                    rec[col] = str(val)
                elif isinstance(val, (datetime.date, datetime.time, datetime.datetime)):
                    rec[col] = val.isoformat()
                else:
                    rec[col] = val
            output.append(rec)
        return output
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
