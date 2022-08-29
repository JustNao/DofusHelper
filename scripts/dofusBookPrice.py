from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from seleniumwire.utils import decode
import sys
import time
import json
from sources.item import itemToName, equipmentPrices
from sources.utils import kamasToString

link = input("Enter the link for the DofusBook build: ")

options = Options()
options.add_argument('--headless')
options.add_argument("log-level=1")
driver = webdriver.Chrome(chrome_options=options)
driver.get(link)

req = driver.wait_for_request(
    r'(.*dofus\/stuffer\/.*)|(.*stuffs\/dofus\/(private)|(public)\/\d*)')
response = req.response
body = decode(response.body, response.headers.get(
    'Content-Encoding', 'identity'))
stuffData = json.loads(body.decode('utf-8'))
totalPrice = 0
if 'items' in stuffData:
  for item in stuffData['items']:
    try:
      totalPrice += equipmentPrices[str(item['official'])]
    except KeyError:
      print(
          f"Missing price for {itemToName[item['official']]}, {str(item['official'])}", )
else:
  for item in stuffData['data']:
    try:
      totalPrice += equipmentPrices[str(item['official'])]
    except KeyError:
      print(
          f"Missing price for {itemToName[item['official']]}, {str(item['official'])}", )

driver.quit()
print(f"{kamasToString(totalPrice)} K")
