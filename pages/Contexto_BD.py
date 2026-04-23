"""
pages/1_📊_Contexto_BD.py
--------------------------
Página de contexto técnico de la base de datos MongoDB.
Muestra metadata, schema inferido, explorador y muestra de documentos.
"""

import streamlit as st
import pandas as pd
from dao.mongo_dao import MongoDAO
from services.data_service import get_dataframe

# ─── Configuración ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Contexto BD · Matrículas",
    page_icon="📊",
    layout="wide",
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
    .page-sub {
        color: #cbd5e1;
        font-size: 0.98rem;
        line-height: 1.5;
    }
    .info-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1rem 1.4rem;
        box-shadow: 0 12px 28px rgba(2, 8, 23, 0.14);
    }
    .info-card h4 { 
        color: #94a3b8; 
        font-size: 0.8rem; 
        text-transform: uppercase;
        letter-spacing: 0.07em; 
        margin: 0 0 0.3rem 0; 
    }
    .info-card p  { 
        color: #f1f5f9; 
        font-size: 1.4rem; 
        font-weight: 700; 
        margin: 0; 
    }
    .field-row {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid #233248;
        border-radius: 10px;
        padding: 0.45rem 0.75rem;
        margin-bottom: 0.4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.5rem;
        min-width: 100%;
        box-sizing: border-box;
    }
    .field-name {
        color: #38bdf8;
        font-family: monospace;
        font-size: 0.85rem;
        font-weight: 600;
        flex: 1;
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .badge {
        flex-shrink: 0;
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
    }
    .badge-green { background: #14532d; color: #4ade80; }
    .badge-yellow { background: #713f12; color: #fbbf24; }
    .badge-red { background: #7f1d1d; color: #f87171; }

    .result-count { 
        color: #94a3b8; 
        font-size: 0.88rem; 
        margin: 0.4rem 0 0.6rem 0; 
    }
    .result-count span { 
        color: #38bdf8; 
        font-weight: 700; 
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.75);
        border-color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# ─── Encabezado ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="page-header">
    <div class="page-kicker">Resumen general</div>
    <div class="page-title">📊 Contexto de la Base de Datos</div>
    <div class="page-sub">
        Consulta el volumen de registros, los campos disponibles y explora la información con búsqueda y filtros en tiempo real.
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Conexión ─────────────────────────────────────────────────────────────────

dao = MongoDAO()
try:
    dao.connect()
except Exception:
    st.error("❌ No fue posible conectar con la base de datos.")
    st.caption("Verifica la configuración de conexión e inténtalo nuevamente.")
    st.stop()

# ─── Métricas ─────────────────────────────────────────────────────────────────

info = dao.get_collection_info()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="info-card"><h4>Base de Datos</h4><p>{info["db_name"]}</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="info-card"><h4>Colección</h4><p>{info["collection_name"]}</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="info-card"><h4>Registros</h4><p>{info["total_documents"]:,}</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="info-card"><h4>Campos</h4><p>{len(info["fields"])}</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Schema ───────────────────────────────────────────────────────────────────

st.markdown("### 🗂️ Estructura de los datos")
st.caption("Campos disponibles y nivel de completitud de la información.")

df_full = get_dataframe(dao)

if df_full.empty:
    st.warning("⚠️ No hay datos en la colección. Ve al Inicio y presiona 'Cargar datos'.")
    dao.disconnect()
    st.stop()

col_schema, col_sample = st.columns([5, 0.2])

with col_schema:
    total = len(df_full)

    colA, colB, colC, colD, colE, colF = st.columns(6)

    for i, col in enumerate(df_full.columns):
        nulos = df_full[col].isna().sum() + (df_full[col] == "NR").sum()
        pct_ok = round((1 - nulos / total) * 100)

        if pct_ok >= 90:
            badge = f'<span class="badge badge-green">✓ {pct_ok}%</span>'
        elif pct_ok >= 50:
            badge = f'<span class="badge badge-yellow">⚠ {pct_ok}%</span>'
        else:
            badge = f'<span class="badge badge-red">✗ {pct_ok}%</span>'

        html = f'<div class="field-row"><span class="field-name">{col}</span><span>{badge}</span></div>'

        if i % 6 == 0:
            colA.markdown(html, unsafe_allow_html=True)
        elif i % 6 == 1:
            colB.markdown(html, unsafe_allow_html=True)
        elif i % 6 == 2:
            colC.markdown(html, unsafe_allow_html=True)
        elif i % 6 == 3:
            colD.markdown(html, unsafe_allow_html=True)
        elif i % 6 == 4:
            colE.markdown(html, unsafe_allow_html=True)
        else:
            colF.markdown(html, unsafe_allow_html=True)

st.divider()
# ══════════════════════════════════════════════════════════════════════════════
# EXPLORADOR DE REGISTROS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("### 🔍 Explorador de Registros")
st.caption("Busca, filtra y ajusta cuántos registros quieres ver.")

COLUMNAS_CLAVE = ["estado", "genero", "estrato", "zona_sede", "grado_label", "edad", "instituci_n", "discapacidad", "nivel"]
cols_disponibles = [c for c in COLUMNAS_CLAVE if c in df_full.columns]
cols_extra = [c for c in df_full.columns if c not in COLUMNAS_CLAVE and not c.startswith("_")]

ctrl1, ctrl2, ctrl3 = st.columns([1.8, 1.2, 0.8])
with ctrl1:
    busqueda = st.text_input("Buscar", placeholder="Ej: I.E. Pío XII, RETIRADO, RURAL...", label_visibility="collapsed")
with ctrl2:
    col_filtro = st.selectbox("Campo", options=["Todos los campos"] + cols_disponibles, label_visibility="collapsed")
with ctrl3:
    max_rows = len(df_full)

    n_rows = st.slider(
        "Registros",
        min_value=10,
        max_value=max_rows,
        value=min(50, max_rows),
        step=10,
        label_visibility="collapsed"
    )

with st.expander("⚙️ Columnas a mostrar", expanded=False):
    cols_seleccionadas = st.multiselect(
        "Columnas",
        options=cols_disponibles + cols_extra,
        default=cols_disponibles,
        label_visibility="collapsed",
    )

if not cols_seleccionadas:
    cols_seleccionadas = cols_disponibles

df_vista = df_full.copy()

if busqueda.strip():
    termino = busqueda.strip().lower()
    if col_filtro == "Todos los campos":
        mask = df_vista.apply(
            lambda row: row.astype(str).str.lower().str.contains(termino).any(),
            axis=1
        )
    else:
        mask = df_vista[col_filtro].astype(str).str.lower().str.contains(termino)

    df_vista = df_vista[mask]

total_filtrado = len(df_vista)
total_bd = len(df_full)

if busqueda.strip():
    st.markdown(
        f'<div class="result-count">Se encontraron <span>{total_filtrado:,}</span> registros que coinciden con <b>"{busqueda}"</b> de un total de {total_bd:,}</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f'<div class="result-count">Mostrando <span>{min(n_rows, total_filtrado):,}</span> de <span>{total_bd:,}</span> registros totales</div>',
        unsafe_allow_html=True
    )

cols_mostrar = [c for c in cols_seleccionadas if c in df_vista.columns]
df_tabla = df_vista[cols_mostrar].head(n_rows).copy()

if "fecha_nacimiento" in df_tabla.columns:
    df_tabla["fecha_nacimiento"] = pd.to_datetime(df_tabla["fecha_nacimiento"], errors="coerce").dt.strftime("%Y-%m-%d")

altura = min(600, max(200, n_rows * 35 + 40))
st.dataframe(df_tabla, use_container_width=True, height=altura, hide_index=True)

if total_filtrado > n_rows:
    st.caption(f"⚠️ Hay {total_filtrado:,} resultados. Aumenta el slider para ver más.")

st.divider()

# ─── Valores únicos por campo ──────────────────────────────────────────────────

st.markdown("### 🔎 Valores únicos por campo")
st.caption("Distribución de categorías en los campos más relevantes.")

campos_cat = ["estado", "genero", "zona_sede", "nivel", "estrato", "discapacidad", "grado_label"]
cols3 = st.columns(3)

for i, campo in enumerate(campos_cat):
    if campo in df_full.columns:
        with cols3[i % 3]:
            conteo = df_full[campo].value_counts().reset_index()
            conteo.columns = [campo, "cantidad"]
            st.markdown(f"**`{campo}`**")
            st.dataframe(conteo, use_container_width=True, hide_index=True, height=180)

dao.disconnect()

st.markdown("---")
st.caption("Fuente: datos.gov.co · SIMAT · Ministerio de Educación Nacional · Colombia")