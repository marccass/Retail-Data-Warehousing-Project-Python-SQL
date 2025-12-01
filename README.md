# End-to-End Retail Data Warehouse Pipeline

## 📌 Project Overview
Aquest projecte simula un entorn de **Business Intelligence** real. L'objectiu és transformar dades brutes de vendes en un **Data Warehouse** optimitzat per a l'anàlisi de negoci.

He construït un pipeline ETL (Extract, Transform, Load) complet utilitzant **Python** i he modelat les dades en un **Star Schema** (Model en Estrella) utilitzant **SQL**.

## 🛠 Tech Stack
* **Python:** Pandas (Data Cleaning), SQLAlchemy (ORM).
* **SQL:** SQLite, Window Functions, Joins, Aggregations.
* **Data Modeling:** Star Schema (Fact Table & Dimension Tables).
* **Visualization:** Matplotlib.

## 🏗 Architecture
Les dades es transformen d'un fitxer pla (`csv`) a un model relacional:
* **Fact Table:** `fact_vendes` (Transaccions).
* **Dimensions:** `dim_clients`, `dim_productes`, `dim_llocs`.

## 📊 Business Insights (Examples)
Mitjançant consultes SQL complexes, hem descobert que:
1.  La categoria **Technology** és la més rendible (17.4% de marge).
2.  La categoria **Furniture** té un rendiment crític (només 2.5%), suggerint problemes de costos logístics.

## 🚀 How to Run
1.  Install dependencies: `pip install -r requirements.txt`
2.  Run ETL pipeline: `python scripts/etl_pipeline.py`
3.  Execute analysis: `python scripts/executar_sql.py`