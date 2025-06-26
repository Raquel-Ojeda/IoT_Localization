from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def get_all_device_data():
    conn = psycopg2.connect(
        dbname="factory_tracking",
        user="postgres",
        password="Caterpillar",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT device_name, latitude, longitude, battery_percentage, satellites, timestamp
        FROM device_location
        ORDER BY device_name, timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "name": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "battery": row[3],
            "satellites": row[4],
            "timestamp": row[5].isoformat()
        })
    return data

@app.route("/api/machines")
def machines():
    return jsonify(get_all_device_data())

if __name__ == "__main__":
    app.run(debug=True)