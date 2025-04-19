from flask import Flask, request, jsonify, render_template
from db_config import get_db_connection
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# === Helpers ===

def call_proc(proc_name, params):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(proc_name, params)
        results = []
        for result in cursor.stored_results():
            cols = [desc[0] for desc in result.description]
            for row in result.fetchall():
                results.append(dict(zip(cols, row)))
        conn.commit()
        return results
    finally:
        cursor.close()
        conn.close()


def call_view(view_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {view_name}")
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        output = []
        for row in rows:
            record = {}
            for col, val in zip(cols, row):
                if isinstance(val, datetime.timedelta):
                    record[col] = str(val)
                elif isinstance(val, (datetime.date, datetime.time, datetime.datetime)):
                    record[col] = val.isoformat()
                else:
                    record[col] = val
            output.append(record)
        return output
    finally:
        cursor.close()
        conn.close()

# === Stored Procedure Endpoints ===

@app.route('/<proc>', methods=['POST'])
def run_procedure(proc):
    # dynamic dispatch: if proc matches a stored procedure
    if proc not in call_proc.__globals__:
        # Not using generic, call by name
        data = request.get_json() or {}
        # all values as list for call_proc
        params = []
        # get parameter order from SQL or assume dict order
        params = list(data.values())
        try:
            results = call_proc(proc, params)
            return jsonify(results)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Procedure not found'}), 404

# === View Endpoints ===

@app.route('/<view>', methods=['GET'])
def run_view(view):
    # Only allow known views
    views = { 'flights_in_the_air', 'flights_on_the_ground', 'people_in_the_air', 
              'people_on_the_ground', 'route_summary', 'alternative_airports' }
    if view not in views:
        return jsonify({'error': 'View not found'}), 404
    try:
        data = call_view(view)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
