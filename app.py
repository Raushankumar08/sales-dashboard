import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Sales Analytics Pro", layout="wide")

# ==============================
# ULTRA CSS
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body {
    font-family: 'Inter', sans-serif;
    background: #0a0e1a;
    color: white;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#111827,#0a0e1a);
}

/* Sidebar styling */
.sidebar-box {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

.profile {
    text-align: center;
    margin-bottom: 20px;
}

.profile img {
    border-radius: 50%;
    width: 80px;
}

.profile-name {
    font-size: 18px;
    font-weight: 600;
}

.profile-role {
    color: #00d4ff;
    font-size: 13px;
}

.sidebar-title {
    font-size: 14px;
    font-weight: 600;
    margin-top: 10px;
}

/* Glass Cards */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}
.glass:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(0,212,255,0.6);
}

.kpi {
    font-size: 26px;
    font-weight: 700;
}

.section {
    margin-top: 30px;
    font-size: 22px;
    font-weight: 600;
}

.footer {
    text-align:center;
    padding:20px;
    border-top:1px solid #00d4ff;
    margin-top:40px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
now = datetime.now().strftime("%d %b %Y | %H:%M")

st.markdown(f"""
<div style="padding:20px;border-bottom:2px solid #00d4ff;">
<div style="display:flex;justify-content:space-between;">
<h1 style="background: linear-gradient(90deg,#00d4ff,#00ff88);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
📊 SALES ANALYTICS PRO
</h1>
<div style="color:#00ff88;">● LIVE | {now}</div>
</div>
<p style="color:#a0a0b0;">Real-time sales intelligence dashboard</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_sales.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# ==============================
# SIDEBAR
# ==============================
st.sidebar.markdown("""
<div class="profile">
<img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png">
<div class="profile-name">Raushan Kumar</div>
<div class="profile-role">Data Analyst</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-box">', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-title">📅 Date Range</div>', unsafe_allow_html=True)
date_range = st.sidebar.date_input("", [])

st.sidebar.markdown('<div class="sidebar-title">🌍 Region</div>', unsafe_allow_html=True)
region = st.sidebar.multiselect("", df["Region"].unique(), default=df["Region"].unique())

st.sidebar.markdown('<div class="sidebar-title">📦 Category</div>', unsafe_allow_html=True)
category = st.sidebar.multiselect("", df["Category"].unique(), default=df["Category"].unique())

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FILTER DATA
# ==============================
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date"] >= str(date_range[0])) &
        (filtered_df["Date"] <= str(date_range[1]))
    ]

filtered_df = filtered_df[
    (filtered_df["Region"].isin(region)) &
    (filtered_df["Category"].isin(category))
]

st.sidebar.markdown(f"""
<div class="sidebar-box">
📊 <b>Total Records:</b> {len(filtered_df)}
</div>
""", unsafe_allow_html=True)

# ==============================
# KPIs
# ==============================
rev = filtered_df["Total Sales"].sum()
orders = filtered_df["Order ID"].nunique()
avg = filtered_df["Total Sales"].mean()
top = filtered_df.groupby("Product")["Total Sales"].sum().idxmax()

c1,c2,c3,c4 = st.columns(4)

c1.markdown(f"<div class='glass'>💰 Revenue<br><div class='kpi'>₹{rev:,.0f}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='glass'>🛒 Orders<br><div class='kpi'>{orders}</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='glass'>📦 Avg Order<br><div class='kpi'>₹{avg:,.0f}</div></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='glass'>🏆 Top Product<br><div class='kpi'>{top}</div></div>", unsafe_allow_html=True)

# ==============================
# TREND
# ==============================
st.markdown("<div class='section'>📈 Monthly Trend</div>", unsafe_allow_html=True)

m = filtered_df.groupby("Month")["Total Sales"].sum().reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=m["Month"],
    y=m["Total Sales"],
    fill='tozeroy',
    line=dict(color='#00d4ff', width=3)
))

fig.update_layout(plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a", font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# ==============================
# CATEGORY + REGION
# ==============================
col1,col2 = st.columns(2)

with col1:
    st.markdown("<div class='section'>📦 Category</div>", unsafe_allow_html=True)
    cat = filtered_df.groupby("Category")["Total Sales"].sum().reset_index()
    fig2 = go.Figure(go.Bar(x=cat["Category"], y=cat["Total Sales"], marker_color="#00ff88"))
    fig2.update_layout(plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a", font=dict(color="white"))
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("<div class='section'>🌍 Region</div>", unsafe_allow_html=True)
    reg = filtered_df.groupby("Region")["Total Sales"].sum().reset_index()
    fig3 = go.Figure(go.Pie(labels=reg["Region"], values=reg["Total Sales"], hole=0.6))
    fig3.update_layout(plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a", font=dict(color="white"))
    st.plotly_chart(fig3, use_container_width=True)

# ==============================
# INSIGHTS
# ==============================
st.markdown("<div class='section'>📊 Smart Insights</div>", unsafe_allow_html=True)

peak = m.loc[m["Total Sales"].idxmax(), "Month"]
top_cat = cat.loc[cat["Total Sales"].idxmax(), "Category"]
low = reg.loc[reg["Total Sales"].idxmin(), "Region"]

i1,i2,i3 = st.columns(3)

i1.markdown(f"<div class='glass'>📈 Peak Month<br><b>{peak}</b></div>", unsafe_allow_html=True)
i2.markdown(f"<div class='glass'>🏆 Top Category<br><b>{top_cat}</b></div>", unsafe_allow_html=True)
i3.markdown(f"<div class='glass'>⚠ Low Region<br><b>{low}</b></div>", unsafe_allow_html=True)

# ==============================
# TABLE
# ==============================
st.markdown("<div class='section'>📋 Data</div>", unsafe_allow_html=True)

st.dataframe(filtered_df)

st.download_button("⬇ Export CSV", filtered_df.to_csv(index=False), "sales.csv")

# ==============================
# FOOTER
# ==============================
st.markdown("""
<div class="footer">
Built with ❤ by Raushan Kumar | 2025<br>
<span style="color:gray;">Python • Streamlit • Plotly</span>
</div>
""", unsafe_allow_html=True)