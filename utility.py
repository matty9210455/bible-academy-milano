import pandas as pd


def get_result (df,name,colonna_search,col_print):
    #print(voti_studenti)
    ris_df = df[df[colonna_search].str.contains(name, case=False, na=False)]
    ris_df_ord = ris_df.sort_values(by=colonna_search)
    return ris_df_ord[col_print]
