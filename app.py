import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Volleyball Tier Maker", layout="wide")
st.title("🏐 Volleyball Team Balancer")

# --- 1. NAME ENTRY ---
# (Keeping it simple for the demo: Paste names or use OCR)
names_input = st.sidebar.text_area("Paste names (comma separated):", "Alex, Sam, Jordan, Taylor, Casey, Jamie, Morgan, Riley, Quinn, Skyler, Charlie, Parker")

if names_input:
    player_list = [n.strip() for n in names_input.split(",") if n.strip()]
    
    # --- 2. TIER ASSIGNMENT ---
    st.header("1. Assign Tiers (1=High, 7=Low)")
    player_tier_map = {}
    cols = st.columns(4) # Spread out the names so it's not a mile long
    for i, name in enumerate(player_list):
        with cols[i % 4]:
            tier = st.selectbox(f"{name}", options=range(1, 8), key=f"t_{name}")
            player_tier_map[name] = tier

    # --- 3. INITIAL GENERATION ---
    if st.button("Generate Balanced Teams"):
        # Sort players into teams using Snake Draft
        buckets = {i: [] for i in range(1, 8)}
        for name, tier in player_tier_map.items():
            buckets[tier].append(name)
        
        teams = {1: [], 2: [], 3: [], 4: []}
        curr = 1
        direction = 1
        
        for t in range(1, 8):
            players = buckets[t]
            random.shuffle(players)
            for p in players:
                teams[curr].append(p)
                curr += direction
                if curr > 4: curr = 4; direction = -1
                if curr < 1: curr = 1; direction = 1
        
        st.session_state.final_teams = teams

    # --- 4. THE "SWAP" TOOL (Manual Override) ---
    if 'final_teams' in st.session_state:
        st.divider()
        st.header("2. Review & Manual Swap")
        st.info("Don't like a matchup? Swap two players below.")

        col_s1, col_s2, col_btn = st.columns([3, 3, 2])
        
        all_players = [p for t in st.session_state.final_teams.values() for p in t]
        
        with col_s1:
            p1 = st.selectbox("Swap player:", all_players, key="swap1")
        with col_s2:
            p2 = st.selectbox("With player:", all_players, key="swap2")
        
        if col_btn.button("🔄 Execute Swap"):
            # Logic to find and swap players across teams
            t1_key = next(k for k, v in st.session_state.final_teams.items() if p1 in v)
            t2_key = next(k for k, v in st.session_state.final_teams.items() if p2 in v)
            
            idx1 = st.session_state.final_teams[t1_key].index(p1)
            idx2 = st.session_state.final_teams[t2_key].index(p2)
            
            st.session_state.final_teams[t1_key][idx1] = p2
            st.session_state.final_teams[t2_key][idx2] = p1
            st.rerun()

        # --- 5. FINAL DISPLAY ---
        t_display = st.columns(4)
        for i in range(1, 5):
            with t_display[i-1]:
                st.success(f"**Team {i}**")
                for member in st.session_state.final_teams[i]:
                    st.write(f"• {member}")
