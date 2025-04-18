from flask import Flask, request, jsonify, render_template
from db_config import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/call_procedure', methods=['POST'])
def call_procedure():
    data = request.get_json()
    proc_name = data.get('proc_name')
    params = data.get('params', [])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.callproc(proc_name, params)

        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
