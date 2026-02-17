# IPMC Test Utility

Validation tool for IPMC boards. This tool checks firmware, verifies network status, and runs the IPMC test suite.

---

## Setup

Ensure the following requirements are met:

- Python 3 installed
- Root privileges (sudo access)

If required install the required Python dependency:

```bash
pip install pyserial
```


## Usage

Run the tester with root privileges:

```bash
sudo python3 ipmc_tester.py
```

---

## Configuration

Update the test suite path and serial devices in the script if needed:

```python
process = subprocess.Popen(
    [
        "sudo", "python3",
        TEST_SUITE,
        "/dev/ttyUSB0", "/dev/ttyUSB1"
    ]
)
```

Replace `/dev/ttyUSB0` and `/dev/ttyUSB1` with the correct serial device names for your system.

---

## Notes

- Ensure the IPMC board is connected before running the tester
- Verify serial device permissions if access errors occur
- Confirm correct test suite path is configured
