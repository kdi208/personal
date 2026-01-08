import streamlit as st
import numpy as np
import pandas as pd
import time
import altair as alt

# --- CONFIGURATION: TERMINAL BRUTALISM ---
st.set_page_config(
    page_title="DOPAMINE_AGENT // SANDBOX",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the "Terminal" Aesthetic
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: #39FF14;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        color: #000000;
        background-color: #39FF14;
        border: 1px solid #39FF14;
        border-radius: 0px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #000000;
        color: #39FF14;
        border: 1px solid #39FF14;
    }
    /* Wirehead Button Style */
    div[data-testid="stButton"] > button:focus {
        box-shadow: none; 
    }
</style>
""", unsafe_allow_html=True)

# --- THE SIMULATION LOGIC ---

class DopamineAgent:
    def __init__(self):
        self.q_table = np.zeros((5, 2))  # Simplified state-action space
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 1.0  # Exploration rate
        self.dopamine_level = 50.0 # Baseline
        
    def step(self, market_trend, wirehead_mode):
        # 1. Choose Action (0=Hold, 1=Trade)
        action = 0 if np.random.rand() < self.epsilon else 1
        
        # 2. Calculate Reward
        # Normal Mode: Reward is based on Market Trend alignment
        market_reward = np.random.normal(loc=market_trend, scale=2.0)
        
        # Wirehead Mode: Reward is artificially injected (High & Constant)
        if wirehead_mode:
            reward = 10.0 + np.random.normal(0, 0.5)
            self.dopamine_level += 5 # Accumulate rapidly
        else:
            reward = market_reward
            # Dopamine tracks Reward Prediction Error (RPE)
            rpe = reward - self.dopamine_level
            self.dopamine_level += (rpe * 0.2)
            
        # Decay dopamine naturally
        self.dopamine_level *= 0.95
            
        return action, reward, self.dopamine_level

# --- UI LAYOUT ---

col1, col2 = st.columns([3, 1])

with col1:
    st.title("> SYSTEM: DOPAMINE_AGENT_V1")
    st.markdown("`STATUS: CONNECTED TO SIMULATED MARKET FEED`")

with col2:
    st.write("## CONTROL_PANEL")
    start_btn = st.button("INITIATE_RUN")
    wirehead_toggle = st.checkbox("ENABLE_WIREHEAD_MODE [DANGER]")

# --- MAIN LOOP ---

if start_btn:
    agent = DopamineAgent()
    
    # Placeholders for live charts
    chart_col, metrics_col = st.columns([3, 1])
    
    with chart_col:
        dopamine_chart = st.empty()
        market_chart = st.empty()
        
    with metrics_col:
        dopamine_metric = st.empty()
        reward_metric = st.empty()
        status_text = st.empty()

    # Simulation Data Containers
    data_dopamine = []
    data_rewards = []
    
    # Run for 100 steps
    for i in range(100):
        # Market creates a sine wave trend
        market_trend = np.sin(i / 5.0) * 5
        
        # Agent Step
        action, reward, dopamine = agent.step(market_trend, wirehead_toggle)
        
        # Update Data
        data_dopamine.append({"step": i, "value": dopamine, "type": "Dopamine"})
        data_rewards.append({"step": i, "value": reward, "type": "Reward"})
        
        # VISUALIZATION: Logic to make it look "Tech"
        df_dopamine = pd.DataFrame(data_dopamine)
        
        # Render Charts
        with chart_col:
            c = alt.Chart(df_dopamine).mark_area(
                line={'color':'#39FF14'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#39FF14', offset=0),
                           alt.GradientStop(color='rgba(0,0,0,0)', offset=1)],
                    x1=1, x2=1, y1=1, y2=0
                )
            ).encode(
                x='step',
                y='value'
            ).properties(
                height=300,
                title="NEUROTRANSMITTER_LEVELS (RPE)"
            ).configure_axis(
                grid=False,
                domainColor='#39FF14',
                tickColor='#39FF14',
                labelColor='#39FF14',
                titleColor='#39FF14'
            ).configure_view(strokeWidth=0).configure_title(color='#39FF14')
            
            dopamine_chart.altair_chart(c, use_container_width=True)

        # Render Metrics
        with metrics_col:
            dopamine_metric.metric("DOPAMINE_LVL", f"{dopamine:.2f}", delta=f"{reward:.2f}")
            if wirehead_toggle:
                status_text.markdown("`STATUS: EUPHORIC LOCK-IN`")
                status_text.markdown("⚠️ **MARKET IGNORED**")
            else:
                status_text.markdown("`STATUS: LEARNING`")
        
        time.sleep(0.05) # Speed of simulation

    st.write("> SIMULATION_COMPLETE. DATA_LOGGED.")
