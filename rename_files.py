import os
import pdb

base_folder = "/root/opendata_ve"
base_folder = "/Users/Palma/Documents/Projects/Contatore"

isole_folder = "isole_VE"
comune_folder = "comune_VE"

for file in os.listdir(os.path.join(base_folder, isole_folder)):
    date = file[12:22].replace("_", "-")
    month = date[0:2]
    day = date[3:5]
    year = date[6:10]

    new_file_name = file[:12] + year + "-" + month + "-" + day + file[22:]
    print("changing ", file)
    print("to", new_file_name)
    old_path = os.path.join(base_folder, isole_folder, file)
    new_path = os.path.join(base_folder, isole_folder, new_file_name)
    os.rename(old_path, new_path)

for file in os.listdir(os.path.join(base_folder, comune_folder)):
    date = file[12:22].replace("_", "-")
    month = date[0:2]
    day = date[3:5]
    year = date[6:10]

    new_file_name = file[:12] + year + "-" + month + "-" + day + file[22:]
    print("changing ", file)
    print("to", new_file_name)
    old_path = os.path.join(base_folder, comune_folder, file)
    new_path = os.path.join(base_folder, comune_folder, new_file_name)
    os.rename(old_path, new_path)
