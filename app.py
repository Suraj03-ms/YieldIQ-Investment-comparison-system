import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import f_oneway, ttest_ind
import numpy as np
from src.predictor import predict_investment

# Page config
st.set_page_config(
    page_title="Investment Analytics Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS Styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e3f 0%, #2d2d5a 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: gradient 3s ease infinite;
        background-size: 200% auto;
    }
    
    @keyframes gradient {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    
    .subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Section Headers */
    .section-header {
        color: #e2e8f0;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Input Styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(30, 30, 63, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(30, 30, 63, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 40px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%);
        border: 1px solid rgba(34, 197, 94, 0.4);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-value {
        font-size: 3rem;
        font-weight: 700;
        color: #22c55e;
        margin: 10px 0;
    }
    
    .result-label {
        color: #86efac;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Stat Card */
    .stat-card {
        background: rgba(30, 30, 63, 0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .stat-title {
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    .stat-value {
        color: #8b5cf6;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .stat-description {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 10px;
    }
    
    /* Success/Warning boxes */
    .success-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        border: 1px solid rgba(34, 197, 94, 0.5);
        border-radius: 12px;
        padding: 15px 20px;
        color: #86efac;
        margin: 10px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.2) 100%);
        border: 1px solid rgba(251, 191, 36, 0.5);
        border-radius: 12px;
        padding: 15px 20px;
        color: #fcd34d;
        margin: 10px 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
        border: 1px solid rgba(59, 130, 246, 0.5);
        border-radius: 12px;
        padding: 15px 20px;
        color: #93c5fd;
        margin: 10px 0;
    }
    
    /* Navigation Pills */
    .nav-pill {
        display: inline-block;
        padding: 10px 20px;
        margin: 5px;
        background: rgba(99, 102, 241, 0.2);
        border-radius: 25px;
        color: #c4b5fd;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .nav-pill.active {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
    }
    
    /* Divider */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #6366f1, #8b5cf6, #6366f1, transparent);
        margin: 30px 0;
        border: none;
    }
    
    /* Labels */
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 30, 63, 0.6) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #8b5cf6; font-size: 1.8rem; margin-bottom: 5px;">📈 InvestPro</h1>
        <p style="color: #94a3b8; font-size: 0.85rem;">Smart Investment Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr style="border-color: rgba(255,255,255,0.1);">', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigate",
        ["🎯 Prediction", "📊 Analytics", "🔬 Statistical Tests"],
        label_visibility="collapsed"
    )
    
    st.markdown('<hr style="border-color: rgba(255,255,255,0.1);">', unsafe_allow_html=True)
    
    # Quick Stats in Sidebar
    st.markdown("""
    <div style="padding: 15px; background: rgba(99, 102, 241, 0.1); border-radius: 12px; margin-top: 20px;">
        <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Market Status</p>
        <p style="color: #22c55e; font-size: 1.2rem; font-weight: 600; margin: 5px 0;">● Live</p>
    </div>
    """, unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Suraj\Desktop\combined_dataset.csv")
    df['Profit'] = df['Final_Value'] - df['Total_Investment']
    df['ROI_%'] = (df['Profit'] / df['Total_Investment']) * 100
    return df

df = load_data()

# Color palette for charts
colors = {
    'LIC': '#6366f1',
    'FD': '#8b5cf6', 
    'Gold': '#f59e0b',
    'Mutual Fund': '#22c55e'
}

# =========================
# 🎯 PAGE 1: PREDICTION
# =========================
if page == "🎯 Prediction":
    st.markdown('<h1 class="main-title">Investment Prediction</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Forecast your investment returns with AI-powered predictions</p>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Input Section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<p class="section-header">Configure Your Investment</p>', unsafe_allow_html=True)
        
        # Investment Type Selection with Icons
        investment_options = {
            "LIC": "🛡️ LIC",
            "FD": "🏦 Fixed Deposit",
            "Gold": "🥇 Gold",
            "Mutual Fund": "📈 Mutual Fund"
        }
        
        investment_display = st.selectbox(
            "Investment Type",
            options=list(investment_options.values()),
            index=0
        )
        investment = [k for k, v in investment_options.items() if v == investment_display][0]
        
        # Year Slider with visual indicator
        year = st.slider(
            "Investment Duration (Years)",
            min_value=1,
            max_value=25,
            value=10,
            help="Select the number of years for your investment"
        )
        
        # Amount Input
        amount = st.number_input(
            "Investment Amount (₹)",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=10000,
            help="Enter your total investment amount"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Predict Button (centered)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            predict_clicked = st.button("🚀 Calculate Returns", use_container_width=True)
    
    # Results Section
    if predict_clicked:
        result = predict_investment(year, amount, investment)
        profit = result - amount
        roi = (profit / amount) * 100
        
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        
        # Result Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">₹{amount:,.0f}</p>
                <p class="metric-label">Investment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">₹{result:,.0f}</p>
                <p class="metric-label">Final Value</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">₹{profit:,.0f}</p>
                <p class="metric-label">Profit</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{roi:.1f}%</p>
                <p class="metric-label">ROI</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Growth Visualization
        st.markdown('<p class="section-header">Projected Growth</p>', unsafe_allow_html=True)
        
        # Create projection data
        years_range = list(range(0, year + 1))
        growth_rate = (result / amount) ** (1 / year) - 1
        projected_values = [amount * ((1 + growth_rate) ** y) for y in years_range]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years_range,
            y=projected_values,
            mode='lines+markers',
            name='Projected Value',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(size=8, color='#8b5cf6'),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.1)'
        ))
        
        fig.add_hline(y=amount, line_dash="dash", line_color="#6366f1", 
                      annotation_text="Initial Investment", annotation_position="right")
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(
                title="Years",
                gridcolor='rgba(255,255,255,0.1)',
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                title="Value (₹)",
                gridcolor='rgba(255,255,255,0.1)',
                showline=True,
                linecolor='rgba(255,255,255,0.2)',
                tickformat=',.0f'
            ),
            hovermode='x unified',
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# =========================
# 📊 PAGE 2: ANALYTICS
# =========================
elif page == "📊 Analytics":
    st.markdown('<h1 class="main-title">Investment Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Comprehensive analysis of investment performance across all asset classes</p>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = df.groupby('Investment_Type').agg({
        'ROI_%': 'mean',
        'Final_Value': 'max',
        'Profit': 'sum'
    }).reset_index()
    
    best_roi = metrics_data.loc[metrics_data['ROI_%'].idxmax()]
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{len(df)}</p>
            <p class="metric-label">Total Records</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{df['Investment_Type'].nunique()}</p>
            <p class="metric-label">Asset Classes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{best_roi['Investment_Type']}</p>
            <p class="metric-label">Best Performer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{df['ROI_%'].mean():.1f}%</p>
            <p class="metric-label">Avg ROI</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-header">Growth Comparison Over Time</p>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        for inv_type in df['Investment_Type'].unique():
            subset = df[df['Investment_Type'] == inv_type].sort_values('Year')
            fig.add_trace(go.Scatter(
                x=subset['Year'],
                y=subset['Final_Value'],
                mode='lines+markers',
                name=inv_type,
                line=dict(color=colors.get(inv_type, '#ffffff'), width=3),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(
                title="Year",
                gridcolor='rgba(255,255,255,0.1)',
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                title="Final Value (₹)",
                gridcolor='rgba(255,255,255,0.1)',
                showline=True,
                linecolor='rgba(255,255,255,0.2)',
                tickformat=',.0f'
            ),
            legend=dict(
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(255,255,255,0.1)',
                font=dict(color='#e2e8f0')
            ),
            hovermode='x unified',
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="section-header">Average ROI by Investment Type</p>', unsafe_allow_html=True)
        
        roi_data = df.groupby('Investment_Type')['ROI_%'].mean().reset_index()
        roi_data = roi_data.sort_values('ROI_%', ascending=True)
        
        fig = go.Figure(go.Bar(
            x=roi_data['ROI_%'],
            y=roi_data['Investment_Type'],
            orientation='h',
            marker=dict(
                color=roi_data['ROI_%'],
                colorscale=[[0, '#6366f1'], [0.5, '#8b5cf6'], [1, '#22c55e']],
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            text=[f'{x:.1f}%' for x in roi_data['ROI_%']],
            textposition='outside',
            textfont=dict(color='#e2e8f0')
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(
                title="ROI (%)",
                gridcolor='rgba(255,255,255,0.1)',
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showline=False
            ),
            margin=dict(l=20, r=80, t=40, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-header">Investment Distribution</p>', unsafe_allow_html=True)
        
        dist_data = df.groupby('Investment_Type')['Total_Investment'].sum().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=dist_data['Investment_Type'],
            values=dist_data['Total_Investment'],
            hole=0.6,
            marker=dict(
                colors=[colors.get(inv, '#ffffff') for inv in dist_data['Investment_Type']],
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            textinfo='percent+label',
            textfont=dict(color='#e2e8f0', size=12),
            hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            height=400,
            annotations=[dict(
                text='Portfolio',
                x=0.5, y=0.5,
                font=dict(size=16, color='#e2e8f0'),
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="section-header">Profit Distribution</p>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        for inv_type in df['Investment_Type'].unique():
            subset = df[df['Investment_Type'] == inv_type]
            fig.add_trace(go.Box(
                y=subset['Profit'],
                name=inv_type,
                marker_color=colors.get(inv_type, '#ffffff'),
                boxpoints='outliers'
            ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                title="Profit (₹)",
                gridcolor='rgba(255,255,255,0.1)',
                showline=True,
                linecolor='rgba(255,255,255,0.2)',
                tickformat=',.0f'
            ),
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap
    st.markdown('<p class="section-header">Year-wise Performance Heatmap</p>', unsafe_allow_html=True)
    
    pivot_data = df.pivot_table(values='ROI_%', index='Investment_Type', columns='Year', aggfunc='mean')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale=[[0, '#1e1e3f'], [0.5, '#6366f1'], [1, '#22c55e']],
        hovertemplate='Investment: %{y}<br>Year: %{x}<br>ROI: %{z:.1f}%<extra></extra>',
        colorbar=dict(
            # ✅ FIX: 'titlefont' is deprecated in Plotly v5+.
            # Title text and font are now nested under the 'title' dict.
            title=dict(
                text='ROI %',
                font=dict(color='#e2e8f0')
            ),
            tickfont=dict(color='#94a3b8')
        )
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(
            title="Year",
            tickmode='linear',
            dtick=5
        ),
        yaxis=dict(title=""),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🔬 PAGE 3: STATISTICAL TESTS
# =========================
elif page == "🔬 Statistical Tests":
    st.markdown('<h1 class="main-title">Statistical Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced statistical tests to validate investment performance differences</p>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Prepare data for tests
    lic = df[df['Investment_Type'] == 'LIC']['Final_Value']
    fd = df[df['Investment_Type'] == 'FD']['Final_Value']
    gold = df[df['Investment_Type'] == 'Gold']['Final_Value']
    mf = df[df['Investment_Type'] == 'Mutual Fund']['Final_Value']
    
    # ANOVA Test
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-header">🔬 ANOVA Test</p>', unsafe_allow_html=True)
        
        f_stat, p_val = f_oneway(lic, fd, gold, mf)
        
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-title">Analysis of Variance (ANOVA)</p>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">
                Tests if there's a significant difference between all investment types
            </p>
            <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                <div style="text-align: center;">
                    <p class="stat-value">{f_stat:.2f}</p>
                    <p style="color: #94a3b8; font-size: 0.8rem;">F-Statistic</p>
                </div>
                <div style="text-align: center;">
                    <p class="stat-value">{p_val:.4f}</p>
                    <p style="color: #94a3b8; font-size: 0.8rem;">P-Value</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if p_val < 0.05:
            st.markdown("""
            <div class="success-box">
                <strong>✅ Significant Difference Found</strong><br>
                <span style="font-size: 0.9rem;">The p-value is less than 0.05, indicating statistically significant differences between investment types.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-box">
                <strong>⚠️ No Significant Difference</strong><br>
                <span style="font-size: 0.9rem;">The p-value is greater than 0.05, suggesting no statistically significant difference.</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="section-header">📊 T-Test Analysis</p>', unsafe_allow_html=True)
        
        t_stat, t_p = ttest_ind(mf, fd)
        
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-title">Independent T-Test (Mutual Fund vs FD)</p>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">
                Compares the means of two specific investment types
            </p>
            <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                <div style="text-align: center;">
                    <p class="stat-value">{t_stat:.2f}</p>
                    <p style="color: #94a3b8; font-size: 0.8rem;">T-Statistic</p>
                </div>
                <div style="text-align: center;">
                    <p class="stat-value">{t_p:.4f}</p>
                    <p style="color: #94a3b8; font-size: 0.8rem;">P-Value</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if t_p < 0.05:
            st.markdown("""
            <div class="success-box">
                <strong>✅ Significant Difference</strong><br>
                <span style="font-size: 0.9rem;">Mutual Funds and FD have significantly different returns.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-box">
                <strong>⚠️ No Significant Difference</strong><br>
                <span style="font-size: 0.9rem;">No significant difference found between Mutual Funds and FD.</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Distribution Comparison
    st.markdown('<p class="section-header">Distribution Comparison</p>', unsafe_allow_html=True)
    
    fig = go.Figure()
    
    for inv_type in df['Investment_Type'].unique():
        subset = df[df['Investment_Type'] == inv_type]['Final_Value']
        fig.add_trace(go.Violin(
            y=subset,
            name=inv_type,
            box_visible=True,
            meanline_visible=True,
            fillcolor=colors.get(inv_type, '#ffffff'),
            line_color='white',
            opacity=0.7
        ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title="Final Value (₹)",
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            tickformat=',.0f'
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown('<p class="section-header">Key Insights</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <strong>📈 Mutual Funds</strong><br>
            <span style="font-size: 0.9rem;">Higher potential returns but with increased volatility. Best for long-term growth-focused investors.</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <strong>🏦 Fixed Deposits</strong><br>
            <span style="font-size: 0.9rem;">Stable and predictable returns. Ideal for risk-averse investors seeking capital preservation.</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
            <strong>🥇 Gold & LIC</strong><br>
            <span style="font-size: 0.9rem;">Traditional safe havens with moderate returns. Good for portfolio diversification.</span>
        </div>
        """, unsafe_allow_html=True)