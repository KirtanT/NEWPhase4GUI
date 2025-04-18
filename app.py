from flask import Flask, request, jsonify, render_template
from db_config import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Helpers to call stored procedures and views

def call_proc(proc_name, params):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(proc_name, params)
        results = []
        # Iterate through any result sets returned
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
        return [dict(zip(cols, row)) for row in rows]
    finally:
        cursor.close()
        conn.close()

# === Stored Procedure Endpoints ===

@app.route('/add_airplane', methods=['POST'])
def add_airplane():
    data = request.get_json()
    params = [
        data['airlineID'],
        data['tail_num'],
        data['seat_capacity'],
        data['speed'],
        data['locationID'],
        data['plane_type'],
        data['maintenanced'],
        data.get('model'),
        data.get('neo')
    ]
    try:
        results = call_proc('add_airplane', params)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_airport', methods=['POST'])
def add_airport():
    data = request.get_json()
    params = [
        data['airportID'],
        data['airport_name'],
        data['city'],
        data['state'],
        data['country'],
        data['locationID']
    ]
    try:
        results = call_proc('add_airport', params)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.get_json()
    params = [
        data['personID'],
        data['first_name'],
        data.get('last_name'),
        data['locationID'],
        data['taxID'],
        data['experience'],
        data.get('miles', 0),
        data.get('funds', 0)
    ]
    try:
        results = call_proc('add_person', params)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/grant_or_revoke_pilot_license', methods=['POST'])
def toggle_pilot_license():
    data = request.get_json()
    params = [
        data['personID'],
        data['license']
    ]
    try:
        results = call_proc('grant_or_revoke_pilot_license', params)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/offer_flight', methods=['POST'])
def offer_flight():
    data = request.get_json()
    params = [
        data['flightID'],
        data['routeID'],
        data['support_airline'],
        data['support_tail'],
        data.get('progress', 0),
        data['next_time'],  # expect format 'HH:MM:SS'
        data['cost']
    ]
    try:
        results = call_proc('offer_flight', params)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/flight_landing', methods=['POST'])
def flight_landing():
    data = request.get_json()
    try:
        results = call_proc('flight_landing', [data['flightID']])
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/flight_takeoff', methods=['POST'])
def flight_takeoff():
    data = request.get_json()
    try:
        results = call_proc('flight_takeoff', [data['flightID']])
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/passengers_board', methods=['POST'])
def passengers_board():
    data = request.get_json()
    try:
        results = call_proc('passengers_board', [data['flightID']])
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/passengers_disembark', methods=['POST'])
def passengers_disembark():
    data = request.get_json()
    try:
        results = call_proc('passengers_disembark', [data['flightID']])
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/assign_pilot', methods=['POST'])
def assign_pilot():
    data = request.get_json()
    params = [
        data['flightID'],
        data['personID']
    ]
    try:
        results = call_proc('assign_pilot', params)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recycle_crew', methods=['POST'])
def recycle_crew():
    data = request.get_json()
    try:
        results = call_proc('recycle_crew', [data['flightID']])
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/retire_flight', methods=['POST'])
def retire_flight():
    data = request.get_json()
    try:
        results = call_proc('retire_flight', [data['flightID']])
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/simulation_cycle', methods=['POST'])
def simulation_cycle():
    try:
        results = call_proc('simulation_cycle', [])
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === View Endpoints ===

@app.route('/flights_in_the_air', methods=['GET'])
def get_flights_in_the_air():
    try:
        return jsonify(call_view('flights_in_the_air'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/flights_on_the_ground', methods=['GET'])
def get_flights_on_the_ground():
    try:
        return jsonify(call_view('flights_on_the_ground'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/people_in_the_air', methods=['GET'])
def get_people_in_the_air():
    try:
        return jsonify(call_view('people_in_the_air'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/people_on_the_ground', methods=['GET'])
def get_people_on_the_ground():
    try:
        return jsonify(call_view('people_on_the_ground'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/route_summary', methods=['GET'])
def get_route_summary():
    try:
        return jsonify(call_view('route_summary'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/alternative_airports', methods=['GET'])
def get_alternative_airports():
    try:
        return jsonify(call_view('alternative_airports'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
