import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Business Growth Simulator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Background */
  .stApp { background: #0f1117; }
  section[data-testid="stSidebar"] { background: #161b27 !important; border-right: 1px solid #1e2535; }

  /* Sidebar text */
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] .stMarkdown { color: #94a3b8 !important; font-size: 13px !important; }

  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }

  /* Slider accent */
  .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] { color: #334155; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: #161b27;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 1rem 1.25rem;
  }
  [data-testid="metric-container"] label { color: #64748b !important; font-size: 12px !important; letter-spacing: .06em; text-transform: uppercase; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 26px !important; font-weight: 700 !important; }
  [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 12px !important; }

  /* Headers */
  h1 { color: #f1f5f9 !important; font-weight: 700 !important; letter-spacing: -.03em; }
  h2 { color: #e2e8f0 !important; font-weight: 600 !important; font-size: 16px !important; }
  h3 { color: #94a3b8 !important; font-weight: 500 !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: .08em; }
  p  { color: #94a3b8 !important; }

  /* Divider */
  hr { border-color: #1e2535 !important; margin: 1.5rem 0 !important; }

  /* Select boxes */
  .stSelectbox select { background: #1e2535 !important; color: #e2e8f0 !important; border: 1px solid #2a3550 !important; }

  /* Section label inside sidebar */
  .section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 6px;
    margin-top: 18px;
  }

  /* Info box */
  .info-box {
    background: #0d1a2e;
    border: 1px solid #1e3a5f;
    border-left: 3px solid #3b82f6;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #64a4d8 !important;
    margin-top: 6px;
  }

  /* Chart container */
  .chart-container {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Plotly shared theme ───────────────────────────────────────────────────────
PLOTLY_BG   = "#161b27"
PLOTLY_GRID = "#1e2535"
PLOTLY_TEXT = "#94a3b8"
PLOTLY_FONT = dict(family="Inter, sans-serif", size=12, color=PLOTLY_TEXT)

def base_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(size=14, color="#e2e8f0"), x=0.02, xanchor="left"),
        paper_bgcolor=PLOTLY_BG,
        plot_bgcolor=PLOTLY_BG,
        font=PLOTLY_FONT,
        xaxis=dict(gridcolor=PLOTLY_GRID, zerolinecolor=PLOTLY_GRID, color=PLOTLY_TEXT),
        yaxis=dict(gridcolor=PLOTLY_GRID, zerolinecolor=PLOTLY_GRID, color=PLOTLY_TEXT),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)),
        margin=dict(l=50, r=20, t=45, b=40),
        hovermode="x unified",
    )

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Parámetros")
    st.markdown("Ajusta los valores para proyectar el crecimiento de tu negocio.")

    st.markdown('<p class="section-label">💰 Economía del producto</p>', unsafe_allow_html=True)
    price        = st.slider("Precio de venta (USD)", 10, 5000, 200, 10, format="$%d")
    cogs_pct     = st.slider("Costo del producto (% del precio)", 5, 80, 30, 1, format="%d%%")
    
    st.markdown('<p class="section-label">📣 Marketing & Adquisición</p>', unsafe_allow_html=True)
    monthly_inv  = st.slider("Inversión mensual en marketing (USD)", 100, 50000, 3000, 100, format="$%d")
    cac          = st.slider("Costo de adquisición por cliente (CAC)", 5, 2000, 80, 5, format="$%d")
    conversion   = st.slider("Tasa de conversión (%)", 0.5, 20.0, 3.5, 0.1, format="%.1f%%")

    st.markdown('<p class="section-label">🔄 Retención & Crecimiento</p>', unsafe_allow_html=True)
    churn        = st.slider("Churn mensual (%)", 0.0, 30.0, 5.0, 0.5, format="%.1f%%")
    growth_rate  = st.slider("Crecimiento orgánico mensual (%)", 0.0, 20.0, 2.0, 0.5, format="%.1f%%")
    ltv_months   = st.slider("Tiempo de vida del cliente (meses)", 1, 36, 12)

    st.markdown('<p class="section-label">🏢 Gastos operativos</p>', unsafe_allow_html=True)
    fixed_costs  = st.slider("Costos fijos mensuales (USD)", 0, 30000, 2500, 100, format="$%d")
    initial_cap  = st.slider("Capital inicial disponible (USD)", 0, 200000, 20000, 1000, format="$%d")

    st.markdown('<p class="section-label">🎯 Escenario</p>', unsafe_allow_html=True)
    scenario     = st.selectbox("Modo de proyección", ["Realista", "Optimista (+30%)", "Conservador (-30%)"])

    st.markdown('<div class="info-box">Los cálculos asumen que la inversión en marketing es constante y se reinvierte automáticamente cuando hay utilidades.</div>', unsafe_allow_html=True)

# ── Simulation logic ──────────────────────────────────────────────────────────
def simulate(price, cogs_pct, monthly_inv, cac, conversion,
             churn, growth_rate, ltv_months, fixed_costs,
             initial_cap, scenario, months=12):

    scen_mult = {"Realista": 1.0, "Optimista (+30%)": 1.30, "Conservador (-30%)": 0.70}[scenario]

    cogs         = price * cogs_pct / 100
    gross_margin = price - cogs
    ltv          = gross_margin * ltv_months

    data = []
    customers = 0
    cash      = initial_cap

    for m in range(1, months + 1):
        # New customers from paid marketing
        leads_paid   = (monthly_inv / max(cac, 1)) * (conversion / 100) * scen_mult
        # Organic growth on top of existing base
        leads_organic = customers * (growth_rate / 100) * scen_mult
        new_customers = max(0, leads_paid + leads_organic)
        
        # Churn existing
        churned = customers * (churn / 100)
        customers = max(0, customers + new_customers - churned)

        # Revenue
        revenue       = customers * price
        cogs_total    = customers * cogs
        gross_profit  = revenue - cogs_total
        total_costs   = monthly_inv + fixed_costs
        net_profit    = gross_profit - total_costs
        cumulative_cash = cash + net_profit

        # Ratios
        roas = revenue / max(monthly_inv, 1)
        cac_ratio = price / max(cac, 1)

        cash = cumulative_cash

        data.append({
            "Mes": m,
            "Clientes": round(customers),
            "Nuevos clientes": round(new_customers),
            "Churned": round(churned),
            "Ingresos": round(revenue, 2),
            "COGS total": round(cogs_total, 2),
            "Margen bruto": round(gross_profit, 2),
            "Costos totales": round(total_costs, 2),
            "Utilidad neta": round(net_profit, 2),
            "Caja acumulada": round(cash, 2),
            "ROAS": round(roas, 2),
            "CAC Ratio": round(cac_ratio, 2),
            "LTV": round(ltv, 2),
        })

    return pd.DataFrame(data)

df = simulate(price, cogs_pct, monthly_inv, cac, conversion,
              churn, growth_rate, ltv_months, fixed_costs, initial_cap, scenario)

# ── KPI Summary ───────────────────────────────────────────────────────────────
st.markdown("# 📈 Simulador de Crecimiento de Negocio")
st.markdown(f"Proyección a **12 meses** · Escenario: **{scenario}**")
st.markdown("---")

final     = df.iloc[-1]
mid       = df.iloc[5]
ltv_val   = (price - price * cogs_pct / 100) * ltv_months
breakeven = next((r["Mes"] for _, r in df.iterrows() if r["Utilidad neta"] >= 0), None)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Clientes — Mes 12",   f"{int(final['Clientes']):,}",    f"+{int(final['Clientes'] - df.iloc[0]['Clientes']):,}")
col2.metric("Ingresos — Mes 12",   f"${final['Ingresos']:,.0f}",      f"${final['Ingresos'] - df.iloc[0]['Ingresos']:,.0f}")
col3.metric("Utilidad neta M12",   f"${final['Utilidad neta']:,.0f}", f"${final['Utilidad neta'] - mid['Utilidad neta']:,.0f} vs M6")
col4.metric("LTV por cliente",     f"${ltv_val:,.0f}",               f"CAC: ${cac}")
col5.metric("Breakeven",           f"Mes {breakeven}" if breakeven else "No alcanzado", "✓ positivo" if breakeven else "⚠ negativo")

st.markdown("---")

# ── Charts row 1 ─────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure(layout=base_layout("Ingresos vs Costos totales"))
    fig.add_trace(go.Scatter(x=df["Mes"], y=df["Ingresos"],
        name="Ingresos", fill="tozeroy",
        line=dict(color="#3b82f6", width=2),
        fillcolor="rgba(59,130,246,0.10)"))
    fig.add_trace(go.Scatter(x=df["Mes"], y=df["Costos totales"],
        name="Costos totales", line=dict(color="#f87171", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=df["Mes"], y=df["Margen bruto"],
        name="Margen bruto", line=dict(color="#34d399", width=2)))
    fig.update_xaxes(title_text="Mes", dtick=1)
    fig.update_yaxes(title_text="USD", tickprefix="$")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    colors = ["#34d399" if v >= 0 else "#f87171" for v in df["Utilidad neta"]]
    fig2 = go.Figure(layout=base_layout("Utilidad neta mensual"))
    fig2.add_trace(go.Bar(
        x=df["Mes"], y=df["Utilidad neta"],
        marker_color=colors, name="Utilidad neta",
        text=[f"${v:,.0f}" for v in df["Utilidad neta"]],
        textposition="outside", textfont=dict(size=10, color="#94a3b8")))
    fig2.add_hline(y=0, line_color="#475569", line_dash="dash", line_width=1)
    fig2.update_xaxes(title_text="Mes", dtick=1)
    fig2.update_yaxes(title_text="USD", tickprefix="$")
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts row 2 ─────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    fig3 = go.Figure(layout=base_layout("Evolución de clientes"))
    fig3.add_trace(go.Scatter(x=df["Mes"], y=df["Clientes"],
        name="Clientes activos", fill="tozeroy",
        line=dict(color="#a78bfa", width=2.5),
        fillcolor="rgba(167,139,250,0.10)"))
    fig3.add_trace(go.Bar(x=df["Mes"], y=df["Nuevos clientes"],
        name="Nuevos", marker_color="rgba(59,130,246,0.5)", yaxis="y2"))
    fig3.add_trace(go.Bar(x=df["Mes"], y=[-v for v in df["Churned"]],
        name="Churned", marker_color="rgba(248,113,113,0.5)", yaxis="y2"))
    fig3.update_layout(
        yaxis2=dict(overlaying="y", side="right", showgrid=False,
                    color=PLOTLY_TEXT, title="Δ clientes/mes"),
        barmode="overlay")
    fig3.update_xaxes(title_text="Mes", dtick=1)
    fig3.update_yaxes(title_text="Clientes activos")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = go.Figure(layout=base_layout("Caja acumulada"))
    fig4.add_trace(go.Scatter(
        x=df["Mes"], y=df["Caja acumulada"],
        fill="tonexty", mode="lines+markers",
        line=dict(color="#fbbf24", width=2.5),
        fillcolor="rgba(251,191,36,0.08)",
        marker=dict(size=6, color="#fbbf24"),
        name="Caja acumulada"))
    fig4.add_hline(y=0, line_color="#f87171", line_dash="dash",
                   line_width=1, annotation_text="Break-even",
                   annotation_font_color="#f87171")
    fig4.update_xaxes(title_text="Mes", dtick=1)
    fig4.update_yaxes(title_text="USD", tickprefix="$")
    st.plotly_chart(fig4, use_container_width=True)

# ── Charts row 3 ─────────────────────────────────────────────────────────────
c5, c6 = st.columns([1.6, 1])

with c5:
    fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    fig5.add_trace(go.Scatter(x=df["Mes"], y=df["ROAS"],
        name="ROAS", line=dict(color="#38bdf8", width=2)), secondary_y=False)
    fig5.add_trace(go.Scatter(x=df["Mes"], y=df["Margen bruto"] / df["Ingresos"].replace(0, 1) * 100,
        name="Margen bruto (%)", line=dict(color="#4ade80", width=2, dash="dot")), secondary_y=True)
    fig5.update_layout(**base_layout("ROAS y margen bruto"))
    fig5.update_xaxes(title_text="Mes", dtick=1, gridcolor=PLOTLY_GRID, color=PLOTLY_TEXT)
    fig5.update_yaxes(title_text="ROAS (×)", secondary_y=False,
                      gridcolor=PLOTLY_GRID, color=PLOTLY_TEXT)
    fig5.update_yaxes(title_text="Margen bruto (%)", secondary_y=True,
                      ticksuffix="%", color=PLOTLY_TEXT, showgrid=False)
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    # Donut: revenue breakdown at month 12
    labels = ["COGS", "Marketing", "Costos fijos", "Utilidad neta"]
    vals_raw = [
        final["COGS total"],
        monthly_inv,
        fixed_costs,
        max(0, final["Utilidad neta"])
    ]
    vals = [max(0, v) for v in vals_raw]
    colors_donut = ["#f87171", "#fbbf24", "#a78bfa", "#34d399"]
    fig6 = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.58,
        marker=dict(colors=colors_donut,
                    line=dict(color=PLOTLY_BG, width=2)),
        textfont=dict(size=11, color="#e2e8f0"),
        hovertemplate="%{label}<br>$%{value:,.0f}<extra></extra>"))
    fig6.update_layout(**base_layout("Distribución de ingresos — Mes 12"))
    fig6.update_layout(
        legend=dict(orientation="v", y=0.5, font=dict(size=11)),
        annotations=[dict(text=f"${final['Ingresos']:,.0f}",
                          x=0.5, y=0.5, font_size=14,
                          font_color="#e2e8f0", showarrow=False)])
    st.plotly_chart(fig6, use_container_width=True)

# ── Data table ────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 Ver tabla de proyección completa"):
    display_df = df[["Mes","Clientes","Nuevos clientes","Churned",
                      "Ingresos","Margen bruto","Costos totales",
                      "Utilidad neta","Caja acumulada","ROAS"]].copy()
    for col in ["Ingresos","Margen bruto","Costos totales","Utilidad neta","Caja acumulada"]:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
    display_df["ROAS"] = display_df["ROAS"].apply(lambda x: f"{x:.2f}×")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#334155; font-size:12px;'>"
    "Business Growth Simulator · Proyecciones ilustrativas basadas en los parámetros ingresados"
    "</p>",
    unsafe_allow_html=True
)
