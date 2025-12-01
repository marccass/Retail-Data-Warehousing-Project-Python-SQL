import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os

# CONFIGURACIÓ
fitxer_csv = 'data/Sample - Superstore.csv'
nom_db = 'vendes.db' # Això crearà un fitxer que és la base de dades

def extreure_dades(path):
    print(f"🔄 Llegint el fitxer: {path}...")
    try:
        df = pd.read_csv(path, encoding='latin1')
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='utf-8')
    return df

def transformacio_neta(df):
    """
    Pas 2: TRANSFORM (Neteja i Modelatge en Estrella)
    """
    print("🧹 Netejant i transformant dades...")
    
    # 1. Dates
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y', errors='coerce')
    
    # 2. Creem la Taula de Dimensions: CLIENTS (DIM_CLIENTS)
    # Seleccionem columnes úniques i eliminem duplicats per tenir un catàleg de clients
    dim_clients = df[['Customer ID', 'Customer Name', 'Segment']].drop_duplicates(subset=['Customer ID'])
    
    # 3. Creem la Taula de Dimensions: PRODUCTES (DIM_PRODUCTES)
    # Atenció: En dades reals, un ID pot tenir noms diferents si ha canviat. 
    # Aquí simplifiquem agafant el primer que trobem.
    dim_productes = df[['Product ID', 'Product Name', 'Category', 'Sub-Category']].drop_duplicates(subset=['Product ID'])
    
    # 4. Creem la Taula de Dimensions: LLOCS (DIM_LLOCS)
    # Fem servir el Codi Postal com a clau
    dim_llocs = df[['Postal Code', 'City', 'State', 'Region', 'Country']].drop_duplicates(subset=['Postal Code'])
    
    # 5. Creem la Taula de Fets: VENDES (FACT_VENDES)
    # Només ens quedem amb els IDs (Claus Foranes) i els números
    fact_vendes = df[['Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 
                      'Customer ID', 'Product ID', 'Postal Code', 
                      'Sales', 'Quantity', 'Discount', 'Profit']]
    
    print(f"   - Clients únics: {len(dim_clients)}")
    print(f"   - Productes únics: {len(dim_productes)}")
    print(f"   - Vendes totals: {len(fact_vendes)}")
    
    return dim_clients, dim_productes, dim_llocs, fact_vendes

def carregar_a_sql(dim_clients, dim_productes, dim_llocs, fact_vendes):
    """
    Pas 3: LOAD (Càrrega a Base de Dades SQL)
    """
    print(f"💾 Guardant dades a {nom_db}...")
    
    # Creem el "motor" de connexió a SQLite
    engine = create_engine(f'sqlite:///{nom_db}')
    
    # Guardem cada DataFrame com una taula SQL
    # if_exists='replace' vol dir que si la taula ja existeix, l'esborra i la torna a crear
    dim_clients.to_sql('dim_clients', engine, if_exists='replace', index=False)
    dim_productes.to_sql('dim_productes', engine, if_exists='replace', index=False)
    dim_llocs.to_sql('dim_llocs', engine, if_exists='replace', index=False)
    fact_vendes.to_sql('fact_vendes', engine, if_exists='replace', index=False)
    
    print("✅ Càrrega completada amb èxit!")

# --- EXECUCIÓ DEL SCRIPT ---
if __name__ == "__main__":
    # 1. Extreure
    df_brut = extreure_dades(fitxer_csv)
    
    # 2. Transformar
    clients, productes, llocs, vendes = transformacio_neta(df_brut)
    
    # 3. Carregar
    carregar_a_sql(clients, productes, llocs, vendes)