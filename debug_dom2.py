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
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
service = Service(ChromeDriverManager().install())
print('Driver installed:', service.path)

driver = webdriver.Chrome(service=service, options=options)
print('Starting browser')
url = 'https://reportplus.mizopower.com/reports'
driver.get(url)
print('Navigated to', url)
WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
print('ReadyState after load:', driver.execute_script('return document.readyState'))
for i in range(1, 7):
    time.sleep(5)
    print(f'Waited {i*5}s, title="{driver.title}", url="{driver.current_url}"')
    if driver.title.lower() != 'loading...':
        break

body_text = driver.execute_script('return document.body.innerText')
print('Body text snippet:', body_text[:1200])
print('Query all inputs count:', driver.execute_script('return document.querySelectorAll("input").length'))
print('Query all buttons count:', driver.execute_script('return document.querySelectorAll("button").length'))
print('Query all divs count:', driver.execute_script('return document.querySelectorAll("div").length'))
print('webdriver flag:', driver.execute_script('return window.navigator.webdriver'))
print('Browser logs:')
for entry in driver.get_log('browser'):
    print(entry)
print('Saving screenshot...')
name = 'debug_reportplus_dom2.png'
driver.save_screenshot(name)
print('Screenshot saved', name)
driver.quit()
