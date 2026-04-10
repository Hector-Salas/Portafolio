# Modelo de Valor Relativo 
Objetivo: Demostrar habilidades en modelado financiero, validación de datos y generación de reportes , alineado a la vacante de Analista de Ciencia de Datos
## Responsabilidades cubiertas
- **Modelos matemáticos** – ERP (Equity Risk Premium) para acciones vs bonos y ratio Oro/SP500.
- **Validación de cotizaciones** – Detección de outliers usando Mediana de Desviaciones Absolutas (MAD).
- **Reportes normativos** – Generación diaria de `cierre_operaciones.csv` y reporte.

## Metodología resumida
- **ERP** = Earnings Yield (1/PE) – TNX Yield (bono USA 10y).  
- **Z-score** con ventana móvil de 360 días.(Modificable) 
- **Señal:** Z > 1.5 → sobreponderar acciones (60%); Z < -1.5 → infraponderar (40%); sino neutral (50%).  
- **Outliers:** MAD con ventana de 5 días, umbral 3.0.  
- **Commodities:** Ratio Oro/SP500, mismo cálculo de Z-score.  
- **Correlación:** Matriz de correlación entre rendimientos de SP500, bonos y oro.

## Cómo ejecutarlo
1. Instalar dependencias: `pip install pandas numpy yfinance scipy seaborn matplotlib`
2. Ejecutar el notebook celda por celda (o correr todo con `Run All`).
3. Los reportes se generan automáticamente en la carpeta `reports/`.

## Contacto:
hsalas2003@gmail.com
