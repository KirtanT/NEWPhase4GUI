from flask import Flask, request, jsonify, render_template
from db_config import get_db_connection
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# route the procedure call back to the html doc
@app.route('/procedure', methods=['POST'])
def prun():
    data = request.get_json()
    procedure_name = data.get('procedure_name')     #grabbing the procedure inputs to input into DB
    inputs = data.get('inputs', [])

    # error catching
    try:
        results = pcall(procedure_name, inputs)
        return results
    except KeyError as ke:
        return jsonify({'error': f'Missing required field: {str(ke)}'}), 400
    except ValueError as ve:
        return jsonify({'error': {str(ke)}}), 400
    except Exception as e:
        return jsonify({f"Unexpected error calling procedure {procedure_name}: {str(e)}"}), 500
    
# create funciton for stored procedures by accessing flight tracking DB
def pcall(procedure_name, inputs):      # using inputs from prun
    connection = get_db_connection()
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
    # making sure view exists
    if view not in {
        'flights_in_the_air', 'flights_on_the_ground',
        'people_in_the_air', 'people_on_the_ground',
        'route_summary', 'alternative_airports'}:
        return 'View not found', 404
    # catching any errors
    try:
        data = vcall(view)
        return jsonify(data)
    except ValueError as ve:
        return jsonify({f"Bad request on {view}: {ve}"}), 400
    except Exception as e:
        return jsonify({f"Unexpected server error when fetching view {view}: {e}"}), 500
    
# create function for view call using input from vrun
def vcall(view):
    connection = get_db_connection()
    cursor = connection.cursor()
    # put it in a try block to make sure there aren't unexpected errors
    try:
        cursor.execute(f"select * from {view}")
        cols = [d[0] for d in cursor.description]   # grabbing columns from DB
        rows = cursor.fetchall()        # grabbing rows from DB
        output = []
        # turning the DB table into dict format
        for row in rows:
            rec = {}
            for col, val in zip(cols, row):
                if isinstance(val, datetime.timedelta):
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
