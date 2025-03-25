from confluent_kafka import Consumer, KafkaException
import threading
import tkinter as tk
import time

KAFKA_TOPIC = 'system-metrics'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Configure Kafka consumer
consumer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'metrics-visualizer',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

# Function to create a usage bar
def usage_bar(percent, length=50):
    bar_length = int(length * percent / 100)
    return '[' + '█' * bar_length + ' ' * (length - bar_length) + ']'

# Function to continuously consume messages and update metrics
def update_metrics():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        try:
            cpu_usage, memory_usage, temperature, fan_speed = map(float, msg.value().decode('utf-8').split(','))

            cpu_bar = usage_bar(cpu_usage)
            memory_bar = usage_bar(memory_usage)

            cpu_label.config(text=f"CPU Usage: {cpu_bar} {cpu_usage:.2f}%")
            memory_label.config(text=f"Memory Usage: {memory_bar} {memory_usage:.2f}%")
            temp_label.config(text=f"CPU Temp: {temperature:.2f} °C")
            fan_label.config(text=f"Fan Speed: {fan_speed:.2f} RPM")

        except Exception as e:
            print(f"Failed to parse message: {e}")

        time.sleep(1)

# Create tkinter window
root = tk.Tk()
root.title("Kafka System Metrics Monitor")

cpu_label = tk.Label(root, font=("Helvetica", 12), text="CPU Usage: ")
cpu_label.pack(pady=5)

memory_label = tk.Label(root, font=("Helvetica", 12), text="Memory Usage: ")
memory_label.pack(pady=5)

temp_label = tk.Label(root, font=("Helvetica", 12), text="CPU Temp: ")
temp_label.pack(pady=5)

fan_label = tk.Label(root, font=("Helvetica", 12), text="Fan Speed: ")
fan_label.pack(pady=5)

thread = threading.Thread(target=update_metrics, daemon=True)
thread.start()

root.mainloop()

consumer.close()
