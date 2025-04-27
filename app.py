from flask import Flask, request, render_template
from db_config import get_db_connection
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# create funciton for stored procedures by accessing flight_tracking database
def pcall(procedure_name, inputs):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(procedure_name, inputs)
        results = []
        for result in cursor.stored_results():
            cols = [d[0] for d in result.description]
            for row in result.fetchall():
                results.append(dict(zip(cols, row)))
        conn.commit()
        return results
    finally:
        cursor.close()
        conn.close()

# route the procedure call back to the html doc
@app.route('/procedure', methods=['POST'])
def prun():
    data = request.get_json()
    procedure_name = data.get('procedure_name')
    inputs = data.get('inputs', [])
    try:
        results = pcall(procedure_name, inputs)
        return results
    except Exception as e:
        return str(e), 500

# view endpoint
def vcall(view):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"select * from {view}")
        cols = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        output = []
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
        conn.close()

@app.route('/view/<view>', methods=['GET'])
def vrun(view):
    if view not in {
        'flights_in_the_air', 'flights_on_the_ground',
        'people_in_the_air', 'people_on_the_ground',
        'route_summary', 'alternative_airports'}:
        return 'View not found', 404
    try:
        data = vcall(view)
        return data
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
