import os
import pandas as pd
import numpy as np
import pdb
import matplotlib.pyplot as plt
import utils as ut
import json
from datetime import datetime, timedelta

base_folder = "/Users/Palma/Documents/Projects/Contatore"
# base_folder = "/root/opendata_ve"
isole_folder = "isole_VE"
comune_folder = "comune_VE"

isole_files = ut.get_files_list(os.path.join(base_folder, isole_folder))
comune_files = ut.get_files_list(os.path.join(base_folder, comune_folder))
#last_isole_path = ut.get_last_file(os.path.join(base_folder, isole_path))
#last_comune_path = ut.get_last_file(os.path.join(base_folder, comune_path))
print(f"found {len(isole_files)} files")
print("first:", comune_files[0])
print("last:", isole_files[-1])

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
num_files_i = ut.get_files_number(os.path.join(base_folder, isole_folder))
num_files_c = ut.get_files_number(os.path.join(base_folder, isole_folder))
start_day_string = comune_files[0][12:22]
start_day = datetime.strptime(start_day_string, '%Y-%m-%d')
last_day_string = comune_files[-1][12:22]
last_day = datetime.strptime(last_day_string, '%Y-%m-%d')
cur_date = start_day
delta = last_day - start_day
iterations = delta.days
print(f"we have {iterations} days")
#pdb.set_trace()
for j in range(iterations+1):

    #for comune_file, isole_file in zip(comune_files, isole_files):
    #print(f"Checking {comune_file[12:23]}..")
    perc = int(j / iterations * 100)
    print(f"\rCompleted: {perc}%", end="")
    # Venezia Comune
    comune_file_name = f"popolazione_{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}_comune.xls"
    comune_path = os.path.join(base_folder, comune_folder, comune_file_name)
    if os.path.exists(comune_path):
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

    isole_file_name = f"popolazione_{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}_isole.xls"
    isole_path = os.path.join(base_folder, isole_folder, isole_file_name)
    if os.path.exists(isole_path):
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

    date = f"{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}"
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

    # step to next day
    cur_date += timedelta(days=1)

#pdb.set_trace()
big_df = pd.DataFrame()
big_df['ve_mu_bu'] = ve_mu_bu
big_df['lido'] = lido
big_df['est'] = est
big_df['ovest'] = ovest
big_df['murano'] = murano
big_df['burano'] = burano
big_df['terraferma'] = terraferma
big_df['dates'] = dates
date_str = f"{last_day.year:04d}-{last_day.month:02d}-{last_day.day:02d}"
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
print("last day (today) is ", date_str)
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
