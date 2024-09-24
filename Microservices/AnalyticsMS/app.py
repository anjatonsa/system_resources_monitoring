from flask import Flask
import paho.mqtt.client as mqtt
import json,pickle
import numpy as np

app = Flask(__name__)

broker_address = "mosquitto"
broker_port = 1883
sub_topic = "sensor/readings"
pub_topic_cpu = "notification/cpu_load"
pub_topic_power = "notification/power"


model_pkl_file1 = "/app/model/cpu_load_model.pkl"
with open(model_pkl_file1, 'rb') as file:  
    cpu_load_model = pickle.load(file)
scaler_pkl_file1 = "/app/model/cpu_scaler.pkl"
with open(scaler_pkl_file1, 'rb') as file:  
    cpu_scaler = pickle.load(file)

model_pkl_file2 = "/app/model/power_model.pkl"
with open(model_pkl_file2, 'rb') as file:  
    power_consp_model = pickle.load(file)
scaler_pkl_file2 = "/app/model/power_scaler.pkl"
with open(scaler_pkl_file2, 'rb') as file:  
    power_scaler = pickle.load(file)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    client.subscribe(sub_topic, qos=0)

def on_publish(client, userdata, result):
    print("data published \n")

def on_message(client, userdata, msg):
    message_data = json.loads(msg.payload.decode())
    print(f"Received message from topic {msg.topic}, {message_data}")
   
    processed_data, time= preprocess_message(message_data, "cpu")
    cpu_load_prediction = cpu_load_model.predict(processed_data)
    print("Predicted data cpu ",cpu_load_prediction[0])
    
    processed_data, _ = preprocess_message(message_data, "power")
    power_consp_prediction = power_consp_model.predict(processed_data)
    print("Predicted data power",power_consp_prediction[0])
    
    handle_prediction(cpu_load_prediction,power_consp_prediction, time)

def preprocess_message(payload, choice):
    if choice=='cpu':
        exclude_fields = ["Series", "Time", "CPU_Load"]
    else:
        exclude_fields = ["Series", "Time", "Power"]

    data = [value for key, value in payload.items() if key not in exclude_fields]
    npdata = np.array(data)

    time_value = payload.get("Time", None)
    if choice=='cpu':
        return cpu_scaler.transform([npdata]), time_value
    else:
        return power_scaler.transform([npdata]),time_value


def handle_prediction(cpu_load_prediction, power_prediction, time):
    message = {}
    message['time'] = time
    message['cpu_load'] = cpu_load_prediction[0][0]
    if cpu_load_prediction[0] > 80:  # CPU load greater than 80%
        message['cpu_load_message'] = "High CPU load!"
    else:
        message['cpu_load_message'] = "Normal CPU load."
    
    json_message = json.dumps(message)
    client.publish(pub_topic_cpu, json_message)
    
    message = {}
    message['time'] = time
    message['power'] = power_prediction[0][0]
    if power_prediction[0] > 240:  # Power greater than 240 Watts
        message['power_message'] = "High power consumption!"
    else:
        message['power_message'] = "Normal power consumption."
        
    json_message = json.dumps(message)
    client.publish(pub_topic_power, json_message)

@app.route('/')
def index():
    return 'Analytics  microservice'


if __name__ == '__main__':

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    client.connect(broker_address, broker_port, 0)
    client.loop_start()

    app.run()
