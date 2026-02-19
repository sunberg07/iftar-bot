from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests

TOKEN = "BURAYA_TELEGRAM_TOKEN"
CHAT_ID = "BURAYA_CHAT_ID"

URL = "https://tesislerrezervasyon.ibb.istanbul/reservation/create/1"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

driver.get(URL)
time.sleep(8)

buttons = driver.find_elements(By.TAG_NAME, "button")

bos_var = False

for b in buttons:
    if "Şubat" in b.text and "Dolu" not in b.text:
        bos_var = True
        send_telegram("🚨 Boş rezervasyon bulundu! Hemen kontrol et!")
        break

if not bos_var:
    print("Hala dolu")

driver.quit()
