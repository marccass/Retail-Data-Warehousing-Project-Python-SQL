-- CONSULTES PER AL PROJECTE CLEARPEAKS
-- Objectiu: Demostrar domini de JOINs, Agregacions i Ranking

-- 1. Quin és el Top 5 de Productes que donen més benefici?
-- Necessitem connectar la taula de fets (números) amb la de productes (noms).
SELECT 
    p."Product Name", 
    p.Category,
    SUM(f.Profit) as Benefici_Total
FROM fact_vendes f
JOIN dim_productes p ON f."Product ID" = p."Product ID"
GROUP BY p."Product Name", p.Category
ORDER BY Benefici_Total DESC
LIMIT 5;

-- 2. Vendes per Regió i Segment de Client
-- Unim Fets amb Llocs i Clients. Això és un "Join de 3 potes".
SELECT 
    l.Region,
    c.Segment,
    SUM(f.Sales) as Vendes_Totals
FROM fact_vendes f
JOIN dim_llocs l ON f."Postal Code" = l."Postal Code"
JOIN dim_clients c ON f."Customer ID" = c."Customer ID"
GROUP BY l.Region, c.Segment
ORDER BY l.Region, Vendes_Totals DESC;

-- 3. (Nivell Avançat) Marge de benefici per Categoria
-- Calculem (Benefici / Vendes) * 100 per veure la rendibilitat.
SELECT 
    p.Category,
    SUM(f.Sales) as Vendes,
    SUM(f.Profit) as Benefici,
    ROUND((SUM(f.Profit) / SUM(f.Sales)) * 100, 2) as Marge_Percentatge
FROM fact_vendes f
JOIN dim_productes p ON f."Product ID" = p."Product ID"
GROUP BY p.Category
ORDER BY Marge_Percentatge DESC;