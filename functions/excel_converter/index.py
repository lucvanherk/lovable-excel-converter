import pandas as pd
import tempfile
from supabase import create_client
import os

# Verkrijg je Supabase credentials uit de omgeving
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Welke kolommen we willen behouden
desired_columns = [
    'Person Name', 'Person First name', 'Person Last name', 'Person LinkedIn', 
    'Person Title', 'Person Department', 'Company', 'Domain',
    'Industries', 'LinkedIn Industry', 'Keywords',
    'Email (FullEnrich)', 'Size', 'City', 'Country'
]

def process_excel(file_path: str, output_filename: str):
    # Inlezen van het geüploade bestand
    df = pd.read_excel(file_path)
    cols = [c for c in desired_columns if c in df.columns]
    missing = set(desired_columns) - set(cols)
    if missing:
        return {'status': 'error', 'missing_columns': list(missing)}

    # Schoonmaken en hernoemen
    df_cleaned = df[cols].copy()
    df_cleaned.rename(columns={'Email (FullEnrich)': 'Email'}, inplace=True)
    df_jex2 = df_cleaned[['Company', 'Domain']]

    # Schrijf naar een tijdelijk bestand en upload naar Supabase Storage
    with tempfile.NamedTemporaryFile(suffix='.xlsx') as tmp:
        with pd.ExcelWriter(tmp.name, engine="openpyxl") as writer:
            df_cleaned.to_excel(writer, sheet_name="JEX", index=False)
            df_jex2.to_excel(writer, sheet_name="JEX2", index=False)
        tmp.seek(0)
        supabase.storage.from_("excel-files").upload(output_filename, tmp.name)

    # Haal de publieke download-URL op
    url = supabase.storage.from_("excel-files").get_public_url(output_filename)
    return {'status': 'success', 'download_url': url}

# HTTP-handler voor Supabase Edge Functions
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['POST'])
def handler():
    data = request.get_json(force=True)
    file_path = data.get('file_path')
    output_filename = data.get('output_filename')
    result = process_excel(file_path, output_filename)
    return jsonify(result)
