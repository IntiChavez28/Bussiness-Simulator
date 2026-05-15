# 📈 Business Growth Simulator

Un simulador interactivo de crecimiento empresarial construido con **Streamlit** y **Plotly**. Esta herramienta permite a emprendedores y dueños de negocio proyectar el comportamiento financiero y operativo de su empresa a 12 meses, ajustando variables clave en tiempo real.

## 🚀 Características

* **Modelado Financiero Completo:** Proyecta ingresos, utilidades netas, COGS y flujo de caja acumulado.
* **Métricas de Adquisición:** Analiza el impacto del CAC (Costo de Adquisición), ROAS y tasas de conversión en el crecimiento de la base de clientes.
* **Análisis de Retención:** Simula el impacto del *churn* (pérdida de clientes) y el crecimiento orgánico mensual.
* **Visualización Interactiva:** Gráficos dinámicos para:
    * Ingresos vs. Costos totales.
    * Utilidad neta mensual (con detección visual de pérdidas/ganancias).
    * Evolución de clientes activos vs. nuevos y churned.
    * Punto de equilibrio (Breakeven) en caja acumulada.
* **Escenarios Dinámicos:** Cambia entre proyecciones Realistas, Optimistas y Conservadoras con un solo clic.

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **Streamlit:** Para la interfaz de usuario y el despliegue rápido.
* **Plotly:** Para la generación de gráficos interactivos y tableros visuales.
* **Pandas & Numpy:** Para la lógica de simulación y procesamiento de datos.

## 📦 Instalación

1.  **Clona este repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/business-growth-simulator.git](https://github.com/tu-usuario/business-growth-simulator.git)
    cd business-growth-simulator
    ```

2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecuta la aplicación:**
    ```bash
    streamlit run business_simulator.py
    ```

## 📋 Parámetros de Simulación

Puedes ajustar los siguientes valores en la barra lateral:
* **Economía del producto:** Precio de venta y porcentaje de COGS.
* **Marketing:** Inversión mensual, CAC y Tasa de Conversión.
* **Retención:** Porcentaje de Churn y Crecimiento Orgánico.
* **Operación:** Costos fijos mensuales y capital inicial.

## 📊 Estructura del Proyecto

```text
business-growth-simulator/
├── business_simulator.py  # Código principal de la aplicación y lógica
├── requirements.txt       # Librerías necesarias (streamlit, plotly)
└── README.md              # Documentación del proyecto