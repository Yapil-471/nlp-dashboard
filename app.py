import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NLP Agriculture News Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: #0d1117;
        color: #e6edf3;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #58a6ff;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px;
        transition: border-color 0.2s;
    }
    [data-testid="metric-container"]:hover {
        border-color: #58a6ff;
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #e6edf3 !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricDelta"] svg {
        color: #3fb950 !important;
    }

    /* Header */
    .hero-header {
        background: linear-gradient(135deg, #0d2137 0%, #1a2d4a 50%, #0d2137 100%);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 32px 40px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(88,166,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #e6edf3;
        margin: 0 0 6px 0;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        color: #8b949e;
        font-size: 0.95rem;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(88,166,255,0.15);
        border: 1px solid rgba(88,166,255,0.3);
        color: #58a6ff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 12px;
        font-family: 'Space Mono', monospace;
    }

    /* Section titles */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e6edf3;
        margin: 0 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #21262d;
        letter-spacing: -0.01em;
    }

    /* Card wrapper */
    .card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* Tag labels */
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-right: 4px;
        font-family: 'Space Mono', monospace;
        letter-spacing: 0.03em;
    }
    .tag-climate  { background: rgba(63,185,80,.15);  color: #3fb950; border: 1px solid rgba(63,185,80,.3); }
    .tag-policy   { background: rgba(255,166,0,.15);  color: #ffa600; border: 1px solid rgba(255,166,0,.3); }
    .tag-price    { background: rgba(248,81,73,.15);  color: #f85149; border: 1px solid rgba(248,81,73,.3); }
    .tag-production{ background: rgba(88,166,255,.15); color: #58a6ff; border: 1px solid rgba(88,166,255,.3);}

    /* Best result badge */
    .best-badge {
        background: linear-gradient(90deg, #f78166, #ff6e40);
        color: white;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        font-family: 'Space Mono', monospace;
    }

    /* Table override */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Divider */
    hr { border-color: #21262d; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #161b22;
        border-radius: 10px;
        border: 1px solid #30363d;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background: #21262d !important;
        color: #e6edf3 !important;
        border-radius: 8px;
    }

    /* Selectbox */
    .stSelectbox label { color: #8b949e; font-size: 0.8rem; }

    /* Info boxes */
    .info-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 12px;
    }
    .info-chip {
        background: #21262d;
        border: 1px solid #30363d;
        color: #c9d1d9;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.82rem;
    }
    .info-chip span {
        color: #58a6ff;
        font-weight: 700;
        font-family: 'Space Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ─── Data ──────────────────────────────────────────────────────────────────────

EXPERIMENTS = pd.DataFrame({
    "Representasi":  ["BoW",        "BoW",        "N-Gram",     "N-Gram",     "TF-IDF",     "TF-IDF"],
    "Model":         ["Decision Tree","Naive Bayes","Decision Tree","Naive Bayes","Decision Tree","Naive Bayes"],
    "Accuracy":      [0.8201,       0.8302,       0.8232,       0.8341,       0.8185,       0.8590],
    "Precision":     [0.8205,       0.8410,       0.8244,       0.8474,       0.8183,       0.8593],
    "Recall":        [0.8201,       0.8302,       0.8232,       0.8341,       0.8185,       0.8590],
    "F1_Score":      [0.8113,       0.8337,       0.8146,       0.8382,       0.8080,       0.8587],
})
EXPERIMENTS["Kombinasi"] = EXPERIMENTS["Representasi"] + " + " + EXPERIMENTS["Model"]
EXPERIMENTS["Is_Best"] = EXPERIMENTS["F1_Score"] == EXPERIMENTS["F1_Score"].max()

CATEGORY_MAP = {
    "Business":  "Price",
    "Sci/Tech":  "Production",
    "World":     "Policy",
    "Sports":    "Tidak Digunakan",
}

CATEGORY_DIST = pd.DataFrame({
    "Kategori":    ["Climate", "Policy", "Price", "Production"],
    "Jumlah":      [25, 25, 25, 25],
    "Warna":       ["#3fb950", "#ffa600", "#f85149", "#58a6ff"],
})

SAMPLE_DATASET = pd.DataFrame({
    "No": list(range(1, 26)),
    "Title": [
        "2nd Hurricane Deepens Wounds in Stricken Florida",
        "Researchers Work on Method to Predict Rainfall",
        "Report: Global warming now inevitable",
        "Putin clears way for Kyoto treaty",
        "Typhoon hits Japanese coast",
        "U.S. Raises Alert in Baghdad's Green Zone",
        "US maize 'threat' to Mexico farms",
        "Kerry Takes Job Creation Message to N.C.",
        "Maoist Rebel Blockade Begins to Pinch Nepal Capital",
        "Iraqi oil exports slump: report",
        "Oil Hits $53 High on Supply Worries",
        "Retail Sales Down; Trade Gap Larger",
        "OPEC Warns Oil Supply Cuts Needed for '05",
        "Shares of PC maker Lenovo slump after IBM deal",
        "U.S. Treasuries Drift Lower",
        "Organic Farming Studied As Demand Rises",
        "Tuna Fish Stocks in Mediterranean in Danger",
        "U.S. Accuses U.N. of Dragging Feet Over Locusts",
        "Hurricanes Blamed for Fruit Infection",
        "Scientists Say Sunoil Could Power Cars, Homes",
        "India's Kashmir Govt to Fight Ban on Shahtoosh Wool",
        "Study: Dead Cicadas Boost Soil Nutrients",
        "Ten Percent of Bird Species to Disappear",
        "Fish agency lets dams off hook",
        "DNA Testing May Curb Illegal Ivory Trade",
    ],
    "Kategori": [
        "Climate","Climate","Climate","Climate","Climate",
        "Policy","Policy","Policy","Policy","Policy",
        "Price","Price","Price","Price","Price",
        "Production","Production","Production","Production","Production",
        "Production","Production","Production","Production","Production",
    ],
})

PREPROCESSING_STEPS = [
    ("Data Cleaning",     "Hapus tanda baca, angka, karakter khusus, dan spasi berlebih"),
    ("Case Folding",      "Ubah seluruh teks ke huruf kecil (lowercase)"),
    ("Tokenization",      "Pecah teks menjadi unit kata (token)"),
    ("Stopword Removal",  "Hapus kata umum (the, is, and, dll.) — sekaligus Data Reduction"),
    ("Stemming",          "Ubah kata ke bentuk dasar (root word)"),
    ("Transformasi Teks", "Representasi numerik: BoW, N-Gram, TF-IDF"),
]

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 NLP Dashboard")
    st.markdown("---")
    st.markdown("**Kelompok:**")
    st.markdown("""
- 202310370311489 · Rifky Rofiq  
- 202310370311326 · M. Senopati P.  
- 202310370311471 · M. Yapil Islami  
    """)
    st.markdown("---")
    st.markdown("**Dataset:** AG News Classification  \n**Sumber:** Kaggle")
    st.markdown("**Total Data:** 7,600 baris  \n**Kategori:** 4 (setelah filtering)")
    st.markdown("---")
    selected_metric = st.selectbox(
        "Tampilkan Metrik Utama",
        ["F1_Score", "Accuracy", "Precision", "Recall"],
        index=0,
    )
    st.markdown("---")
    st.caption("Mini Project · Pemrosesan Bahasa Alami")

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">MINI PROJECT · NLP · 2024</div>
    <p class="hero-title">🌾 Klasifikasi Berita Pertanian</p>
    <p class="hero-subtitle">
        Sistem klasifikasi teks berbasis NLP untuk mengelompokkan berita pertanian
        menggunakan algoritma Decision Tree &amp; Naive Bayes dengan representasi BoW, N-Gram, dan TF-IDF.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── KPI Row ───────────────────────────────────────────────────────────────────
best = EXPERIMENTS.loc[EXPERIMENTS["Is_Best"].idxmax()]
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Best Accuracy",  f"{best['Accuracy']:.4f}",  "TF-IDF + Naive Bayes")
kpi2.metric("Best Precision", f"{best['Precision']:.4f}", "TF-IDF + Naive Bayes")
kpi3.metric("Best Recall",    f"{best['Recall']:.4f}",    "TF-IDF + Naive Bayes")
kpi4.metric("Best F1-Score",  f"{best['F1_Score']:.4f}",  "TF-IDF + Naive Bayes")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Hasil Eksperimen", "📂 Dataset & EDA", "⚙️ Preprocessing", "🏆 Perbandingan"])

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#c9d1d9",
    font_family="Plus Jakarta Sans",
    title_font_color="#e6edf3",
    legend_bgcolor="rgba(22,27,34,0.8)",
    legend_bordercolor="#30363d",
    legend_borderwidth=1,
)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 · Hasil Eksperimen
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<p class="section-title">Perbandingan Semua Eksperimen</p>', unsafe_allow_html=True)

        colors = ["#f85149" if r else "#58a6ff" for r in EXPERIMENTS["Is_Best"]]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=EXPERIMENTS["Kombinasi"],
            y=EXPERIMENTS[selected_metric],
            marker_color=colors,
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>" + selected_metric + ": %{y:.4f}<extra></extra>",
            text=[f"{v:.4f}" for v in EXPERIMENTS[selected_metric]],
            textposition="outside",
            textfont=dict(size=11, family="Space Mono"),
        ))
        fig_bar.update_layout(
            **PLOTLY_THEME,
            height=320,
            margin=dict(t=20, b=80, l=10, r=10),
            xaxis=dict(tickangle=-30, gridcolor="#21262d", tickfont=dict(size=10)),
            yaxis=dict(
                range=[0.78, 0.88],
                gridcolor="#21262d",
                tickformat=".3f",
                tickfont=dict(family="Space Mono", size=10),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.markdown('<p class="section-title">Radar Chart — Metrik Terbaik</p>', unsafe_allow_html=True)

        categories = ["Accuracy", "Precision", "Recall", "F1-Score"]
        values_best = [best["Accuracy"], best["Precision"], best["Recall"], best["F1_Score"]]
        worst = EXPERIMENTS.loc[EXPERIMENTS["F1_Score"].idxmin()]
        values_worst = [worst["Accuracy"], worst["Precision"], worst["Recall"], worst["F1_Score"]]

        fig_radar = go.Figure()
        for vals, name, color, fillcolor in [
            (values_best,  "TF-IDF + Naive Bayes",   "#f85149", "rgba(248,81,73,0.15)"),
            (values_worst, "TF-IDF + Decision Tree", "#58a6ff", "rgba(88,166,255,0.15)"),
        ]:
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                name=name,
                fill="toself",
                fillcolor=fillcolor,
                line=dict(color=color, width=2),
                hovertemplate="%{theta}: %{r:.4f}<extra></extra>",
            ))
        fig_radar.update_layout(
            **PLOTLY_THEME,
            height=320,
            margin=dict(t=20, b=20, l=20, r=20),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0.79, 0.87],
                    tickformat=".2f", tickfont=dict(size=9, family="Space Mono"),
                    gridcolor="#30363d", linecolor="#30363d",
                ),
                angularaxis=dict(gridcolor="#30363d", linecolor="#30363d"),
            ),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Detail table
    st.markdown('<p class="section-title">Tabel Detail Hasil</p>', unsafe_allow_html=True)
    df_display = EXPERIMENTS[["Kombinasi", "Accuracy", "Precision", "Recall", "F1_Score", "Is_Best"]].copy()
    df_display.columns = ["Kombinasi", "Accuracy", "Precision", "Recall", "F1-Score", "Best"]
    for col in ["Accuracy", "Precision", "Recall", "F1-Score"]:
        df_display[col] = df_display[col].apply(lambda x: f"{x:.4f}")
    df_display["Best"] = df_display["Best"].apply(lambda x: "★ TERBAIK" if x else "")
    st.dataframe(
        df_display.style.apply(
            lambda row: ["background: rgba(248,81,73,0.1); color: #f85149" if row["Best"] == "★ TERBAIK" else "" for _ in row],
            axis=1,
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("""
    <div class="card" style="margin-top:16px;">
        <p style="margin:0 0 8px 0; font-weight:700; color:#e6edf3;">💡 Kesimpulan Eksperimen</p>
        <p style="margin:0; color:#8b949e; font-size:0.88rem; line-height:1.7;">
            Kombinasi <strong style="color:#f85149">TF-IDF + Naive Bayes</strong> menghasilkan performa terbaik
            dengan F1-Score <strong style="color:#f85149; font-family:'Space Mono',monospace;">0.8587</strong> dan
            Accuracy <strong style="color:#f85149; font-family:'Space Mono',monospace;">0.8590</strong>.
            TF-IDF mampu menyoroti kata-kata penting, sementara Naive Bayes efektif dalam memodelkan
            distribusi probabilitas kata per kategori. Sebaliknya, TF-IDF + Decision Tree menghasilkan
            performa terendah karena kompleksitas fitur yang tinggi tidak sesuai dengan mekanisme pemisahan
            Decision Tree.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 · Dataset & EDA
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col_a, col_b = st.columns([1, 1], gap="large")

    with col_a:
        st.markdown('<p class="section-title">Distribusi Kategori (100 Sample)</p>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=CATEGORY_DIST["Kategori"],
            values=CATEGORY_DIST["Jumlah"],
            marker_colors=CATEGORY_DIST["Warna"].tolist(),
            hole=0.55,
            hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Porsi: %{percent}<extra></extra>",
            textinfo="label+percent",
            textfont=dict(size=12, family="Plus Jakarta Sans"),
        ))
        fig_pie.update_layout(
            **PLOTLY_THEME,
            height=300,
            margin=dict(t=10, b=10, l=10, r=10),
            annotations=[dict(text="Balanced", x=0.5, y=0.5, font_size=13,
                              font_color="#8b949e", showarrow=False)],
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('<p class="section-title">Pemetaan Kategori</p>', unsafe_allow_html=True)
        map_df = pd.DataFrame(CATEGORY_MAP.items(), columns=["Kategori Asli (AG News)", "Kategori Baru (Pertanian)"])
        st.dataframe(map_df, use_container_width=True, hide_index=True)

    with col_b:
        st.markdown('<p class="section-title">Informasi Dataset</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-row">
            <div class="info-chip">Total data: <span>7,600</span></div>
            <div class="info-chip">Sample berita: <span>100</span></div>
            <div class="info-chip">Sumber: <span>Kaggle</span></div>
        </div>
        <div class="info-row">
            <div class="info-chip">Task: <span>Classification</span></div>
            <div class="info-chip">Distribusi: <span>Seimbang</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-title" style="margin-top:12px;">Atribut Dataset</p>', unsafe_allow_html=True)
        attrs = pd.DataFrame({
            "Atribut":   ["Title", "Description", "Class Index"],
            "Tipe":      ["Text", "Text", "Integer"],
            "Keterangan": [
                "Judul berita (fitur input)",
                "Ringkasan isi berita (fitur input)",
                "Label kategori (target klasifikasi)",
            ],
        })
        st.dataframe(attrs, use_container_width=True, hide_index=True)

        st.markdown('<p class="section-title" style="margin-top:12px;">Masalah yang Teridentifikasi</p>', unsafe_allow_html=True)
        issues = [
            "Dataset tidak spesifik berita pertanian → remapping kategori",
            "Label perlu dipetakan ke domain pertanian",
            "Teks mengandung noise (tanda baca, angka, simbol)",
            "Perlu preprocessing untuk meningkatkan kualitas",
        ]
        for issue in issues:
            st.markdown(f"- {issue}")

    st.markdown("---")
    st.markdown('<p class="section-title">Sample Dataset (25 Data)</p>', unsafe_allow_html=True)

    tag_html = {
        "Climate":    '<span class="tag tag-climate">Climate</span>',
        "Policy":     '<span class="tag tag-policy">Policy</span>',
        "Price":      '<span class="tag tag-price">Price</span>',
        "Production": '<span class="tag tag-production">Production</span>',
    }

    display_df = SAMPLE_DATASET.copy()
    display_df["Kategori_Display"] = display_df["Kategori"].map(tag_html)

    st.dataframe(
        display_df[["No", "Title", "Kategori"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "No": st.column_config.NumberColumn("No", width="small"),
            "Title": st.column_config.TextColumn("Judul Berita", width="large"),
            "Kategori": st.column_config.TextColumn("Kategori"),
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 · Preprocessing
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">Pipeline Preprocessing</p>', unsafe_allow_html=True)

    step_colors = ["#58a6ff", "#3fb950", "#ffa600", "#f85149", "#a371f7", "#ff6e40"]
    cols_steps = st.columns(3)
    for i, (step, desc) in enumerate(PREPROCESSING_STEPS):
        with cols_steps[i % 3]:
            st.markdown(f"""
            <div class="card" style="border-left: 3px solid {step_colors[i]}; min-height:100px;">
                <p style="margin:0 0 6px 0; font-weight:700; color:{step_colors[i]}; font-size:0.82rem;
                   font-family:'Space Mono',monospace; letter-spacing:0.04em;">STEP {i+1}</p>
                <p style="margin:0 0 6px 0; font-weight:700; color:#e6edf3;">{step}</p>
                <p style="margin:0; color:#8b949e; font-size:0.83rem; line-height:1.6;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-title">Contoh Transformasi Data</p>', unsafe_allow_html=True)

    BEFORE_AFTER = [
        ("Data Cleaning",
         "Wall St. Bears Claw Back Into the Black (Reuters) Reuters - Short-sellers, Wall Street's dwindling\\band of ultra-cynics...",
         "Wall St Bears Claw Back Into the Black Reuters Reuters Short sellers Wall Street s dwindling band of ultra cynics seeing green again"),
        ("Case Folding",
         "Wall St Bears Claw Back Into the Black Reuters Reuters Short sellers Wall Street s dwindling band of ultra cynics",
         "wall st bears claw back into the black reuters reuters short sellers wall street s dwindling band of ultra cynics"),
        ("Stemming",
         "Chad seeks refugee aid IMF Chad asks IMF loan pay looking refugees conflict torn Darfur western Sudan",
         "chad seek refuge aid imf chad ask imf loan pay look refuge conflict torn darfur western sudan"),
    ]
    for step, before, after in BEFORE_AFTER:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:#1c2128;border:1px solid #f85149;border-radius:10px;padding:14px;margin-bottom:10px;">
                <p style="margin:0 0 6px 0;color:#f85149;font-size:0.75rem;font-weight:700;
                   font-family:'Space Mono',monospace;">SEBELUM · {step}</p>
                <p style="margin:0;color:#c9d1d9;font-size:0.82rem;line-height:1.6;word-break:break-word;">{before}</p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#1c2128;border:1px solid #3fb950;border-radius:10px;padding:14px;margin-bottom:10px;">
                <p style="margin:0 0 6px 0;color:#3fb950;font-size:0.75rem;font-weight:700;
                   font-family:'Space Mono',monospace;">SESUDAH · {step}</p>
                <p style="margin:0;color:#c9d1d9;font-size:0.82rem;line-height:1.6;word-break:break-word;">{after}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="section-title">Metode Representasi Teks</p>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    for col, name, desc, color in [
        (r1, "Bag of Words (BoW)", "Menghitung frekuensi kemunculan setiap kata. Sederhana dan efektif, namun tidak mempertimbangkan konteks atau urutan kata.", "#58a6ff"),
        (r2, "N-Gram (Bigram)", "Membentuk kombinasi n kata berurutan sebagai satu fitur. Mampu menangkap konteks dan hubungan antar kata.", "#3fb950"),
        (r3, "TF-IDF", "Memberikan bobot pada kata berdasarkan frekuensi dalam dokumen (TF) dan kelangkaan di seluruh corpus (IDF). Paling optimal untuk klasifikasi teks.", "#ffa600"),
    ]:
        col.markdown(f"""
        <div class="card" style="border-top: 3px solid {color}; text-align:center;">
            <p style="font-weight:800; color:{color}; margin:0 0 8px 0;">{name}</p>
            <p style="color:#8b949e; font-size:0.83rem; margin:0; line-height:1.6;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 · Perbandingan
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">Perbandingan Antar Metode Representasi</p>', unsafe_allow_html=True)

    # Group by representasi
    grouped = EXPERIMENTS.groupby("Representasi")[["Accuracy", "Precision", "Recall", "F1_Score"]].mean().reset_index()

    fig_group = go.Figure()
    colors_repr = {"BoW": "#58a6ff", "N-Gram": "#3fb950", "TF-IDF": "#ffa600"}
    for metric in ["Accuracy", "Precision", "Recall", "F1_Score"]:
        for _, row in grouped.iterrows():
            fig_group.add_trace(go.Bar(
                name=row["Representasi"],
                x=[metric],
                y=[row[metric]],
                marker_color=colors_repr[row["Representasi"]],
                legendgroup=row["Representasi"],
                showlegend=(metric == "Accuracy"),
                hovertemplate=f"<b>{row['Representasi']}</b><br>{metric}: {row[metric]:.4f}<extra></extra>",
            ))
    fig_group.update_layout(
        **PLOTLY_THEME,
        height=340,
        barmode="group",
        margin=dict(t=20, b=20, l=10, r=10),
        xaxis=dict(gridcolor="#21262d"),
        yaxis=dict(range=[0.81, 0.86], gridcolor="#21262d", tickformat=".3f",
                   tickfont=dict(family="Space Mono", size=10)),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
    )
    st.plotly_chart(fig_group, use_container_width=True)

    # Per-algorithm comparison
    st.markdown('<p class="section-title">Decision Tree vs Naive Bayes</p>', unsafe_allow_html=True)

    algo_groups = EXPERIMENTS.groupby("Model")[["Accuracy", "Precision", "Recall", "F1_Score"]].mean().reset_index()

    c1, c2 = st.columns(2)
    for col, metric in [(c1, "Accuracy"), (c2, "F1_Score")]:
        dt_val = algo_groups.loc[algo_groups["Model"] == "Decision Tree", metric].values[0]
        nb_val = algo_groups.loc[algo_groups["Model"] == "Naive Bayes",   metric].values[0]
        fig_h = go.Figure()
        fig_h.add_trace(go.Bar(
            y=["Decision Tree", "Naive Bayes"],
            x=[dt_val, nb_val],
            orientation="h",
            marker_color=["#58a6ff", "#f85149"],
            text=[f"{dt_val:.4f}", f"{nb_val:.4f}"],
            textposition="inside",
            textfont=dict(family="Space Mono", size=12, color="white"),
            hovertemplate="<b>%{y}</b><br>" + metric + ": %{x:.4f}<extra></extra>",
        ))
        fig_h.update_layout(
            **PLOTLY_THEME,
            title=dict(text=f"Rata-rata {metric}", font_size=13),
            height=180,
            margin=dict(t=40, b=10, l=10, r=10),
            xaxis=dict(range=[0.80, 0.87], gridcolor="#21262d",
                       tickformat=".3f", tickfont=dict(family="Space Mono", size=9)),
            yaxis=dict(gridcolor="#21262d"),
            showlegend=False,
        )
        col.plotly_chart(fig_h, use_container_width=True)

    st.markdown("---")
    st.markdown('<p class="section-title">📋 Rangkuman Akhir</p>', unsafe_allow_html=True)

    summary_data = {
        "Kombinasi":  ["BoW + DT", "BoW + NB", "N-Gram + DT", "N-Gram + NB", "TF-IDF + DT", "TF-IDF + NB ★"],
        "Accuracy":   ["0.8201", "0.8302", "0.8232", "0.8341", "0.8185", "0.8590"],
        "F1-Score":   ["0.8113", "0.8337", "0.8146", "0.8382", "0.8080", "0.8587"],
        "Ranking":    ["#5", "#3", "#4", "#2", "#6", "#1"],
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(
        summary_df.style.apply(
            lambda row: ["background:rgba(248,81,73,0.12); color:#f85149" if "★" in row["Kombinasi"] else "" for _ in row],
            axis=1,
        ),
        use_container_width=True,
        hide_index=True,
    )