import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import json
from config_local_app import CREDENTIAL,IS_LOCAL,PATH_CREDENTIAL


# Inizializza Firebase
def intialize_db_firebase():
    cred = ""
    if IS_LOCAL:
        cred = credentials.Certificate(PATH_CREDENTIAL+"serviceAccountKey.json")
    else:
        cred = credentials.Certificate(CREDENTIAL)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def upload_dataframe_to_firestore(db, df, collection_name,id_col):
    for i, row in df.iterrows():
        #print(f"row {i}")
        data = row.to_dict()
        doc_id = str(data[id_col])
        data.pop(id_col, None)
        db.collection(collection_name).document(doc_id).set(data)

def create_df_form_cloud(db,raccolta):
    docs = db.collection(raccolta).get()
    lista_dati = [doc.to_dict() for doc in docs]
    df = pd.DataFrame(lista_dati)
    # 5️⃣ (Opzionale) Aggiungi colonna ID trasformando il campo "STUDENTE"
    #if "STUDENTE" in df_alunni.columns:
    #    df_alunni["ID"] = df_alunni["STUDENTE"].str.strip().str.replace(r"\s+", "_", regex=True)
    # 6️⃣ Visualizza il DataFrame
    print(df.head())
    return df
