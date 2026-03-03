# IPMC Test Utility (Windows)

Validation tool for IPMC boards. Checks firmware, verifies network status, and runs the IPMC test suite.

---

## Requirements

- Python 3 installed
- `pyserial` library

```bash
pip install pyserial
```

---

## Setup

Run `config.py` **once** when setting up the test station:

```bash
python config.py
```

Follow the on-screen steps — you will be asked to plug in the IPMC and CTRL boards one at a time so the ports are detected automatically. This saves a `config.json` file which is used by the tester on every subsequent run.

Re-run `config.py` only if the USB cables are moved to different ports on the PC.

---

## Usage

```bash
python ipmc_tester.py
```

---

## Notes

- Keep USB cables plugged into the same physical ports on the PC — COM port assignments are stable as long as cables are not moved
- Ensure both IPMC and CTRL boards are powered and connected before running the tester
- If `config.json` is missing, run `config.py` first

---
