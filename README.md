# System Metrics Pipeline Project

The pipeline established takes system metrics data available on my system and sends them to a Kafka topic established. The consumer script takes the data sent (messages) and then displays them in a GUI interface using TKinter.

**Steps:**
1. Start Zookeeper
"zookeeper-server-start.sh config/zookeeper.properties"
2. Start Kafka
"kafka-server-start.sh config/server.properties"
3. Create Kafka Topic
"kafka-topics.sh --create --topic <system-metrics> --bootstrap-server localhost:9092"
4. Run system_metrics_producer.py
"python3 system_metrics_producer.py"
5. Run visualize_metrics.py
"python3 visualize_metrics.py"

Libraries: TKinter, Threading, CPUinfo, Kafka, Zookeeper

