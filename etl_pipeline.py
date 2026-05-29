"""
Pipeline de Automatización Financiera: Control de Desviaciones Presupuestarias
Autor: Rodrigo Alegre Alay
Descripción: ETL script que limpia datos contables sucios, calcula desvíos de OPEX/CAPEX,
             y genera alertas automáticas para la toma de decisiones.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def cargar_y_limpiar_datos(filepath):
    """Carga el archivo CSV, elimina registros nulos y estandariza fechas."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: El archivo {filepath} no existe.")
        
    df = pd.read_csv(filepath)
    
    # 1. Limpieza de filas completamente vacías (típico de reportes ERP)
    df = df.dropna(how='all')
    df = df.dropna(subset=['Centro_Costo', 'Monto_Real'])
    
    # 2. Estandarización de formatos de fecha mediante formato mixto
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='mixed')
    
    # 3. Asegurar tipos de datos numéricos para cálculos financieros
    df['Monto_Real'] = df['Monto_Real'].astype(float)
    df['Monto_Presupuesto'] = df['Monto_Presupuesto'].astype(float)
    
    return df

def analizar_desviaciones(df, umbral_alerta=1.05):
    """Calcula variaciones y levanta alertas si el gasto real supera el umbral presupuestado."""
    # Agrupamos por Centro de Costo y Tipo de Gasto
    resumen = df.groupby(['Centro_Costo', 'Tipo_Gasto']).agg({
        'Monto_Real': 'sum',
        'Monto_Presupuesto': 'sum'
    }).reset_index()
    
    # Cálculos de control de gestión
    resumen['Desvio_Absoluto'] = resumen['Monto_Real'] - resumen['Monto_Presupuesto']
    resumen['Ejecucion_Pct'] = resumen['Monto_Real'] / resumen['Monto_Presupuesto']
    
    # Lógica de Alertas de Control (Trigger de Alerta)
    print("\n=== AUDITORÍA DE ALERTAS PRESUPUESTARIAS ===")
    for index, row in resumen.iterrows():
        if row['Ejecucion_Pct'] >= umbral_alerta:
            print(f"[ALERTA CRÍTICA] {row['Centro_Costo']} ({row['Tipo_Gasto']}) "
                  f"ha excedido el presupuesto. Ejecución: {row['Ejecucion_Pct']:.1%}. "
                  f"Desvío: ${row['Desvio_Absoluto']:,.0f} CLP")
            
    return resumen

def generar_grafico_control(resumen, output_image='reporte_desvios.png'):
    """Genera una visualización ejecutiva del porcentaje de ejecución por área."""
    plt.figure(figsize=(10, 6))
    
    # Crear barras dinámicas
    colores = ['#e63946' if x >= 1.05 else '#a8dadc' for x in resumen['Ejecucion_Pct']]
    
    labels = resumen['Centro_Costo'] + " (" + resumen['Tipo_Gasto'] + ")"
    bars = plt.bar(labels, resumen['Ejecucion_Pct'] * 100, color=colores, edgecolor='black')
    
    # Línea base del presupuesto (100%)
    plt.axhline(y=100, color='gray', linestyle='--', linewidth=1.5, label='Presupuesto Aprobado (100%)')
    
    # Estética del gráfico corporativo
    plt.title('Porcentaje de Ejecución Presupuestaria por Centro de Costo', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('% Ejecución Real vs Presupuesto', fontsize=12)
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.legend()
    
    # Añadir etiquetas de texto sobre las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 2,
                 f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
                 
    plt.tight_layout()
    plt.savefig(output_image)
    print(f"\n[INFO] Gráfico ejecutivo exportado con éxito como '{output_image}'.")

if __name__ == "__main__":
    # Ejecución del Pipeline Completo (Simulación de Cierre de Mes)
    archivo_origen = "data_presupuesto.csv"
    
    data_limpia = cargar_y_limpiar_datos(archivo_origen)
    reporte_financiero = analizar_desviaciones(data_limpia)
    generar_grafico_control(reporte_financiero)