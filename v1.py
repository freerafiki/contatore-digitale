import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

st.title("Contatore Digitale")
st.markdown("## Centro Storico")
st.write("A Venezia, in centro storico, siamo (sulla carta)")
with open('data/today.json') as json_file:
    today_data = json.load(json_file)
#st.metric(label="", value=today_data['ve_mu_bu'])
st.markdown(f"## {today_data['ve_mu_bu']}")
st.write("residenti, divisi tra:")

#st.write("### - san marco, castello, cannaregio, sant'elena")
st.write(
    f"- {today_data['est']} a san marco, castello, cannaregio, sant'elena")
#st.write("### - dorsoduro, san polo, santa croce, giudecca")
st.write(
    f"- {today_data['ovest']} a dorsoduro, san polo, santa croce, giudecca")
#st.write("### - murano, s.erasmo")
st.write(f"- {today_data['murano']} a murano, s.erasmo")
#st.write("### - burano, mazzorbo, torcello")
st.write(f"- {today_data['burano']} a burano, mazzorbo, torcello")

st.markdown("## Comune")
st.markdown("A livello di comune, abbiamo:")
st.markdown(
    f"- (come detto), {today_data['isole']} nella venezia insulare (centro storico)")
st.markdown(f"- {today_data['lido']} nella venezia litorale (lido)")
st.markdown(f"- {today_data['terraferma']} in terraferma")
st.markdown(f"- {today_data['comune']} in totale nel comune")

add_selectbox = st.sidebar.selectbox(
    "Che zona vuoi visualizzare?",
    ("Venezia Murano Burano", "Home phone", "Mobile phone")
)

st.markdown("## Grafici")
df = pd.read_csv("data/aggregated_data_today.csv")
#st.line_chart(df['ve_mu_bu'].values / 10000)
st.markdown("#### Centro Storico")
fig, ax = plt.subplots()
#st.write(ax)
ax.plot(df['dates'].values, df['ve_mu_bu'].values)
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
st.pyplot(fig)
st.markdown("#### Terraferma")
fig, ax = plt.subplots()
ax.plot(df['dates'].values, df['terraferma'].values)
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
st.pyplot(fig)

st.markdown("## Dati")
st.markdown(
    "Il contenuto della pagina è una rielaborazione dei dati relativi a Venezia.")
st.markdown(
    "Fonte: Opendata del comune di venezia, disponibili su dati.venezia.it")
st.markdown("Esempio: [Popolazione per sesso ed età - Municipalità di Venezia Murano Burano](https://dati.venezia.it/?q=content/popolazione-sesso-ed-et%C3%A0-municipalit%C3%A0-di-venezia-murano-burano-0) ")
st.markdown(
    "Disponibili sotto [Licenza CC-BY](https://dati.venezia.it/?q=licenza/cc)")

st.markdown("## Credits")
st.markdown(
    "Il contatore dei veneziani è un'idea orginariamente di Venessia.com, non mia. [Qui](https://www.venessia.com/contatoreabitanti/) trovate maggiori informazioni al riguardo.")
st.markdown("Questo progetto punta ad una rielaborazione dei dati e alla creazione di un'API che permetta di diffondere le informazioni in maniera più rapida e veloce.")
