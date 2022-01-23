import os
import pandas as pd
import numpy as np
import pdb
import matplotlib.pyplot as plt
import utils as ut
import json
from datetime import datetime, timedelta

current_path = os.getcwd()
if "Palma" in current_path:
    base_folder = "/Users/Palma/Documents/Projects/Contatore"
else:
    base_folder = "/root/opendata_ve"
isole_folder = "isole_VE"
comune_folder = "comune_VE"

isole_files = ut.get_files_list(os.path.join(base_folder, isole_folder))
comune_files = ut.get_files_list(os.path.join(base_folder, comune_folder))
#last_isole_path = ut.get_last_file(os.path.join(base_folder, isole_path))
#last_comune_path = ut.get_last_file(os.path.join(base_folder, comune_path))
print(f"found {len(isole_files)} files")
print("first:", comune_files[0])
print("last:", isole_files[-1])

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

    # check if the file is already in daily/
    date = f"{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}"
    date_str = f"{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}"
    hypothetic_file_name = f"data/daily/{date_str}.json"
    if not os.path.exists(hypothetic_file_name):
        print(f"{hypothetic_file_name} not found, making it")
        #for comune_file, isole_file in zip(comune_files, isole_files):
        #print(f"Checking {comune_file[12:23]}..")
        perc = int(j / iterations * 100)
        print(f"\rCompleted: {perc}%", end="")
        # Venezia Comune
        comune_file_name = f"popolazione_{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}_comune.xls"
        comune_path = os.path.join(base_folder, comune_folder, comune_file_name)
        if os.path.exists(comune_path):
            new_comune_df = ut.df_comune(comune_path)
        if new_comune_df.isValid() is True:
            comune_df = new_comune_df
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
            new_isole_df = ut.df_isole(isole_path)
        if new_isole_df.isValid() is True:
            isole_df = new_isole_df
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

        with open(hypothetic_file_name, 'w') as fj:
            json.dump(todays_dict, fj, indent=2)
    else:
        print(f"{hypothetic_file_name} found, skipping it")
    # step to next day
    cur_date += timedelta(days=1)

    
