from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt

# Flask app with custom template folder (webpages)
app = Flask(__name__, template_folder="webpages")

# Global variable to store latest ESP message
latest_msg = "Waiting for ESP data..."

# MQTT callback
def on_message(client, userdata, msg):
    global latest_msg
    latest_msg = msg.payload.decode()
    print(f"Received message: {latest_msg} on topic: {msg.topic}")

# MQTT setup
client = mqtt.Client(client_id="", protocol=mqtt.MQTTv311, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.connect("broker.hivemq.com", 1883)
client.subscribe("nandhini")  # ESP sends here
client.on_message = on_message
client.loop_start()  # Background thread

# Flask routes
@app.route("/")
def home():
    return render_template("home.html")  # webpages/home.html render aagum

@app.route("/latest")
def latest():
    return jsonify({"message": latest_msg})  # API to get latest ESP message

# Run Flask app
if __name__ == "__main__":
    # Hostinger requires host=0.0.0.0, port managed automatically
    app.run(host="0.0.0.0", port=5000, debug=True)
