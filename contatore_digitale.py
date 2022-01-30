import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

st.title("Contatore Digitale")
st.markdown("""
L'idea di questa pagina è di rielaborare gli open data che Venezia offre riguardo alla residenza.

Il progetto è sul nascere, è più un test che sto portando avanti per capire cosa si può fare. 
Sicuramente ci sono errori e problemi.

Sulla sidebar (da telefono c'è una freccettina in alto a sinistra) puoi scegliere l'area che ti interessa.
""")

zone = ["Venezia Centro Storico", 
        "Isole (Centro Storico, Murano, Burano, Lido)", 
        "Comune di Venezia",
        "Terraferma",
        "Lido",
        "Murano (con Sant'Erasmo)",
        "Burano (con Mazzorbo e Torcello)",
        "Venezia Est (San Marco, Castello, Cannaregio, Sant'Elena)",
        "Venezia Ovest (Dorsoduro, San Polo, Santa Croce, Giudecca)"
        ]
zona = st.sidebar.selectbox(
    "Che zona vuoi visualizzare?", (zone)
)
st.markdown(f"# {zona}")

## READING THE DATA
with open('data/today.json') as json_file:
    today_data = json.load(json_file)
df = pd.read_csv("data/aggregated_data_today.csv")

if zona == "Venezia Centro Storico":    
    st.markdown(f"#### Al giorno d'oggi **{today_data['centro_storico']}** residenti")
    values_plot = df['centro_storico'].values
elif zona == "Isole (Centro Storico, Murano, Burano, Lido)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['isole']}** residenti")
    values_plot = df['isole'].values
elif zona == "Comune di Venezia":
    st.markdown(f"#### Al giorno d'oggi **{today_data['comune']}** residenti")
    values_plot = df['comune'].values
elif zona == "Terraferma":
    st.markdown(f"#### Al giorno d'oggi **{today_data['terraferma']}** residenti")
    values_plot = df['terraferma'].values
elif zona == "Lido":
    st.markdown(f"#### Al giorno d'oggi **{today_data['lido']}** residenti")
    values_plot = df['lido'].values
elif zona == "Murano (con Sant'Erasmo)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['murano']}** residenti")
    values_plot = df['murano'].values
elif zona == "Burano (con Mazzorbo e Torcello)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['burano']}** residenti")
    values_plot = df['burano'].values
elif zona == "Venezia Est (San Marco, Castello, Cannaregio, Sant'Elena)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['est']}** residenti")
    values_plot = df['est'].values
elif zona == "Venezia Ovest (Dorsoduro, San Polo, Santa Croce, Giudecca)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['ovest']}** residenti")
    values_plot = df['ovest'].values
else:
    st.markdown("#### Scegli una opzione dal menu (freccia in alto a sinistra)")
    values_plot = df['comune'].values

st.markdown("## Grafici")
st.markdown("""
Questa sezione è dedicata ai grafici. 
Lo scopo è visualizzare e dare un'idea della tendenza. 
Scegliendo dal menu la zona il grafico si aggiorna automaticamente.
""")



# PLOT 
fig, ax = plt.subplots()
ax.plot(df['dates'].values, values_plot)
ax.xaxis.set_major_locator(plt.MaxNLocator(5))
st.pyplot(fig)

st.markdown("""
### Vista generale
Come sono divisi i residenti in tutto il comune di Venezia?
""")
fig, ax = plt.subplots()
values = [today_data['centro_storico'], 
            today_data['murano'],
            today_data['terraferma'],
            today_data['lido'],
            today_data['burano']]
labels = ["Venezia Centro Storico", 
        "Murano (con Sant'Erasmo)",
        "Terraferma",
        "Lido",
        "Burano (con Mazzorbo e Torcello)"]
plt.title(f"Residenti al {today_data['date']}")
ax.pie(x=values, labels=labels)
st.pyplot(fig)

st.markdown("## Fonte")
st.markdown("""
Il contenuto della pagina è una rielaborazione dei dati relativi a Venezia.

Fonte: Opendata del comune di venezia, disponibili su dati.venezia.it

Esempio: [Popolazione per sesso ed età - Municipalità di Venezia Murano Burano](https://dati.venezia.it/?q=content/popolazione-sesso-ed-et%C3%A0-municipalit%C3%A0-di-venezia-murano-burano-0)

Disponibili sotto [Licenza CC-BY](https://dati.venezia.it/?q=licenza/cc)
""")

st.markdown("""
## Crediti

Il contatore dei veneziani è un'idea orginariamente di Venessia.com, non mia. [Qui](https://www.venessia.com/contatoreabitanti/) trovate maggiori informazioni al riguardo.
Questo progetto punta ad una rielaborazione dei dati e alla creazione di una API che permetta di diffondere le informazioni in maniera più rapida e veloce.
""")

st.markdown("""
## Ri-Uso

I dati sono pensati per il ri-uso. 
L'idea sarebbe di creare come detto una API che dia il numero di residenti, e magari in futuro anche un ecosistema che ritorni informazioni più interessanti e più dettagliate.
Anche una serie di icone o badge/shields ([vedi esempio](https://shields.io/) - [codice](https://github.com/badges/shields)) che diversi siti possano usare.

Al momento questo non c'è, ma su [opendata.lanassa.net](opendata.lanassa.net) trovate i primi tentativi di raccogliere i dati.
Il file [`aggregated_data.csv`](https://opendata.lanassa.net/aggregated_data_today.csv) contiene i dati aggregati come CSV (virgola come separatore) 
e il file [`today.json`](https://opendata.lanassa.net/today.json) contiene i dati di oggi come JSON. Il file JSON ha questa struttura:
""")
today_data
st.markdown("""
Questi due file (`aggregated_data.csv` e `today.json`) sono aggiornati giornalieramente (alle 00:12) e sovrascritti, in modo che uno possa usarli a piacimento.

Il codice che genera questa pagina si trova sulla [repo github](https://github.com/freerafiki/contatore-digitale): è python, fatto con Streamlit.
""")