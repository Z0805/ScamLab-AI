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
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99,102,241,0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(168,85,247,0.15),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(14,165,233,0.10),
            transparent 35%
        ),
        #080b14;

    color: #f8fafc;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 45px;
    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.96),
            rgba(15,23,42,0.96)
        );

    border: 1px solid rgba(129,140,248,0.35);

    box-shadow:
        0 0 45px rgba(99,102,241,0.16),
        inset 0 1px 0 rgba(255,255,255,0.06);

    margin-bottom: 28px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 30px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(129,140,248,0.35);
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: 52px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -2px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #a5b4fc,
            #c084fc
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 20px;
    color: #cbd5e1;
    margin-top: 12px;
}

.hero-description {
    font-size: 15px;
    color: #94a3b8;
    margin-top: 10px;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    min-height: 180px;
    padding: 25px;
    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.92),
            rgba(15,23,42,0.88)
        );

    border: 1px solid rgba(148,163,184,0.16);

    transition: all 0.25s ease;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.22);
}

.feature-card:hover {
    transform: translateY(-5px);

    border-color:
        rgba(129,140,248,0.55);

    box-shadow:
        0 15px 45px rgba(79,70,229,0.18);
}

.feature-icon {
    font-size: 34px;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}

.feature-text {
    font-size: 14px;
    line-height: 1.6;
    color: #94a3b8;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-heading {
    font-size: 27px;
    font-weight: 800;
    color: #f8fafc;
    margin-top: 15px;
    margin-bottom: 5px;
}

.section-description {
    color: #94a3b8;
    margin-bottom: 18px;
}

.compact-heading {
    font-size: 21px;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 10px;
    margin-bottom: 12px;
}


/* ============================================================
   TEXT AREA
   ============================================================ */

textarea {
    background-color:
        rgba(15,23,42,0.85) !important;

    color: #f8fafc !important;

    border:
        1px solid rgba(129,140,248,0.25)
        !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 12px;

    border:
        1px solid rgba(129,140,248,0.35);

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );

    color: white;
    font-weight: 700;
    padding: 10px 22px;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #c4b5fd;

    box-shadow:
        0 0 22px rgba(124,58,237,0.45);

    transform: translateY(-2px);
}


/* ============================================================
   METRICS
   ============================================================ */

[data-testid="stMetric"] {
    background:
        rgba(30,41,59,0.72);

    border:
        1px solid rgba(148,163,184,0.16);

    padding: 15px;
    border-radius: 18px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 12px !important;
}

[data-testid="stMetricValue"] {
    color: #a5b4fc !important;
    font-size: 22px !important;
}


/* ============================================================
   SCREENSHOT
   ============================================================ */

.screenshot-preview {
    display: flex;
    justify-content: center;
    margin: 10px 0 20px 0;
}

.screenshot-preview img {
    max-width: 420px !important;
    max-height: 500px !important;
    object-fit: contain;

    border-radius: 16px;

    border:
        1px solid rgba(129,140,248,0.25);

    box-shadow:
        0 10px 35px rgba(0,0,0,0.35);
}


/* ============================================================
   ML RESULT CARD
   ============================================================ */

.ml-card {
    padding: 22px;
    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            rgba(49,46,129,0.35),
            rgba(30,41,59,0.75)
        );

    border:
        1px solid rgba(129,140,248,0.35);

    margin-top: 15px;
    margin-bottom: 20px;
}

.ml-title {
    font-size: 18px;
    font-weight: 700;
    color: #c4b5fd;
    margin-bottom: 10px;
}

.ml-text {
    font-size: 15px;
    color: #cbd5e1;
    line-height: 1.7;
}


/* ============================================================
   NEW: RISK METER
   ============================================================ */

.risk-card {
    padding: 20px;
    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.82),
            rgba(15,23,42,0.75)
        );

    border:
        1px solid rgba(129,140,248,0.25);

    margin-top: 18px;
    margin-bottom: 18px;
}

.risk-title {
    font-size: 17px;
    font-weight: 700;
    color: #c4b5fd;
    margin-bottom: 10px;
}

.explanation-card {
    padding: 15px 18px;
    margin: 8px 0;

    border-radius: 14px;

    background: rgba(30,41,59,0.65);

    border-left:
        3px solid #818cf8;

    color: #cbd5e1;

    font-size: 14px;
}


/* ============================================================
   SAFETY CENTER
   ============================================================ */

.safety-card {
    min-height: 150px;

    padding: 22px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.85),
            rgba(15,23,42,0.80)
        );

    border:
        1px solid rgba(129,140,248,0.20);
}

.safety-icon {
    font-size: 30px;
    margin-bottom: 10px;
}

.safety-title {
    font-size: 17px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 7px;
}

.safety-text {
    font-size: 13px;
    line-height: 1.6;
    color: #94a3b8;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    padding: 35px;
    color: #64748b;
}

.footer-title {
    font-size: 20px;
    font-weight: 700;
    color: #a5b4fc;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-badge">
🛡️ DIGITAL SAFETY • AI SECURITY
</div>

<h1>ScamLab AI</h1>

<div class="hero-subtitle">
Intelligent Scam Detection & Digital Threat Analysis
</div>

<div class="hero-description">
Analyze suspicious messages and screenshots, identify scam
patterns, and understand the risks before taking action.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FEATURE CARDS
# ============================================================

card1, card2, card3 = st.columns(3)

with card1:
    st.markdown("""
    <div class="feature-card">

    <div class="feature-icon">🔍</div>

    <div class="feature-title">
    Smart Message Analysis
    </div>

    <div class="feature-text">
    Detect suspicious language, urgency, threats,
    payment requests and other scam indicators.
    </div>

    </div>
    """, unsafe_allow_html=True)


with card2:
    st.markdown("""
    <div class="feature-card">

    <div class="feature-icon">📸</div>

    <div class="feature-title">
    Screenshot Intelligence
    </div>

    <div class="feature-text">
    Extract text from suspicious screenshots using
    OCR technology and analyze the detected content.
    </div>

    </div>
    """, unsafe_allow_html=True)


with card3:
    st.markdown("""
    <div class="feature-card">

    <div class="feature-icon">🤖</div>

    <div class="feature-title">
    Machine Learning Detection
    </div>

    <div class="feature-text">
    Use a trained machine-learning model alongside
    explainable scam detection rules.
    </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MESSAGE SCANNER
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-heading">'
    '📩 Message Threat Scanner'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Paste a suspicious message and let ScamLab AI analyze it.'
    '</div>',
    unsafe_allow_html=True
)


message = st.text_area(
    "Suspicious message",
    height=170,
    placeholder=(
        "Example:\n"
        "Congratulations! You have won a prize. "
        "Click this link immediately to claim your reward."
    ),
    label_visibility="collapsed"
)


if st.button(
    "🔍  Scan Message for Threats",
    type="primary"
):

    if message.strip():

        result = analyze_message(message)

        st.divider()

        st.markdown(
            '<div class="compact-heading">'
            '🎯 Threat Assessment'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # MAIN RESULTS
        # ----------------------------------------------------

        score_col, risk_col, category_col = st.columns(3)


        with score_col:
            st.metric(
                "Rule-Based Risk Score",
                f"{result['score']}/100"
            )


        with risk_col:
            st.metric(
                "Risk Level",
                result["risk_level"]
            )


        with category_col:
            st.metric(
                "Detected Category",
                result["category"]
            )


        # ----------------------------------------------------
        # RISK METER
        # ----------------------------------------------------

        st.markdown("""
        <div class="risk-card">

        <div class="risk-title">
        📊 Threat Risk Meter
        </div>

        </div>
        """, unsafe_allow_html=True)

        score = result["score"]

        st.progress(score / 100)


        if score >= 70:

            st.error(
                f"🚨 HIGH RISK — Threat score: {score}/100"
            )

        elif score >= 40:

            st.warning(
                f"⚠️ SUSPICIOUS — Threat score: {score}/100"
            )

        elif score >= 20:

            st.info(
                f"🔎 POTENTIALLY SUSPICIOUS — Threat score: {score}/100"
            )

        else:

            st.success(
                f"✅ LOW RISK — Threat score: {score}/100"
            )


        # ----------------------------------------------------
        # MACHINE LEARNING RESULT
        # ----------------------------------------------------

        st.markdown("""
        <div class="ml-card">

        <div class="ml-title">
        🤖 Machine Learning Analysis
        </div>

        <div class="ml-text">
        The trained ML model independently evaluated the
        message using learned text patterns.
        </div>

        </div>
        """, unsafe_allow_html=True)


        ml_col1, ml_col2 = st.columns(2)


        with ml_col1:

            st.metric(
                "ML Prediction",
                result["ml_prediction"]
            )


        with ml_col2:

            st.metric(
                "ML Scam Probability",
                f"{result['ml_probability']:.2f}%"
            )


        # ----------------------------------------------------
        # WHY FLAGGED
        # ----------------------------------------------------

        st.markdown(
            "### 🔎 Why Was This Message Flagged?"
        )


        if result["indicators"]:

            for indicator in result["indicators"]:

                st.markdown(
                    f"""
                    <div class="explanation-card">
                    ⚠️ {indicator}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.success(
                "No major scam indicators detected."
            )


        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        st.markdown(
            "### 🛡️ Recommended Action"
        )

        st.info(
            result["recommendation"]
        )


    else:

        st.warning(
            "⚠️ Please enter a message to scan."
        )


# ============================================================
# SCREENSHOT SCANNER
# ============================================================

st.divider()

st.markdown(
    '<div class="section-heading">'
    '📸 Screenshot Threat Scanner'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Upload a screenshot of a suspicious SMS, email or notification.'
    '</div>',
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Upload screenshot",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)


if uploaded_file:

    image = Image.open(uploaded_file)


    st.markdown(
        '<div class="screenshot-preview">',
        unsafe_allow_html=True
    )


    st.image(
        image,
        caption="Uploaded suspicious content",
        width=420
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    if st.button(
        "📝  Extract Text with OCR"
    ):

        extracted_text = extract_text(image)

        st.session_state["extracted_text"] = extracted_text


# ============================================================
# OCR RESULT
# ============================================================

if "extracted_text" in st.session_state:

    extracted_text = st.session_state["extracted_text"]


    st.divider()


    st.markdown(
        '<div class="section-heading">'
        '📝 OCR Intelligence'
        '</div>',
        unsafe_allow_html=True
    )


    edited_text = st.text_area(
        "Extracted text",
        extracted_text,
        height=170
    )


    if st.button(
        "🛡️  Analyze Extracted Content",
        type="primary"
    ):

        if edited_text.strip():

            result = analyze_message(
                edited_text
            )


            st.divider()


            st.markdown(
                '<div class="compact-heading">'
                '🎯 Screenshot Threat Assessment'
                '</div>',
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # SCREENSHOT RESULTS
            # ------------------------------------------------

            score_col, risk_col, category_col = st.columns(3)


            with score_col:

                st.metric(
                    "Rule-Based Risk Score",
                    f"{result['score']}/100"
                )


            with risk_col:

                st.metric(
                    "Risk Level",
                    result["risk_level"]
                )


            with category_col:

                st.metric(
                    "Detected Category",
                    result["category"]
                )


            # ------------------------------------------------
            # RISK METER
            # ------------------------------------------------

            st.markdown("""
            <div class="risk-card">

            <div class="risk-title">
            📊 Screenshot Threat Risk Meter
            </div>

            </div>
            """, unsafe_allow_html=True)


            score = result["score"]

            st.progress(score / 100)


            if score >= 70:

                st.error(
                    f"🚨 HIGH RISK — Threat score: {score}/100"
                )

            elif score >= 40:

                st.warning(
                    f"⚠️ SUSPICIOUS — Threat score: {score}/100"
                )

            elif score >= 20:

                st.info(
                    f"🔎 POTENTIALLY SUSPICIOUS — Threat score: {score}/100"
                )

            else:

                st.success(
                    f"✅ LOW RISK — Threat score: {score}/100"
                )


            # ------------------------------------------------
            # ML RESULT
            # ------------------------------------------------

            st.markdown("""
            <div class="ml-card">

            <div class="ml-title">
            🤖 Machine Learning Analysis
            </div>

            <div class="ml-text">
            The trained ML model independently evaluated
            the OCR-extracted message.
            </div>

            </div>
            """, unsafe_allow_html=True)


            ml_col1, ml_col2 = st.columns(2)


            with ml_col1:

                st.metric(
                    "ML Prediction",
                    result["ml_prediction"]
                )


            with ml_col2:

                st.metric(
                    "ML Scam Probability",
                    f"{result['ml_probability']:.2f}%"
                )


            # ------------------------------------------------
            # WHY FLAGGED
            # ------------------------------------------------

            st.markdown(
                "### 🔎 Why Was This Screenshot Flagged?"
            )


            if result["indicators"]:

                for indicator in result["indicators"]:

                    st.markdown(
                        f"""
                        <div class="explanation-card">
                        ⚠️ {indicator}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.success(
                    "No major scam indicators detected."
                )


            # ------------------------------------------------
            # RECOMMENDATION
            # ------------------------------------------------

            st.markdown(
                "### 🛡️ Recommended Action"
            )


            st.info(
                result["recommendation"]
            )


        else:

            st.warning(
                "⚠️ No readable text was detected."
            )


# ============================================================
# SAFETY CENTER
# ============================================================

st.divider()

st.markdown(
    '<div class="section-heading">'
    '🛡️ Scam Safety Center'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Quick safety checks to help you recognize common scam tactics.'
    '</div>',
    unsafe_allow_html=True
)


safety1, safety2, safety3 = st.columns(3)


with safety1:

    st.markdown("""
    <div class="safety-card">

    <div class="safety-icon">🔐</div>

    <div class="safety-title">
    Never Share OTPs
    </div>

    <div class="safety-text">
    Never reveal your OTP, PIN or password to someone
    who contacts you unexpectedly.
    </div>

    </div>
    """, unsafe_allow_html=True)


with safety2:

    st.markdown("""
    <div class="safety-card">

    <div class="safety-icon">🔗</div>

    <div class="safety-title">
    Verify Links
    </div>

    <div class="safety-text">
    Avoid unexpected links. Open the official app or
    website yourself to verify important requests.
    </div>

    </div>
    """, unsafe_allow_html=True)


with safety3:

    st.markdown("""
    <div class="safety-card">

    <div class="safety-icon">💳</div>

    <div class="safety-title">
    Don't Rush Payments
    </div>

    <div class="safety-text">
    Urgency, threats and unexpected payment requests
    are important warning signs to investigate.
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
Detect suspicious patterns. Think before you click.
</p>

<p>
AI-powered educational project for digital scam awareness.
</p>

</div>
""", unsafe_allow_html=True)