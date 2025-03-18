import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Oppsett for ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

service = Service(r"C:\Users\zapp8\osint-dashboard\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Definer hvilke sider vi skal hente artikler fra
categories = {
    "Teknologi": "https://www.forskning.no/tag/teknologi",
    "Informasjonsteknologi": "https://www.forskning.no/tag/informasjonsteknologi",
    "Genteknologi": "https://www.forskning.no/tag/genteknologi"
}

# CSV-fil for lagring av tidligere artikler
csv_file = "artikler.csv"

# Hvis CSV-filen ikke finnes, lag en ny med kolonneoverskrifter
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Kategori", "Tittel", "Dato", "Link"])  # Kolonneoverskrifter

# Hent eksisterende artikler for å unngå duplikater
existing_links = set()
with open(csv_file, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Hopp over overskrifter
    for row in reader:
        existing_links.add(row[3])  # Lagrer eksisterende lenker

new_articles = []

for category, url in categories.items():
    print(f"\n🔹 Henter artikler fra {category.upper()} - {url} 🔹\n")

    driver.get(url)
    time.sleep(5)  # Vent for å sikre at innholdet lastes

    # Finn alle artikler
    articles = driver.find_elements(By.TAG_NAME, "article")

    if not articles:
        print("🚫 Fant ingen artikler! Sjekk om HTML-strukturen er annerledes.\n")
        continue

    for article in articles[:5]:  # Henter de 5 nyeste artiklene
        try:
            title_tag = article.find_element(By.TAG_NAME, "h2")  # Tittel
            link_tag = article.find_element(By.TAG_NAME, "a")  # Link
            date_tag = article.find_element(By.TAG_NAME, "time")  # Publiseringsdato

            title = title_tag.text.strip()
            link = link_tag.get_attribute("href")
            date = date_tag.get_attribute("datetime")

            # Sjekk om artikkelen allerede er lagret
            if link in existing_links:
                continue  # Hopp over artikkelen hvis den er lagret før

            print(f"- {title}")
            print(f"  Dato: {date}")
            print(f"  Link: {link}\n")

            # Legg til i ny liste
            new_articles.append([category, title, date, link])

        except Exception as e:
            print(f"⚠️ Feil ved parsing av en artikkel: {e}")

# Lukk nettleseren
driver.quit()

# Lagre nye artikler i CSV-filen
if new_articles:
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(new_articles)

    print(f"✅ Lagret {len(new_articles)} nye artikler i '{csv_file}'.")
else:
    print("ℹ️ Ingen nye artikler funnet.")

