import psutil
import time
import threading
import tkinter as tk

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Function to get memory usage
def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

# Function to create a usage bar
def usage_bar(percent, length=50):
    bar_length = int(length * percent / 100)
    return '[' + '█' * bar_length + ' ' * (length - bar_length) + ']'

# Function to update the metrics in the tkinter window
def update_metrics():
    while True:
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()

        # Create usage bars
        cpu_bar = usage_bar(cpu_usage)
        memory_bar = usage_bar(memory_usage)

        # Update the labels
        cpu_label.config(text=f"CPU Usage: {cpu_bar} {cpu_usage:.2f}%")
        memory_label.config(text=f"Memory Usage: {memory_bar} {memory_usage:.2f}%")
        
        # Sleep for 1 second before updating again
        time.sleep(1)

# Create the main tkinter window
root = tk.Tk()
root.title("System Metrics Monitor")

# CPU usage label
cpu_label = tk.Label(root, font=("Helvetica", 12), text="CPU Usage: ")
cpu_label.pack(pady=10)

# Memory usage label
memory_label = tk.Label(root, font=("Helvetica", 12), text="Memory Usage: ")
memory_label.pack(pady=10)

# Start the thread to update metrics
thread = threading.Thread(target=update_metrics, daemon=True)
thread.start()

# Run the tkinter main loop
root.mainloop()