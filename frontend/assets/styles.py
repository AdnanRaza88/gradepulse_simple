CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

:root {
    --bg:     #E4EBF5;
    --light:  #FFFFFF;
    --dark:   #B8C4D8;
    --accent: #4A7FE5;
    --green:  #38C97A;
    --red:    #E05D5D;
    --orange: #F5A623;
    --text:   #2D3748;
    --muted:  #7A90A8;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden; }

.main .block-container { padding: 2rem 2.5rem !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: var(--bg) !important;
    box-shadow: 4px 0 20px rgba(184,196,216,0.6) !important;
}

/* Cards */
.card {
    background: var(--bg);
    border-radius: 20px;
    box-shadow: 8px 8px 20px var(--dark), -8px -8px 20px var(--light);
    padding: 24px;
    margin-bottom: 20px;
}
.card-inset {
    background: var(--bg);
    border-radius: 14px;
    box-shadow: inset 4px 4px 10px var(--dark), inset -4px -4px 10px var(--light);
    padding: 18px;
    margin-bottom: 14px;
}

/* Stat */
.stat {
    background: var(--bg);
    border-radius: 18px;
    box-shadow: 6px 6px 16px var(--dark), -6px -6px 16px var(--light);
    padding: 18px;
    text-align: center;
}
.stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
}
.stat-lbl { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: .07em; margin-top:3px; }

/* Buttons */
.stButton > button {
    background: var(--bg) !important;
    color: var(--text) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 5px 5px 12px var(--dark), -5px -5px 12px var(--light) !important;
    font-weight: 600 !important;
    transition: all .15s ease !important;
}
.stButton > button:hover { box-shadow: 3px 3px 8px var(--dark), -3px -3px 8px var(--light) !important; color: var(--accent) !important; }
.stButton > button:active { box-shadow: inset 3px 3px 8px var(--dark), inset -3px -3px 8px var(--light) !important; }

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg) !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: inset 3px 3px 7px var(--dark), inset -3px -3px 7px var(--light) !important;
    color: var(--text) !important;
}

/* Page title */
.ptitle { font-family:'Space Grotesk',sans-serif; font-size:1.7rem; font-weight:700; color:var(--text); margin-bottom:2px; }
.psub   { font-size:.88rem; color:var(--muted); margin-bottom:24px; }

/* AI response */
.ai-box {
    background: var(--bg);
    border-radius: 18px;
    box-shadow: 6px 6px 16px var(--dark), -6px -6px 16px var(--light);
    border-left: 4px solid var(--accent);
    padding: 26px;
    margin-top: 16px;
}

/* Alerts */
.ok  { background:rgba(56,201,122,.1); border-left:4px solid var(--green); border-radius:10px; padding:12px 16px; color:#1a6b3a; font-weight:500; margin:8px 0; }
.err { background:rgba(224,93,93,.1);  border-left:4px solid var(--red);   border-radius:10px; padding:12px 16px; color:#7a1c1c; font-weight:500; margin:8px 0; }

/* Grade badge */
.gb { display:inline-block; padding:3px 12px; border-radius:20px; font-weight:700; font-size:.82rem; }
.ga { background:rgba(56,201,122,.15); color:var(--green); }
.gb_ { background:rgba(74,127,229,.15); color:var(--accent); }
.gc { background:rgba(245,166,35,.15); color:var(--orange); }
.gf { background:rgba(224,93,93,.15); color:var(--red); }

/* Sidebar brand */
.brand { font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700; color:var(--accent); text-align:center; padding:16px 0 4px; }
.brand-sub { font-size:.68rem; color:var(--muted); text-align:center; letter-spacing:.07em; margin-bottom:20px; }

.dot-on  { display:inline-block; width:7px; height:7px; border-radius:50%; background:var(--green); margin-right:5px; }
.dot-off { display:inline-block; width:7px; height:7px; border-radius:50%; background:var(--red);   margin-right:5px; }
</style>
"""
