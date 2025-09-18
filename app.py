import pandas as pd
import numpy as np
from flask import Flask, request, render_template
from utility import get_result
from config_local_app import PATH_FILE,IS_LOCAL,USE_EXCEL
from db_firebase import upload_dataframe_to_firestore,intialize_db_firebase,create_df_form_cloud

app = Flask(__name__)
df =[]
sheet_list = ["studenti","iscrizioni","voti"]
####GETDATA
if USE_EXCEL:
    for sheet in sheet_list:
        df.append( pd.read_excel(PATH_FILE+ "database.xlsx", sheet_name=sheet))
else:
    db = intialize_db_firebase()
    for sheet in sheet_list:
        df.append( create_df_form_cloud(db,sheet))

###PRINT RESULT
col_stampare_voti = ["STUDENTE", "MATERIA", "VOTO", "ANNO DI CORSO","ANNO"]
col_stampa_alunni = ["STUDENTE","EMAIL", "NUMERO DI TELEFONO"]
col_stampa_iscrizioni = ["STUDENTE","ANNO","TIPOLOGIA","NOTE","AC"]

@app.route("/", methods=["GET"])
def search():
    df_alunni = df[0]
    df_iscrizioni = df[1]
    df_voti = df[2]
    query = request.args.get("query", default=None, type=str)
    print(f"nome cercato: {query}")
    results = {}
    if query:
    # Trovo tutti gli studenti che contengono la query
        studenti_match = get_result(df_alunni,query,"STUDENTE",col_stampa_alunni)
        altri = set(get_result(df_iscrizioni,query,"STUDENTE",col_stampa_iscrizioni)["STUDENTE"]).union(
            set(get_result(df_voti,query,"STUDENTE",col_stampare_voti)["STUDENTE"])
        )

        tutti_studenti = set(studenti_match["STUDENTE"]).union(altri)

        for stud in tutti_studenti:
            stud_info = df_alunni[df_alunni["STUDENTE"] == stud][col_stampa_alunni].to_dict(orient="records")
            iscr = df_iscrizioni[df_iscrizioni["STUDENTE"] == stud][col_stampa_iscrizioni].to_dict(orient="records")
            voti_stud = df_voti[df_voti["STUDENTE"] == stud][col_stampare_voti].to_dict(orient="records")

            results[stud] = {
                "info": stud_info[0] if stud_info else {},   # se non esiste in df studenti
                "iscrizioni": iscr,
                "voti": voti_stud
            }

        ##results = get_result(df_voti,query,"STUDENTE",col_stampare_voti)
    return render_template("search.html", risultati=results)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

    ''''


    hold_search = True
    with pd.ExcelWriter(PATH_EXPORT + "database.xlsx", engine="openpyxl") as writer:
        df_alunni.to_excel(writer, sheet_name="Studenti", index=False)
        df_iscrizioni.to_excel(writer, sheet_name="Iscrizioni", index=False)
        df_voti.to_excel(writer, sheet_name="Voti", index=False)

    while hold_search:
        query = input("Inserisci il nome da cercare o end per uscire: ").strip().lower()
        if query == "end":
            hold_search = False
        else:
            print("ALUNNI")
            ris_alunni = df_iscrizioni[df_iscrizioni["STUDENTE"].str.contains(query, case=False, na=False)]
            print_df(ris_alunni,"STUDENTE","AC",col_stampa_alunni)

            print("VOTI")
            ris_voti = df_voti[df_voti["STUDENTE"].str.contains(query, case=False, na=False)]
            print_df(ris_voti,"STUDENTE","AC",col_stampare_voti)



            ris_alunni_ord = ris_alunni.sort_values(by="NOME COMPLETO").sort_values(by="AC")
            print ("Iscrizioni trovate")
            print(ris_alunni_ord[col_stampa_alunni].to_string(index=False))

            ris_voti = df_voti[df_voti["STUDENTE"].str.contains(query, case=False, na=False)]
            ris_voti_ord = ris_voti.sort_values(by="STUDENTE").sort_values(by="ANNO DI CORSO")
            print ("Voti ottenuti")
            print(ris_voti_ord[colonne_da_stampare_voti].to_string(index=False))
            '''
