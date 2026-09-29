from picamera2 import Picamera2
import time
from datetime import datetime

picam2 = Picamera2()

config = picam2.create_still_configuration(
    main={"size": (1920, 1080)}
)
picam2.configure(config)

picam2.start()
time.sleep(2)

# Generate unique filename
filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")

picam2.capture_file(filename)

print("Saved:", filename)

picam2.stop()