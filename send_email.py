import smtplib
import ssl
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 🔹 Konfigurer e-post (BYTT UT MED DINE DETALJER)
SMTP_SERVER = "smtp.gmail.com"  # For Gmail. Bruk "smtp.office365.com" for Outlook.
SMTP_PORT = 587
EMAIL_SENDER = "dinemail@gmail.com"  # Bytt ut med din e-post
EMAIL_PASSWORD = "dittappassord"  # Bruk et "App Password" fra Google eller Outlook
EMAIL_RECEIVER = "mottakeremail@gmail.com"  # E-posten som skal motta varselet

# 🔹 Les inn de nyeste artiklene fra CSV
csv_file = "artikler.csv"
df = pd.read_csv(csv_file)

# 🔹 Filtrer ut artikler fra siste 24 timer
df["Dato"] = pd.to_datetime(df["Dato"], errors="coerce")
latest_articles = df[df["Dato"] >= pd.Timestamp.now() - pd.Timedelta(days=1)]

if latest_articles.empty:
    print("Ingen nye artikler i dag. E-post sendes ikke.")
else:
    # 🔹 Bygg e-postinnhold
    email_subject = f"📢 Nye artikler fra Forskning.no ({len(latest_articles)})"
    email_body = "<h2>📢 Her er dagens nye artikler:</h2><ul>"

    for _, row in latest_articles.iterrows():
        email_body += f"<li><a href='{row['Link']}'>{row['Tittel']}</a> ({row['Dato'].strftime('%Y-%m-%d')})</li>"

    email_body += "</ul><br><p>Automatisk generert av ditt OSINT-dashboard 🚀</p>"

    # 🔹 Send e-post
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_body, "html"))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ E-post med nye artikler sendt!")
    except Exception as e:
        print(f"❌ Feil ved sending av e-post: {e}")
