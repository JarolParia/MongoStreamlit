"""
pages/2_🔍_Analisis.py
-----------------------
Página de análisis interactivo con gráficos Plotly y filtros en sidebar.
Responde preguntas de negocio concretas sobre las matrículas escolares.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dao.mongo_dao import MongoDAO
from services.data_service import (
    get_dataframe,
    conteo_por_campo,
    conteo_por_dos_campos,
    distribucion_edades,
    top_instituciones,
    resumen_general,
)

# ─── Configuración ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Análisis · Matrículas",
    page_icon="🔍",
    layout="wide",
)

COLORS = {
    "primary":    "#38bdf8",
    "secondary":  "#818cf8",
    "success":    "#4ade80",
    "warning":    "#fbbf24",
    "danger":     "#f87171",
    "bg":         "#0f172a",
    "card":       "#1e293b",
    "border":     "#334155",
    "text":       "#f1f5f9",
    "muted":      "#94a3b8",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.6)",
    font=dict(color=COLORS["text"], family="sans-serif"),
    xaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"]),
    yaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"]),
    margin=dict(t=50, b=40, l=40, r=20),
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    .page-header {
        background: linear-gradient(135deg, rgba(15, 39, 68, 0.95), rgba(30, 58, 95, 0.9));
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 18px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 18px 40px rgba(2, 8, 23, 0.2);
    }
    .page-kicker {
        display: inline-block;
        padding: 0.22rem 0.7rem;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.24);
        color: #bae6fd;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    .page-title {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0 0 0.3rem 0;
    }
    .page-sub { color: #cbd5e1; font-size: 0.98rem; line-height: 1.5; }
    .chart-title    { color: #f1f5f9; font-size: 1rem; font-weight: 700; margin-bottom: 0.2rem; }
    .chart-question { color: #94a3b8; font-size: 0.82rem; font-style: italic; margin-bottom: 0.8rem; }
    .kpi-box {
        background: linear-gradient(135deg, #1e3a5f, #0f2744);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 0.9rem 1rem;
        text-align: center;
        box-shadow: 0 12px 28px rgba(2, 8, 23, 0.14);
    }
    .kpi-box h4 { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;
                  letter-spacing: 0.07em; margin: 0 0 0.3rem 0; }
    .kpi-box p  { color: #38bdf8; font-size: 1.6rem; font-weight: 700; margin: 0; }
    div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.75);
        border-color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# ─── Conexión ─────────────────────────────────────────────────────────────────

dao = MongoDAO()
try:
    dao.connect()
except Exception as e:
    st.error("❌ No fue posible conectar con la base de datos.")
    st.stop()

df_base = get_dataframe(dao)

if df_base.empty:
    st.warning("⚠️ No hay datos disponibles. Ve al Inicio y presiona 'Cargar datos'.")
    dao.disconnect()
    st.stop()

# ─── Sidebar: filtros ─────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🔍 Filtros")
    st.caption("Los filtros aplican a todos los gráficos.")
    estado_opts  = ["Todos"] + sorted(df_base["estado"].dropna().unique().tolist())
    sel_estado   = st.selectbox("Estado",      estado_opts)
    genero_opts  = ["Todos"] + sorted(df_base["genero"].dropna().unique().tolist())
    sel_genero   = st.selectbox("Género",      genero_opts)
    zona_opts    = ["Todos"] + sorted(df_base["zona_sede"].dropna().unique().tolist())
    sel_zona     = st.selectbox("Zona",        zona_opts)
    estrato_opts = ["Todos"] + sorted(df_base["estrato"].dropna().unique().tolist())
    sel_estrato  = st.selectbox("Estrato",     estrato_opts)
    inst_opts    = ["Todas"] + sorted(df_base["instituci_n"].dropna().unique().tolist())
    sel_inst     = st.selectbox("Institución", inst_opts)

# ─── Aplicar filtros ──────────────────────────────────────────────────────────

df = df_base.copy()
if sel_estado  != "Todos":  df = df[df["estado"]      == sel_estado]
if sel_genero  != "Todos":  df = df[df["genero"]      == sel_genero]
if sel_zona    != "Todos":  df = df[df["zona_sede"]   == sel_zona]
if sel_estrato != "Todos":  df = df[df["estrato"]     == sel_estrato]
if sel_inst    != "Todas":  df = df[df["instituci_n"] == sel_inst]

# ─── Encabezado ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="page-header">
    <div class="page-kicker">Exploración interactiva</div>
    <div class="page-title">🔍 Análisis de Matrículas Escolares</div>
    <div class="page-sub">Explora el comportamiento de la matrícula con filtros dinámicos y visualizaciones enfocadas en los indicadores más relevantes.</div>
</div>
""", unsafe_allow_html=True)
st.caption(f"Mostrando **{len(df):,}** registros con los filtros seleccionados.")
st.divider()

# ─── KPIs ─────────────────────────────────────────────────────────────────────

resumen = resumen_general(df)
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f'<div class="kpi-box"><h4>Estudiantes</h4><p>{resumen.get("total",0):,}</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-box"><h4>Matriculados</h4><p>{resumen.get("matriculados",0):,}</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-box"><h4>Retirados</h4><p>{resumen.get("retirados",0):,}</p></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-box"><h4>Con Discapacidad</h4><p>{resumen.get("con_discapacidad",0):,}</p></div>', unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="kpi-box"><h4>Edad Promedio</h4><p>{resumen.get("edad_promedio","—")}</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FILA 1: Treemap instituciones  |  Scatter estrato × edad coloreado por estado
# ══════════════════════════════════════════════════════════════════════════════

col1, col2 = st.columns([1, 1.1])

with col1:
    # BAR HORIZONTAL — top instituciones
    st.markdown('<div class="chart-title">🏫 Top Instituciones por Número de Estudiantes</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿Qué instituciones concentran la mayor población estudiantil?</div>', unsafe_allow_html=True)

    df_inst = top_instituciones(df, top_n=8)
    if not df_inst.empty:
        fig1 = px.bar(
            df_inst.sort_values("cantidad"),
            x="cantidad", y="instituci_n",
            orientation="h",
            color="cantidad",
            color_continuous_scale=["#1e3a5f", "#38bdf8"],
            labels={"cantidad": "Estudiantes", "instituci_n": "Institución"},
        )
        fig1.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False,
                           yaxis_title="", xaxis_title="Estudiantes", height=370)
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Sin datos para este filtro.")

with col2:
    # BAR AGRUPADO — edad promedio por estrato y estado
    st.markdown('<div class="chart-title">📊 Edad Promedio por Estrato y Estado</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿Los estudiantes retirados tienen edades distintas según su estrato?</div>', unsafe_allow_html=True)

    df_sc = df[["edad", "estrato", "estado"]].dropna()
    df_sc = df_sc[df_sc["edad"].between(4, 20) & df_sc["estado"].isin(["MATRICULADO", "RETIRADO"])]

    if not df_sc.empty:
        df_avg = (
            df_sc.groupby(["estrato", "estado"])["edad"]
            .mean()
            .round(1)
            .reset_index()
            .rename(columns={"edad": "edad_promedio"})
        )
        fig2 = px.bar(
            df_avg, x="estrato", y="edad_promedio", color="estado",
            barmode="group",
            color_discrete_map={"MATRICULADO": COLORS["success"], "RETIRADO": COLORS["danger"]},
            text="edad_promedio",
            labels={"estrato": "Estrato", "edad_promedio": "Edad promedio", "estado": "Estado"},
        )
        fig2.update_traces(textposition="outside", textfont_color=COLORS["text"])
        fig2.update_layout(**PLOTLY_LAYOUT, height=370,
                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sin datos para este filtro.")

# ══════════════════════════════════════════════════════════════════════════════
# FILA 2: Pirámide poblacional  |  Heatmap estrato × grado
# ══════════════════════════════════════════════════════════════════════════════

col3, col4 = st.columns(2)

with col3:
    # PIRÁMIDE POBLACIONAL — reemplaza el bar chart de estrato × género
    st.markdown('<div class="chart-title">🎂 Pirámide Poblacional por Edad y Género</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿Cómo se compara la distribución de edades entre hombres y mujeres?</div>', unsafe_allow_html=True)

    df_pir = df[df["edad"].between(4, 20) & df["genero"].isin(["HOMBRE", "MUJER"])].copy()

    if not df_pir.empty:
        conteo_h = df_pir[df_pir["genero"] == "HOMBRE"]["edad"].value_counts().reset_index()
        conteo_h.columns = ["edad", "cantidad"]
        conteo_h["cantidad"] = -conteo_h["cantidad"]   # negativo = izquierda
        conteo_h["genero"] = "HOMBRE"

        conteo_m = df_pir[df_pir["genero"] == "MUJER"]["edad"].value_counts().reset_index()
        conteo_m.columns = ["edad", "cantidad"]
        conteo_m["genero"] = "MUJER"

        df_pir_plot = pd.concat([conteo_h, conteo_m]).sort_values("edad")

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="HOMBRE",
            y=df_pir_plot[df_pir_plot["genero"] == "HOMBRE"]["edad"],
            x=df_pir_plot[df_pir_plot["genero"] == "HOMBRE"]["cantidad"],
            orientation="h",
            marker_color=COLORS["primary"],
            hovertemplate="Edad %{y}<br>Hombres: %{customdata}<extra></extra>",
            customdata=df_pir_plot[df_pir_plot["genero"] == "HOMBRE"]["cantidad"].abs(),
        ))
        fig3.add_trace(go.Bar(
            name="MUJER",
            y=df_pir_plot[df_pir_plot["genero"] == "MUJER"]["edad"],
            x=df_pir_plot[df_pir_plot["genero"] == "MUJER"]["cantidad"],
            orientation="h",
            marker_color=COLORS["secondary"],
            hovertemplate="Edad %{y}<br>Mujeres: %{x}<extra></extra>",
        ))
        _layout_pir = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis", "margin")}
        fig3.update_layout(
            **_layout_pir,
            barmode="relative",
            xaxis=dict(
                title="← Hombres  |  Mujeres →",
                gridcolor=COLORS["border"],
                tickvals=[-60, -40, -20, 0, 20, 40, 60],
                ticktext=["60", "40", "20", "0", "20", "40", "60"],
            ),
            yaxis=dict(title="Edad", gridcolor=COLORS["border"]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(t=50, b=40, l=40, r=20),
            height=400,
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Sin datos de edad o género disponibles.")

with col4:
    # BAR 100% APILADO — tasa retiro vs matriculado por estrato
    st.markdown('<div class="chart-title">📋 Retiro vs Matrícula por Estrato (%)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿En qué estrato es mayor la proporción de retiro escolar?</div>', unsafe_allow_html=True)

    df_ep = conteo_por_dos_campos(df, "estrato", "estado")
    df_ep = df_ep[df_ep["estado"].isin(["MATRICULADO", "RETIRADO"])]

    if not df_ep.empty:
        totales = df_ep.groupby("estrato")["cantidad"].transform("sum")
        df_ep = df_ep.copy()
        df_ep["pct"] = (df_ep["cantidad"] / totales * 100).round(1)

        fig4 = px.bar(
            df_ep, x="estrato", y="pct", color="estado",
            barmode="stack",
            color_discrete_map={"MATRICULADO": COLORS["success"], "RETIRADO": COLORS["danger"]},
            text=df_ep["pct"].apply(lambda v: f"{v}%"),
            labels={"estrato": "Estrato", "pct": "% Estudiantes", "estado": "Estado"},
        )
        fig4.update_traces(textposition="inside", textfont_color="white")
        fig4.update_layout(**PLOTLY_LAYOUT, height=400,
                           yaxis_title="% Estudiantes", xaxis_title="Estrato",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Sin datos para este filtro.")

# ══════════════════════════════════════════════════════════════════════════════
# FILA 3: Box plot edades por grado  |  Línea de retiro acumulado por grado
# ══════════════════════════════════════════════════════════════════════════════

col5, col6 = st.columns(2)

with col5:
    # BOX PLOT — distribución de edades por grado
    st.markdown('<div class="chart-title">📦 Dispersión de Edades por Grado</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿Hay estudiantes fuera del rango esperado para su grado (rezago o adelanto)?</div>', unsafe_allow_html=True)

    df_box = df[df["edad"].between(4, 20) & df["grado_label"].notna()].copy()

    if not df_box.empty:
        orden_grados = sorted(df_box["grado_label"].unique(),
                              key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 99)
        fig5 = px.box(
            df_box, x="grado_label", y="edad",
            color="grado_label",
            category_orders={"grado_label": orden_grados},
            color_discrete_sequence=[
                COLORS["primary"], COLORS["secondary"], COLORS["success"],
                COLORS["warning"], COLORS["danger"], COLORS["muted"],
            ],
            labels={"grado_label": "Grado", "edad": "Edad"},
            points="outliers",
        )
        fig5.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=370)
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Sin datos de edad disponibles.")

with col6:
    # GRÁFICO DE ÁREA — tasa de retiro por grado
    st.markdown('<div class="chart-title">📉 Tasa de Retiro por Grado</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿En qué grado se concentra la mayor deserción escolar?</div>', unsafe_allow_html=True)

    if "grado_label" in df.columns and "estado" in df.columns:
        df_ret = (
            df.groupby("grado_label")["estado"]
            .value_counts()
            .unstack(fill_value=0)
            .reset_index()
        )
        if "RETIRADO" not in df_ret.columns:
            df_ret["RETIRADO"] = 0
        if "MATRICULADO" not in df_ret.columns:
            df_ret["MATRICULADO"] = 0

        df_ret["total"] = df_ret["RETIRADO"] + df_ret["MATRICULADO"]
        df_ret["pct_retiro"] = (df_ret["RETIRADO"] / df_ret["total"].replace(0, np.nan) * 100).round(1)
        df_ret = df_ret.sort_values("grado_label",
                                    key=lambda s: s.map(lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 99))

        if not df_ret.empty:
            fig6 = go.Figure()
            fig6.add_trace(go.Scatter(
                x=df_ret["grado_label"],
                y=df_ret["pct_retiro"],
                mode="lines+markers+text",
                fill="tozeroy",
                fillcolor="rgba(248,113,113,0.15)",
                line=dict(color=COLORS["danger"], width=2.5),
                marker=dict(size=9, color=COLORS["danger"],
                            line=dict(color="white", width=1.5)),
                text=df_ret["pct_retiro"].apply(lambda v: f"{v}%" if pd.notna(v) else ""),
                textposition="top center",
                textfont=dict(color=COLORS["text"], size=11),
                hovertemplate="<b>%{x}</b><br>Retiro: %{y:.1f}%<extra></extra>",
            ))
            fig6.update_layout(**PLOTLY_LAYOUT,
                               yaxis_title="% Retiro",
                               xaxis_title="Grado",
                               height=370)
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.info("Sin datos para este filtro.")
    else:
        st.info("Sin datos para este filtro.")

# ══════════════════════════════════════════════════════════════════════════════
# FILA 4: Zona donut  |  Discapacidad donut
# ══════════════════════════════════════════════════════════════════════════════

col7, col8 = st.columns(2)

with col7:
    # DONUT — proporción rural vs urbana
    st.markdown('<div class="chart-title">🥧 Proporción Rural vs Urbana</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿Qué porcentaje de estudiantes pertenece a cada zona?</div>', unsafe_allow_html=True)

    df_zona = conteo_por_campo(df, "zona_sede")
    if not df_zona.empty:
        colores_zona = [COLORS["warning"], COLORS["success"], COLORS["primary"]]
        fig7 = go.Figure(go.Pie(
            labels=df_zona["zona_sede"],
            values=df_zona["cantidad"],
            hole=0.55,
            marker_colors=colores_zona,
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>%{value} estudiantes<br>%{percent}<extra></extra>",
        ))
        fig7.update_layout(
            **PLOTLY_LAYOUT,
            showlegend=False,
            annotations=[dict(
                text=f"<b>{len(df):,}</b><br>total",
                x=0.5, y=0.5, font_size=13,
                font_color=COLORS["text"],
                showarrow=False,
            )],
            height=370,
        )
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.info("Sin datos para este filtro.")

with col8:
    # DONUT — tipos de discapacidad
    st.markdown('<div class="chart-title">♿ Tipos de Discapacidad Reportada</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-question">¿Qué proporción de estudiantes presenta cada tipo de discapacidad?</div>', unsafe_allow_html=True)

    df_disc = conteo_por_campo(df, "discapacidad")
    if not df_disc.empty:
        colores_disc = [
            COLORS["muted"], COLORS["primary"], COLORS["secondary"],
            COLORS["warning"], COLORS["danger"], COLORS["success"],
        ]
        fig8 = go.Figure(go.Pie(
            labels=df_disc["discapacidad"],
            values=df_disc["cantidad"],
            hole=0.55,
            marker_colors=colores_disc,
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>%{value} estudiantes<br>%{percent}<extra></extra>",
        ))
        fig8.update_layout(
            **PLOTLY_LAYOUT,
            legend=dict(font=dict(size=10), orientation="v"),
            annotations=[dict(
                text=f"<b>{len(df):,}</b><br>total",
                x=0.5, y=0.5, font_size=13,
                font_color=COLORS["text"],
                showarrow=False,
            )],
            height=370,
        )
        st.plotly_chart(fig8, use_container_width=True)
    else:
        st.info("Sin datos para este filtro.")

# ─── Cierre ───────────────────────────────────────────────────────────────────

dao.disconnect()
st.markdown("---")
st.caption("Fuente: datos.gov.co · SIMAT · Ministerio de Educación Nacional · Colombia")