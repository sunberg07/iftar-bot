import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URLS = {
    "Restoran 1": "https://tesislerrezervasyon.ibb.istanbul/reservation/create/1",
    "Restoran 8": "https://tesislerrezervasyon.ibb.istanbul/reservation/create/8",
    "Restoran 10": "https://tesislerrezervasyon.ibb.istanbul/reservation/create/10"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

bos_bilgiler = []

for name, url in URLS.items():
    print(f"{name} kontrol ediliyor...")
    driver.get(url)
    time.sleep(15)

    elements = driver.find_elements(By.XPATH, "//*[contains(text(),'Şubat')]")

    for el in elements:
        text = el.text.strip()

        if text and "Dolu" not in text:
            bos_bilgiler.append(f"{name} → {text}")

if bos_bilgiler:
    mesaj = "🚨 BOŞ REZERVASYON BULUNDU!\n\n"
    for bilgi in bos_bilgiler:
        mesaj += f"✅ {bilgi}\n\n"
    send_telegram(mesaj)
else:
    print("Tüm restoranlar dolu.")

driver.quit()
