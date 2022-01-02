import os
import pandas as pd
import numpy as np
import pdb
import matplotlib.pyplot as plt
import utils as ut
import json

base_folder = "/Users/Palma/Documents/Projects/Contatore"
# base_folder = "/root/opendata_ve"
isole_folder = "isole_VE"
comune_folder = "comune_VE"

isole_files = ut.get_files_list(os.path.join(base_folder, isole_folder))
comune_files = ut.get_files_list(os.path.join(base_folder, comune_folder))
#last_isole_path = ut.get_last_file(os.path.join(base_folder, isole_path))
#last_comune_path = ut.get_last_file(os.path.join(base_folder, comune_path))

ve_mu_bu = []
lido = []
est = []
ovest = []
murano = []
burano = []
isole = []
comune = []
terraferma = []
dates = []
counter = 0
num_files = ut.get_files_number(os.path.join(base_folder, isole_folder))
for comune_file, isole_file in zip(comune_files, isole_files):
    #print(f"Checking {comune_file[12:23]}..")
    perc = int(counter / num_files * 100)
    print(f"\rCompleted: {perc}%", end="")
    counter += 1
    # Venezia Comune
    comune_path = os.path.join(base_folder, comune_folder, comune_file)
    comune_df = ut.df_comune(comune_path)
    #print("\nComune di Venezia\n")
    ve_mu_bu_values = comune_df.get_venezia_insulare()
    ve_mu_bu_tot = np.sum(ve_mu_bu_values[2:])
    lido_values = comune_df.get_venezia_litorale()
    lido_tot = np.sum(lido_values[2:])
    totale_comune_values = comune_df.get_totale_comune()
    totale_comune_tot = np.sum(totale_comune_values[2:])
    terraferma_tot = totale_comune_tot - lido_tot - ve_mu_bu_tot
    #print(f"insulare: {ve_mu_bu_tot}\nlido: {lido_tot}\ncomune: {totale_comune_tot}\n")

    isole_path = os.path.join(base_folder, isole_folder, isole_file)
    isole_df = ut.df_isole(isole_path)
    #print("\nVenezia e Isole\n")
    est_values = isole_df.get_est()
    est_tot = np.sum(est_values[2:])
    ovest_values = isole_df.get_ovest()
    ovest_tot = np.sum(ovest_values[2:])
    murano_values = isole_df.get_murano()
    murano_tot = np.sum(murano_values[2:])
    burano_values = isole_df.get_burano()
    burano_tot = np.sum(burano_values[2:])
    isole_values = isole_df.get_total()
    isole_tot = np.sum(isole_values[2:])

    #print(f"est: {est_tot}\novest: {ovest_tot}")
    #print(f"murano: {murano_tot}\nburano: {burano_tot}")
    #print("tot:", isole_tot)

    date = comune_file[12:22].replace("_", "-")
    dates.append(date)
    ve_mu_bu.append(ve_mu_bu_tot)
    lido.append(lido_tot)
    est.append(est_tot)
    ovest.append(ovest_tot)
    murano.append(murano_tot)
    burano.append(burano_tot)
    isole.append(isole_tot)
    comune.append(totale_comune_tot)
    terraferma.append(terraferma_tot)

big_df = pd.DataFrame()
big_df['ve_mu_bu'] = ve_mu_bu
big_df['lido'] = lido
big_df['est'] = est
big_df['ovest'] = ovest
big_df['murano'] = murano
big_df['burano'] = burano
big_df['terraferma'] = terraferma
big_df['dates'] = dates
date_str = comune_file[12:22]
todays_dict = {
    've_mu_bu':int(ve_mu_bu_tot),
    'lido':int(lido_tot),
    'est':int(est_tot),
    'ovest':int(ovest_tot),
    'murano':int(murano_tot),
    'burano':int(burano_tot),
    'isole':int(isole_tot),
    'comune':int(totale_comune_tot),
    'terraferma':int(terraferma_tot)
}
output_folder = "data"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
daily_json_path = os.path.join(output_folder, f"{date_str}.json")
with open(daily_json_path, 'w') as fj:
    json.dump(todays_dict, fj, indent=2)
todays_dict['date'] = date_str
current_json_path = os.path.join(output_folder, "today.json")
with open(current_json_path, 'w') as fj:
    json.dump(todays_dict, fj, indent=2)
dataframe_path = os.path.join(output_folder, f"aggregated_data_today.csv")
big_df.to_csv(dataframe_path)
