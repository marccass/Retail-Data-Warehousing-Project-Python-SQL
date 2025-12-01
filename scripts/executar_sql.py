import pandas as pd
from sqlalchemy import create_engine

# Connectem a la base de dades que has creat
engine = create_engine('sqlite:///vendes.db')

def executar_query(titol, query_sql):
    print(f"\n--- {titol} ---")
    # Pandas llegeix directament el resultat de la query SQL
    df_resultat = pd.read_sql(query_sql, engine)
    print(df_resultat)

# QUERY 1: Top Productes
query1 = """
SELECT p."Product Name", SUM(f.Profit) as Benefici
FROM fact_vendes f
JOIN dim_productes p ON f."Product ID" = p."Product ID"
GROUP BY p."Product Name"
ORDER BY Benefici DESC LIMIT 5;
"""

executar_query("TOP 5 PRODUCTES MÉS RENTABLES", query1)

# QUERY 2: Marge per Categoria
query2 = """
SELECT p.Category, ROUND((SUM(f.Profit) / SUM(f.Sales)) * 100, 2) as Marge_Pct
FROM fact_vendes f
JOIN dim_productes p ON f."Product ID" = p."Product ID"
GROUP BY p.Category
ORDER BY Marge_Pct DESC;
"""

executar_query("MARGE DE BENEFICI PER CATEGORIA", query2)