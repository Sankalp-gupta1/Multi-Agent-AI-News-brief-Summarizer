import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import streamlit.components.v1 as components
from agents.publisher import generate_article
from datetime import datetime
import re

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Strategic Intelligence Terminal",
    page_icon="🤖",
    layout="wide"
)

# ---------------- DYNAMIC JET-BOT UI STYLING ---------------- #
st.markdown("""
<style>
    /* Global Theme */
    [data-testid="stAppViewContainer"] {
        background-color: #030508;
        color: #e0e6ed;
        overflow-x: hidden;
    }
    [data-testid="stSidebar"] {
        background-color: #080a0f;
        border-right: 1px solid #1e293b;
    }

    /* THE JET-HUMANOID ROBOTS (Patrolling the screen) */
    .jet-bot-asset {
        position: fixed;
        width: 300px;
        height: 400px;
        background: url('https://pngimg.com/d/robot_PNG93.png');
        background-size: contain;
        background-repeat: no-repeat;
        z-index: 999;
        pointer-events: none;
        filter: drop-shadow(0 0 30px #00d4ff);
    }

    .bot-alpha {
        top: 15%;
        animation: fly-patrol-top 22s linear infinite;
    }

    .bot-omega {
        bottom: 10%;
        transform: scaleX(-1);
        animation: fly-patrol-bottom 28s linear infinite;
    }

    @keyframes fly-patrol-top {
        0% { left: -350px; transform: translateY(0) rotate(5deg); }
        25% { transform: translateY(100px) rotate(-5deg); }
        50% { left: 50%; transform: translateY(0) rotate(5deg); }
        75% { transform: translateY(-100px) rotate(-5deg); }
        100% { left: 110%; transform: translateY(0) rotate(5deg); }
    }

    @keyframes fly-patrol-bottom {
        0% { right: -350px; transform: scaleX(-1) translateY(0); }
        50% { right: 50%; transform: scaleX(-1) translateY(-120px); }
        100% { right: 110%; transform: scaleX(-1) translateY(0); }
    }

    /* TERMINAL HEADER */
    .terminal-title-container {
        text-align: center;
        padding: 40px;
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(3,5,8,0) 80%);
        border: 1px solid #1e293b;
        border-radius: 20px;
        margin-bottom: 40px;
        position: relative;
        z-index: 1000;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.1);
    }

    /* CHOTA SIZE TEXT YAHA FIX KIYA HAI */
    .terminal-title-container h2 {
        font-size: 2.2rem;
        letter-spacing: 4px;
        font-weight: 700;
        color: #ffffff;
        text-transform: none;
        margin: 0;
        text-shadow: 0 0 20px #00d4ff;
        line-height: 1.4;
    }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff, #6366f1);
        color: white; font-weight: 800; border: none; border-radius: 5px; height: 3.8rem;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px #00d4ff; transform: translateY(-3px);
    }

    /* SIDEBAR ELEMENTS */
    .sidebar-pill {
        display: flex; align-items: center; background: #0f172a;
        padding: 12px; border-radius: 10px; border: 1px solid #00d4ff;
        margin-top: 25px; text-decoration: none !important;
    }
    .sidebar-pill img { width: 35px; height: 35px; border-radius: 50%; margin-right: 15px; border: 1px solid #fff; }
</style>

<div class="jet-bot-asset bot-alpha"></div>
<div class="jet-bot-asset bot-omega"></div>
""", unsafe_allow_html=True)

# ---------------- NEWSPAPER COMPONENT ---------------- #
def get_newspaper_html(text, img_url):
    clean_text = re.sub(r'\*\*|b>|//', '', text)
    lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
    title = lines[0] if lines else "INTELLIGENCE REPORT"
    body = lines[1:]
    mid = len(body) // 2

    def format_lines(items):
        res = ""
        for item in items:
            if len(item) < 55 or item.endswith(':'):
                res += f"<h4 style='font-family:\"Playfair Display\", serif; border-top: 2px solid #000; padding-top: 10px; margin-top: 25px; font-weight: 900;'>{item}</h4>"
            else:
                res += f"<p style='margin-bottom: 15px;'>{item}</p>"
        return res

    html = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <div id="capture-zone" style="background-color: #f4f1ea; color: #1a1a1a; padding: 60px; border: 1px solid #d1d1d1; font-family: 'Libre Baskerville', serif; width: 950px; margin: auto; box-shadow: 20px 20px 80px rgba(0,0,0,0.9); position: relative; z-index: 1001;">
        <div style="text-align: center; border-bottom: 5px solid #1a1a1a; padding-bottom: 15px; margin-bottom: 10px;">
            <h1 style="font-family: 'Playfair Display', serif; font-size: 5.5rem; font-weight: 900; margin: 0; letter-spacing: -3px; line-height: 0.9;">THE INTELLIGENCE TIMES</h1>
        </div>
        <div style="display: flex; justify-content: space-between; font-family: monospace; border-bottom: 2px solid #1a1a1a; padding: 10px 0; margin-bottom: 35px; font-weight: bold;">
            <span>VOL. CCXIX // NO. {datetime.now().strftime('%m%d')}</span>
            <span>PRICE: CLASSIFIED</span>
            <span>{datetime.now().strftime('%A, %B %d, %Y').upper()}</span>
        </div>
        <h2 style="font-family: 'Playfair Display', serif; font-size: 3.2rem; text-align: center; border-bottom: 1px solid #000; padding-bottom: 25px; margin-bottom: 30px; font-weight: 900; line-height: 1.1;">{title}</h2>
        <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 50px;">
            <div style="text-align: justify; font-size: 1.15rem; line-height: 1.8;">
                <img src='{img_url}' style='width:100%; border: 2px solid #000; margin-bottom: 30px; padding: 8px; background: #fff;'>
                {format_lines(body[:mid])}
            </div>
            <div style="text-align: justify; font-size: 1.15rem; line-height: 1.8; border-left: 1px solid #1a1a1a; padding-left: 30px;">
                {format_lines(body[mid:])}
                <div style='margin-top: 50px; border: 2px solid #000; padding: 20px; background: #fff;'>
                    <strong style='font-size: 0.9rem; text-transform: uppercase;'>Proprietary Analysis</strong>
                    <p style='font-size: 0.8rem; margin-top: 5px;'>Certified by Sankalp Gupta. Distribution restricted.</p>
                </div>
            </div>
        </div>
    </div>
    <div style="text-align: center; margin-top: 50px;">
        <button onclick="takeScreenshot()" style="background: #00d4ff; color: black; border: none; padding: 20px 50px; font-weight: 900; border-radius: 8px; cursor: pointer; font-size: 1.3rem; letter-spacing: 2px; box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);">📸 DOWNLOAD REPORT IMAGE (PNG)</button>
    </div>
    <script>
    function takeScreenshot() {{
        const target = document.getElementById('capture-zone');
        html2canvas(target, {{ scale: 2, useCORS: true, backgroundColor: "#f4f1ea" }}).then(canvas => {{
            const a = document.createElement('a');
            a.download = 'Intelligence_Times_{datetime.now().strftime('%Y%m%d')}.png';
            a.href = canvas.toDataURL('image/png');
            a.click();
        }});
    }}
    </script>
    """
    return html

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown("<h2 style='color:white;'>OPERATIONS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**Principal Operator:** Sankalp Gupta")
    st.markdown(f"""
        <a href="https://github.com/Sankalp-gupta1" class="sidebar-pill" target="_blank">
            <img src="https://github.com/Sankalp-gupta1.png">
            <span>Sankalp-gupta1 / Source</span>
        </a>
    """, unsafe_allow_html=True)
    if st.button("TERMINATE SESSION"):
        st.rerun()

# ---------------- MAIN UI ---------------- #
st.markdown("""
    <div class="terminal-title-container">
        <h2>Hi, we are AI Agents. We can generate a news report for you on any given topic today.</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("SUBJECT TARGET", placeholder="Define Intelligence Scope...")
    region = st.text_input("REGION SECTOR", placeholder="Location...")
with col2:
    tone = st.selectbox("FRAMEWORK", ["Detailed Analytical", "Executive Summary"])
    engine = st.selectbox("COMPUTE NODE", ["Groq Llama 3.1", "Claude 3.5 Sonnet", "Neural Link 3.1"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("EXECUTE DATA SYNTHESIS"):
    if not topic:
        st.error("Error: Target subject required.")
    else:
        with st.spinner("Synthesizing Daily Gazette..."):
            result = generate_article(topic=topic, tone=tone, city=region)
            article, img = result if isinstance(result, tuple) else (result, "")

        html_out = get_newspaper_html(article, img)
        components.html(html_out, height=1700, scrolling=True)

st.markdown("<br><div style='text-align:center; color:#334155; font-size:11px; letter-spacing:4px;'>STRICTLY INTERNAL // AUTHORIZED BY SANKALP GUPTA</div>", unsafe_allow_html=True)




# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# import streamlit.components.v1 as components
# from agents.publisher import generate_article
# from datetime import datetime
# import re

# # ---------------- PAGE CONFIG ---------------- #
# st.set_page_config(
#     page_title="Strategic Intelligence Terminal",
#     page_icon="🤖",
#     layout="wide"
# )

# # ---------------- DYNAMIC JET-BOT UI STYLING ---------------- #
# st.markdown("""
# <style>
#     /* Global Theme */
#     [data-testid="stAppViewContainer"] {
#         background-color: #030508;
#         color: #e0e6ed;
#         overflow-x: hidden;
#     }
#     [data-testid="stSidebar"] {
#         background-color: #080a0f;
#         border-right: 1px solid #1e293b;
#     }

#     /* THE JET-HUMANOID ROBOTS (Patrolling the screen) */
#     .jet-bot-asset {
#         position: fixed;
#         width: 300px;
#         height: 400px;
#         /* Using a high-quality humanoid robot asset with jet-flame feel */
#         background: url('https://pngimg.com/d/robot_PNG93.png');
#         background-size: contain;
#         background-repeat: no-repeat;
#         z-index: 999;
#         pointer-events: none;
#         filter: drop-shadow(0 0 30px #00d4ff);
#     }

#     /* Bot 1: Flying across the top */
#     .bot-alpha {
#         top: 15%;
#         animation: fly-patrol-top 22s linear infinite;
#     }

#     /* Bot 2: Flying across the bottom (Mirrored) */
#     .bot-omega {
#         bottom: 10%;
#         transform: scaleX(-1);
#         animation: fly-patrol-bottom 28s linear infinite;
#     }

#     @keyframes fly-patrol-top {
#         0% { left: -350px; transform: translateY(0) rotate(5deg); }
#         25% { transform: translateY(100px) rotate(-5deg); }
#         50% { left: 50%; transform: translateY(0) rotate(5deg); }
#         75% { transform: translateY(-100px) rotate(-5deg); }
#         100% { left: 110%; transform: translateY(0) rotate(5deg); }
#     }

#     @keyframes fly-patrol-bottom {
#         0% { right: -350px; transform: scaleX(-1) translateY(0); }
#         50% { right: 50%; transform: scaleX(-1) translateY(-120px); }
#         100% { right: 110%; transform: scaleX(-1) translateY(0); }
#     }

#     /* TERMINAL HEADER */
#     .terminal-title-container {
#         text-align: center;
#         padding: 60px;
#         background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(3,5,8,0) 80%);
#         border: 1px solid #1e293b;
#         border-radius: 20px;
#         margin-bottom: 50px;
#         position: relative;
#         z-index: 1000;
#         box-shadow: 0 0 40px rgba(0, 212, 255, 0.1);
#     }

#     .terminal-title-container h1 {
#         font-size: 3.5rem;
#         letter-spacing: 12px;
#         font-weight: 900;
#         color: #ffffff;
#         text-transform: uppercase;
#         margin: 0;
#         text-shadow: 0 0 25px #00d4ff;
#     }

#     /* BUTTONS */
#     .stButton>button {
#         background: linear-gradient(90deg, #00d4ff, #6366f1);
#         color: white; font-weight: 800; border: none; border-radius: 5px; height: 3.8rem;
#     }
#     .stButton>button:hover {
#         box-shadow: 0 0 30px #00d4ff; transform: translateY(-3px);
#     }

#     /* SIDEBAR ELEMENTS */
#     .sidebar-pill {
#         display: flex; align-items: center; background: #0f172a;
#         padding: 12px; border-radius: 10px; border: 1px solid #00d4ff;
#         margin-top: 25px; text-decoration: none !important;
#     }
#     .sidebar-pill img { width: 35px; height: 35px; border-radius: 50%; margin-right: 15px; border: 1px solid #fff; }
# </style>

# <div class="jet-bot-asset bot-alpha"></div>
# <div class="jet-bot-asset bot-omega"></div>
# """, unsafe_allow_html=True)

# # ---------------- NEWSPAPER COMPONENT ---------------- #
# def get_newspaper_html(text, img_url):
#     clean_text = re.sub(r'\*\*|b>|//', '', text)
#     lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
#     title = lines[0] if lines else "INTELLIGENCE REPORT"
#     body = lines[1:]
#     mid = len(body) // 2

#     def format_lines(items):
#         res = ""
#         for item in items:
#             if len(item) < 55 or item.endswith(':'):
#                 res += f"<h4 style='font-family:\"Playfair Display\", serif; border-top: 2px solid #000; padding-top: 10px; margin-top: 25px; font-weight: 900;'>{item}</h4>"
#             else:
#                 res += f"<p style='margin-bottom: 15px;'>{item}</p>"
#         return res

#     html = f"""
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
#     <div id="capture-zone" style="background-color: #f4f1ea; color: #1a1a1a; padding: 60px; border: 1px solid #d1d1d1; font-family: 'Libre Baskerville', serif; width: 950px; margin: auto; box-shadow: 20px 20px 80px rgba(0,0,0,0.9); position: relative; z-index: 1001;">
#         <div style="text-align: center; border-bottom: 5px solid #1a1a1a; padding-bottom: 15px; margin-bottom: 10px;">
#             <h1 style="font-family: 'Playfair Display', serif; font-size: 5.5rem; font-weight: 900; margin: 0; letter-spacing: -3px; line-height: 0.9;">THE INTELLIGENCE TIMES</h1>
#         </div>
#         <div style="display: flex; justify-content: space-between; font-family: monospace; border-bottom: 2px solid #1a1a1a; padding: 10px 0; margin-bottom: 35px; font-weight: bold;">
#             <span>VOL. CCXIX // NO. {datetime.now().strftime('%m%d')}</span>
#             <span>PRICE: CLASSIFIED</span>
#             <span>{datetime.now().strftime('%A, %B %d, %Y').upper()}</span>
#         </div>
#         <h2 style="font-family: 'Playfair Display', serif; font-size: 3.2rem; text-align: center; border-bottom: 1px solid #000; padding-bottom: 25px; margin-bottom: 30px; font-weight: 900; line-height: 1.1;">{title}</h2>
#         <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 50px;">
#             <div style="text-align: justify; font-size: 1.15rem; line-height: 1.8;">
#                 <img src='{img_url}' style='width:100%; border: 2px solid #000; margin-bottom: 30px; padding: 8px; background: #fff;'>
#                 {format_lines(body[:mid])}
#             </div>
#             <div style="text-align: justify; font-size: 1.15rem; line-height: 1.8; border-left: 1px solid #1a1a1a; padding-left: 30px;">
#                 {format_lines(body[mid:])}
#                 <div style='margin-top: 50px; border: 2px solid #000; padding: 20px; background: #fff;'>
#                     <strong style='font-size: 0.9rem; text-transform: uppercase;'>Proprietary Analysis</strong>
#                     <p style='font-size: 0.8rem; margin-top: 5px;'>Certified by Sankalp Gupta. Distribution restricted.</p>
#                 </div>
#             </div>
#         </div>
#     </div>
#     <div style="text-align: center; margin-top: 50px;">
#         <button onclick="takeScreenshot()" style="background: #00d4ff; color: black; border: none; padding: 20px 50px; font-weight: 900; border-radius: 8px; cursor: pointer; font-size: 1.3rem; letter-spacing: 2px; box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);">📸 DOWNLOAD REPORT IMAGE (PNG)</button>
#     </div>
#     <script>
#     function takeScreenshot() {{
#         const target = document.getElementById('capture-zone');
#         html2canvas(target, {{ scale: 2, useCORS: true, backgroundColor: "#f4f1ea" }}).then(canvas => {{
#             const a = document.createElement('a');
#             a.download = 'Intelligence_Times_{datetime.now().strftime('%Y%m%d')}.png';
#             a.href = canvas.toDataURL('image/png');
#             a.click();
#         }});
#     }}
#     </script>
#     """
#     return html

# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("<h2 style='color:white;'>OPERATIONS</h2>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.markdown(f"**Principal Operator:** Sankalp Gupta")
#     st.markdown(f"""
#         <a href="https://github.com/Sankalp-gupta1" class="sidebar-pill" target="_blank">
#             <img src="https://github.com/Sankalp-gupta1.png">
#             <span>Sankalp-gupta1 / Source</span>
#         </a>
#     """, unsafe_allow_html=True)
#     if st.button("TERMINATE SESSION"):
#         st.rerun()

# # ---------------- MAIN UI ---------------- #
# st.markdown("""
#     <div class="terminal-title-container">
#         <h1>Hi we are AI Agents We can Genrate for you a news report on your  given topic today</h1>
#     </div>
# """, unsafe_allow_html=True)

# col1, col2 = st.columns(2)
# with col1:
#     topic = st.text_input("SUBJECT TARGET", placeholder="Define Intelligence Scope...")
#     region = st.text_input("REGION SECTOR", placeholder="Location...")
# with col2:
#     tone = st.selectbox("FRAMEWORK", ["Detailed Analytical", "Executive Summary"])
#     engine = st.selectbox("COMPUTE NODE", ["Groq Llama 3.1", "Claude 3.5 Sonnet", "Neural Link 3.1"])

# st.markdown("<br>", unsafe_allow_html=True)

# if st.button("EXECUTE DATA SYNTHESIS"):
#     if not topic:
#         st.error("Error: Target subject required.")
#     else:
#         with st.spinner("Synthesizing Daily Gazette..."):
#             result = generate_article(topic=topic, tone=tone, city=region)
#             article, img = result if isinstance(result, tuple) else (result, "")

#         html_out = get_newspaper_html(article, img)
#         components.html(html_out, height=1700, scrolling=True)

# st.markdown("<br><div style='text-align:center; color:#334155; font-size:11px; letter-spacing:4px;'>STRICTLY INTERNAL // AUTHORIZED BY SANKALP GUPTA</div>", unsafe_allow_html=True)




# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# import streamlit.components.v1 as components
# from agents.publisher import generate_article
# from datetime import datetime
# import re
# import time

# # ---------------- PAGE CONFIG ---------------- #
# st.set_page_config(
#     page_title="Strategic Intelligence Terminal",
#     page_icon="🤖",
#     layout="wide"
# )

# # ---------------- HI-TECH FLYING HUMANOID ANIMATION ---------------- #
# st.markdown("""
# <style>
#     /* Main Theme */
#     [data-testid="stAppViewContainer"] {
#         background-color: #030508;
#         color: #e0e6ed;
#         overflow-x: hidden;
#     }
#     [data-testid="stSidebar"] {
#         background-color: #080a0f;
#         border-right: 1px solid #1e293b;
#     }

#     /* THE FLYING HUMANOID BOTS (Exactly as per your image) */
#     .jet-bot {
#         position: fixed;
#         width: 220px;
#         height: 320px;
#         /* Using the high-tech humanoid model with blue visor and jet effects */
#         background: url('https://pngimg.com/d/robot_PNG93.png');
#         background-size: contain;
#         background-repeat: no-repeat;
#         z-index: 1000;
#         pointer-events: none;
#         filter: drop-shadow(0 0 20px #00d4ff);
#     }

#     /* Robot 1: Patrolling across the top */
#     .bot-top {
#         top: 10%;
#         animation: bot-patrol-top 25s linear infinite;
#     }

#     /* Robot 2: Patrolling across the bottom (Mirrored) */
#     .bot-bottom {
#         bottom: 5%;
#         transform: scaleX(-1);
#         animation: bot-patrol-bottom 30s linear infinite;
#     }

#     @keyframes bot-patrol-top {
#         0% { left: -250px; transform: translateY(0) rotate(5deg); }
#         25% { transform: translateY(50px) rotate(-5deg); }
#         50% { left: 50%; transform: translateY(0px) rotate(5deg); }
#         75% { transform: translateY(-50px) rotate(-5deg); }
#         100% { left: 110%; transform: translateY(0) rotate(5deg); }
#     }

#     @keyframes bot-patrol-bottom {
#         0% { right: -250px; transform: scaleX(-1) translateY(0); }
#         50% { right: 50%; transform: scaleX(-1) translateY(-80px); }
#         100% { right: 110%; transform: scaleX(-1) translateY(0); }
#     }

#     /* Header Design */
#     .terminal-header {
#         text-align: center;
#         padding: 60px;
#         background: radial-gradient(circle, rgba(0,212,255,0.15) 0%, rgba(3,5,8,0) 70%);
#         border: 2px solid #1e293b;
#         border-radius: 20px;
#         margin-bottom: 50px;
#         position: relative;
#         z-index: 100;
#         box-shadow: 0 0 40px rgba(0,212,255,0.1);
#     }

#     .terminal-header h1 {
#         font-size: 3.5rem;
#         letter-spacing: 12px;
#         font-weight: 900;
#         color: #ffffff;
#         text-transform: uppercase;
#         margin: 0;
#         text-shadow: 0 0 15px #00d4ff;
#     }

#     /* GitHub Sidebar Pill */
#     .sidebar-pill {
#         display: flex; align-items: center; background: #0f172a;
#         padding: 12px; border-radius: 10px; border: 1px solid #00d4ff;
#         margin-top: 25px; text-decoration: none !important;
#     }
#     .sidebar-pill img { width: 35px; height: 35px; border-radius: 50%; margin-right: 15px; border: 1px solid #fff; }
#     .sidebar-pill span { color: white; font-size: 0.85rem; font-weight: bold; }

#     /* Action Button */
#     .stButton>button {
#         background: linear-gradient(90deg, #00d4ff, #6366f1);
#         color: white; font-weight: 800; border: none; border-radius: 0px; height: 3.8rem; transition: 0.4s;
#     }
#     .stButton>button:hover {
#         box-shadow: 0 0 35px #00d4ff; transform: scale(1.02);
#     }
# </style>

# <div class="jet-bot bot-top"></div>
# <div class="jet-bot bot-bottom"></div>
# """, unsafe_allow_html=True)

# # ---------------- NEWSPAPER RENDERING ---------------- #
# def get_newspaper_html(text, img_url):
#     clean_text = re.sub(r'\*\*|b>|//', '', text)
#     lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
#     title = lines[0] if lines else "INTELLIGENCE UPDATE"
#     body = lines[1:]
#     mid = len(body) // 2

#     def format_lines(items):
#         res = ""
#         for item in items:
#             if len(item) < 55 or item.endswith(':'):
#                 res += f"<h4 style='font-family:\"Playfair Display\", serif; border-top: 2px solid #000; padding-top: 10px; margin-top: 20px; font-weight: 900;'>{item}</h4>"
#             else:
#                 res += f"<p style='margin-bottom: 15px;'>{item}</p>"
#         return res

#     html = f"""
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
#     <div id="capture-zone" style="background-color: #f4f1ea; color: #1a1a1a; padding: 60px; border: 1px solid #d1d1d1; font-family: 'Libre Baskerville', serif; width: 950px; margin: auto; box-shadow: 20px 20px 80px rgba(0,0,0,0.9); position: relative; z-index: 1001;">
#         <div style="text-align: center; border-bottom: 5px solid #1a1a1a; padding-bottom: 15px; margin-bottom: 10px;">
#             <h1 style="font-family: 'Playfair Display', serif; font-size: 6rem; font-weight: 900; margin: 0; letter-spacing: -3px; line-height: 0.9;">THE INTELLIGENCE TIMES</h1>
#         </div>
#         <div style="display: flex; justify-content: space-between; font-family: monospace; border-bottom: 2px solid #1a1a1a; padding: 10px 0; margin-bottom: 35px; font-weight: bold; font-size: 0.9rem;">
#             <span>VOL. CCXIX // NO. {datetime.now().strftime('%m%d')}</span>
#             <span>PRICE: CLASSIFIED</span>
#             <span>{datetime.now().strftime('%A, %B %d, %Y').upper()}</span>
#         </div>
#         <h2 style="font-family: 'Playfair Display', serif; font-size: 3.2rem; text-align: center; border-bottom: 1px solid #000; padding-bottom: 20px; margin-bottom: 30px; line-height: 1.1; font-weight: 900;">{title}</h2>
#         <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 50px;">
#             <div style="text-align: justify; font-size: 1.15rem; line-height: 1.8;">
#                 <img src='{img_url}' style='width:100%; border: 2px solid #000; margin-bottom: 25px; padding: 8px; background: #fff;'>
#                 {format_lines(body[:mid])}
#             </div>
#             <div style="text-align: justify; font-size: 1.15rem; line-height: 1.8; border-left: 2px solid #1a1a1a; padding-left: 30px;">
#                 {format_lines(body[mid:])}
#                 <div style='margin-top: 50px; border: 2px solid #000; padding: 20px; background: #fff;'>
#                     <strong style='font-size: 0.9rem; text-transform: uppercase;'>Proprietary Analysis</strong>
#                     <p style='font-size: 0.8rem; margin-top: 5px;'>This document is classified under Executive Intelligence Protocol. Reproduction is prohibited.</p>
#                 </div>
#             </div>
#         </div>
#         <div style='text-align: center; border-top: 2px solid #1a1a1a; margin-top: 40px; font-weight: bold; padding-top: 20px;'>END OF EDITION</div>
#     </div>
#     <div style="text-align: center; margin-top: 40px;">
#         <button onclick="takeScreenshot()" style="background: #00d4ff; color: black; border: none; padding: 20px 50px; font-weight: 900; border-radius: 8px; cursor: pointer; font-size: 1.3rem; letter-spacing: 2px; box-shadow: 0 10px 25px rgba(0,212,255,0.4);">📸 DOWNLOAD FULL NEWSPAPER (PNG)</button>
#     </div>
#     <script>
#     function takeScreenshot() {{
#         const target = document.getElementById('capture-zone');
#         html2canvas(target, {{ scale: 2, useCORS: true, backgroundColor: "#f4f1ea" }}).then(canvas => {{
#             const a = document.createElement('a');
#             a.download = 'Intelligence_Times_{datetime.now().strftime('%Y%m%d')}.png';
#             a.href = canvas.toDataURL('image/png');
#             a.click();
#         }});
#     }}
#     </script>
#     """
#     return html

# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("<h2 style='color:white; letter-spacing:2px;'>OPERATIONS</h2>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.markdown(f"**Principal Operator:** Sankalp Gupta")
#     st.markdown(f"""
#         <a href="https://github.com/Sankalp-gupta1" class="sidebar-pill" target="_blank">
#             <img src="https://github.com/Sankalp-gupta1.png">
#             <span>Sankalp-gupta1 / Source</span>
#         </a>
#     """, unsafe_allow_html=True)
#     if st.button("TERMINATE SESSION"):
#         st.rerun()

# # ---------------- MAIN UI ---------------- #
# st.markdown("""
#     <div class="terminal-header">
#         <h1>STRATEGIC INTELLIGENCE TERMINAL</h1>
#     </div>
# """, unsafe_allow_html=True)

# c1, c2 = st.columns(2)
# with c1:
#     topic = st.text_input("SUBJECT TARGET", placeholder="Target Scope (e.g. AI Future)")
#     region = st.text_input("REGION", placeholder="Location...")
# with c2:
#     tone = st.selectbox("FRAMEWORK", ["Detailed Analytical", "Executive Summary"])
#     engine = st.selectbox("NODE", ["Groq Llama 3.1", "Claude 3.5 Sonnet", "Neural Link 3.1"])

# st.markdown("<br>", unsafe_allow_html=True)

# if st.button("EXECUTE DATA SYNTHESIS"):
#     if not topic:
#         st.error("Protocol Error: Subject target required.")
#     else:
#         with st.spinner("Agents Active... Processing Data..."):
#             result = generate_article(topic=topic, tone=tone, city=region)
#             article, img = result if isinstance(result, tuple) else (result, "")

#         html_out = get_newspaper_html(article, img)
#         components.html(html_out, height=1650, scrolling=True)

# st.markdown("<br><div style='text-align:center; color:#334155; font-size:11px; letter-spacing:4px;'>STRICTLY INTERNAL // AUTHORIZED BY SANKALP GUPTA</div>", unsafe_allow_html=True)















# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# import streamlit.components.v1 as components
# from agents.publisher import generate_article
# from datetime import datetime
# import re
# import time

# # ---------------- PAGE CONFIG ---------------- #
# st.set_page_config(
#     page_title="Strategic Intelligence Terminal",
#     page_icon="🤖",
#     layout="wide"
# )

# # ---------------- ADVANCED CYBERNETIC UI ---------------- #
# st.markdown("""
# <style>
#     /* Main App Background */
#     [data-testid="stAppViewContainer"] {
#         background-color: #030508;
#         color: #e0e6ed;
#         overflow-x: hidden;
#     }
#     [data-testid="stSidebar"] {
#         background-color: #080a0f;
#         border-right: 1px solid #1e293b;
#     }

#     /* THE FLYING HUMANOID ROBOTS */
#     .robo-agent {
#         position: fixed;
#         width: 180px;
#         height: 280px;
#         background: url('https://pngimg.com/d/robot_PNG93.png');
#         background-size: contain;
#         background-repeat: no-repeat;
#         z-index: 99;
#         pointer-events: none;
#         filter: drop-shadow(0 0 20px #00d4ff);
#     }

#     /* Robot 1: Flying across the screen */
#     .agent-left {
#         top: 20%;
#         animation: fly-across 20s linear infinite;
#     }

#     /* Robot 2: Fixed Guard on Right */
#     .agent-guard {
#         right: 5%;
#         top: 40%;
#         transform: scaleX(-1);
#         animation: hover-float 4s ease-in-out infinite;
#     }

#     @keyframes fly-across {
#         0% { left: -200px; transform: translateY(0px) rotate(10deg); }
#         50% { left: 50%; transform: translateY(-100px) rotate(-10deg); }
#         100% { left: 110%; transform: translateY(0px) rotate(10deg); }
#     }

#     @keyframes hover-float {
#         0%, 100% { transform: scaleX(-1) translateY(0); filter: drop-shadow(0 0 15px #00d4ff); }
#         50% { transform: scaleX(-1) translateY(-30px); filter: drop-shadow(0 0 35px #6366f1); }
#     }

#     /* HEADER DESIGN */
#     .cyber-header {
#         text-align: center;
#         padding: 50px;
#         background: linear-gradient(180deg, rgba(0,212,255,0.1) 0%, rgba(3,5,8,0) 100%);
#         border: 1px solid #1e293b;
#         border-radius: 20px;
#         margin-bottom: 40px;
#         position: relative;
#         z-index: 100;
#     }

#     .cyber-header h1 {
#         font-family: 'Inter', sans-serif;
#         font-size: 3.5rem;
#         letter-spacing: 10px;
#         font-weight: 900;
#         text-transform: uppercase;
#         color: #ffffff;
#         text-shadow: 0 0 15px #00d4ff;
#     }

#     /* GitHub Sidebar */
#     .sidebar-pill {
#         display: flex; align-items: center; background: #0f172a;
#         padding: 12px; border-radius: 10px; border: 1px solid #00d4ff;
#         margin-top: 25px; text-decoration: none !important;
#     }
#     .sidebar-pill img { width: 35px; height: 35px; border-radius: 50%; margin-right: 15px; border: 1px solid #fff; }
#     .sidebar-pill span { color: white; font-size: 0.85rem; font-weight: bold; }

#     /* Control Panel Buttons */
#     .stButton>button {
#         background: linear-gradient(90deg, #00d4ff, #6366f1);
#         color: white;
#         font-weight: 800;
#         border: none;
#         border-radius: 5px;
#         height: 3.5rem;
#         transition: 0.3s;
#     }
#     .stButton>button:hover {
#         box-shadow: 0 0 30px #00d4ff;
#         transform: scale(1.02);
#     }
# </style>

# <div class="robo-agent agent-left"></div>
# <div class="robo-agent agent-guard"></div>
# """, unsafe_allow_html=True)

# # ---------------- NEWSPAPER RENDERING ---------------- #
# def get_newspaper_html(text, img_url):
#     clean_text = re.sub(r'\*\*|b>|//', '', text)
#     lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
#     title = lines[0] if lines else "INTELLIGENCE UPDATE"
#     body = lines[1:]
#     mid = len(body) // 2

#     def format_lines(items):
#         res = ""
#         for item in items:
#             if len(item) < 50 or item.endswith(':'):
#                 res += f"<h4 style='font-family:\"Playfair Display\", serif; border-top: 2px solid #000; padding-top: 10px; margin-top: 20px;'>{item}</h4>"
#             else:
#                 res += f"<p style='margin-bottom: 15px;'>{item}</p>"
#         return res

#     html = f"""
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
#     <div id="capture-zone" style="background-color: #f4f1ea; color: #1a1a1a; padding: 60px; border: 1px solid #d1d1d1; font-family: 'Libre Baskerville', serif; width: 950px; margin: auto; box-shadow: 20px 20px 60px rgba(0,0,0,0.8);">
#         <div style="text-align: center; border-bottom: 5px solid #1a1a1a; padding-bottom: 10px;">
#             <h1 style="font-family: 'Playfair Display', serif; font-size: 5.5rem; font-weight: 900; margin: 0; letter-spacing: -3px;">THE INTELLIGENCE TIMES</h1>
#         </div>
#         <div style="display: flex; justify-content: space-between; font-family: monospace; border-bottom: 2px solid #1a1a1a; padding: 8px 0; margin-bottom: 30px; font-weight: bold;">
#             <span>VOL. CCXIX // NO. {datetime.now().strftime('%m%d')}</span>
#             <span>PRICE: CLASSIFIED</span>
#             <span>{datetime.now().strftime('%A, %B %d, %Y').upper()}</span>
#         </div>
#         <h2 style="font-family: 'Playfair Display', serif; font-size: 3rem; text-align: center; border-bottom: 1px solid #000; padding-bottom: 15px; margin-bottom: 25px;">{title}</h2>
#         <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 40px;">
#             <div style="text-align: justify; font-size: 1.1rem; line-height: 1.7;">
#                 <img src='{img_url}' style='width:100%; border: 2px solid #000; margin-bottom: 20px; padding: 5px; background: #fff;'>
#                 {format_lines(body[:mid])}
#             </div>
#             <div style="text-align: justify; font-size: 1.1rem; line-height: 1.7; border-left: 1px solid #1a1a1a; padding-left: 25px;">
#                 {format_lines(body[mid:])}
#                 <div style='margin-top: 40px; border: 2px solid #000; padding: 15px; background: #fff;'>
#                     <strong style='font-size: 0.8rem;'>PROPRIETARY ANALYSIS</strong>
#                     <p style='font-size: 0.75rem; margin: 0;'>Classified Executive Level. Reproduction is strictly prohibited.</p>
#                 </div>
#             </div>
#         </div>
#     </div>
#     <div style="text-align: center; margin-top: 30px;">
#         <button onclick="takeScreenshot()" style="background: #00d4ff; color: black; border: none; padding: 15px 40px; font-weight: bold; border-radius: 50px; cursor: pointer;">📷 DOWNLOAD NEWSPAPER AS PNG</button>
#     </div>
#     <script>
#     function takeScreenshot() {{
#         const target = document.getElementById('capture-zone');
#         html2canvas(target, {{ scale: 2, useCORS: true, backgroundColor: "#f4f1ea" }}).then(canvas => {{
#             const a = document.createElement('a');
#             a.download = 'Newspaper_{datetime.now().strftime('%Y%m%d')}.png';
#             a.href = canvas.toDataURL();
#             a.click();
#         }});
#     }}
#     </script>
#     """
#     return html

# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("<h2 style='color:white; letter-spacing:2px;'>OPERATIONS</h2>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.markdown(f"**Investigator:** Sankalp Gupta")
#     st.markdown(f"""
#         <a href="https://github.com/Sankalp-gupta1" class="sidebar-pill" target="_blank">
#             <img src="https://github.com/Sankalp-gupta1.png">
#             <span>Sankalp-gupta1 / Source</span>
#         </a>
#     """, unsafe_allow_html=True)
#     if st.button("TERMINATE SESSION"):
#         st.rerun()

# # ---------------- MAIN UI ---------------- #
# st.markdown("""
#     <div class="cyber-header">
#         <h1>STRATEGIC INTELLIGENCE TERMINAL</h1>
#     </div>
# """, unsafe_allow_html=True)

# c1, c2 = st.columns(2)
# with c1:
#     topic = st.text_input("SUBJECT TARGET", placeholder="Define Scope...")
#     region = st.text_input("REGION", placeholder="Global Sector...")
# with c2:
#     tone = st.selectbox("FRAMEWORK", ["Detailed Analytical", "Executive Summary"])
#     engine = st.selectbox("NODE", ["Groq Llama 3.1", "Claude 3.5 Sonnet"])

# if st.button("EXECUTE DATA SYNTHESIS"):
#     if not topic:
#         st.error("Error: Subject Required.")
#     else:
#         with st.spinner("Agents Active... Processing Data..."):
#             # Mocking result for demo
#             result = generate_article(topic=topic, tone=tone, city=region)
#             article, img = result if isinstance(result, tuple) else (result, "")

#         html_out = get_newspaper_html(article, img)
#         components.html(html_out, height=1500, scrolling=True)

# st.markdown("<br><div style='text-align:center; color:#334155; font-size:11px; letter-spacing:3px;'>ENCRYPTED SESSION // AUTHORIZED BY SANKALP GUPTA</div>", unsafe_allow_html=True)


