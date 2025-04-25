import pandas as pd
import os

def load_menu_data():
    path = os.path.join(os.path.dirname(__file__), '..', 'menu_data.xlsx')
    df = pd.read_excel(path)
    df.fillna('', inplace=True)
    return df

def filter_menu(df, gastronomic_type):
    if 'CATEGORIA' in df.columns:
        return df[df['CATEGORIA'].str.lower().str.contains(gastronomic_type.lower())]
    else:
        # fallback: assume entire dataset is usable
        return df








