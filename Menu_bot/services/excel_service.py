import pandas as pd

def load_menu_data():
    df = pd.read_excel('menu_data.xlsx')
    df.fillna('', inplace=True)
    return df

def filter_menu(df, gastronomic_type):
    return df[df['Opciones'].str.lower().str.contains(gastronomic_type.lower())]









