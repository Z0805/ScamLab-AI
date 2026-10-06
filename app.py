import streamlit as st
from PIL import Image
from ocr import extract_text
from analyzer import analyze_message

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ScamLab AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THEME MANAGEMENT
# ============================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Theme color palettes
THEMES = {
    "dark": {
        "bg_primary": "#0a0e1a",
        "bg_secondary": "#151b2f",
        "bg_tertiary": "#1f2747",
        "bg_card": "#232d3e",
        "text_primary": "#f0f4f9",
        "text_secondary": "#9ca3af",
        "text_tertiary": "#6b7280",
        "text_input": "#f0f4f9",
        "accent_primary": "#6366f1",
        "accent_secondary": "#8b5cf6",
        "accent_tertiary": "#ec4899",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#06b6d4",
        "border": "rgba(99, 102, 241, 0.15)",
        "border_hover": "rgba(99, 102, 241, 0.35)",
        "shadow": "0 10px 40px rgba(0, 0, 0, 0.5)",
        "shadow_hover": "0 20px 60px rgba(99, 102, 241, 0.2)",
    },
    "light": {
        "bg_primary": "#fafbfc",
        "bg_secondary": "#f1f3f7",
        "bg_tertiary": "#e8ecf5",
        "bg_card": "#ffffff",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "text_tertiary": "#64748b",
        "text_input": "#1e293b",
        "accent_primary": "#4f46e5",
        "accent_secondary": "#7c3aed",
        "accent_tertiary": "#db2777",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "info": "#0891b2",
        "border": "rgba(79, 70, 229, 0.12)",
        "border_hover": "rgba(79, 70, 229, 0.25)",
        "shadow": "0 10px 40px rgba(0, 0, 0, 0.08)",
        "shadow_hover": "0 20px 60px rgba(79, 70, 229, 0.12)",
    }
}

current_theme = THEMES[st.session_state.theme]

# ============================================================
# CUSTOM CSS WITH DYNAMIC THEME VARIABLES
# ============================================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

* {{
    box-sizing: border-box;
}}

:root {{
    --bg-primary: {current_theme['bg_primary']};
    --bg-secondary: {current_theme['bg_secondary']};
    --bg-tertiary: {current_theme['bg_tertiary']};
    --bg-card: {current_theme['bg_card']};
    --text-primary: {current_theme['text_primary']};
    --text-secondary: {current_theme['text_secondary']};
    --text-tertiary: {current_theme['text_tertiary']};
    --text-input: {current_theme['text_input']};
    --accent-primary: {current_theme['accent_primary']};
    --accent-secondary: {current_theme['accent_secondary']};
    --accent-tertiary: {current_theme['accent_tertiary']};
    --success: {current_theme['success']};
    --warning: {current_theme['warning']};
    --danger: {current_theme['danger']};
    --info: {current_theme['info']};
    --border: {current_theme['border']};
    --border-hover: {current_theme['border_hover']};
    --shadow: {current_theme['shadow']};
    --shadow-hover: {current_theme['shadow_hover']};
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: var(--bg-primary);
    color: var(--text-primary);
}}

.block-container {{
    max-width: 1300px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}}

/* ============================================================
   THEME TOGGLE - FIXED POSITION
   ============================================================ */

.stSidebar [data-testid="stSidebarNav"] {{
    background-color: transparent;
}}

.sidebar-theme-toggle {{
    display: flex;
    gap: 0.75rem;
    margin: 1.5rem 0;
    padding: 0 1rem;
}}

.sidebar-theme-toggle button {{
    flex: 1;
    padding: 0.75rem 1rem !important;
    border-radius: 10px !important;
    border: 2px solid var(--border) !important;
    background: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.3s ease !important;
    cursor: pointer;
}}

.sidebar-theme-toggle button:hover {{
    border-color: var(--border-hover) !important;
    background: var(--bg-tertiary) !important;
    color: var(--accent-primary) !important;
}}

/* ============================================================
   HERO SECTION
   ============================================================ */

.hero {{
    padding: 3rem 2.5rem;
    border-radius: 24px;
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border: 2px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}}

.hero::before {{
    content: '';
    position: absolute;
    top: -30%;
    right: -30%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, var(--accent-primary), transparent 70%);
    opacity: 0.03;
    border-radius: 50%;
    pointer-events: none;
}}

.hero::after {{
    content: '';
    position: absolute;
    bottom: -20%;
    left: -20%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, var(--accent-secondary), transparent 70%);
    opacity: 0.02;
    border-radius: 50%;
    pointer-events: none;
}}

.hero-badge {{
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    border: 1px solid var(--border);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}}

.hero h1 {{
    font-size: clamp(2.5rem, 6vw, 3.5rem);
    font-weight: 800;
    margin: 0;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}}

.hero-subtitle {{
    font-size: clamp(1.2rem, 3vw, 1.5rem);
    color: var(--text-primary);
    margin-top: 0.8rem;
    font-weight: 600;
}}

.hero-description {{
    font-size: clamp(0.9rem, 2vw, 1rem);
    color: var(--text-secondary);
    margin-top: 0.8rem;
    line-height: 1.6;
    max-width: 600px;
}}

/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {{
    min-height: 200px;
    padding: clamp(1.5rem, 4vw, 2rem);
    border-radius: 18px;
    background: var(--bg-card);
    border: 2px solid var(--border);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}}

.feature-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
    transform: scaleX(0);
    transition: transform 0.35s ease;
}}

.feature-card:hover {{
    transform: translateY(-8px);
    border-color: var(--border-hover);
    box-shadow: var(--shadow-hover);
    background: var(--bg-tertiary);
}}

.feature-card:hover::before {{
    transform: scaleX(1);
}}

.feature-icon {{
    font-size: clamp(2rem, 5vw, 2.5rem);
    margin-bottom: 1rem;
    display: inline-block;
}}

.feature-title {{
    font-size: clamp(1.1rem, 2.5vw, 1.3rem);
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
}}

.feature-text {{
    font-size: clamp(0.9rem, 1.8vw, 1rem);
    line-height: 1.6;
    color: var(--text-secondary);
}}

/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-heading {{
    font-size: clamp(1.8rem, 5vw, 2rem);
    font-weight: 800;
    color: var(--text-primary);
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.section-heading-icon {{
    font-size: clamp(1.8rem, 5vw, 2rem);
}}

.section-description {{
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
    font-size: clamp(0.9rem, 2vw, 1rem);
    line-height: 1.6;
}}

.compact-heading {{
    font-size: clamp(1.3rem, 3vw, 1.6rem);
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}

/* ============================================================
   TEXT AREA & INPUT - FIXED FOR LIGHT THEME
   ============================================================ */

textarea {{
    background-color: var(--bg-card) !important;
    color: var(--text-input) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: clamp(0.8rem, 1.5vw, 0.95rem) !important;
    transition: all 0.3s ease !important;
    padding: 1rem !important;
}}

textarea::placeholder {{
    color: var(--text-secondary) !important;
    opacity: 0.7 !important;
}}

textarea:focus {{
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    outline: none !important;
}}

/* ============================================================
   FILE UPLOADER - RESPONSIVE TEXT COLOR
   ============================================================ */

[data-testid="stFileUploadDropzone"] {{
    background-color: var(--bg-secondary) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 12px !important;
}}

[data-testid="stFileUploadDropzone"] * {{
    color: var(--text-primary) !important;
}}

/* Upload label text */
.stFileUploader label {{
    color: var(--text-primary) !important;
}}

/* Upload section text */
[data-testid="stFileUploader"] {{
    color: var(--text-primary) !important;
}}

[data-testid="stFileUploader"] div {{
    color: var(--text-primary) !important;
}}

/* All file uploader text elements */
[data-testid="stFileUploader"] p {{
    color: var(--text-primary) !important;
}}

[data-testid="stFileUploader"] span {{
    color: var(--text-primary) !important;
}}

/* Drag and drop text */
[data-testid="stFileUploadDropzone"] p {{
    color: var(--text-secondary) !important;
}}

/* File upload button text */
[data-testid="stFileUploadDropzone"] button {{
    color: var(--accent-primary) !important;
}}

/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {{
    border-radius: 12px !important;
    border: 2px solid var(--accent-primary) !important;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    padding: clamp(0.75rem, 2vw, 0.9rem) clamp(1.5rem, 3vw, 1.8rem) !important;
    font-size: clamp(0.85rem, 1.5vw, 0.95rem) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3) !important;
    width: 100% !important;
}}

.stButton > button:hover {{
    transform: translateY(-3px) !important;
    box-shadow: var(--shadow-hover) !important;
    border-color: var(--accent-secondary) !important;
}}

.stButton > button:active {{
    transform: translateY(-1px) !important;
}}

/* ============================================================
   METRICS
   ============================================================ */

[data-testid="stMetric"] {{
    background: var(--bg-card);
    border: 2px solid var(--border);
    padding: clamp(1rem, 2vw, 1.2rem);
    border-radius: 14px;
    transition: all 0.3s ease;
}}

[data-testid="stMetric"]:hover {{
    border-color: var(--border-hover);
    background: var(--bg-tertiary);
}}

[data-testid="stMetricLabel"] {{
    color: var(--text-secondary) !important;
    font-size: clamp(0.75rem, 1.5vw, 0.85rem) !important;
    font-weight: 600 !important;
}}

[data-testid="stMetricValue"] {{
    color: var(--accent-primary) !important;
    font-size: clamp(1.5rem, 3vw, 1.8rem) !important;
    font-weight: 800 !important;
    font-family: 'JetBrains Mono', monospace !important;
}}

/* ============================================================
   PROGRESS BAR
   ============================================================ */

.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
    border-radius: 10px !important;
}}

.stProgress > div > div {{
    background: var(--bg-tertiary) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}}

/* ============================================================
   SCREENSHOT PREVIEW
   ============================================================ */

.screenshot-preview {{
    display: flex;
    justify-content: center;
    margin: 1rem 0 1.5rem 0;
}}

.screenshot-preview img {{
    max-width: 100% !important;
    max-height: 500px !important;
    object-fit: contain;
    border-radius: 16px;
    border: 2px solid var(--border);
    box-shadow: var(--shadow);
    transition: all 0.3s ease;
}}

.screenshot-preview img:hover {{
    transform: scale(1.02);
    border-color: var(--accent-primary);
}}

/* ============================================================
   ML RESULT CARD
   ============================================================ */

.ml-card {{
    padding: clamp(1.5rem, 3vw, 2rem);
    border-radius: 16px;
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
    border: 2px solid var(--border);
    margin-top: 1.2rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
}}

.ml-title {{
    font-size: clamp(1.1rem, 2vw, 1.3rem);
    font-weight: 700;
    color: var(--accent-primary);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}

.ml-text {{
    font-size: clamp(0.9rem, 1.8vw, 1rem);
    color: var(--text-secondary);
    line-height: 1.7;
}}

/* ============================================================
   RISK METER CARD
   ============================================================ */

.risk-card {{
    padding: clamp(1.5rem, 3vw, 2rem);
    border-radius: 16px;
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
    border: 2px solid var(--border);
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
}}

.risk-title {{
    font-size: clamp(1.1rem, 2vw, 1.3rem);
    font-weight: 700;
    color: var(--accent-primary);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}}

.explanation-card {{
    padding: clamp(1rem, 2vw, 1.2rem) clamp(1rem, 2vw, 1.2rem);
    margin: 0.75rem 0;
    border-radius: 12px;
    background: var(--bg-secondary);
    border-left: 4px solid var(--accent-primary);
    color: var(--text-secondary);
    font-size: clamp(0.85rem, 1.5vw, 0.95rem);
    line-height: 1.6;
    transition: all 0.3s ease;
}}

.explanation-card:hover {{
    border-left-color: var(--accent-secondary);
    background: var(--bg-tertiary);
}}

/* ============================================================
   SAFETY CENTER CARDS
   ============================================================ */

.safety-card {{
    min-height: 180px;
    padding: clamp(1.5rem, 3vw, 1.8rem);
    border-radius: 16px;
    background: var(--bg-card);
    border: 2px solid var(--border);
    transition: all 0.35s ease;
    box-shadow: var(--shadow);
}}

.safety-card:hover {{
    transform: translateY(-6px);
    border-color: var(--border-hover);
    background: var(--bg-tertiary);
    box-shadow: var(--shadow-hover);
}}

.safety-icon {{
    font-size: clamp(2rem, 4vw, 2.2rem);
    margin-bottom: 0.8rem;
    display: inline-block;
}}

.safety-title {{
    font-size: clamp(1rem, 2vw, 1.2rem);
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.6rem;
}}

.safety-text {{
    font-size: clamp(0.85rem, 1.6vw, 0.95rem);
    line-height: 1.6;
    color: var(--text-secondary);
}}

/* ============================================================
   DIVIDER
   ============================================================ */

hr {{
    border: none;
    height: 1px;
    background: var(--border);
    margin: 2rem 0;
}}

/* ============================================================
   ALERTS & MESSAGES
   ============================================================ */

[data-testid="stAlert"] {{
    background-color: transparent !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    padding: clamp(1rem, 2vw, 1.2rem) !important;
}}

[data-testid="stAlert"][data-baseweb="notification"] {{
    background-color: rgba(99, 102, 241, 0.08) !important;
    border-color: var(--accent-primary) !important;
}}

/* ============================================================
   FOOTER
   ============================================================ */

.footer {{
    text-align: center;
    padding: clamp(2rem, 4vw, 2.5rem) 1.5rem;
    color: var(--text-secondary);
    border-top: 1px solid var(--border);
    margin-top: 2.5rem;
}}

.footer-title {{
    font-size: clamp(1.5rem, 3vw, 1.8rem);
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.8rem;
}}

.footer p {{
    font-size: clamp(0.85rem, 1.5vw, 0.95rem);
    line-height: 1.8;
    margin: 0.5rem 0;
    color: var(--text-secondary);
}}

/* ============================================================
   SIDEBAR STYLES
   ============================================================ */

.stSidebar {{
    background-color: var(--bg-secondary) !important;
}}

.stSidebar [data-testid="stSidebarContent"] {{
    background-color: var(--bg-secondary) !important;
}}

.stSidebar > div:first-child {{
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
}}

/* ============================================================
   MARKDOWN TEXT - ENSURE VISIBILITY
   ============================================================ */

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
    color: var(--text-primary) !important;
}}

.stMarkdown p {{
    color: var(--text-primary) !important;
}}

.stMarkdown {{
    color: var(--text-primary) !important;
}}

/* ============================================================
   TABLET LAYOUT (768px - 1024px)
   ============================================================ */

@media (max-width: 1024px) {{

    .block-container {{
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }}

    .hero {{
        padding: 2.5rem 2rem;
    }}

    .hero h1 {{
        font-size: 2.5rem;
    }}

    .hero-description {{
        font-size: 0.95rem;
    }}

    .feature-card {{
        min-height: 180px;
        padding: 1.5rem;
    }}

    .safety-card {{
        min-height: 160px;
    }}

}}

/* ============================================================
   MOBILE LAYOUT (480px - 767px)
   ============================================================ */

@media (max-width: 767px) {{

    .block-container {{
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}

    .hero {{
        padding: 2rem 1.5rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
    }}

    .hero::before,
    .hero::after {{
        display: none;
    }}

    .hero-badge {{
        font-size: 0.7rem;
        padding: 0.4rem 0.8rem;
        margin-bottom: 0.8rem;
    }}

    .hero h1 {{
        font-size: 2rem;
        letter-spacing: -0.8px;
    }}

    .hero-subtitle {{
        font-size: 1.1rem;
        margin-top: 0.6rem;
    }}

    .hero-description {{
        font-size: 0.85rem;
        margin-top: 0.6rem;
    }}

    .feature-card {{
        min-height: auto;
        padding: 1.2rem;
        border-radius: 14px;
        margin-bottom: 0.8rem;
    }}

    .feature-icon {{
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }}

    .feature-title {{
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }}

    .feature-text {{
        font-size: 0.85rem;
    }}

    .section-heading {{
        font-size: 1.4rem;
        margin-top: 1.2rem;
        margin-bottom: 0.4rem;
    }}

    .section-heading-icon {{
        font-size: 1.4rem;
    }}

    .section-description {{
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }}

    .compact-heading {{
        font-size: 1.2rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }}

    .stButton > button {{
        padding: 0.7rem 1.2rem !important;
        font-size: 0.8rem !important;
        width: 100% !important;
        border-radius: 10px !important;
    }}

    [data-testid="stMetric"] {{
        padding: 0.8rem;
        border-radius: 10px;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.7rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.3rem !important;
    }}

    .risk-card {{
        padding: 1.2rem;
        border-radius: 14px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }}

    .risk-title {{
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }}

    .ml-card {{
        padding: 1.2rem;
        border-radius: 14px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }}

    .ml-title {{
        font-size: 1.1rem;
        margin-bottom: 0.6rem;
    }}

    .ml-text {{
        font-size: 0.85rem;
    }}

    .explanation-card {{
        padding: 0.8rem 1rem;
        margin: 0.6rem 0;
        border-radius: 10px;
        font-size: 0.8rem;
    }}

    .safety-card {{
        min-height: auto;
        padding: 1.2rem;
        border-radius: 14px;
        margin-bottom: 0.8rem;
    }}

    .safety-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.6rem;
    }}

    .safety-title {{
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
    }}

    .safety-text {{
        font-size: 0.8rem;
    }}

    textarea {{
        font-size: 0.85rem !important;
        padding: 0.8rem !important;
    }}

    .screenshot-preview img {{
        max-height: 350px !important;
        border-radius: 12px;
    }}

    hr {{
        margin: 1.5rem 0;
    }}

    .footer {{
        padding: 1.5rem 1rem;
        margin-top: 1.5rem;
    }}

    .footer-title {{
        font-size: 1.3rem;
        margin-bottom: 0.6rem;
    }}

    .footer p {{
        font-size: 0.8rem;
        line-height: 1.6;
        margin: 0.4rem 0;
    }}

    [data-testid="stColumn"] {{
        gap: 0.5rem;
    }}

}}

/* ============================================================
   SMALL MOBILE LAYOUT (max-width: 480px)
   ============================================================ */

@media (max-width: 480px) {{

    .block-container {{
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-top: 0.8rem !important;
    }}

    .hero {{
        padding: 1.5rem 1.2rem;
        border-radius: 14px;
        margin-bottom: 1.2rem;
    }}

    .hero h1 {{
        font-size: 1.7rem;
        letter-spacing: -0.5px;
    }}

    .hero-subtitle {{
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }}

    .hero-description {{
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }}

    .feature-card {{
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
    }}

    .feature-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.6rem;
    }}

    .feature-title {{
        font-size: 0.9rem;
        margin-bottom: 0.4rem;
    }}

    .feature-text {{
        font-size: 0.8rem;
    }}

    .section-heading {{
        font-size: 1.3rem;
        margin-top: 1rem;
    }}

    .section-heading-icon {{
        font-size: 1.3rem;
    }}

    .section-description {{
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
    }}

    .compact-heading {{
        font-size: 1.1rem;
        margin-top: 0.6rem;
        margin-bottom: 0.6rem;
    }}

    .stButton > button {{
        padding: 0.6rem 1rem !important;
        font-size: 0.75rem !important;
    }}

    [data-testid="stMetric"] {{
        padding: 0.6rem;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.65rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.2rem !important;
    }}

    .risk-card {{
        padding: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }}

    .ml-card {{
        padding: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }}

    .explanation-card {{
        padding: 0.7rem 0.8rem;
        margin: 0.5rem 0;
        font-size: 0.75rem;
    }}

    .safety-card {{
        padding: 1rem;
        margin-bottom: 0.6rem;
    }}

    .safety-icon {{
        font-size: 1.6rem;
    }}

    .safety-title {{
        font-size: 0.9rem;
    }}

    .safety-text {{
        font-size: 0.75rem;
    }}

    textarea {{
        font-size: 0.8rem !important;
        padding: 0.7rem !important;
    }}

    .screenshot-preview img {{
        max-height: 280px !important;
    }}

    .footer {{
        padding: 1.2rem 0.8rem;
        margin-top: 1.2rem;
    }}

    .footer-title {{
        font-size: 1.2rem;
    }}

    .footer p {{
        font-size: 0.75rem;
    }}

}}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR - THEME TOGGLE
# ============================================================

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌙 Dark", use_container_width=True):
            st.session_state.theme = "dark"
            st.rerun()
    
    with col2:
        if st.button("☀️ Light", use_container_width=True):
            st.session_state.theme = "light"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    ### 📚 Quick Safety Tips
    
    ✅ **Always verify independently**
    - Check official websites/apps
    - Call official phone numbers
    - Never use numbers from messages
    
    🔒 **Protect Your Data**
    - Never share OTPs or passwords
    - Don't reveal personal info
    - Be suspicious of urgency
    
    🚨 **Red Flag Indicators**
    - Poor grammar/spelling
    - Urgent/threatening language
    - Unexpected payment requests
    - Shortened/suspicious links
    
    📞 **If Something Feels Wrong**
    - Stop and verify independently
    - Report to authorities
    - Block and warn others
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: var(--text-secondary); font-size: 0.8rem; line-height: 1.6;'>
    Made with ❤️ for Digital Safety
    
    ScamLab AI - Educational Initiative
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# HERO SECTION
# ============================================================

st.markdown(f"""
<div class="hero">

<div class="hero-badge">
🛡️ ADVANCED SECURITY ANALYSIS
</div>

<h1>ScamLab AI</h1>

<div class="hero-subtitle">
🔍 Intelligent Scam Detection & Threat Analysis
</div>

<div class="hero-description">
Advanced AI-powered analysis to detect suspicious messages, analyze screenshots, 
and identify potential security threats before they cause harm.
</div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Smart Message Analysis</div>
        <div class="feature-text">
            Detect suspicious language patterns, urgency tactics, threats, 
            payment requests and sophisticated scam indicators.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📸</div>
        <div class="feature-title">Screenshot Intelligence</div>
        <div class="feature-text">
            Extract text from suspicious screenshots using advanced OCR 
            technology and analyze the detected content instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">ML-Powered Detection</div>
        <div class="feature-text">
            Trained machine learning model combined with explainable 
            detection rules for comprehensive threat assessment.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MESSAGE SCANNER SECTION
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-heading">
    <span class="section-heading-icon">📩</span>
    Message Threat Scanner
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-description">
Paste a suspicious message and let ScamLab AI analyze it for potential threats and scam patterns.
</div>
""", unsafe_allow_html=True)

message = st.text_area(
    "Suspicious message",
    height=140,
    placeholder=(
        "Example:\n"
        "Congratulations! You have won ₹50,000! Click here immediately "
        "to claim your reward. Limited time offer!"
    ),
    label_visibility="collapsed"
)

scan_col1, scan_col2, scan_col3 = st.columns([2, 2, 3])

with scan_col1:
    scan_button = st.button("🔍 Scan Message", use_container_width=True, type="primary")

with scan_col2:
    clear_button = st.button("🔄 Clear", use_container_width=True)

if clear_button:
    st.session_state["message_text"] = ""
    st.rerun()

if scan_button:
    if message.strip():
        result = analyze_message(message)
        
        st.divider()
        
        st.markdown("""
        <div class="compact-heading">
            <span>🎯</span> Threat Assessment
        </div>
        """, unsafe_allow_html=True)
        
        # METRICS
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric("Risk Score", f"{result['score']}/100")
        
        with metric_col2:
            st.metric("Risk Level", result["risk_level"])
        
        with metric_col3:
            st.metric("Category", result["category"])
        
        # RISK METER
        st.markdown("""
        <div class="risk-card">
            <div class="risk-title">📊 Threat Risk Meter</div>
        </div>
        """, unsafe_allow_html=True)
        
        score = result["score"]
        
        if score >= 70:
            st.progress(score / 100, text=f"🚨 HIGH RISK: {score}/100")
            st.error(f"**HIGH RISK DETECTED** — This message shows strong scam indicators. Do not click any links or provide personal information.")
        elif score >= 40:
            st.progress(score / 100, text=f"⚠️ SUSPICIOUS: {score}/100")
            st.warning(f"**SUSPICIOUS CONTENT** — Proceed with caution. Verify independently before taking any action.")
        elif score >= 20:
            st.progress(score / 100, text=f"🔎 POTENTIALLY SUSPICIOUS: {score}/100")
            st.info(f"**POTENTIALLY SUSPICIOUS** — Some warning signs detected. Exercise caution.")
        else:
            st.progress(score / 100, text=f"✅ LOW RISK: {score}/100")
            st.success(f"**LOW RISK** — No major scam indicators detected, but always verify independently.")
        
        # ML ANALYSIS
        st.markdown("""
        <div class="ml-card">
            <div class="ml-title">🤖 Machine Learning Analysis</div>
            <div class="ml-text">The trained ML model independently evaluated this message using learned patterns from known scams.</div>
        </div>
        """, unsafe_allow_html=True)
        
        ml_col1, ml_col2 = st.columns(2)
        
        with ml_col1:
            st.metric("ML Prediction", result["ml_prediction"])
        
        with ml_col2:
            st.metric("Scam Probability", f"{result['ml_probability']:.1f}%")
        
        # WHY FLAGGED
        st.markdown("### 🔎 Why Was This Flagged?")
        
        if result["indicators"]:
            for indicator in result["indicators"]:
                st.markdown(f"""
                <div class="explanation-card">
                    ⚠️ {indicator}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No major scam indicators detected.")
        
        # RECOMMENDATION
        st.markdown("### 🛡️ Recommended Action")
        st.info(result["recommendation"])
    
    else:
        st.warning("⚠️ Please enter a message to scan.")

# ============================================================
# SCREENSHOT SCANNER SECTION
# ============================================================

st.divider()

st.markdown("""
<div class="section-heading">
    <span class="section-heading-icon">📸</span>
    Screenshot Threat Scanner
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-description">
Upload a screenshot of a suspicious SMS, email, notification or chat message for analysis.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload screenshot",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

if uploaded_file:
    image = Image.open(uploaded_file)
    
    st.markdown('<div class="screenshot-preview">', unsafe_allow_html=True)
    st.image(image, caption="Uploaded suspicious content", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    ocr_col1, ocr_col2, ocr_col3 = st.columns([2, 2, 3])
    
    with ocr_col1:
        if st.button("📝 Extract Text", use_container_width=True, type="primary"):
            with st.spinner("🔄 Extracting text..."):
                extracted_text = extract_text(image)
                st.session_state["extracted_text"] = extracted_text
                st.success("✅ Text extracted successfully!")

# ============================================================
# OCR RESULT SECTION
# ============================================================

if "extracted_text" in st.session_state:
    extracted_text = st.session_state["extracted_text"]
    
    st.divider()
    
    st.markdown("""
    <div class="section-heading">
        <span class="section-heading-icon">📝</span>
        OCR Intelligence
    </div>
    """, unsafe_allow_html=True)
    
    edited_text = st.text_area(
        "Extracted text (editable)",
        extracted_text,
        height=140,
        label_visibility="collapsed"
    )
    
    analyze_ocr_col1, analyze_ocr_col2, analyze_ocr_col3 = st.columns([2, 2, 3])
    
    with analyze_ocr_col1:
        if st.button("🛡️ Analyze Content", use_container_width=True, type="primary"):
            if edited_text.strip():
                with st.spinner("🔄 Analyzing..."):
                    result = analyze_message(edited_text)
                
                st.divider()
                
                st.markdown("""
                <div class="compact-heading">
                    <span>🎯</span> Screenshot Threat Assessment
                </div>
                """, unsafe_allow_html=True)
                
                score_col, risk_col, category_col = st.columns(3)
                
                with score_col:
                    st.metric("Risk Score", f"{result['score']}/100")
                
                with risk_col:
                    st.metric("Risk Level", result["risk_level"])
                
                with category_col:
                    st.metric("Category", result["category"])
                
                st.markdown("""
                <div class="risk-card">
                    <div class="risk-title">📊 Screenshot Threat Risk Meter</div>
                </div>
                """, unsafe_allow_html=True)
                
                score = result["score"]
                
                if score >= 70:
                    st.progress(score / 100, text=f"🚨 HIGH RISK: {score}/100")
                    st.error(f"**HIGH RISK DETECTED** — This screenshot contains strong scam indicators.")
                elif score >= 40:
                    st.progress(score / 100, text=f"⚠️ SUSPICIOUS: {score}/100")
                    st.warning(f"**SUSPICIOUS CONTENT** — Be cautious and verify independently.")
                elif score >= 20:
                    st.progress(score / 100, text=f"🔎 POTENTIALLY SUSPICIOUS: {score}/100")
                    st.info(f"**POTENTIALLY SUSPICIOUS** — Some warning signs present.")
                else:
                    st.progress(score / 100, text=f"✅ LOW RISK: {score}/100")
                    st.success(f"**LOW RISK** — Screenshot appears legitimate.")
                
                st.markdown("""
                <div class="ml-card">
                    <div class="ml-title">🤖 Machine Learning Analysis</div>
                    <div class="ml-text">The ML model evaluated the extracted text using advanced pattern recognition.</div>
                </div>
                """, unsafe_allow_html=True)
                
                ml_col1, ml_col2 = st.columns(2)
                
                with ml_col1:
                    st.metric("ML Prediction", result["ml_prediction"])
                
                with ml_col2:
                    st.metric("Scam Probability", f"{result['ml_probability']:.1f}%")
                
                st.markdown("### 🔎 Why Was This Flagged?")
                
                if result["indicators"]:
                    for indicator in result["indicators"]:
                        st.markdown(f"""
                        <div class="explanation-card">
                            ⚠️ {indicator}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ No major scam indicators detected.")
                
                st.markdown("### 🛡️ Recommended Action")
                st.info(result["recommendation"])
            
            else:
                st.warning("⚠️ No readable text was detected.")

# ============================================================
# SAFETY CENTER
# ============================================================

st.divider()

st.markdown("""
<div class="section-heading">
    <span class="section-heading-icon">🛡️</span>
    Scam Safety Center
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-description">
Essential security tips to help you recognize and avoid common scam tactics and fraud schemes.
</div>
""", unsafe_allow_html=True)

# Row 1
safety_col1, safety_col2, safety_col3 = st.columns(3)

with safety_col1:
    st.markdown("""
    <div class="safety-card">
        <div class="safety-icon">🔐</div>
        <div class="safety-title">Never Share OTPs</div>
        <div class="safety-text">
            Your OTP, PIN, or password is personal. Never share it with anyone, 
            even if they claim to be from your bank.
        </div>
    </div>
    """, unsafe_allow_html=True)

with safety_col2:
    st.markdown("""
    <div class="safety-card">
        <div class="safety-icon">🔗</div>
        <div class="safety-title">Verify Links First</div>
        <div class="safety-text">
            Don't click unexpected links. Open the official app or website directly 
            to verify any requests.
        </div>
    </div>
    """, unsafe_allow_html=True)

with safety_col3:
    st.markdown("""
    <div class="safety-card">
        <div class="safety-icon">💳</div>
        <div class="safety-title">Don't Rush Payments</div>
        <div class="safety-text">
            Urgency and threats are red flags. Take time to verify independently 
            before making any payments.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Row 2
safety_col4, safety_col5, safety_col6 = st.columns(3)

with safety_col4:
    st.markdown("""
    <div class="safety-card">
        <div class="safety-icon">📞</div>
        <div class="safety-title">Call Official Numbers</div>
        <div class="safety-text">
            Never use numbers from messages. Look up official customer service 
            numbers independently.
        </div>
    </div>
    """, unsafe_allow_html=True)

with safety_col5:
    st.markdown("""
    <div class="safety-card">
        <div class="safety-icon">👀</div>
        <div class="safety-title">Watch for Red Flags</div>
        <div class="safety-text">
            Poor grammar, spelling errors, and generic greetings are common 
            in phishing messages.
        </div>
    </div>
    """, unsafe_allow_html=True)

with safety_col6:
    st.markdown("""
    <div class="safety-card">
        <div class="safety-icon">🚨</div>
        <div class="safety-title">Report & Block</div>
        <div class="safety-text">
            Report scam messages to your provider. Block the sender and warn 
            people in your contact list.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown("""
<div class="footer">

<div class="footer-title">
🛡️ ScamLab AI
</div>

<p>
Think before you click. Verify before you act. Stay secure.
</p>

<p>
AI-powered educational initiative for digital scam awareness and cybersecurity literacy.
</p>

<p style='margin-top: 1rem; font-size: 0.75rem;'>
⚠️ Always verify through official channels. This tool is for educational purposes only.
</p>

</div>
""", unsafe_allow_html=True)
