import pandas as pd
from config import USE_EXCEL, EXCEL_PATH

def intervalli_anni(start, end):
    if start > end:
        start, end = end, start
    return [f"{anno}-{anno+1}" for anno in range(start, end)]


def create_df_from_xlsx(primo_anno,ultimo_anno):
    anni = intervalli_anni(primo_anno, ultimo_anno)
    '''DATTAFRAME'''
    df_list_voti = [pd.read_excel(EXCEL_PATH+anno +" bible academy milano.xlsx",sheet_name="Voti") for anno in anni]
    voti_studenti = pd.concat(df_list_voti, ignore_index=True)
    return voti_studenti

def get_voti (name,voti_studenti):
    #print(voti_studenti)
    col_voti = ["Studente", "Materia", "Voto", "Anno di corso","Anno"]
    ris_voti = voti_studenti[voti_studenti["Studente"].str.contains(name, case=False, na=False)]
    ris_voti_ord = ris_voti.sort_values(by="Studente").sort_values(by="Anno di corso")
    return ris_voti_ord[col_voti]
