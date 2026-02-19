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
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

bos_restoranlar = []

for name, url in URLS.items():
    print(f"{name} kontrol ediliyor...")
    driver.get(url)
    time.sleep(8)

    buttons = driver.find_elements(By.TAG_NAME, "button")

    for b in buttons:
        if "Şubat" in b.text and "Dolu" not in b.text:
            bos_restoranlar.append(name)
            break

if bos_restoranlar:
    mesaj = "🚨 BOŞ REZERVASYON VAR!\n\n"
    for r in bos_restoranlar:
        mesaj += f"✅ {r}\n"
    send_telegram(mesaj)
else:
    print("Tüm restoranlar dolu.")

driver.quit()
