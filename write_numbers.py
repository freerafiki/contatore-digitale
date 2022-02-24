import os
import pandas as pd
import numpy as np
import pdb
import matplotlib.pyplot as plt
import utils as ut
import json
from datetime import datetime, timedelta

if __name__ == '__main__':


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
    # setting cur_date to the start day.
    # this will be updated and used to create date information as strings
    cur_date = start_day
    delta = last_day - start_day
    iterations = delta.days
    print(f"we have {iterations+1} days")

    # We prepar two data frames, one for the simple data and one with the full data
    # we will fill them later
    simple_df = pd.DataFrame()
    full_df = pd.DataFrame()
    dates = [] # list of dates

    # labels dictionary:
    # keys are the keywords
    # and labels are the italiana explanation
    labels_dict = ut.get_labels()
    labels = labels_dict.keys()
    # these dictionaries will be filled with lists of values
    ve_ins_data = {}
    lido_data = {}
    comune_data = {}
    est_data = {}
    ovest_data = {}
    murano_data = {}
    burano_data = {}
    isole_data = {}
    terraferma_data = {}
    centro_storico_data = {}
    # here we create the empty lists
    for l_key in labels:
        ve_ins_data[l_key] = []
        lido_data[l_key] = []
        comune_data[l_key] = []
        est_data[l_key] = []
        ovest_data[l_key] = []
        murano_data[l_key] = []
        burano_data[l_key] = []
        isole_data[l_key] = []
        terraferma_data[l_key] = []
        centro_storico_data[l_key] = []

    # loop through the data (.xls files)
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

        # preparing the values for the aggregated data
        # we need to update each list inside the dict
        # so use an ad-hoc method
        ut.append_values(centro_storico_data, centro_storico_dict, labels)
        ut.append_values(ve_ins_data, ve_ins_dict, labels)
        ut.append_values(lido_data, lido_dict, labels)
        ut.append_values(comune_data, comune_dict, labels)
        ut.append_values(est_data, est_dict, labels)
        ut.append_values(ovest_data, ovest_dict, labels)
        ut.append_values(murano_data, murano_dict, labels)
        ut.append_values(burano_data, burano_dict, labels)
        ut.append_values(isole_data, isole_dict, labels)
        ut.append_values(terraferma_data, terraferma_dict, labels)
        dates.append(date)
        # step to next day
        cur_date += timedelta(days=1)

    #pdb.set_trace()
    # here we fill the dataframes
    # the simple with only total information
    simple_df['dates'] = dates
    simple_df['centro_storico'] = centro_storico_data['total']
    simple_df['ve_mu_bu'] = ve_ins_data['total']
    simple_df['lido'] = lido_data['total']
    simple_df['est'] = est_data['total']
    simple_df['ovest'] = ovest_data['total']
    simple_df['murano'] = murano_data['total']
    simple_df['burano'] = burano_data['total']
    simple_df['isole'] = isole_data['total']
    simple_df['terraferma'] = terraferma_data['total']
    simple_df['comune'] = comune_data['total']


    # and the full with all age information also
    # loop are repeated so columns are ordered
    # worse for code but better for readability of the .csv
    full_df['dates'] = dates
    for label in labels:
        full_df[f"centro_storico_{label}"] = centro_storico_data[label]
    for label in labels:
        full_df[f"ve_mu_bu_{label}"] = ve_ins_data[label]
    for label in labels:
        full_df[f"lido_{label}"] = lido_data[label]
    for label in labels:
        full_df[f"est_{label}"] = est_data[label]
    for label in labels:
        full_df[f"ovest_{label}"] = ovest_data[label]
    for label in labels:
        full_df[f"murano_{label}"] = murano_data[label]
    for label in labels:
        full_df[f"burano_{label}"] = burano_data[label]
    for label in labels:
        full_df[f"isole_{label}"] = isole_data[label]
    for label in labels:
        full_df[f"terraferma_{label}"] = terraferma_data[label]
    for label in labels:
        full_df[f"comune_{label}"] = comune_data[label]

    dataframe_path = os.path.join(output_folder, f"aggregated_full_data_until_today.csv")
    full_df.to_csv(dataframe_path)
    simple_dataframe_path = os.path.join(output_folder, f"aggregated_simple_data_until_today.csv")
    simple_df.to_csv(simple_dataframe_path)

    # Values
    date_str = f"{last_day.year:04d}-{last_day.month:02d}-{last_day.day:02d}"
    todays_dict = {
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
    print("last day (today) is ", date_str)
    # daily_json_path = os.path.join(daily_output_folder, f"{date_str}.json")
    # with open(daily_json_path, 'w') as fj:
    #     json.dump(todays_dict, fj, indent=2)
    # todays_dict['date'] = date_str
    current_json_path = os.path.join(output_folder, "today.json")
    with open(current_json_path, 'w') as fj:
        json.dump(todays_dict, fj, indent=2)
