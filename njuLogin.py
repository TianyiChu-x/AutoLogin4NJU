import time
import logging
import configparser
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from paddleocr import PaddleOCR
import pytesseract


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    credentials = config['credentials']
    OCR = config['OCR']
    settings = config['settings']
    return {
        'username': credentials.get('username'),
        'password': credentials.get('password'),
        'engine': OCR.get('engine'),
        'sleep_duration': settings.getint('sleep_duration'),
        'use_headless': settings.getboolean('use_headless'),
        'use_gpu': settings.getboolean('use_gpu'),
    }


def setup_logging():
    logger = logging.getLogger('WebLogin')
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler('nju_login.log', maxBytes=5*1024*1024, backupCount=2)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def recognize_captcha(image_path, logger, config):
    logger.info("Starting captcha recognition.")
    if config['engine'] == 'paddleocr':
        ocr = PaddleOCR(use_gpu=config['use_gpu'], use_angle_cls=False, lang='en')
        result = ocr.ocr(image_path, cls=True)
        
        if result:
            text_lines = [line[1][0] for line in result[0] if line[1]]
            recognized_text = ''.join(text_lines)
        else:
            recognized_text = ''

    elif config['engine'] == 'tesseract':
        result = pytesseract.image_to_string(image_path, lang='eng')
        if result:
            recognized_text = result.replace(' ', '').replace('\n', '')
        else:
            recognized_text = ''

    else:
        recognized_text = ''
        logger.error("Invalid OCR engine specified in config.ini.")
    logger.info('Recognized text: {}'.format(recognized_text))
    return recognized_text


def login(config, logger):
    logger.info("Starting login process.")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') if config['use_headless'] else None
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://p.nju.edu.cn/")
        logger.info("Page loaded successfully.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captchaImg"))
        )
        logger.info("Captcha image found.")

        captcha_img = driver.find_element(By.ID, "captchaImg")
        captcha_url = captcha_img.get_attribute('src')

        driver.execute_script("window.open('{}');".format(captcha_url))
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

        captcha_img = driver.find_element(By.TAG_NAME, "img")
        captcha_img.screenshot('captcha.png')
        logger.info("Captcha screenshot taken.")

        driver.switch_to.window(driver.window_handles[0])

        captcha_code = recognize_captcha('captcha.png', logger, config)

        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        captcha_input = driver.find_element(By.ID, "captchaResponse")

        username_input.send_keys(config['username'])
        password_input.send_keys(config['password'])
        captcha_input.send_keys(captcha_code)
        logger.info("Credentials and captcha code entered.")

        captcha_input.send_keys(Keys.ENTER)
        logger.info("Login form submitted.")

    finally:
        time.sleep(config['sleep_duration'])
        driver.quit()
        logger.info("Driver closed.")


logger = setup_logging()
config = read_config()
while True:
    try:
        login(config, logger)
    except TimeoutException:
        logger.error("Timeout exception occurred. Maybe you have already logged in.")
        continue
    time.sleep(config['sleep_duration'])