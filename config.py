import os

# Usa Excel in locale, DB in produzione
USE_EXCEL = os.getenv("USE_EXCEL", "true").lower() == "true"

# Path file Excel
EXCEL_PATH = os.getenv("EXCEL_PATH", "../Bible Academy Milano/")

# Stringa connessione DB (Railway la fornisce)
DATABASE_URL = os.getenv("DATABASE_URL")
