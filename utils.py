import os
import numpy as np
import pandas as pd
import pdb

def get_last_file(folder):
    files_list = os.listdir(folder)
    sorted = np.sort(files_list)
    full_path = os.path.join(folder, sorted[-1])
    print("read", full_path)
    return full_path

def get_files_list(folder):
    return np.sort(os.listdir(folder))

def get_files_number(folder):
    return len(os.listdir(folder))

class df_comune(object):
    """a class with base methods"""

    def __init__(self, file_path):
        try:
            self.df = pd.read_html(file_path)[0]
            self.isEmpty = False
        except:
            self.df = None 
            self.isEmpty = True

    def isValid(self):
        if self.isEmpty is True:
            return False
        return True

    def get_venezia_insulare(self):
        """venezia, murano, burano"""
        row_c1 = self.df["Municipalita'"] == "VENEZIA - MURANO - BURANO (VENEZIA INSULARE)"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values

    def get_venezia_litorale(self):
        row_c1 = self.df["Municipalita'"] == "LIDO - PELLESTRINA (VENEZIA LITORALE)"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values

    def get_totale_comune(self):
        row_c1 = self.df["Municipalita'"] == "TOTALI"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values


class df_isole(object):
    """a class with base methods"""

    def __init__(self, file_path):
        try:
            self.df = pd.read_html(file_path)[0]
            self.isEmpty = False
        except:
            self.df = None 
            self.isEmpty = True

    def isValid(self):
        if self.isEmpty is True:
            return False
        return True

    def get_est(self):
        """san marco, castello, cannaregio, sant'elena"""
        row_c1 = self.df["Quartiere"] == "S. MARCO, CASTELLO, S. ELENA, CANNAREGIO"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values

    def get_ovest(self):
        """dorsoduro, san polo, santa croce, giudecca"""
        row_c1 = self.df["Quartiere"] == "DORSODURO, S. POLO, S. CROCE, GIUDECCA, SACCA FISO"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values

    def get_murano(self):
        """murano, s.erasmo"""
        row_c1 = self.df["Quartiere"] == "MURANO, S. ERASMO"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values

    def get_burano(self):
        """burano, mazzorbo, torcello"""
        row_c1 = self.df["Quartiere"] == "BURANO, MAZZORBO, TORCELLO"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values

    def get_total(self):
        """tutti"""
        row_c1 = self.df["Quartiere"] == "TOTALI"
        row_c2 = self.df["Sesso"] == "M+F"
        row_values = row_c1.values*row_c2.values
        index = np.argmax(row_values.astype(int))
        row_values = self.df.iloc[index]
        return row_values
