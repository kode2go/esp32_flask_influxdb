# Project

1. The code sets up a Flask web application to display and manage data received from an ESP32 device and stored in an InfluxDB database.
2. It utilizes the Flask-SocketIO extension for real-time updates and dynamic data visualization using Plotly.
3. The code includes routes for receiving and displaying real-time data, as well as historical data for the current day and the previous day.
4. Data points received from the ESP32 device are stored in InfluxDB with timestamps.
5. The /flask/rec route handles the reception of data from the ESP32 and stores it in the InfluxDB database. It also emits the data to connected clients.
6. The /flask/display route displays real-time data in a Plotly chart using the SocketIO connection for updates.
7. The /flask/history route presents links to view data for the current day and the previous day.
8. Clicking on these links triggers requests to the /flask/history_data route to fetch and display historical data.

```
/flask/rec
  - Receives data from the ESP32 device and stores it in InfluxDB.
  - Emits the data to connected clients.

/flask/display
  - Displays real-time data using a Plotly chart.
  - Utilizes Flask-SocketIO for real-time updates.
  - Renders data using the 'display2.html' template.

/flask/history
  - Presents links for the current day and previous day data.
  - Clicking on these links triggers requests to '/flask/history_data' for data.

HTML Templates:
- 'display2.html'
  - Template for displaying real-time data in a Plotly chart.
- 'history.html'
  - Template for displaying links to current and previous day data.

```

# Getting started with influxdb:
https://github.com/kode2go/influxdb/tree/main

# requirements

python-influxdb
socketio
