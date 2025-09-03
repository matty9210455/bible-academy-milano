from flask import Flask, request, render_template
import pandas as pd
from models.db import get_connection
from config import USE_EXCEL, EXCEL_PATH
from utility import create_df_from_xlsx, get_voti

app = Flask(__name__)

# Se lavori in locale con Excel
if USE_EXCEL:
    df =create_df_from_xlsx(2019,2025)
else:
    # Esempio con PostgreSQL (Railway)
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM persone", conn)

@app.route("/", methods=["GET"])
def search():
    query = request.args.get("query", default=None, type=str)
    results = None
    if query:
        results = get_voti(query,df)
    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
