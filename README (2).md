# Smart Accident Detection & Emergency Alert System

Raspberry Pi based crash detection system. Detects a vehicle impact
(accelerometer) or a manual SOS button press, captures a photo, and
sends an automatic alert — photo, GPS location, and SMS — to an
emergency contact.

Built with `picamera2`, `mpu6050`, `RPi.GPIO`, `pyserial`, and the
Telegram Bot API.

## Features

- 🚨 Crash detection via MPU6050 accelerometer (±4g threshold) or a physical SOS button
- 📷 Automatic photo capture on trigger (Picamera2, 1080p)
- 📍 Live location shared via a Google Maps link
- 📲 Instant Telegram alert (photo + location)
- ✉️ SOS SMS via SIM800 GSM module over UART

## Hardware

| Component | Notes |
|---|---|
| Raspberry Pi | Pi 5 recommended (`/dev/ttyAMA0` UART) |
| Pi Camera Module | via `picamera2` |
| MPU6050 | accelerometer/gyroscope, I2C address `0x68` |
| Push button | GPIO 21 (BCM), internal pull-up |
| SIM800-series GSM module | UART, 115200 baud |

## Setup

```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
```

**`requirements.txt`:**
```
picamera2
requests
pyserial
mpu6050-raspberrypi
RPi.GPIO
```

Enable serial and I2C interfaces:
```bash
sudo raspi-config   # Interface Options → Serial Port, I2C → Enable
```

### Secrets

Copy the example env file and fill in your real values — **never commit
`.env`** (it's already in `.gitignore`):

```bash
cp .env.example .env
```

`.env`:
```
BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
EMERGENCY_PHONE=+91XXXXXXXXXX
```

Load them in `main.py` instead of hardcoding:
```python
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
EMERGENCY_PHONE = os.environ["EMERGENCY_PHONE"]
```
(add `python-dotenv` to `requirements.txt` if you use `load_dotenv`)

You'll also need a `LocationParser.py` exposing `getLocationUrl()`,
returning a Google Maps link (e.g. from a GPS module or a fixed test
location).

## Usage

```bash
python main.py
```

Runs continuously, polling the sensor/button twice a second. On
trigger it:
1. Captures a photo
2. Sends the photo + location link to Telegram
3. Sends an SOS SMS to the emergency contact

`Ctrl+C` to stop (GPIO cleans up on exit).

## Project structure

```
.
├── main.py              # integrated system: sensing + capture + alerts
├── CameraTest.py         # standalone camera test
├── BotTelegram.py        # standalone Telegram send test
├── LocationParser.py     # GPS/location helper (not included)
├── .env.example
├── .gitignore
└── requirements.txt
```

## Known limitations / roadmap

- [ ] Timestamped filenames instead of overwriting `captured_image.jpg`
- [ ] Support multiple emergency contacts
- [ ] Add a cooldown period after a trigger to avoid duplicate alerts
- [ ] Field-test and tune the crash threshold (currently ±4g)
- [ ] Auto-detect the serial port instead of hardcoding `/dev/ttyAMA0`

## ⚠️ Security note

If a bot token, chat ID, or phone number was ever hardcoded and pushed
to this repo in an earlier commit, treat it as compromised: regenerate
the Telegram bot token via [@BotFather](https://t.me/BotFather)
(`/revoke`) even after removing it from the latest commit, since it
still exists in git history unless the history is rewritten.

## License

Add a license of your choice (e.g. MIT) if you intend to make this repo public.
