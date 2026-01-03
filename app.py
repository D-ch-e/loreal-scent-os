import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. 頁面與狀態設定 (Config & State) ---
st.set_page_config(
    page_title="L'ORÉAL SCENT OS",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'recipe' not in st.session_state:
    st.session_state.recipe = {}
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'saved_presets' not in st.session_state:
    st.session_state.saved_presets = []

# CSS (Enhanced with animations)
st.markdown("""
<style>
:root {
     --bg-main: #FFFFFF;
     --bg-soft: #FAFAFA;
     --bg-card: #F5F5F5;
     --border-light: #D8D8D8;
     --text-main: #111111;
     --text-muted: #555555;
     --accent: #8C6D1F;
     --accent-gold: #BE9C5C;
}

* {
     font-family: "Nicolas Cochin", "Nicolas Cochin Regular", "Cochin", serif !important;
}

html, body, [class*="css"], [class*="st"] {
     font-family: "Nicolas Cochin", "Nicolas Cochin Regular", "Cochin", serif !important;
     color: var(--text-main) !important;
}

/* Force Nicolas Cochin on all text elements */
h1, h2, h3, h4, h5, h6, p, span, div, label, button, input, textarea, select, option, li, a {
     font-family: "Nicolas Cochin", "Nicolas Cochin Regular", "Cochin", serif !important;
}

.stApp {
     background-color: var(--bg-main);
     color: var(--text-main);
}

p, div, span, label, li, small {
     color: var(--text-main) !important;
}

h1, h2, h3, h4, h5, h6 {
     color: #000000 !important;
     font-weight: 600;
}

.centered-title {
     text-align: center;
     font-size: 3rem;
     letter-spacing: 4px;
     font-weight: 600;
     margin-bottom: 0.5rem;
     animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
     from { opacity: 0; transform: translateY(-20px); }
     to { opacity: 1; transform: translateY(0); }
}

.centered-text {
     text-align: center;
     color: var(--text-muted) !important;
     font-size: 1.05rem;
}

textarea, input {
     background-color: #FFFFFF !important;
     color: var(--text-main) !important;
     border: 1px solid var(--border-light) !important;
     border-radius: 4px !important;
     transition: border-color 0.3s ease;
}

textarea:focus, input:focus {
     border-color: var(--accent) !important;
}

.stButton > button {
     background-color: #FFFFFF !important;
     color: var(--text-main) !important;
     border: 1px solid var(--border-light) !important;
     border-radius: 4px;
     font-weight: 600;
     letter-spacing: 1px;
     padding: 0.45rem 1.2rem;
     transition: all 0.2s ease;
}

.stButton > button:hover {
     background-color: var(--bg-soft) !important;
     border-color: var(--accent) !important;
     transform: translateY(-2px);
     box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* 修正側邊欄按鈕顯示問題 */
button[kind="header"] span {
     display: none !important;
}

button[kind="header"]::after {
     content: "☰";
     font-size: 1.5rem;
     font-family: Arial, sans-serif !important;
}

/* 確保按鈕本身可見 */
button[kind="header"] {
     display: block !important;
     visibility: visible !important;
}

section[data-testid="stSidebar"] {
     background-color: #FFFFFF;
     border-right: 1px solid var(--border-light);
}

div[data-testid="metric-container"] {
     background-color: #FFFFFF;
     border: 1px solid var(--border-light);
     padding: 12px;
     border-radius: 6px;
     transition: transform 0.2s ease;
}

div[data-testid="metric-container"]:hover {
     transform: scale(1.02);
}

.community-card,
.manifesto-box {
     background-color: var(--bg-card);
     border: 1px solid var(--border-light);
     border-radius: 8px;
     padding: 18px;
     transition: all 0.3s ease;
}

.community-card:hover {
     transform: translateY(-4px);
     box-shadow: 0 6px 12px rgba(0,0,0,0.1);
     border-color: var(--accent);
}

thead tr th {
     background-color: var(--bg-soft) !important;
     color: #000000 !important;
}

tbody tr td {
     color: var(--text-main) !important;
}

div[data-baseweb="select"] span {
     color: var(--text-main) !important;
}

div[data-testid="stProgress"] > div > div {
     background-color: #000000 !important;
}

/* Chart background - force white */
canvas {
     background-color: #FFFFFF !important;
}

[data-testid="stVegaLiteChart"] {
     background-color: #FFFFFF !important;
}

.pulse {
     animation: pulse 2s infinite;
}

@keyframes pulse {
     0%, 100% { opacity: 1; }
     50% { opacity: 0.5; }
}

/* ===== SCENT IMAGE CARD (REFINED) ===== */
.scent-card {
    position: relative;
    height: 240px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    cursor: pointer;
}

.scent-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

.scent-bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    z-index: 1;
}

.scent-overlay {
    position: absolute;
    inset: 0;
    z-index: 2;
    background: linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.6) 100%);
}

.scent-content {
    position: relative;
    z-index: 3;
    height: 100%;
    padding: 1.2rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    text-align: left;
}

.scent-layer {
    font-size: 0.75rem;
    opacity: 0.9;
    margin: 0 0 4px 0;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.scent-content h2 {
    margin: 4px 0;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.scent-content h3 {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 600;
    opacity: 0.95;
}

/* Mobile optimization */
@media (max-width: 768px) {
    .scent-card {
        height: 200px;
    }
    
    .scent-content {
        padding: 1rem;
    }

    .scent-content h2 {
        font-size: 1.2rem;
    }
    
    .scent-content h3 {
        font-size: 1rem;
    }
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 2. 側邊欄邏輯 ---
if st.session_state.page == 'home' and not st.session_state.generated:
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/9/9d/L%27Or%C3%A9al_logo.svg", width=150)
        st.markdown("### SYSTEM STATUS")
        
        st.success("● ONLINE: LE SABLIER PRO")
        st.caption("Firmware: v3.0.1 | Latency: 12ms")
        
        st.markdown("---")
        st.markdown("### LIVE SENSORS")
        col1, col2 = st.columns(2)
        col1.metric("HRV", "45ms", "Relaxed")
        col2.metric("TEMP", "36.5°C", "Normal")
        
        st.markdown("---")
        st.markdown("### ENVIRONMENT")
        st.caption("Location: Taipei, Taiwan")
        st.caption("Humidity: 75% (High)")
        st.caption("Air Quality: Moderate")

        st.markdown("---")
        st.markdown("### CAPSULE STATUS")
        st.caption("Detected Capsules & Fluid Levels")
        
        tank_data = {
            "Pod 1: Citrus (Top)": 0.8,
            "Pod 2: Orange (Top)": 0.6,
            "Pod 3: Mint (Top)": 0.9,
            "Pod 4: Bergamot (Top)": 0.4,
            "Pod 5: Rose (Heart)": 0.7,
            "Pod 6: Jasmine (Heart)": 0.3,
            "Pod 7: Geranium (Heart)": 0.5,
            "Pod 8: Lavender (Heart)": 0.6,
            "Pod 9: Musk (Base)": 0.8,
            "Pod 10: Vanilla (Base)": 0.9,
            "Pod 11: Cedar (Base)": 0.9,
            "Pod 12: Benzoin (Base)": 0.5,
            "Pod 13: Solvent (Alc)": 0.7,
        }
        
        with st.container():
            for name, level in tank_data.items():
                st.text(name)
                st.progress(level)
            
        if st.session_state.saved_presets:
            st.markdown("---")
            st.info(f"💾 {len(st.session_state.saved_presets)} Saved Presets")
            
else:
    with st.sidebar:
        st.empty()
        if st.session_state.page == 'community':
            if st.button("BACK TO GENERATOR"):
                st.session_state.page = 'home'
                st.rerun()
        elif st.session_state.page == 'presets':
            if st.button("BACK TO HOME"):
                st.session_state.page = 'home'
                st.rerun()

# --- 3. 頁面內容 ---

# =========== 頁面 A: GENERATOR ===========
if st.session_state.page == 'home':
    
    st.markdown("<h1 class='centered-title'>L'ORÉAL SCENT OS</h1>", unsafe_allow_html=True)
    
    if not st.session_state.generated:
        st.markdown("<p class='centered-text'>DUAL-CORE GENERATIVE ENGINE</p>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            user_input = st.text_area(
                "DESCRIBE YOUR DESIRED SCENT ATMOSPHERE", 
                height=150, 
                value=st.session_state.user_input,
                placeholder="E.g. I want the feeling of a library in London, old books, rain outside, and a cup of earl grey tea.",
                key="scent_input"
            )
            
            st.markdown("##### 💡 QUICK INSPIRATIONS")
            preset_col1, preset_col2, preset_col3 = st.columns(3)
            with preset_col1:
                if st.button("📚 Library", use_container_width=True):
                    st.session_state.user_input = "Old books, leather chairs, wooden shelves, and quiet contemplation"
                    st.rerun()
            with preset_col2:
                if st.button("🌊 Ocean", use_container_width=True):
                    st.session_state.user_input = "Fresh sea breeze, salt water, driftwood, and morning sun on waves"
                    st.rerun()
            with preset_col3:
                if st.button("☕ Café", use_container_width=True):
                    st.session_state.user_input = "Fresh coffee beans, warm pastries, vanilla, and cozy afternoon ambiance"
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("✨ GENERATE SCENT SIGNATURE", use_container_width=True):
                if user_input:
                    st.session_state.user_input = user_input
                    st.session_state.generated = True
                    st.session_state.recipe = {
                        'name': f"CUSTOM-{len(st.session_state.saved_presets)+1:03d}",
                        'input': user_input,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M")
                    }
                    st.rerun()
                else:
                    st.warning("Please describe your desired scent first.")

    else:
        # Header with recipe name
        col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
        with col_header2:
            st.markdown(f"<h2 style='text-align: center;'>{st.session_state.recipe['name']}</h2>", unsafe_allow_html=True)
        
        with col_header3:
            if st.button("NEW GENERATION"):
                st.session_state.generated = False
                st.session_state.user_input = ""
                st.rerun()

        st.markdown("---")

        # Phase 1 & 2
        col_phase1, col_phase2 = st.columns(2)
        
        with col_phase1:
            st.markdown("### PHASE 1: LDM CREATION")
            st.caption("Navigating Latent Space & Synthesizing Molecules...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i in range(100):
                time.sleep(0.005)
                progress_bar.progress(i + 1)
                if i % 20 == 0:
                    status_text.text(f"Processing... {i}%")
            status_text.empty()
            st.success("✔ Molecular Structure Created")
            st.caption("Generated 847 candidate molecules")
            
        with col_phase2:
            st.markdown("### PHASE 2: PIML PHYSICS")
            st.caption("Simulating 6-Hour Evaporation Dynamics...")
            progress_bar2 = st.progress(0)
            status_text2 = st.empty()
            for i in range(100):
                time.sleep(0.005)
                progress_bar2.progress(i + 1)
                if i % 20 == 0:
                    status_text2.text(f"Optimizing... {i}%")
            status_text2.empty()
            st.success("✔ Optimization Complete")
            st.caption("Validated across 3 climate conditions")

        st.markdown("<br>", unsafe_allow_html=True)

        # Evolution curve
        c_chart1, c_chart2, c_chart3 = st.columns([1, 2, 1])
        with c_chart2:
            st.markdown("##### SCENT EVOLUTION CURVE (6 HOURS)")
            t = np.linspace(0, 6, 50)
            chart_data = pd.DataFrame({
                'Top Notes': 50 * np.exp(-1.2 * t),
                'Heart Notes': 30 * np.exp(-0.4 * t),
                'Base Notes': 40 * np.exp(-0.1 * t)
            }, index=t)
            st.line_chart(chart_data, height=250, color=["#F4D03F", "#A569BD", "#DC7633"])

        st.markdown("---")

        # Recipe cards with images
        st.markdown("<h3 style='text-align: center;'>FINAL RECIPE</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        rc1, rc2, rc3, rc4, rc5 = st.columns(5)
        
        # Define scent data with online images
        scents_data = [
            {
                "name": "ORANGE",
                "percent": "15%",
                "layer": "Top",
                "image": "https://images.unsplash.com/photo-1582979512210-99b6a53386f9?w=500&h=500&fit=crop&q=80"
            },
            {
                "name": "CITRUS",
                "percent": "20%",
                "layer": "Top",
                "image": "https://images.unsplash.com/photo-1590502593747-42a996133562?w=500&h=500&fit=crop&q=80"
            },
            {
                "name": "ROSE",
                "percent": "10%",
                "layer": "Heart",
                "image": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=500&h=500&fit=crop&q=80"
            },
            {
                "name": "MUSK",
                "percent": "35%",
                "layer": "Base",
                "image": "https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=500&h=500&fit=crop&q=80"
            },
            {
                "name": "AMBERGRIS",
                "percent": "20%",
                "layer": "Base",
                "image": "https://images.unsplash.com/photo-1604762524889-8088e03e6beb?w=500&h=500&fit=crop&q=80"
            }
        ]
        
        for i, col in enumerate([rc1, rc2, rc3, rc4, rc5]):
            scent = scents_data[i]
            
            with col:
                st.markdown(f"""
                <div class="scent-card">
                    <div class="scent-bg" style="background-image: url('{scent['image']}');"></div>
                    <div class="scent-overlay"></div>
                    <div class="scent-content" style="color: #FFFFFF;">
                        <p class="scent-layer">{scent['layer']} Note</p>
                        <h2>{scent['name']}</h2>
                        <h3>{scent['percent']}</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # User guide
        st.markdown("<br><br>", unsafe_allow_html=True)
        with st.container():
             st.markdown(f"""
             <div class='manifesto-box'>
                <h4>📖 USER GUIDE & SCENT INTRODUCTION</h4>
                <p><strong>Your Input:</strong> <em>"{st.session_state.recipe['input'][:100]}..."</em></p>
                <p><strong>Olfactory Profile:</strong> This scent captures the essence of <em>"Quiet Intellect"</em>. The volatility of the top notes provides an immediate awakening, while the heavy molecular weight of the base notes ensures a sillage that lasts through 8 hours.</p>
                <p><strong>Physical Properties:</strong> Optimized for high-humidity environments (Taiwan). The PIML engine has added <strong>Hydrophobic Fixatives</strong> to prevent the scent from breaking down.</p>
                <p><strong>How to Wear:</strong> Apply 2 sprays to pulse points. Wait 30 seconds for the alcohol to evaporate before experiencing the true Heart Note.</p>
                <p><strong>Best For:</strong> Indoor environments, 20-26°C, moderate activity level</p>
             </div>
             """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Action buttons
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            if st.button("SAVE PRESET", use_container_width=True):
                if st.session_state.recipe not in st.session_state.saved_presets:
                    st.session_state.saved_presets.append(st.session_state.recipe.copy())
                    st.toast("✅ Preset saved successfully!", icon="💾")
                else:
                    st.toast("ℹ️ Preset already saved", icon="ℹ️")
        with ac2:
            if st.button("SHARE", use_container_width=True):
                st.toast("Published to community!", icon="🌐")
        with ac3:
            if st.button("COMMUNITY", use_container_width=True):
                st.session_state.page = 'community'
                st.rerun()

        if st.session_state.saved_presets:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📚 VIEW MY PRESETS"):
                st.session_state.page = 'presets'
                st.rerun()

# =========== 頁面 B: COMMUNITY ===========
elif st.session_state.page == 'community':
    
    st.markdown("<h1 class='centered-title'>SCENT COMMUNITY MARKETPLACE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='centered-text'>Discover & Download Presets created by users worldwide</p>", unsafe_allow_html=True)
    
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("🔍 Search presets...", placeholder="Search by name, creator, or tags")
    with search_col2:
        sort_by = st.selectbox("Sort by", ["Trending", "Recent", "Popular"])
    
    st.markdown("---")

    scents = [
        {"name": "CYBER RAIN", "user": "@Alex_TW", "tags": ["#Neon", "#Metallic", "#Night"], "notes": "Ozone, Metal, Musk", "downloads": 1247},
        {"name": "SUNDAY MORNING", "user": "@Sarah_J", "tags": ["#Cozy", "#Cotton", "#Coffee"], "notes": "Linen, Latte, Vanilla", "downloads": 2891},
        {"name": "FOREST WORK", "user": "@David_Eng", "tags": ["#Focus", "#Green", "#Wood"], "notes": "Pine, Vetiver, Moss", "downloads": 1653},
        {"name": "TOKYO DRIFT", "user": "@Kenji_JP", "tags": ["#Speed", "#Rubber", "#Asphalt"], "notes": "Burnt Rubber, Smoke, Leather", "downloads": 987},
    ]

    row1_1, row1_2 = st.columns(2)
    row2_1, row2_2 = st.columns(2)
    cols = [row1_1, row1_2, row2_1, row2_2]

    for i, scent in enumerate(scents):
        with cols[i]:
            st.markdown(f"""
            <div class='community-card'>
                <h3>{scent['name']}</h3>
                <p style='color: #8C6D1F;'>Created by {scent['user']}</p>
                <p style='font-size: 0.9em;'><strong>Notes:</strong> {scent['notes']}</p>
                <p><em>{' '.join(scent['tags'])}</em></p>
                <p style='font-size: 0.85em; color: #888;'>⬇️ {scent['downloads']} downloads</p>
            </div>
            """, unsafe_allow_html=True)
            download_col, preview_col = st.columns(2)
            with download_col:
                if st.button(f"📥 DOWNLOAD", key=f"dl_{i}", use_container_width=True):
                    st.toast(f"✅ Downloaded {scent['name']}!", icon="📥")
            with preview_col:
                if st.button(f"👁️ PREVIEW", key=f"pv_{i}", use_container_width=True):
                    st.toast(f"Preview: {scent['notes']}", icon="👁️")

    st.markdown("<br><br>", unsafe_allow_html=True)

# =========== 頁面 C: MY PRESETS ===========
elif st.session_state.page == 'presets':
    st.markdown("<h1 class='centered-title'>MY SAVED PRESETS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='centered-text'>Your personal scent library</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.saved_presets:
        st.info("No saved presets yet. Create your first scent!")
        if st.button("➕ CREATE NEW SCENT"):
            st.session_state.page = 'home'
            st.rerun()
    else:
        for idx, preset in enumerate(st.session_state.saved_presets):
            with st.expander(f"📋 {preset['name']} - {preset['timestamp']}"):
                st.markdown(f"**Original Input:** {preset['input']}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"🔄 REGENERATE", key=f"regen_{idx}"):
                        st.session_state.user_input = preset['input']
                        st.session_state.page = 'home'
                        st.session_state.generated = False
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ DELETE", key=f"del_{idx}"):
                        st.session_state.saved_presets.pop(idx)
                        st.rerun()
                with col3:
                    if st.button(f"📤 EXPORT", key=f"exp_{idx}"):
                        st.toast("Exported successfully!", icon="✅")
