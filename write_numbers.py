import os
import pandas as pd
import numpy as np
import pdb
import matplotlib.pyplot as plt
import utils as ut
import json
from datetime import datetime, timedelta

current_path = os.getcwd()
#pdb.set_trace()
if "Palma" in current_path:
    base_folder = "/Users/Palma/Documents/Projects/Contatore"
elif "palma" in current_path:
    base_folder = os.path.join(current_path, os.pardir)
else:
    base_folder = "/root/opendata_ve"
isole_folder = "isole_VE"
comune_folder = "comune_VE"

# output paths
output_folder = "data"
daily_output_folder = os.path.join(output_folder, "daily")
# create them if needed
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
if not os.path.exists(daily_output_folder):
    os.mkdir(daily_output_folder)

isole_files = ut.get_files_list(os.path.join(base_folder, isole_folder))
comune_files = ut.get_files_list(os.path.join(base_folder, comune_folder))
#last_isole_path = ut.get_last_file(os.path.join(base_folder, isole_path))
#last_comune_path = ut.get_last_file(os.path.join(base_folder, comune_path))
print(f"found {len(isole_files)} files")
print("first:", comune_files[0])
print("last:", isole_files[-1])

centro_storico = []
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
    isole_file_name = f"popolazione_{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}_isole.xls"
    isole_path = os.path.join(base_folder, isole_folder, isole_file_name)

    # if we are missing a day, just keep the data from yesterday
    # since we start reading files, the first file is not missing
    # so comune_df and isole_df should always be initialized
    if os.path.exists(comune_path):
        new_comune_df = ut.df_comune(comune_path)
    if new_comune_df.isValid() is True:
        comune_df = new_comune_df
    if os.path.exists(isole_path):
        new_isole_df = ut.df_isole(isole_path)
    if new_isole_df.isValid() is True:
        isole_df = new_isole_df

    # now each has a dictionary of values
    ve_ins_dict = comune_df.get_venezia_insulare()
    lido_dict = comune_df.get_venezia_litorale()
    comune_dict = comune_df.get_totale_comune()
    est_dict = isole_df.get_est()
    ovest_dict = isole_df.get_ovest()
    murano_dict = isole_df.get_murano()
    burano_dict = isole_df.get_burano()
    isole_dict = isole_df.get_total()
    labels_dict = ut.get_labels()
    terraferma_dict = {}
    centro_storico_dict = {}
    # using a loop to fill the values we are not reading but calculating
    # it's easier to make and to read and there are very few keys,
    # so no problem
    for _key in ve_ins_dict.keys():
        terraferma_dict[_key] = comune_dict[_key] - lido_dict[_key] - ve_ins_dict[_key]
        centro_storico_dict[_key] = est_dict[_key] + ovest_dict[_key]

    # if we do not have the daily file, repair and save it
    # otherwise skip
    date = f"{cur_date.year:04d}-{cur_date.month:02d}-{cur_date.day:02d}"
    cur_daily_json_path = os.path.join(daily_output_folder, f"{date}.json")
    if not os.path.exists(cur_daily_json_path):
        json_info = {
            'labels':labels_dict,
            'centro_storico':centro_storico_dict,
            've_mu_bu':ve_ins_dict,
            'lido':lido_dict,
            'est':est_dict,
            'ovest':ovest_dict,
            'murano':murano_dict,
            'burano':burano_dict,
            'isole':isole_dict,
            'comune':comune_dict,
            'terraferma':terraferma_dict
        }
        with open(cur_daily_json_path, 'w') as fj:
            json.dump(json_info, fj, indent=2)

    print("stopping here, TODO: aggregate the data and save in the .csv")
    pdb.set_trace()

    # preparing the values for the aggregated data


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
    centro_storico.append(centro_storico_tot)

    # step to next day
    cur_date += timedelta(days=1)

#pdb.set_trace()
big_df = pd.DataFrame()
big_df['centro_storico'] = centro_storico
big_df['ve_mu_bu'] = ve_mu_bu
big_df['lido'] = lido
big_df['est'] = est
big_df['ovest'] = ovest
big_df['murano'] = murano
big_df['burano'] = burano
big_df['isole'] = isole
big_df['terraferma'] = terraferma
big_df['comune'] = comune
big_df['dates'] = dates
date_str = f"{last_day.year:04d}-{last_day.month:02d}-{last_day.day:02d}"
# Values
todays_dict = {
    'centro_storico':int(centro_storico_tot),
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

daily_json_path = os.path.join(daily_output_folder, f"{date_str}.json")
with open(daily_json_path, 'w') as fj:
    json.dump(todays_dict, fj, indent=2)
todays_dict['date'] = date_str
current_json_path = os.path.join(output_folder, "today.json")
with open(current_json_path, 'w') as fj:
    json.dump(todays_dict, fj, indent=2)
dataframe_path = os.path.join(output_folder, f"aggregated_data_today.csv")
big_df.to_csv(dataframe_path)
