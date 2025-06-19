import os

BASE_DOWNLOAD_DIR = os.path.join(os.getcwd(), "rto_wise_data")
BASE_URL = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"

# Needs to be changed everyday
STATE_DROPDOWN_LABEL = 'j_idt41_label'
LEFT_REFRESH_BUTTON_LABEL = "j_idt77"
RIGHT_REFRESH_BUTTON_LABEL = "j_idt72"

YEAR_STATE_MAPPING = {
    "2025" : [
        "Uttar Pradesh(77)",
        "UT of DNH and DD(3)", "West Bengal(57)"
    ]
}

# CONSTANTS
YEAR_DROPDOWN_LABEL = "selectedYear_label"
X_AXIS_LABEL = "xaxisVar_label"
Y_AXIS_LABEL = "yaxisVar_label"

# S3 CREDENTIALS
S3_BUCKET_NAME = ""
S3_ACCESS_KEY = ""
S3_SECRET_KEY = ""
S3_REGION = ""

# EV and ICE
FUEL_TYPES_EV = [7, 21]
FUEL_TYPES_ICE = [14, 15, 16, 17, 18, 19]
FUEL_TYPES = FUEL_TYPES_EV


# Vehicle Categories
TWO_WHEELER = [0, 1, 2]
FOUR_WHEELER = []
VEHICLE_CATEGORIES = TWO_WHEELER


# CHROME OPTIONS
CHROME_OPTIONS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-notifications",
    "--disable-blink-features=AutomationControlled"
]

CHROME_EXPERIMENTAL_OPTIONS = {
    "excludeSwitches": ["enable-automation"],
    "useAutomationExtension": False
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
]

PREFS = {
    "download.default_directory": BASE_DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

