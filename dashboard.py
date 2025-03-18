import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Last inn data fra CSV
csv_file = "artikler.csv"

try:
    df = pd.read_csv(csv_file)

    # 🔹 Fjerne tidssoner fra "Dato"-kolonnen
    df["Dato"] = df["Dato"].str.replace(r"(\+.*)", "", regex=True)  # Fjerner tidssonen
    df["Dato"] = pd.to_datetime(df["Dato"], errors="coerce")  # Konverterer til datetime
    df = df.dropna(subset=["Dato"])  # Fjerner eventuelle tomme datoer

    # Streamlit-app
    st.title("📊 OSINT Dashboard - Forskning.no")

    # Velg kategori
    category = st.selectbox("Velg kategori:", df["Kategori"].unique())

    # Filtrer data
    filtered_df = df[df["Kategori"] == category].sort_values(by="Dato", ascending=False)

    # 🔹 VIS GRAFER: Antall artikler over tid
    st.subheader(f"📈 Artikkeltrend for {category}")

    # Tell antall artikler per måned
    df_trend = filtered_df.groupby(filtered_df["Dato"].dt.to_period("M")).count()

    # Plott grafen
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df_trend.index.astype(str), df_trend["Tittel"], marker="o", linestyle="-")
    ax.set_xlabel("Måned")
    ax.set_ylabel("Antall artikler")
    ax.set_title(f"Antall artikler over tid i {category}")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

    # 🔹 VIS TABELL OG LENKER
    st.subheader(f"📰 Siste artikler innen {category}")
    for _, row in filtered_df.iterrows():
        st.markdown(f"- [{row['Tittel']}]({row['Link']}) ({row['Dato'].strftime('%Y-%m-%d')})")

except FileNotFoundError:
    st.error("CSV-filen med artikler ble ikke funnet. Kjør scraperen først!")
