from os import getenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

WAIT_SECONDS = int(getenv("WAIT_SECONDS", "30"))
BASE_URL = getenv("BASE_URL", "http://localhost:8080")
DRIVER = getenv("DRIVER", "chrome").lower()


def before_all(context):
    """Executed once before all tests"""
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS
    # Select either Chrome or Firefox
    if "firefox" in DRIVER:
        context.driver = get_firefox()
    else:
        context.driver = get_chrome()
    context.driver.implicitly_wait(context.wait_seconds)
    context.config.setup_logging()


def after_all(context):
    """Executed after all tests"""
    context.driver.quit()


######################################################################
# Utility functions to create web drivers
######################################################################


def get_chrome():
    """Creates a head‑less Chromium driver for Behave tests"""
    print("Running Behave using the Chrome driver...\n")
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")  # modern head‑less mode
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.binary_location = "/usr/bin/chromium"  # <── chromium binary
    service = Service("/usr/bin/chromedriver")  # <── matching driver
    return webdriver.Chrome(service=service, options=opts)


def get_firefox():
    """Creates a headless Firefox driver"""
    print("Running Behave using the Firefox driver...\n")
    options = webdriver.FirefoxOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)
