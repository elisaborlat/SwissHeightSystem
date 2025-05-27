import pandas as pd
import geopandas as gpd

class DataManager:
    def __init__(self):
        self.data = None
        self.gdf = None
    
    def load_data(self, excel_file_path):
        """
        Load and merge data from multiple Excel sheets, ensuring uniqueness in columns
        and converting to GeoDataFrame.
        """

        # Load the file path
        file_path = 'data/raw/' + excel_file_path 

        if self.data is None:

            # Load Lagekoordinaten2 sheet
            print('---Loading Sheet Lagekoordinaten2---')
            df_lagekoordinaten = pd.read_excel(
                file_path,
                sheet_name='Lagekoordinaten2',
                usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13],
                names=['UELN_Nr', 'Kt_Ord', 'Groupe', 'E_LV95', 'N_LV95',\
                       'LN02', 'Typ/Bez', 'Herkunft', 'Ort', 'Punktart',\
                           'EVRF_trans_lon', 'EVRF_trans_lat', 'Lage_LHN95'],
                header=0
            )
            print(f'Lagekoordinaten2: {len(df_lagekoordinaten)} lines loaded.')

            # Load LHN95_DEF sheet
            print('---Loading Sheet LHN95-DEF---')
            df_lhn95_def = pd.read_excel(
                file_path,
                sheet_name='LHN95-DEF',
                usecols=[3, 4, 7, 8, 11, 14, 17],
                names=['Kt_Ord', 'LHN95_Herk', 'LHN95_Pot', 'LHN95_vPot', 'LHN95_Hortho', 'LHN95_Hnorm', 'LHN95_LN02'],
                header=0
            ).dropna(axis=0, how='all')
            print(f'LHN95-DEF: {len(df_lhn95_def)} lines loaded.')

            # Check for duplicates in 'Kt_Ord'
            self.check_duplicate('Kt_Ord', df_lhn95_def)

            # Merge Lagekoordinaten2 and LHN95_DEF
            resultat = pd.merge(df_lagekoordinaten, df_lhn95_def, on='Kt_Ord', how='left')
            print(f'Merge on attribute Kt_Ord: {len(resultat)} lines.')

            # Load EVRF2019_final_update sheet
            print('---Loading Sheet EVRF2019_final_update---')
            df_evrf2019_final_update = pd.read_excel(
                file_path,
                sheet_name='EVRF2019_final_update',
                usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                names=['Country', 'UELN_Nr', 'Pt_No_1', 'Pt_No_2', 'id_in_neighborhood', 'neighb_country',
                    'ETRS89_lat', 'ETRS89_lon', 'EVRF2019_pot', 'EVRF2019_Hnorm', 'EVRF2019_sH', 'EVRF2019_v', 'EVRF2019_pot_MT', 'EVRF2019_Hnorm_MT'],
                header=2
            ).dropna(subset=['UELN_Nr'])
            print(f'EVRF2019_final_update: {len(df_evrf2019_final_update)} lines loaded.')
        
            # Check for duplicates in 'UELN_Nr'
            self.check_duplicate('UELN_Nr', df_evrf2019_final_update)

            # Merge with EVRF2019_final_update on 'UELN_Nr'
            resultat = pd.merge(resultat, df_evrf2019_final_update, on='UELN_Nr', how='left')
            print(f'Merge on attribute UELN_Nr: {len(resultat)} lines.')

            # Load EVRF2019_alleCH sheet
            print('---Loading Sheet EVRF2019_alleCH---')
            df_evrf2019_alleCH = pd.read_excel(
                file_path,
                sheet_name='EVRF2019_alleCH',
                usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13,14],
                names=['alle_Kt_Ord', 'alle_kind', 'UELN_Nr', 'alle_Pt_No_1', 'alle_Pt_No_2', 'alle_id_in_neighborhood', 'alle_neighb_country',
                    'alle_ETRS89_lat', 'alle_ETRS89_lon', 'alle_EVRF2019_pot', 'alle_EVRF2019_Hnorm', 'alle_EVRF2019_sH', 'alle_EVRF2019_v', 'alle_EVRF2019_pot_MT', 'alle_EVRF2019_Hnorm_MT'],
                header=2
            ).dropna(subset=['UELN_Nr']) # line without UELN Nr are remouved 
            print(f'EVRF2019_alleCH: {len(df_evrf2019_alleCH)} lines loaded.')

            # Check for duplicates in 'UELN_Nr'
            self.check_duplicate('UELN_Nr', df_evrf2019_alleCH)

            # Merge with EVRF2019_alleCH on 'UELN_Nr'
            resultat = pd.merge(resultat, df_evrf2019_alleCH, on='UELN_Nr', how='left')
            print(f'Merge on attribute UELN_Nr: {len(resultat)} lines.')
            
            resultat['Pt_No_1'] = resultat['Pt_No_1'].astype(str)
            resultat['alle_Pt_No_1'] = resultat['alle_Pt_No_1'].astype(str)
            
            # Convert to GeoDataFrame
            gdf = gpd.GeoDataFrame(resultat, geometry=gpd.points_from_xy(resultat['E_LV95'], resultat['N_LV95']))

            # Store the results
            self.data = resultat
            self.gdf = gdf
            
    def check_duplicate(self, column_name, other_df=None):
        """Check for duplicate values in a specified column of a DataFrame."""
        if other_df is None : 
            df = self.data
        else : 
            df = other_df
            
        if df[column_name].is_unique:
            print(f"The '{column_name}' column is unique.")
        else:
            print(f"The '{column_name}' column is NOT unique.")
            # Find duplicated values and create a mask
            duplicated_mask = df[column_name].duplicated(keep=False)  # keep=False to mark all duplicates
            # Filter the DataFrame to return only rows with duplicated values
            duplicated_df = df[duplicated_mask]
            print(f"Duplicated {column_name} values: {duplicated_df[column_name].tolist()}")
            return duplicated_df
