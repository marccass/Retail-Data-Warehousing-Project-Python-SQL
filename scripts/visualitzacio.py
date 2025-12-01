import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1. Connectar a la Base de Dades
engine = create_engine('sqlite:///vendes.db')

# 2. Obtenir les dades amb SQL
query = """
SELECT p.Category, ROUND((SUM(f.Profit) / SUM(f.Sales)) * 100, 2) as Marge_Pct
FROM fact_vendes f
JOIN dim_productes p ON f."Product ID" = p."Product ID"
GROUP BY p.Category
ORDER BY Marge_Pct DESC;
"""
df = pd.read_sql(query, engine)

# 3. Crear el Gràfic
plt.figure(figsize=(10, 6))
colors = ['#2ecc71', '#3498db', '#e74c3c'] # Verd, Blau, Vermell (per al pitjor)

# Creem un gràfic de barres
bars = plt.bar(df['Category'], df['Marge_Pct'], color=colors)

# Afegim títol i etiquetes
plt.title('Rendibilitat per Categoria (Marge %)', fontsize=16)
plt.ylabel('Marge de Benefici (%)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Afegim el valor a sobre de cada barra
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

# 4. Guardar la imatge
plt.savefig('marge_benefici.png')
print("✅ Gràfic guardat com a 'marge_benefici.png'")