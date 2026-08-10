from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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
print('URL after navigation:', driver.current_url)
print('Title:', driver.title)
print('ReadyState:', driver.execute_script('return document.readyState'))
print('Page source snippet:', driver.page_source[:1000])

time.sleep(5)
driver.save_screenshot('debug_reportplus.png')
print('Saved screenshot debug_reportplus.png')
driver.quit()
