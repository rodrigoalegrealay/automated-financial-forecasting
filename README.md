# Pipeline ETL: Automatización de Control Presupuestario (OPEX/CAPEX)

## 📌 Propósito del Proyecto
Este proyecto implementa un pipeline automatizado en **Python (Pandas)** enfocado en ingeniería de datos financieros y control de gestión. El script procesa reportes de gastos multifuente/ERPs, ejecuta la limpieza de anomalías en los registros, consolida la información por centros de costos y genera alertas tempranas automáticas ante desviaciones presupuestarias críticas.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3
* **Librerías principales:** Pandas (Procesamiento y ETL), Matplotlib (Visualización Corporativa), OS (Gestión de Entornos).

## 📊 Arquitectura del Script y Funcionalidades
1. **Fase de Extracción y Limpieza (ETL):** Remueve registros nulos estructurales de sistemas de datos y estandariza múltiples formatos de fechas financieras a un estándar ISO (`YYYY-MM-DD`).
2. **Lógica Financiera Core:** Agrupa las transacciones por centro de costo de manera dinámica, calculando el desvío absoluto y los porcentajes reales de ejecución frente al Forecast aprobado.
3. **Módulo de Alertas Automáticas:** Gatilla notificaciones en consola para los ítems que sobrepasan un umbral de riesgo parametrizable (Ej: >105% del presupuesto).
4. **Reportería Visual:** Genera de manera automática un reporte gráfico (`reporte_desvios.png`) con formato e indicadores condicionales listos para la toma de decisiones de la gerencia de primera línea.
