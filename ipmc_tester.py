#!/usr/bin/env python3

"""
IPMC Test Utility
Quick validation tool for IPMC boards - checks firmware and network before running tests.

Author: Pranav
"""

import serial
import time
import subprocess
import sys
import re
import os

# Serial settings
PORT = "/dev/ttyUSB0"
BAUD = 115200

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_SUITE = os.path.join(SCRIPT_DIR, "test-suite_2020.py")

def run_serial_commands():
	try:
		ser = serial.Serial(PORT, BAUD, timeout=1)
		time.sleep(2)  # wait for port to initialize

		# Send "version"
		ser.write(b"version\r\n")
		time.sleep(1)
		output1 = ser.read_all().decode(errors="ignore")
		print("Output of 'version':")
		print(output1)

		# Check software revision
		if "SW revision : fallback-7z014s-v0.9.6" not in output1:
			print("❌ Software revision is not correct. Stopping.")
			input("Enter to exit... ")
			ser.close()
			sys.exit(1)

		# Send "network.status"
		ser.write(b"network.status\r\n")
		time.sleep(1)
		output2 = ser.read_all().decode(errors="ignore")
		print("Output of 'network.status':")
		print(output2)

		ser.close()

		# Check network link status
		if "Network status: Link is UP, interface is UP" not in output2:
			print("❌ Network link is not UP. Stopping.")
			input("Enter to exit... ")
			sys.exit(1)

		# Extract IP address
		ip_match = re.search(r"IP Address:\s+(\d+\.\d+\.\d+\.\d+)", output2)
		if not ip_match or ip_match.group(1) in ["0.0.0.0", "unset"]:
			print("❌ No valid IP address assigned. Stopping.")
			input("Enter to exit... ")
			sys.exit(1)

		print(f"✅ Valid Firmware found")
		print(f"✅ Valid IP found: {ip_match.group(1)}")

	except Exception as e:
		print(f"Error: {e}")
		sys.exit(1)

if __name__ == "__main__":
	run_serial_commands()

	input("Enter to continue... ")

	process = subprocess.Popen(
		[
			"sudo", "python3",
			TEST_SUITE,
			"/dev/ttyUSB0", "/dev/ttyUSB1"
		]
	)
	process.wait()

	input("Enter to exit... ")

