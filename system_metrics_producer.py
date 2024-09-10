from confluent_kafka import Producer
import psutil
import time
import cpuinfo

KAFKA_TOPIC = 'system-metrics'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Configure the Producer
producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. Triggered by poll() or flush(). """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def get_cpu_temperature():
    """ Get CPU temperature using cpuinfo or any other method available """
    info = cpuinfo.get_cpu_info()
    # Replace this with the correct way to get temperature data from cpuinfo
    # Since cpuinfo does not provide temperature, you may need to use another library
    temperature = 0  # Replace with actual logic if available
    return temperature

def produce_metrics():
    while True:
        # Collect system metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        temperature = get_cpu_temperature()  # Replace with actual logic for temperature
        fan_speed = 0  # If you have another method to get fan speed, replace this

        # Prepare message
        message = f"{cpu_usage},{memory_usage},{temperature},{fan_speed}"

        # Print the message to standard output
        print(f"Producing message: {message}")

        # Send message to Kafka
        producer.produce(KAFKA_TOPIC, value=message, callback=delivery_report)
        producer.flush()  # Wait for all messages to be delivered

        time.sleep(2)  # Send metrics every 2 seconds

if __name__ == "__main__":
    produce_metrics()