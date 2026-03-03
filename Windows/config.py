#!/usr/bin/env python3
"""
IPMC Tester - Port Configuration
Run this once to set up COM ports. Re-run if ports change.

Author: Pranav Govekar
"""

import serial.tools.list_ports
import json
import os
import sys
import time


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")


def get_ports():
    return set(p.device for p in serial.tools.list_ports.comports())


def wait_for_new_port(existing_ports, label):
    print(f"   Waiting for {label} board to appear...")
    while True:
        time.sleep(1)
        current_ports = get_ports()
        new_ports = current_ports - existing_ports
        if len(new_ports) == 1:
            port = new_ports.pop()
            print(f"   ✅ Detected {label} port: {port}")
            print()
            return port
        elif len(new_ports) > 1:
            print(f"   ⚠️  Multiple new ports detected, please unplug and try again.")
            return None


def main():
    print("=== IPMC Tester - Port Configuration ===")
    print()
    print("This will detect your COM ports automatically.")
    print("You will be asked to plug in each board one at a time.")
    print()

    input("Step 1: Unplug BOTH the IPMC and CTRL boards, then press Enter... ")
    print()

    # Snapshot of ports with nothing plugged in
    baseline_ports = get_ports()
    if baseline_ports:
        print(f"   (Other existing COM ports detected and will be ignored: {', '.join(sorted(baseline_ports))})")
        print()

    # Detect IPMC port
    input("Step 2: Plug in the IPMC (test board) and press Enter... ")
    ipmc_port = None
    while ipmc_port is None:
        ipmc_port = wait_for_new_port(baseline_ports, "IPMC")
        if ipmc_port is None:
            input("   Please unplug the board, then plug it in again and press Enter... ")

    # Detect CTRL port
    known_ports = baseline_ports | {ipmc_port}
    input("Step 3: Plug in the CTRL (reference board) and press Enter... ")
    ctrl_port = None
    while ctrl_port is None:
        ctrl_port = wait_for_new_port(known_ports, "CTRL")
        if ctrl_port is None:
            input("   Please unplug the board, then plug it in again and press Enter... ")

    # Save config
    config = {
        "ipmc_port": ipmc_port,
        "ctrl_port": ctrl_port
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print(f"✅ Config saved to config.json")
    print(f"   IPMC port : {ipmc_port}")
    print(f"   CTRL port : {ctrl_port}")
    print()
    input("Enter to exit... ")


if __name__ == "__main__":
    main()
