import datetime
import random
import time
import os
from configs import config

def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)

def random_delay(min_seconds=0.5, max_seconds=1.0):
    """Add random delay to mimic human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def setup_directories():
    """Create necessary directory structure"""
    os.makedirs(config.BASE_DOWNLOAD_DIR, exist_ok=True)

