import pandas as pd
from read_file import parse_input_file
# Oggetto per il passaggio di dataframe e manipolazione degli stessi all'interno del codice.
class All():
    def __init__(self, file_path = None):
        self.file_path = file_path
        self.df_globalproperties, self.df_nodes, self.df_beams,  self.df_tetra, self.df_hexa, self.df_properties, self.df_solvers = parse_input_file(self.file_path)

    def get_df(self, idx):
        match idx:
            case 0: return self.df_nodes
            case 1: return self.df_beams
            case 2: return self.df_tetra
            case 3: return self.df_hexa
    
    def set_df(self, idx, df):
        match idx:
            case 0: self.df_nodes = df
            case 1: self.df_beams = df
            case 2: self.df_tetra = df
            case 3: self.df_hexa = df