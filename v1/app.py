from flask import Flask, request, render_template
from influxdb import InfluxDBClient
from datetime import datetime
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 

# InfluxDB connection settings
INFLUXDB_HOST = 'localhost'  # Replace with your InfluxDB host
INFLUXDB_PORT = 8086  # Replace with your InfluxDB port
INFLUXDB_DATABASE = 'esp02'

client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)

# Create the InfluxDB database if it doesn't exist
if INFLUXDB_DATABASE not in client.get_list_database():
    client.create_database(INFLUXDB_DATABASE)

client.switch_database(INFLUXDB_DATABASE)

@app.route('/flask/rec', methods=['POST'])
def receive_data():
    try:
        print("Received data")
        received_data = request.form.get('data')  # Assuming the ESP32 sends the data as a form field named 'data'
        received_device_name = request.form.get('device_name')
        # Create a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Define the JSON data point to write to InfluxDB
        data_point = [
            {
                "measurement": "data",
                "time": timestamp,  # Use 'time' instead of 'timestamp'
                "fields": {
                    "value": float(received_data)
                }
            }
        ]

        # Write the data point to InfluxDB
        client.write_points(data_point)

        socketio.emit('new_data', {'time': timestamp, 'value': float(received_data)})

        return "Data received successfully", 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return str(e), 500

from datetime import datetime, timedelta

@app.route('/flask/display')
def display_data():
    # Query InfluxDB to retrieve data
    # current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now()
    five_minutes_ago = current_time - timedelta(minutes=5)
    current_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    five_minutes_ago_str = five_minutes_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
    # query = "SELECT * FROM data"  # Modify the query as needed
    # query = f"SELECT * FROM data WHERE time >= '{current_date}T00:00:00Z' AND time < '{current_date}T23:59:59Z'"
    query = f"SELECT * FROM data WHERE time >= '{five_minutes_ago_str}' AND time <= '{current_time_str}'"
    result = client.query(query)


    # Convert the result to a list of dictionaries
    data_points = list(result.get_points())

    return render_template('display2.html', data_points=data_points)

@app.route('/flask/history')
def history():
    return render_template('history2.html')

from datetime import datetime, timedelta
from flask import jsonify


@app.route('/flask/history_data')
def history_data():
    day = request.args.get('day')
    if day == 'current':
        data = get_data_for_current_day()
    elif day == 'previous':
        data = get_data_for_previous_day()
    else:
        data = []

    return jsonify(data)

def get_data_for_current_day():
    current_time = datetime.now()
    end_time = current_time
    start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    return get_data_between_times(start_time, end_time)

def get_data_for_previous_day():
    current_time = datetime.now()
    end_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=1)
    return get_data_between_times(start_time, end_time)

def get_data_between_times(start_time, end_time):
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    query = f"SELECT * FROM data WHERE time >= '{start_time_str}' AND time <= '{end_time_str}'"
    result = client.query(query)
    data_points = list(result.get_points())
    return data_points


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
