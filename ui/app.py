import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import streamlit.components.v1 as components
from agents.publisher import generate_article
from datetime import datetime
import re
import time

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="The Intelligence Times",
    page_icon="📰",
    layout="wide"
)

# ---------------- CONTROL PANEL STYLING ---------------- #
st.markdown("""
<style>
    /* Global Background & Terminal Style */
    [data-testid="stAppViewContainer"] {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* GitHub Sidebar Pill */
    .sidebar-pill {
        display: flex;
        align-items: center;
        background: #1c2128;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #38bdf8;
        margin-top: 20px;
        text-decoration: none !important;
        transition: 0.3s ease;
    }
    .sidebar-pill:hover {
        background: #38bdf8;
    }
    .sidebar-pill:hover span { color: #000; }
    .sidebar-pill img {
        width: 30px; height: 30px;
        border-radius: 50%; margin-right: 12px;
        border: 1px solid #fff;
    }
    .sidebar-pill span {
        color: white; font-size: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Terminal Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
    }

    /* Execution Button */
    .stButton>button {
        background-color: #ffffff;
        color: #000;
        font-weight: 800;
        border-radius: 0px;
        width: 100%;
        letter-spacing: 2px;
    }
    .stButton>button:hover {
        background-color: #38bdf8;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- NEWSPAPER HTML GENERATOR ---------------- #
def generate_newspaper_html(text, img_url):
    # Sanitize text: Remove artifacts
    clean_text = re.sub(r'\*\*|b>|//', '', text)
    lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
    
    title = lines[0] if lines else "INTELLIGENCE BRIEFING"
    body_parts = lines[1:]
    
    mid = len(body_parts) // 2
    left_content = body_parts[:mid]
    right_content = body_parts[mid:]

    def format_block(block_lines):
        html = ""
        for line in block_lines:
            if len(line) < 50 or line.endswith(':'):
                html += f"<span style='font-family: \"Playfair Display\", serif; font-size: 1.4rem; font-weight: 800; margin-top: 20px; margin-bottom: 5px; border-top: 2px solid #000; padding-top: 5px; display: block; color: #000;'>{line}</span>"
            else:
                html += f"<p style='margin-bottom: 15px;'>{line}</p>"
        return html

    # Main HTML with Image Download Script
    full_html = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    
    <div id="newspaper-capture" style="background-color: #f4f1ea; color: #1a1a1a; padding: 50px; border: 1px solid #d1d1d1; font-family: 'Libre Baskerville', serif; width: 900px; margin: auto; box-shadow: 10px 10px 40px rgba(0,0,0,0.5);">
        <div style="text-align: center; border-bottom: 5px solid #1a1a1a; margin-bottom: 5px; padding-bottom: 10px;">
            <h1 style="font-family: 'Playfair Display', serif; font-size: 5.5rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: -4px; color: #000; line-height: 1;">THE INTELLIGENCE TIMES</h1>
        </div>
        <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 0.85rem; border-bottom: 2px solid #1a1a1a; padding: 5px 0; margin-bottom: 30px; font-weight: bold;">
            <span>VOL. CCXVIII // NO. {datetime.now().strftime('%m%d')}</span>
            <span>PRICE: CLASSIFIED</span>
            <span>{datetime.now().strftime('%A, %B %d, %Y').upper()}</span>
        </div>
        
        <div style="font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; margin-bottom: 20px; color: #000; border-bottom: 1px solid #000; padding-bottom: 15px; text-align: center; line-height: 1.1;">{title}</div>
        
        <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 40px;">
            <div style="font-size: 1.1rem; line-height: 1.7; text-align: justify;">
                <img src='{img_url}' style='width:100%; border: 2px solid #000; margin-bottom: 20px; padding: 5px; background: #fff;'>
                {format_block(left_content)}
            </div>
            <div style="font-size: 1.1rem; line-height: 1.7; text-align: justify; border-left: 2px solid #1a1a1a; padding-left: 25px;">
                {format_block(right_content)}
                <div style='margin-top: 40px; border: 2px solid #000; padding: 15px; background: #fff;'>
                    <p style='font-size: 0.85rem; font-weight: bold; margin: 0 0 5px 0;'>PROPRIETARY ANALYSIS</p>
                    <p style='font-size: 0.75rem; margin: 0;'>Classified Executive Dissemination Level. Authorized access only. Reproduction is prohibited.</p>
                </div>
            </div>
        </div>
        <div style='text-align: center; border-top: 2px solid #1a1a1a; margin-top: 30px; font-weight: bold; font-size: 0.9rem; padding-top: 15px;'>END OF EDITION</div>
    </div>

    <div style="text-align: center; margin-top: 30px;">
        <button onclick="downloadAsImage()" style="background-color: #38bdf8; color: black; border: none; padding: 15px 30px; font-size: 1.2rem; font-weight: bold; cursor: pointer; border-radius: 5px; letter-spacing: 1px;">📷 DOWNLOAD REPORT AS IMAGE</button>
    </div>

    <script>
    function downloadAsImage() {{
        const element = document.getElementById('newspaper-capture');
        html2canvas(element, {{ 
            scale: 2,
            useCORS: true,
            backgroundColor: "#f4f1ea"
        }}).then(canvas => {{
            const link = document.createElement('a');
            link.download = 'Intelligence_Times_{datetime.now().strftime('%Y%m%d')}.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        }});
    }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Libre+Baskerville:wght@400;700&display=swap" rel="stylesheet">
    """
    return full_html

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown("<h2 style='color:white;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**Principal Operator:** Sankalp Gupta")
    
    # GitHub Link Sidebar
    st.markdown(f"""
        <a href="https://github.com/Sankalp-gupta1" class="sidebar-pill" target="_blank">
            <img src="https://github.com/Sankalp-gupta1.png">
            <span>Sankalp-gupta1 / Source</span>
        </a>
    """, unsafe_allow_html=True)
    
    if st.button("TERMINATE SESSION"):
        st.rerun()

# ---------------- MAIN UI ---------------- #
st.markdown("<h2 style='text-align:center; color:white; letter-spacing:4px; font-weight:800;'>STRATEGIC INTELLIGENCE TERMINAL</h2>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    topic = st.text_input("SUBJECT TARGET", placeholder="Define Scope (e.g. AI Ethics)")
    region = st.text_input("REGION", placeholder="Global, India, etc.")
with c2:
    tone = st.selectbox("FRAMEWORK", ["Detailed Analytical", "Executive Summary", "Strategic Review"])
    engine = st.selectbox("COMPUTE SOURCE", ["Groq Llama 3.1", "Claude 3.5 Sonnet", "Neural Link 3.1"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("EXECUTE DATA SYNTHESIS"):
    if not topic:
        st.error("Error: Target subject must be defined before execution.")
    else:
        with st.spinner("Synthesizing Daily Edition..."):
            result = generate_article(topic=topic, tone=tone, city=region)
            
            # Handling result
            if isinstance(result, tuple):
                article_text, img_url = result
            else:
                article_text, img_url = result, ""

        # Rendering via components.html for full control
        html_code = generate_newspaper_html(article_text, img_url)
        components.html(html_code, height=1400, scrolling=True)

st.markdown("<br><div style='text-align:center; color:#334155; font-size:10px; letter-spacing:2px;'>STRICTLY INTERNAL // ENCRYPTED SESSION // © 2026 SANKALP GUPTA</div>", unsafe_allow_html=True)




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
#     page_title="The Intelligence Times",
#     page_icon="📰",
#     layout="wide"
# )

# # ---------------- CONTROL PANEL STYLING ---------------- #
# st.markdown("""
# <style>
#     /* Control Panel Theme */
#     [data-testid="stAppViewContainer"] {
#         background-color: #0d1117;
#         color: #c9d1d9;
#         font-family: 'Inter', sans-serif;
#     }

#     [data-testid="stSidebar"] {
#         background-color: #161b22;
#         border-right: 1px solid #30363d;
#     }

#     /* GitHub Sidebar Pill */
#     .sidebar-pill {
#         display: flex;
#         align-items: center;
#         background: #1c2128;
#         padding: 10px;
#         border-radius: 8px;
#         border: 1px solid #38bdf8;
#         margin-top: 20px;
#         text-decoration: none !important;
#         transition: 0.3s ease;
#     }
#     .sidebar-pill:hover {
#         background: #38bdf8;
#     }
#     .sidebar-pill:hover span { color: #000; }
#     .sidebar-pill img {
#         width: 30px; height: 30px;
#         border-radius: 50%; margin-right: 12px;
#         border: 1px solid #fff;
#     }
#     .sidebar-pill span {
#         color: white; font-size: 0.8rem;
#         font-family: 'JetBrains Mono', monospace;
#     }

#     /* Terminal Inputs */
#     .stTextInput>div>div>input, .stSelectbox>div>div>select {
#         background-color: #0f172a !important;
#         color: #f8fafc !important;
#         border: 1px solid #1e293b !important;
#     }

#     /* Execution Button */
#     .stButton>button {
#         background-color: #ffffff;
#         color: #000;
#         font-weight: 800;
#         border-radius: 0px;
#         width: 100%;
#         letter-spacing: 2px;
#     }
#     .stButton>button:hover {
#         background-color: #38bdf8;
#         color: #fff;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- NEWSPAPER HTML GENERATOR ---------------- #
# def generate_newspaper_html(text, img_url):
#     # Cleaning artifacts (stars, stray tags)
#     clean_text = re.sub(r'\*\*|b>|//', '', text)
#     lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
    
#     title = lines[0] if lines else "INTELLIGENCE BRIEFING"
#     body_parts = lines[1:]
    
#     mid = len(body_parts) // 2
#     left_content = body_parts[:mid]
#     right_content = body_parts[mid:]

#     def format_block(block_lines):
#         html = ""
#         for line in block_lines:
#             if len(line) < 50 or line.endswith(':'):
#                 html += f"<span style='font-family: \"Playfair Display\", serif; font-size: 1.4rem; font-weight: 800; margin-top: 20px; margin-bottom: 5px; border-top: 2px solid #000; padding-top: 5px; display: block; color: #000;'>{line}</span>"
#             else:
#                 html += f"<p style='margin-bottom: 15px;'>{line}</p>"
#         return html

#     # Constructing the actual HTML for rendering
#     full_html = f"""
#     <div style="background-color: #f4f1ea; color: #1a1a1a; padding: 50px; border: 1px solid #d1d1d1; font-family: 'Libre Baskerville', serif; max-width: 1000px; margin: auto; box-shadow: 10px 10px 40px rgba(0,0,0,0.5);">
#         <div style="text-align: center; border-bottom: 5px solid #1a1a1a; margin-bottom: 5px; padding-bottom: 10px;">
#             <h1 style="font-family: 'Playfair Display', serif; font-size: 5.5rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: -4px; color: #000; line-height: 1;">THE INTELLIGENCE TIMES</h1>
#         </div>
#         <div style="display: flex; justify-content: space-between; font-family: monospace; font-size: 0.85rem; border-bottom: 2px solid #1a1a1a; padding: 5px 0; margin-bottom: 30px; font-weight: bold;">
#             <span>VOL. CCXVIII // NO. {datetime.now().strftime('%m%d')}</span>
#             <span>PRICE: CLASSIFIED</span>
#             <span>{datetime.now().strftime('%A, %B %d, %Y').upper()}</span>
#         </div>
        
#         <div style="font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; margin-bottom: 20px; color: #000; border-bottom: 1px solid #000; padding-bottom: 15px; text-align: center; line-height: 1.1;">{title}</div>
        
#         <div style="display: grid; grid-template-columns: 1.6fr 1fr; gap: 40px;">
#             <div style="font-size: 1.1rem; line-height: 1.7; text-align: justify;">
#                 <img src='{img_url}' style='width:100%; border: 1px solid #000; margin-bottom: 20px; padding: 5px; background: #fff;'>
#                 {format_block(left_content)}
#             </div>
#             <div style="font-size: 1.1rem; line-height: 1.7; text-align: justify; border-left: 2px solid #1a1a1a; padding-left: 25px;">
#                 {format_block(right_content)}
#                 <div style='margin-top: 40px; border: 2px solid #000; padding: 15px; background: #fff;'>
#                     <p style='font-size: 0.85rem; font-weight: bold; margin: 0 0 5px 0;'>PROPRIETARY ANALYSIS</p>
#                     <p style='font-size: 0.75rem; margin: 0;'>This document is classified as Executive Dissemination Level. Authorized access only. Reproduction is strictly prohibited.</p>
#                 </div>
#             </div>
#         </div>
#         <div style='text-align: center; border-top: 2px solid #1a1a1a; margin-top: 30px; font-weight: bold; font-size: 0.9rem; padding-top: 15px;'>END OF EDITION</div>
#     </div>
#     <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Libre+Baskerville:wght@400;700&display=swap" rel="stylesheet">
#     """
#     return full_html

# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("<h2 style='color:white;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.markdown(f"**Principal Operator:** Sankalp Gupta")
    
#     # GitHub Link Sidebar
#     st.markdown(f"""
#         <a href="https://github.com/Sankalp-gupta1" class="sidebar-pill" target="_blank">
#             <img src="https://github.com/Sankalp-gupta1.png">
#             <span>Sankalp-gupta1 / Source</span>
#         </a>
#     """, unsafe_allow_html=True)
    
#     if st.button("TERMINATE SESSION"):
#         st.rerun()

# # ---------------- MAIN UI ---------------- #
# st.markdown("<h2 style='text-align:center; color:white; letter-spacing:4px; font-weight:800;'>STRATEGIC INTELLIGENCE TERMINAL</h2>", unsafe_allow_html=True)

# c1, c2 = st.columns(2)
# with c1:
#     topic = st.text_input("SUBJECT TARGET", placeholder="Define Scope (e.g. AI Ethics)")
#     region = st.text_input("REGION", placeholder="Global, India, etc.")
# with c2:
#     tone = st.selectbox("FRAMEWORK", ["Detailed Analytical", "Executive Summary", "Strategic Review"])
#     engine = st.selectbox("COMPUTE SOURCE", ["Groq Llama 3.1", "Claude 3.5 Sonnet", "Neural Link 3.1"])

# st.markdown("<br>", unsafe_allow_html=True)

# if st.button("EXECUTE DATA SYNTHESIS"):
#     if not topic:
#         st.error("Error: Target subject must be defined before execution.")
#     else:
#         with st.spinner("Accessing nodes and synthesizing edition..."):
#             result = generate_article(topic=topic, tone=tone, city=region)
            
#             # Handling return types
#             if isinstance(result, tuple):
#                 article_text, img_url = result
#             else:
#                 article_text, img_url = result, ""

#         # Rendering the Newspaper Grid using IFrame components
#         newspaper_html = generate_newspaper_html(article_text, img_url)
#         components.html(newspaper_html, height=1500, scrolling=True)
        
#         st.download_button("DOWNLOAD REPORT", data=article_text, file_name=f"Gazette_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)

# st.markdown("<br><div style='text-align:center; color:#334155; font-size:10px; letter-spacing:2px;'>STRICTLY INTERNAL // ENCRYPTED SESSION // © 2026 SANKALP GUPTA</div>", unsafe_allow_html=True)


















# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from agents.publisher import generate_article
# from datetime import datetime
# import re
# import time

# # ---------------- PAGE CONFIG ---------------- #
# st.set_page_config(
#     page_title="Strategic Intelligence Gazette",
#     page_icon="📰",
#     layout="wide"
# )

# # ---------------- ULTIMATE NEWSPAPER UI ---------------- #
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400&display=swap');
    
#     /* Global Styling */
#     [data-testid="stAppViewContainer"] {
#         background-color: #0d1117;
#         color: #c9d1d9;
#         font-family: 'Inter', sans-serif;
#     }

#     [data-testid="stSidebar"] {
#         background-color: #161b22;
#         border-right: 1px solid #30363d;
#     }

#     /* GitHub Sidebar Pill - Fixed in Sidebar */
#     .sidebar-pill {
#         display: flex;
#         align-items: center;
#         background: #0d1117;
#         padding: 10px;
#         border-radius: 8px;
#         border: 1px solid #58a6ff;
#         margin-top: 20px;
#         text-decoration: none !important;
#     }
#     .sidebar-pill img {
#         width: 30px;
#         height: 30px;
#         border-radius: 50%;
#         margin-right: 10px;
#     }
#     .sidebar-pill span {
#         color: white;
#         font-size: 0.8rem;
#         font-family: 'JetBrains Mono', monospace;
#     }

#     /* NEWSPAPER SHEET */
#     .newspaper-sheet {
#         background-color: #f4f1ea; /* Authentic aged paper */
#         color: #1a1a1a;
#         padding: 60px;
#         border: 1px solid #d1d1d1;
#         box-shadow: 20px 20px 60px rgba(0,0,0,0.5);
#         max-width: 1100px;
#         margin: auto;
#     }

#     /* THE MASTHEAD (Top Banner) */
#     .masthead {
#         text-align: center;
#         border-bottom: 5px double #1a1a1a;
#         margin-bottom: 20px;
#         padding-bottom: 10px;
#     }
#     .masthead h1 {
#         font-family: 'Playfair Display', serif;
#         font-size: 4.5rem;
#         font-weight: 900;
#         margin: 0;
#         text-transform: uppercase;
#         color: #000;
#         letter-spacing: -2px;
#     }

#     /* Sub-header (Date, Edition) */
#     .sub-masthead {
#         display: flex;
#         justify-content: space-between;
#         font-family: 'Libre Baskerville', serif;
#         font-size: 0.85rem;
#         border-bottom: 2px solid #1a1a1a;
#         padding: 8px 0;
#         margin-bottom: 40px;
#         text-transform: uppercase;
#         font-weight: bold;
#     }

#     /* HEADLINE */
#     .headline {
#         font-family: 'Playfair Display', serif;
#         font-size: 3.5rem;
#         line-height: 1.0;
#         font-weight: 900;
#         text-align: center;
#         margin-bottom: 30px;
#         color: #000;
#         border-bottom: 1px solid #d1d1d1;
#         padding-bottom: 20px;
#     }

#     /* MULTI-COLUMN CONTENT */
#     .news-columns {
#         column-count: 2;
#         column-gap: 50px;
#         column-rule: 1px solid #1a1a1a; /* Divider line */
#         font-family: 'Libre Baskerville', serif;
#         text-align: justify;
#     }

#     .section-head {
#         font-family: 'Playfair Display', serif;
#         font-size: 1.8rem;
#         font-weight: 900;
#         margin-top: 25px;
#         margin-bottom: 15px;
#         color: #000;
#         text-decoration: underline;
#         text-decoration-thickness: 1px;
#     }

#     .article-text {
#         font-size: 1.15rem;
#         line-height: 1.7;
#         margin-bottom: 20px;
#         color: #222;
#     }

#     /* IMAGE STYLING */
#     .news-img-box {
#         border: 1px solid #1a1a1a;
#         padding: 8px;
#         background: #fff;
#         margin-bottom: 30px;
#     }

#     .dropcap {
#         float: left;
#         font-family: 'Playfair Display', serif;
#         font-size: 4.5rem;
#         line-height: 0.8;
#         padding-top: 4px;
#         padding-right: 8px;
#         padding-left: 3px;
#         color: #000;
#     }

# </style>
# """, unsafe_allow_html=True)

# # ---------------- FORMATTING ENGINE ---------------- #
# def render_newspaper_edition(text):
#     lines = text.split('\n')
#     formatted_html = ""
#     is_headline_set = False
#     is_first_para = True
    
#     for line in lines:
#         line = line.strip()
#         if not line: continue
        
#         # Heading Detection
#         if (line.startswith('**') and line.endswith('**')) or line.startswith('//'):
#             content = line.replace('**', '').replace('//', '').strip()
#             if not is_headline_set:
#                 formatted_html += f"<div class='headline'>{content}</div>"
#                 formatted_html += "<div class='news-columns'>" # Start multi-columns
#                 is_headline_set = True
#             else:
#                 formatted_html += f"<div class='section-head'>{content}</div>"
#         else:
#             # Inline bolding
#             line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            
#             # Add Dropcap to first paragraph
#             if is_headline_set and is_first_para:
#                 formatted_html += f"<p class='article-text'><span class='dropcap'>{line[0]}</span>{line[1:]}</p>"
#                 is_first_para = False
#             else:
#                 formatted_html += f"<p class='article-text'>{line}</p>"
            
#     if is_headline_set:
#         formatted_html += "</div>" # Close multi-columns
#     return formatted_html

# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("<h2 style='color:white; letter-spacing:2px;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.markdown(f"**Principal Operator:** Sankalp Gupta")
    
#     # GitHub Sidebar Pill
#     st.markdown(f"""
#         <a href="https://github.com/Sankalp-gupta1/Multi-Agent-AI-News-brief-Summarizer" class="sidebar-pill" target="_blank">
#             <img src="https://github.com/Sankalp-gupta1.png">
#             <span>Sankalp-gupta1 / Source</span>
#         </a>
#     """, unsafe_allow_html=True)
    
#     if st.button("RESET TERMINAL"):
#         st.rerun()

# # ---------------- UI CONTROLS ---------------- #
# st.markdown("<h2 style='text-align:center; color:white; font-weight:800; letter-spacing:4px;'>STRATEGIC INTELLIGENCE TERMINAL</h2>", unsafe_allow_html=True)

# col_a, col_b = st.columns(2)
# with col_a:
#     topic = st.text_input("PRIMARY SUBJECT", placeholder="Specify Intelligence Target...")
#     region = st.text_input("GEOGRAPHIC JURISDICTION", placeholder="City, Region, or Global...")
# with col_b:
#     tone = st.selectbox("FRAMEWORK", ["Detailed Analytical", "Executive Summary", "Strategic Review"])
#     engine = st.selectbox("PROCESSING NODE", ["Neural Link 3.1", "Groq Llama 3.1", "Claude 3.5 Sonnet"])

# if st.button("DEPLOY AGENTS & SYNTHESIZE"):
#     if not topic:
#         st.warning("Subject target required for deployment.")
#     else:
#         with st.spinner("Synthesizing Daily Gazette..."):
#             result = generate_article(topic=topic, tone=tone, city=region)
#             article = result[0] if isinstance(result, tuple) else result
#             img_url = result[1] if isinstance(result, tuple) else None

#         st.markdown("<hr style='border:1px solid #30363d'>", unsafe_allow_html=True)
        
#         # --- THE OFFICIAL GAZETTE RENDERING ---
#         st.markdown(f"""
#         <div class='newspaper-sheet'>
#             <div class='masthead'>
#                 <h1>The Intelligence Times</h1>
#             </div>
#             <div class='sub-masthead'>
#                 <span>VOL. CCXVII ... NO. {datetime.now().strftime('%m%d')}</span>
#                 <span>GLOBAL EDITION - PRICE: CLASSIFIED</span>
#                 <span>{datetime.now().strftime('%A, %B %d, %Y').upper()}</span>
#             </div>
#             {f"<div class='news-img-box'><img src='{img_url}' style='width:100%'></div>" if img_url else ""}
#             {render_newspaper_edition(article)}
#             <div style='text-align:center; border-top: 1px solid #1a1a1a; margin-top:30px; padding-top:10px; font-weight:900;'>*** END OF INTELLIGENCE BRIEF ***</div>
#         </div>
#         """, unsafe_allow_html=True)

#         st.download_button("DOWNLOAD OFFICIAL GAZETTE (TXT)", data=article, file_name=f"Intelligence_Times_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)

# st.markdown("<br><div style='text-align:center; color:#334155; font-size:10px; letter-spacing:2px;'>FOR OFFICIAL USE ONLY // ENCRYPTED LINK // SANKALP GUPTA SYSTEMS</div>", unsafe_allow_html=True)










# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from agents.publisher import generate_article
# from datetime import datetime
# import re
# import time

# # ---------------- PAGE CONFIG ---------------- #
# st.set_page_config(
#     page_title="Global Intelligence Terminal",
#     page_icon="📡",
#     layout="wide"
# )

# # ---------------- ELITE MONOCHROME UI ---------------- #
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
#     [data-testid="stAppViewContainer"] {
#         background-color: #030507;
#         color: #94a3b8;
#         font-family: 'Inter', sans-serif;
#     }

#     [data-testid="stSidebar"] {
#         background-color: #080a0c;
#         border-right: 1px solid #1e293b;
#     }

#     .terminal-header {
#         border-bottom: 1px solid #1e293b;
#         padding: 30px 0;
#         margin-bottom: 40px;
#         text-align: center;
#     }
#     .main-title {
#         font-size: 1.8rem;
#         font-weight: 800;
#         letter-spacing: 4px;
#         color: #ffffff;
#         text-transform: uppercase;
#     }

#     .stTextInput>div>div>input, .stSelectbox>div>div>select {
#         background-color: #0f172a !important;
#         color: #f8fafc !important;
#         border: 1px solid #1e293b !important;
#         border-radius: 2px !important;
#         font-family: 'JetBrains Mono', monospace;
#     }

#     .stButton>button {
#         background-color: #f8fafc;
#         color: #020617;
#         border-radius: 0px;
#         font-weight: 800;
#         border: none;
#         padding: 1rem;
#         width: 100%;
#         letter-spacing: 2px;
#         transition: 0.3s all;
#     }
#     .stButton>button:hover {
#         background-color: #38bdf8;
#         color: #ffffff;
#         box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
#     }

#     /* GitHub Link in Sidebar */
#     .sidebar-github {
#         display: flex;
#         align-items: center;
#         background: rgba(15, 23, 42, 0.9);
#         padding: 10px;
#         border-radius: 5px;
#         border: 1px solid #38bdf8;
#         text-decoration: none !important;
#         margin-top: 20px;
#     }
#     .sidebar-github img {
#         width: 30px;
#         height: 30px;
#         border-radius: 50%;
#         margin-right: 10px;
#     }
#     .sidebar-github span {
#         color: #fff;
#         font-size: 0.7rem;
#         font-family: 'JetBrains Mono', monospace;
#     }

#     .agent-log {
#         background: #080a0c;
#         border-left: 2px solid #38bdf8;
#         padding: 10px 15px;
#         font-family: 'JetBrains Mono', monospace;
#         font-size: 0.8rem;
#         color: #10b981;
#         margin-bottom: 10px;
#     }

#     .intel-wrapper {
#         background-color: #080a0c;
#         padding: 60px;
#         border: 1px solid #1e293b;
#         margin-top: 20px;
#     }
    
#     .meta-bar {
#         font-family: 'JetBrains Mono', monospace;
#         font-size: 0.7rem;
#         color: #38bdf8;
#         display: flex;
#         justify-content: space-between;
#         margin-bottom: 40px;
#         text-transform: uppercase;
#         border-bottom: 1px solid #1e293b;
#         padding-bottom: 10px;
#     }

#     /* Updated Heading Style to match Market & Financial Analysis */
#     .report-title, .section-label {
#         color: #ffffff;
#         font-size: 2rem;
#         font-weight: 800;
#         margin-bottom: 25px;
#         margin-top: 40px;
#         line-height: 1.2;
#     }

#     .report-text {
#         font-size: 1.15rem;
#         line-height: 2;
#         color: #cbd5e1;
#         margin-bottom: 25px;
#     }

#     .bold-text {
#         color: #f8fafc;
#         font-weight: 600;
#     }

#     .stImage {
#         border: 1px solid #1e293b;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- FORMATTING ENGINE ---------------- #
# def render_intel_content(text):
#     lines = text.split('\n')
#     html_output = ""
#     for line in lines:
#         line = line.strip()
#         if not line: continue
        
#         # Sabhi headings ko ek hi style mein convert karne ke liye
#         if (line.startswith('**') and line.endswith('**')) or line.startswith('//'):
#             content = line.replace('**', '').replace('//', '').strip()
#             html_output += f"<div class='section-label'>{content}</div>"
#         else:
#             line = re.sub(r'\*\*(.*?)\*\*', r'<span class="bold-text">\1</span>', line)
#             html_output += f"<p class='report-text'>{line}</p>"
#     return html_output

# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("<h3 style='color:white; letter-spacing:2px;'>OPERATIONS</h3>", unsafe_allow_html=True)
#     st.markdown("---")
#     st.markdown(f"**Investigator:** Sankalp Gupta")
#     st.markdown("**Status:** System Ready")
#     st.markdown("**Grid:** Sector 7-G")
    
#     if st.button("TERMINATE SESSION"):
#         st.rerun()
    
#     # GitHub Link moved inside Sidebar
#     st.markdown(f"""
#         <div style="margin-top: 50px;">
#             <a href="https://github.com/Sankalp-gupta1/Multi-Agent-AI-News-brief-Summarizer" class="sidebar-github" target="_blank">
#                 <img src="https://github.com/Sankalp-gupta1.png">
#                 <span>Sankalp-gupta1 / Source</span>
#             </a>
#         </div>
#     """, unsafe_allow_html=True)

# # ---------------- HEADER ---------------- #
# st.markdown("""
# <div class='terminal-header'>
#     <div class='main-title'>Strategic Intelligence Terminal</div>
# </div>
# """, unsafe_allow_html=True)

# # ---------------- CONTROL PANEL ---------------- #
# c1, c2 = st.columns(2)
# with c1:
#     topic = st.text_input("SUBJECT TARGET", placeholder="Target Keyword...")
#     region = st.text_input("GEOGRAPHICAL SECTOR", placeholder="Region...")
# with c2:
#     tone = st.selectbox("ANALYTICAL DEPTH", ["Executive Summary", "Deep Analytical", "Policy Review"])
#     engine = st.selectbox("COMPUTE SOURCE", ["Groq Llama 3.1", "Claude 3.5 Sonnet", "GPT-4o Agentic"])

# st.markdown("<br>", unsafe_allow_html=True)

# if st.button("EXECUTE DATA SYNTHESIS"):
#     if not topic:
#         st.error("Protocol Violation: Target Subject Required.")
#     else:
#         log_placeholder = st.empty()
#         logs = ["Initializing Agentic Swarm...", "Accessing Global News Nodes...", "Deploying Robotics Analysis Engine...", "Synthesizing Brief..."]
#         for log in logs:
#             log_placeholder.markdown(f"<div class='agent-log'>> {log}</div>", unsafe_allow_html=True)
#             time.sleep(0.5)
            
#         try:
#             with st.spinner("Processing High-Fidelity Data..."):
#                 result = generate_article(topic=topic, tone=tone, city=region)
#                 if isinstance(result, (tuple, list)):
#                     article_content, img_src = result[0], result[1] if len(result) > 1 else None
#                 else:
#                     article_content, img_src = result, None

#             st.markdown("---")
#             if img_src:
#                 st.image(img_src, use_container_width=True)
            
#             st.markdown(f"""
#             <div class='intel-wrapper'>
#                 <div class='meta-bar'>
#                     <span>ID: {datetime.now().strftime('%d%m%H%M')}</span>
#                     <span>LEVEL: CLASSIFIED</span>
#                     <span>LOC: {region.upper() if region else 'GLOBAL'}</span>
#                 </div>
#                 {render_intel_content(article_content)}
#             </div>
#             """, unsafe_allow_html=True)

#             st.download_button("DOWNLOAD DATA PACKET", data=article_content, file_name="Intel_Log.txt", use_container_width=True)

#         except Exception as e:
#             st.error(f"System Critical Error: {str(e)}")

# st.markdown("<br><div style='text-align:center; color:#334155; font-size:10px; letter-spacing:3px;'>INTERNAL USE ONLY • ENCRYPTED CONNECTION</div>", unsafe_allow_html=True)






 


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from agents.publisher import generate_article
# from datetime import datetime

# # ---------------- PAGE CONFIG ---------------- #
# st.set_page_config(
#     page_title="AI Global Intelligence Brief",
#     page_icon="🌍",
#     layout="wide"
# )

# # ---------------- PREMIUM CSS ---------------- #
# st.markdown("""
# <style>
# /* Overall background & text color */
# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #0f172a, #1e293b);
#     color: #f1f5f9;
#     font-family: 'Segoe UI', sans-serif;
# }

# /* Sidebar */
# .css-1d391kg {padding-top: 2rem;} /* default padding override */
# [data-testid="stSidebar"] {
#     background: rgba(15,23,42,0.95);
#     color: #f1f5f9;
#     font-weight: 600;
# }

# /* Sidebar links */
# .stSidebar .stButton>button {
#     background: linear-gradient(90deg, #6366f1, #8b5cf6);
#     color: white;
#     border-radius: 20px;
#     height: 2.5rem;
#     font-size: 14px;
#     font-weight: 600;
#     margin-bottom: 0.5rem;
#     border: none;
# }

# /* Padding for content */
# .block-container {
#     padding-top: 2rem;
#     padding-left: 3rem;
#     padding-right: 3rem;
# }

# /* Buttons */
# .stButton>button {
#     background: linear-gradient(90deg, #6366f1, #8b5cf6);
#     color: white;
#     border-radius: 30px;
#     height: 3rem;
#     font-size: 16px;
#     font-weight: 600;
#     border: none;
#     transition: transform 0.2s;
# }
# .stButton>button:hover {
#     transform: scale(1.05);
# }

# /* Report Card */
# .report-card {
#     background: rgba(255,255,255,0.05);
#     padding: 2rem 2.5rem;
#     border-radius: 25px;
#     backdrop-filter: blur(15px);
#     border: 1px solid rgba(255,255,255,0.2);
#     margin-top: 20px;
# }

# /* Headings inside report */
# .report-card h2, .report-card h3, .report-card h4 {
#     color: #facc15;
#     font-weight: 800;
#     margin-top: 1.5rem;
# }

# /* Paragraph content */
# .report-card p, .report-card span {
#     font-size: 16px;
#     line-height: 1.8;
#     color: #e5e7eb;
# }

# /* Horizontal rule styling */
# hr {
#     border: 0;
#     height: 1px;
#     background: rgba(255,255,255,0.2);
#     margin: 1.5rem 0;
# }

# /* Right corner footer */
# .footer-right {
#     position: fixed;
#     right: 20px;
#     bottom: 20px;
#     font-size: 14px;
#     color: #94a3b8;
# }
# .footer-right a {
#     color: #fbbf24;
#     text-decoration: none;
#     font-weight: bold;
# }
# .footer-right a:hover {
#     text-decoration: underline;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ---------------- #
# st.sidebar.markdown("<h2 style='color:#fbbf24'>🌍 AI Global Brief</h2>", unsafe_allow_html=True)
# st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# refresh_image = st.sidebar.button("🔄 Refresh Image")
# st.sidebar.markdown("<hr>", unsafe_allow_html=True)
# st.sidebar.markdown("Made by Sankalp Gupta • [GitHub](https://github.com/Sankalp-gupta1)", unsafe_allow_html=True)

# # ---------------- HEADER ---------------- #
# st.markdown("""
# <h1 style='text-align:center; font-size:3rem; font-weight:900; color:#fbbf24;'>🌍 AI Global Intelligence Brief</h1>
# <p style='text-align:center; font-size:1.2rem; color:#94a3b8; font-style:italic;'>
# Ultra Strict Factual Intelligence Engine
# </p>
# """, unsafe_allow_html=True)

# st.markdown("<hr>", unsafe_allow_html=True)

# # ---------------- INPUT SECTION ---------------- #
# st.markdown("### 📝 Enter Intelligence Parameters")

# topic = st.text_input(
#     "Enter Topic:",
#     placeholder="e.g. Delhi Pollution Crisis"
# )

# tone = st.selectbox(
#     "Select Tone:",
#     ["Formal", "Analytical"]
# )

# region = st.text_input(
#     "Enter Region / City / Country:",
#     placeholder="e.g. Tokyo, London, California, Brazil"
# )

# st.markdown("<hr>", unsafe_allow_html=True)

# # ---------------- GENERATE BUTTON ---------------- #
# if st.button("🚀 Generate Ultra Strict Report", use_container_width=True):

#     if not topic:
#         st.warning("Please enter a topic before generating report.")
#         st.stop()

#     # -------- Metrics -------- #
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Mode", "Ultra Strict")
#     with col2:
#         st.metric("Model", "Groq Llama 3.1")
#     with col3:
#         st.metric("Generated At", datetime.now().strftime("%H:%M"))

#     st.markdown("<hr>", unsafe_allow_html=True)

#     # -------- AI Generation -------- #
#     try:
#         with st.spinner("Generating factual intelligence report..."):
#             result = generate_article(
#                 topic=topic,
#                 tone=tone,
#                 city=region
#             )

#         if isinstance(result, tuple):
#             article, image_url = result
#         else:
#             article = result
#             image_url = None

#         if not article:
#             st.error("AI returned empty response.")
#             st.stop()

#     except Exception as e:
#         st.error(f"Error generating report: {e}")
#         st.stop()

#     # -------- Image -------- #
#     if image_url:
#         st.image(image_url, use_container_width=True)

#     # -------- Report Output -------- #
#     st.markdown("<div class='report-card'>", unsafe_allow_html=True)
#     st.markdown("<h2>📑 Executive Intelligence Summary</h2>", unsafe_allow_html=True)
    
#     for paragraph in article.split("\n\n"):
#         st.markdown(f"<p>{paragraph}</p>", unsafe_allow_html=True)
    
#     st.markdown("</div>", unsafe_allow_html=True)

#     # -------- Download -------- #
#     st.download_button(
#         "⬇ Download Report",
#         data=article,
#         file_name="Ultra_Strict_Intelligence_Report.txt",
#         mime="text/plain",
#         use_container_width=True
#     )

# st.markdown("<hr>", unsafe_allow_html=True)

# # ---------------- FOOTER ---------------- #
# st.markdown("""
# <div class="footer-right">
# Made by <a href="https://github.com/Sankalp-gupta1" target="_blank">Sankalp Gupta</a>
# </div>
# """, unsafe_allow_html=True)

# st.caption("AI Global Intelligence Engine • Ultra Strict Mode • 2026")

