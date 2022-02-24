import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

st.title("Contatore Digitale")
st.markdown("""
L'idea di questa pagina è di rielaborare gli open data che Venezia offre riguardo alla residenza.
I numeri si aggiornano automaticamente ogni notte.

Il progetto è sul nascere, è più un test che sto portando avanti per capire cosa si può fare.
Sicuramente ci sono errori e problemi. Più informazioni alla fine della pagina.

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
st.sidebar.markdown("## Scegli la zona di Venezia")
zona = st.sidebar.radio(
    "Che zona vuoi visualizzare?", (zone)
)
st.markdown(f"# {zona}")

## READING THE DATA
with open('data/today.json') as json_file:
    today_data = json.load(json_file)
df = pd.read_csv("data/aggregated_full_data_until_today.csv")
labels = today_data['labels']

if zona == "Venezia Centro Storico":
    st.markdown(f"#### Al giorno d'oggi **{today_data['centro_storico']['total']}** residenti")
    str_root = 'centro_storico'
elif zona == "Isole (Centro Storico, Murano, Burano, Lido)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['isole']['total']}** residenti")
    str_root = 'isole'
elif zona == "Comune di Venezia":
    st.markdown(f"#### Al giorno d'oggi **{today_data['comune']['total']}** residenti")
    str_root = 'comune'
elif zona == "Terraferma":
    st.markdown(f"#### Al giorno d'oggi **{today_data['terraferma']['total']}** residenti")
    str_root = 'terraferma'
elif zona == "Lido":
    st.markdown(f"#### Al giorno d'oggi **{today_data['lido']['total']}** residenti")
    str_root = 'lido'
elif zona == "Murano (con Sant'Erasmo)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['murano']['total']}** residenti")
    str_root = 'murano'
elif zona == "Burano (con Mazzorbo e Torcello)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['burano']['total']}** residenti")
    str_root = 'burano'
elif zona == "Venezia Est (San Marco, Castello, Cannaregio, Sant'Elena)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['est']['total']}** residenti")
    str_root = 'est'
elif zona == "Venezia Ovest (Dorsoduro, San Polo, Santa Croce, Giudecca)":
    st.markdown(f"#### Al giorno d'oggi **{today_data['ovest']['total']}** residenti")
    str_root = 'ovest'
else:
    st.markdown("#### Scegli una opzione dal menu (freccia in alto a sinistra)")
    str_root = 'centro_storico'

st.markdown("## Grafici")
st.markdown("""
Il primo grafico mostra il numero di residenti (in totale, senza divisioni per fasce d'età) della zona selezionata.
Scegliendo dal menu (in alto a sinistra) la zona il grafico si aggiorna automaticamente.
""")

# aliceblue, antiquewhite, aqua, aquamarine, azure, beige, bisque, black, blanchedalmond, blue, blueviolet, brown, burlywood, cadetblue, chartreuse, chocolate, coral, cornflowerblue, cornsilk, crimson, cyan, darkblue, darkcyan, darkgoldenrod, darkgray, darkgrey, darkgreen, darkkhaki, darkmagenta, darkolivegreen, darkorange, darkorchid, darkred, darksalmon, darkseagreen, darkslateblue, darkslategray, darkslategrey, darkturquoise, darkviolet, deeppink, deepskyblue, dimgray, dimgrey, dodgerblue, firebrick, floralwhite, forestgreen, fuchsia, gainsboro, ghostwhite, gold, goldenrod, gray, grey, green, greenyellow, honeydew, hotpink, indianred, indigo, ivory, khaki, lavender, lavenderblush, lawngreen, lemonchiffon, lightblue, lightcoral, lightcyan, lightgoldenrodyellow, lightgray, lightgrey, lightgreen, lightpink, lightsalmon, lightseagreen, lightskyblue, lightslategray, lightslategrey, lightsteelblue, lightyellow, lime, limegreen, linen, magenta, maroon, mediumaquamarine, mediumblue, mediumorchid, mediumpurple, mediumseagreen, mediumslateblue, mediumspringgreen, mediumturquoise, mediumvioletred, midnightblue, mintcream, mistyrose, moccasin, navajowhite, navy, oldlace, olive, olivedrab, orange, orangered, orchid, palegoldenrod, palegreen, paleturquoise, palevioletred, papayawhip, peachpuff, peru, pink, plum, powderblue, purple, red, rosybrown, royalblue, rebeccapurple, saddlebrown, salmon, sandybrown, seagreen, seashell, sienna, silver, skyblue, slateblue, slategray, slategrey, snow, springgreen, steelblue, tan, teal, thistle, tomato, turquoise, violet, wheat, white, whitesmoke, yellow, yellowgreen
fig = go.Figure()
#colors = ['mediumpurple', 'aquamarine', 'steelblue', 'mediumseagreen', \
#          'tomato', 'turquoise', 'springgreen', 'brown']
#for color, label in zip(colors, labels):
#    if not label == 'total':
y_vals = df[f"{str_root}_total"].values
fig.add_trace(go.Scatter(
    x=df['dates'],
    y=y_vals,
    hoverinfo='x+y',
    fill='tozeroy',
    line=dict(width=1.5, color='turquoise')
    #stackgroup='one', # define stack group
    #groupnorm='fraction' # sets the normalization for the sum of the stackgroup
))

# this would be only once if we plotted more data lines, that's why here
fig.update_layout(yaxis_range=(np.min(y_vals)*0.999, np.max(y_vals)*1.001),
                  margin={'l':10, 'r':10, 't':10, 'b':10})
st.plotly_chart(fig, use_container_width=True)
st.sidebar.markdown("## Altro")
pie_chart = st.sidebar.checkbox('Grafico a torta dei residenti divisi per età', value=True)
if pie_chart:
    st.markdown("""
### Grafico a torta
Per cercare di capire meglio come sono divisi i residenti per fasce d'età (si tiene conto solo della zona selezionata)
""")
    fig, ax = plt.subplots()
    pie_labels = []
    pie_values = []
    for k in today_data[str_root].keys():

        if not k == "total":
            pie_labels.append(labels[k])
            pie_values.append(today_data[str_root][k])

    ax.pie(pie_values, labels=pie_labels)
    st.pyplot(fig)
# fig, ax = plt.subplots()
# values = [today_data['centro_storico'],
#             today_data['murano'],
#             today_data['terraferma'],
#             today_data['lido'],
#             today_data['burano']]
# labels = ["Venezia Centro Storico",
#         "Murano (con Sant'Erasmo)",
#         "Terraferma",
#         "Lido",
#         "Burano (con Mazzorbo e Torcello)"]
# plt.title(f"Residenti al {today_data['date']}")
# ax.pie(x=values, labels=labels)
# st.pyplot(fig)
st.sidebar.markdown("## Informazioni")
show_source = st.sidebar.checkbox('Fonte', value=True)
if show_source:
    st.markdown("## Fonte")
    st.markdown("""
    Il contenuto della pagina è una rielaborazione dei dati relativi a Venezia.

    Fonte: Opendata del comune di venezia, disponibili su dati.venezia.it

    Esempio: [Popolazione per sesso ed età - Municipalità di Venezia Murano Burano](https://dati.venezia.it/?q=content/popolazione-sesso-ed-et%C3%A0-municipalit%C3%A0-di-venezia-murano-burano-0)

    Disponibili sotto [Licenza CC-BY](https://dati.venezia.it/?q=licenza/cc)
    """)

show_credits = st.sidebar.checkbox('Crediti', value=True)
if show_credits:
    st.markdown("""
## Crediti

Il contatore dei veneziani è un'idea orginariamente di Venessia.com, non mia.
[Qui trovate maggiori informazioni al riguardo](https://www.venessia.com/contatoreabitanti/).
Dateci un'occhiata, ne vale la pena.
Questo progetto punta ad una rielaborazione dei dati e alla creazione di una API che permetta di diffondere le informazioni in maniera più rapida e veloce.
""")

show_re_use = st.sidebar.checkbox('Ri-Uso', value=True)
if show_re_use:
    st.markdown("""
## Ri-Uso

I dati sono pensati per il ri-uso.
L'idea sarebbe di creare come detto una API che dia il numero di residenti, e magari in futuro anche un ecosistema che ritorni informazioni più interessanti e più dettagliate.
Anche una serie di icone o badge/shields ([vedi esempio](https://shields.io/) - [codice](https://github.com/badges/shields)) che diversi siti possano usare.

Mi piacerebbe molto lavorare sull'analisi dei dati e cercare di utilizzarli per tirar fuori delle valutazioni e delle conclusioni automaticamente.

Al momento questo non ci sono ancora API, ma su [https://opendata.lanassa.net](https://opendata.lanassa.net) trovate i primi tentativi di raccogliere i dati.
""")

show_data = st.sidebar.checkbox('Dati', value=True)
if show_data:
    st.markdown("""
## Dati
I file:
- [`aggregated_full_data_until_today.csv`](https://opendata.lanassa.net/aggregated_full_data_until_today.csv) contiene tutti i dati usati aggregati (incluse le fasce d'età) divisi per colonne in formato CSV (virgola come separatore)
- [`aggregated_simple_data_until_today.csv`](https://opendata.lanassa.net/aggregated_full_data_until_today.csv) contiene solo il dato totale per zona aggregato (senza le fasce d'età) divisi per colonne in formato CSV (virgola come separatore)
- [`today.json`](https://opendata.lanassa.net/today.json) contiene i dati di oggi come JSON.

Per avere un'idea dei dati, puoi dare un'occhiata qui al file JSON come anteprima.
""")
show_json = st.checkbox('mostrare il file json')
if show_json:
    today_data
st.markdown("""
Questi tre file (`aggregated_full_data_until_today.csv`, `aggregated_simple_data_until_today.csv` e `today.json`) sono aggiornati giornalieramente (alle 00:12) e sovrascritti,
in modo che uno possa usarli sapendo di trovare la stessa struttura ogni giorno con i nuovi dati.

Il codice che genera questa pagina si trova sulla [repo github](https://github.com/freerafiki/contatore-digitale): è python, fatto con Streamlit.
""")
show_contacts = st.sidebar.checkbox('Contatti', value=True)
if show_contacts:
    st.markdown("""
## Contatti

In caso di suggerimenti o segnalazioni, [contattatemi via mail](mailto:admin@freelab.org)
o [aprite una issue su github](https://github.com/freerafiki/contatore-digitale/issues/new)
(per quello vi serve un account github, ma è sicuramente comodo per questioni tecniche)
""")
