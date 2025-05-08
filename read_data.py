import serial
import csv
import time

# Configure the serial connection (adjust the port name accordingly)
SERIAL_PORT = "/dev/cu.usbmodem1101"  # Change this for Windows (e.g., "COM3") or Mac (e.g., "/dev/cu.usbmodem14101")
BAUD_RATE = 115200
OUTPUT_FILE = "sensor_data.csv"

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for connection

# Open CSV file for writing
with open(OUTPUT_FILE, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Timestamp", "Heart Rate (BPM)", "X", "Y", "Z", "Temp (°C)", "Motion"])  # CSV Header

    print("Collecting data... Press Ctrl+C to stop.")

    try:
        while True:
            line = ser.readline().decode("utf-8").strip()  # Read and decode the serial line
            if line and not line.startswith("Timestamp"):  # Skip header line
                print(line)  # Print to console
                csv_writer.writerow(line.split(","))  # Write to CSV
                csvfile.flush()  # Ensure data is written

    except KeyboardInterrupt:
        print("\nData collection stopped. File saved as:", OUTPUT_FILE)
        ser.close()