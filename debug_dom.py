from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
service = Service(ChromeDriverManager().install())
print('Driver installed:', service.path)

driver = webdriver.Chrome(service=service, options=options)
print('Starting browser')
url = 'https://reportplus.mizopower.com/reports'
driver.get(url)
WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
print('Current URL:', driver.current_url)
print('Title:', driver.title)
time.sleep(5)
inputs = driver.find_elements('xpath', '//input')
print('Input count:', len(inputs))
for i, inp in enumerate(inputs[:20], start=1):
    print(i, inp.get_attribute('name'), inp.get_attribute('id'), inp.get_attribute('type'), inp.get_attribute('placeholder'), inp.get_attribute('class'))
frames = driver.find_elements('tag name', 'iframe')
print('Iframe count:', len(frames))
for i, fr in enumerate(frames, start=1):
    print('iframe', i, fr.get_attribute('src'), fr.get_attribute('id'))
page = driver.page_source.lower()
print('Contains username?', 'username' in page)
print('Contains password?', 'password' in page)
print('Contains sign in?', 'sign in' in page)
print('Contains login?', 'login' in page)
name = 'debug_reportplus_dom.png'
driver.save_screenshot(name)
print('Screenshot saved', name)
driver.quit()
