import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agents.publisher import generate_article
from datetime import datetime

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Global Intelligence Brief",
    page_icon="🌍",
    layout="wide"
)

# ---------------- PREMIUM CSS ---------------- #
st.markdown("""
<style>
/* Overall background & text color */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #f1f5f9;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
.css-1d391kg {padding-top: 2rem;} /* default padding override */
[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.95);
    color: #f1f5f9;
    font-weight: 600;
}

/* Sidebar links */
.stSidebar .stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 20px;
    height: 2.5rem;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 0.5rem;
    border: none;
}

/* Padding for content */
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 30px;
    height: 3rem;
    font-size: 16px;
    font-weight: 600;
    border: none;
    transition: transform 0.2s;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Report Card */
.report-card {
    background: rgba(255,255,255,0.05);
    padding: 2rem 2.5rem;
    border-radius: 25px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.2);
    margin-top: 20px;
}

/* Headings inside report */
.report-card h2, .report-card h3, .report-card h4 {
    color: #facc15;
    font-weight: 800;
    margin-top: 1.5rem;
}

/* Paragraph content */
.report-card p, .report-card span {
    font-size: 16px;
    line-height: 1.8;
    color: #e5e7eb;
}

/* Horizontal rule styling */
hr {
    border: 0;
    height: 1px;
    background: rgba(255,255,255,0.2);
    margin: 1.5rem 0;
}

/* Right corner footer */
.footer-right {
    position: fixed;
    right: 20px;
    bottom: 20px;
    font-size: 14px;
    color: #94a3b8;
}
.footer-right a {
    color: #fbbf24;
    text-decoration: none;
    font-weight: bold;
}
.footer-right a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.markdown("<h2 style='color:#fbbf24'>🌍 AI Global Brief</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

refresh_image = st.sidebar.button("🔄 Refresh Image")
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("Made by Sankalp Gupta • [GitHub](https://github.com/Sankalp-gupta1)", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown("""
<h1 style='text-align:center; font-size:3rem; font-weight:900; color:#fbbf24;'>🌍 AI Global Intelligence Brief</h1>
<p style='text-align:center; font-size:1.2rem; color:#94a3b8; font-style:italic;'>
Ultra Strict Factual Intelligence Engine
</p>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- INPUT SECTION ---------------- #
st.markdown("### 📝 Enter Intelligence Parameters")

topic = st.text_input(
    "Enter Topic:",
    placeholder="e.g. Delhi Pollution Crisis"
)

tone = st.selectbox(
    "Select Tone:",
    ["Formal", "Analytical"]
)

region = st.text_input(
    "Enter Region / City / Country:",
    placeholder="e.g. Tokyo, London, California, Brazil"
)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- GENERATE BUTTON ---------------- #
if st.button("🚀 Generate Ultra Strict Report", use_container_width=True):

    if not topic:
        st.warning("Please enter a topic before generating report.")
        st.stop()

    # -------- Metrics -------- #
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mode", "Ultra Strict")
    with col2:
        st.metric("Model", "Groq Llama 3.1")
    with col3:
        st.metric("Generated At", datetime.now().strftime("%H:%M"))

    st.markdown("<hr>", unsafe_allow_html=True)

    # -------- AI Generation -------- #
    try:
        with st.spinner("Generating factual intelligence report..."):
            result = generate_article(
                topic=topic,
                tone=tone,
                city=region
            )

        if isinstance(result, tuple):
            article, image_url = result
        else:
            article = result
            image_url = None

        if not article:
            st.error("AI returned empty response.")
            st.stop()

    except Exception as e:
        st.error(f"Error generating report: {e}")
        st.stop()

    # -------- Image -------- #
    if image_url:
        st.image(image_url, use_container_width=True)

    # -------- Report Output -------- #
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    st.markdown("<h2>📑 Executive Intelligence Summary</h2>", unsafe_allow_html=True)
    
    for paragraph in article.split("\n\n"):
        st.markdown(f"<p>{paragraph}</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # -------- Download -------- #
    st.download_button(
        "⬇ Download Report",
        data=article,
        file_name="Ultra_Strict_Intelligence_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown("""
<div class="footer-right">
Made by <a href="https://github.com/Sankalp-gupta1" target="_blank">Sankalp Gupta</a>
</div>
""", unsafe_allow_html=True)

st.caption("AI Global Intelligence Engine • Ultra Strict Mode • 2026")


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

# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #0f172a, #1e293b);
#     color: white;
# }

# .block-container {
#     padding-top: 2rem;
#     padding-left: 3rem;
#     padding-right: 3rem;
# }

# .stButton>button {
#     background: linear-gradient(90deg, #6366f1, #8b5cf6);
#     color: white;
#     border-radius: 30px;
#     height: 3rem;
#     font-size: 16px;
#     font-weight: 600;
#     border: none;
# }

# .report-card {
#     background: rgba(255,255,255,0.05);
#     padding: 2rem;
#     border-radius: 20px;
#     backdrop-filter: blur(15px);
#     border: 1px solid rgba(255,255,255,0.1);
#     margin-top: 20px;
# }

# </style>
# """, unsafe_allow_html=True)

# # ---------------- HEADER ---------------- #
# st.markdown("""
# <h1 style='text-align:center;'>🌍 AI Global Intelligence Brief</h1>
# <p style='text-align:center; color:#94a3b8;'>
# Ultra Strict Factual Intelligence Engine
# </p>
# """, unsafe_allow_html=True)

# st.markdown("---")

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

# st.markdown("---")

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

#     st.markdown("---")

#     # -------- AI Generation -------- #
#     try:
#         with st.spinner("Generating factual intelligence report..."):
#             result = generate_article(
#                 topic=topic,
#                 tone=tone,
#                 city=region
#             )

#         # 🔥 SAFE UNPACKING
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
#     st.markdown("### 📑 Executive Intelligence Summary")
#     st.write(article)
#     st.markdown("</div>", unsafe_allow_html=True)

#     # -------- Download -------- #
#     st.download_button(
#         "⬇ Download Report",
#         data=article,
#         file_name="Ultra_Strict_Intelligence_Report.txt",
#         mime="text/plain",
#         use_container_width=True
#     )

# st.markdown("---")
# st.caption("AI Global Intelligence Engine • Ultra Strict Mode • 2026")




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

# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #0f172a, #1e293b);
#     color: white;
# }

# .block-container {
#     padding-top: 2rem;
#     padding-left: 3rem;
#     padding-right: 3rem;
# }

# .stButton>button {
#     background: linear-gradient(90deg, #6366f1, #8b5cf6);
#     color: white;
#     border-radius: 30px;
#     height: 3rem;
#     font-size: 16px;
#     font-weight: 600;
#     border: none;
# }

# .stButton>button:hover {
#     box-shadow: 0 8px 25px rgba(99,102,241,0.6);
#     transform: scale(1.02);
# }

# .report-card {
#     background: rgba(255,255,255,0.05);
#     padding: 2rem;
#     border-radius: 20px;
#     backdrop-filter: blur(15px);
#     border: 1px solid rgba(255,255,255,0.1);
#     margin-top: 20px;
# }

# </style>
# """, unsafe_allow_html=True)


# # ---------------- HEADER ---------------- #
# st.markdown("""
# <h1 style='text-align:center;'>🌍 AI Global Intelligence Brief</h1>
# <p style='text-align:center; color:#94a3b8;'>
# Ultra Strict Factual Intelligence Engine
# </p>
# """, unsafe_allow_html=True)

# st.markdown("---")


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

# st.markdown("---")


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

#     st.markdown("---")

#     # -------- AI Generation -------- #
#     with st.spinner("Generating factual intelligence report..."):
#         article, image_url = generate_article(
#             topic=topic,
#             tone=tone,
#             city=region
#         )

#     # -------- Image -------- #
#     if image_url:
#         st.image(image_url, use_container_width=True)

#     # -------- Report Output -------- #
#     st.markdown("<div class='report-card'>", unsafe_allow_html=True)
#     st.markdown("### 📑 Executive Intelligence Summary")
#     st.write(article)
#     st.markdown("</div>", unsafe_allow_html=True)

#     # -------- Download -------- #
#     st.download_button(
#         "⬇ Download Report",
#         data=article,
#         file_name="Ultra_Strict_Intelligence_Report.txt",
#         mime="text/plain",
#         use_container_width=True
#     )

# st.markdown("---")
# st.caption("AI Global Intelligence Engine • Ultra Strict Mode • 2026")











# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from agents.contextualist import gather_context
# from agents.scout import analyze_context
# from agents.publisher import generate_article
# from datetime import datetime

# # ---------------- PAGE CONFIG ---------------- #
# # st.set_page_config(
# #     page_title="AI Daily Global Brief",
# #     page_icon="🌍",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # ---------------- ADVANCED PREMIUM CSS ---------------- #
# st.markdown("""
# <style>

# /* Global Background */
# [data-testid="stAppViewContainer"] {
#     background: radial-gradient(circle at 20% 20%, #1f2a44, #0e1117 60%);
#     color: #ffffff;
# }

# /* Remove default padding */
# .block-container {
#     padding-top: 2rem;
#     padding-left: 3rem;
#     padding-right: 3rem;
# }

# /* Glass Card */
# .glass-card {
#     background: rgba(255,255,255,0.05);
#     backdrop-filter: blur(20px);
#     border: 1px solid rgba(255,255,255,0.1);
#     padding: 2rem;
#     border-radius: 20px;
#     box-shadow: 0 10px 40px rgba(0,0,0,0.5);
#     transition: 0.3s ease-in-out;
# }

# .glass-card:hover {
#     transform: translateY(-5px);
#     box-shadow: 0 20px 60px rgba(0,0,0,0.6);
# }

# /* Metric Cards */
# .metric-card {
#     background: linear-gradient(135deg, #1e293b, #0f172a);
#     padding: 1.5rem;
#     border-radius: 18px;
#     text-align: center;
#     box-shadow: 0 8px 30px rgba(0,0,0,0.4);
#     transition: 0.3s;
# }

# .metric-card:hover {
#     transform: scale(1.05);
# }

# .metric-title {
#     font-size: 14px;
#     color: #94a3b8;
# }

# .metric-value {
#     font-size: 28px;
#     font-weight: bold;
#     margin-top: 5px;
# }

# /* Button Styling */
# .stButton>button {
#     background: linear-gradient(90deg, #6366f1, #8b5cf6);
#     color: white;
#     border-radius: 30px;
#     height: 3rem;
#     font-size: 16px;
#     font-weight: 600;
#     border: none;
#     transition: 0.3s;
# }

# .stButton>button:hover {
#     transform: scale(1.03);
#     box-shadow: 0 10px 25px rgba(99,102,241,0.5);
# }

# /* Section Title */
# .section-title {
#     font-size: 24px;
#     font-weight: 700;
#     margin-bottom: 1rem;
# }

# /* Footer */
# .footer {
#     text-align: center;
#     margin-top: 80px;
#     padding: 20px;
#     font-size: 14px;
#     color: #64748b;
# }

# /* Sidebar Styling */
# [data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0f172a, #111827);
# }

# </style>
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("## ⚙ Intelligence Control")
#     st.markdown("---")

#     auto_refresh = st.toggle("Auto Refresh", value=False)
#     show_image = st.toggle("Show Image", value=True)

#     st.markdown("---")
#     st.markdown("### 🧠 System Status")
#     st.success("Agents: Online")
#     st.info("Pipelines: Connected")
#     st.warning("Mode: Groq / API Enabled")

# # ---------------- HEADER ---------------- #
# st.markdown("""
# <h1 style='text-align:center; font-size:48px;'>🌍 AI Global Intelligence Brief</h1>
# <p style='text-align:center; color:#94a3b8;'>Enterprise-Grade Autonomous News Intelligence Engine</p>
# """, unsafe_allow_html=True)

# st.markdown("---")

# # ---------------- CUSTOM INPUTS ---------------- #
# st.markdown("### 📝 Enter Custom Intelligence Brief Parameters")

# user_prompt = st.text_input(
#     "Enter Topic:",
#     placeholder="e.g. US Elections, Delhi Pollution, Global AI News..."
# )

# topics = ["Global News", "Finance", "Weather", "Technology", "Health"]

# selected_topics = st.multiselect(
#     "Select Additional Topics:",
#     options=topics,
#     default=[]
# )

# tone = st.selectbox(
#     "Select Tone:",
#     ["Formal", "Analytical", "Aggressive"]
# )

# region = st.selectbox(
#     "Select Region:",
#     ["Global", "India", "US", "Europe", "Asia"]
# )

# st.markdown("---")

# # ---------------- MAIN ACTION ---------------- #
# if st.button("🚀 Generate Executive Intelligence Report", use_container_width=True):

#     # ---------------- METRICS ---------------- #
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown(f"""
#         <div class='metric-card'>
#             <div class='metric-title'>Data Sources</div>
#             <div class='metric-value'>3</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with col2:
#         st.markdown(f"""
#         <div class='metric-card'>
#             <div class='metric-title'>Agents Active</div>
#             <div class='metric-value'>3</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with col3:
#         st.markdown(f"""
#         <div class='metric-card'>
#             <div class='metric-title'>Generated At</div>
#             <div class='metric-value'>{datetime.now().strftime('%H:%M')}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown("---")

#     # ---------------- BUILD FINAL PROMPT ---------------- #
#     if not user_prompt:
#         user_prompt = "Global intelligence summary."

#     final_prompt = user_prompt

#     if selected_topics:
#         final_prompt += " Include updates on: " + ", ".join(selected_topics)

#     final_prompt += f" Write in a {tone.lower()} tone."
#     final_prompt += f" Focus on {region} region."

#     # ---------------- AGENT PIPELINE ---------------- #
#     with st.spinner("🔎 Aggregating global data streams..."):
#         context_msg = gather_context()

#     with st.spinner("🧠 Running multi-agent strategic analysis..."):
#         scout_msg = analyze_context(context_msg)

#     combined_msg = scout_msg + " | User Request: " + final_prompt

#     with st.spinner("✍ Generating executive-level briefing..."):
#         article, image_url = generate_article(combined_msg)



#     st.markdown("---")

#     if show_image and image_url:
#         st.image(image_url, use_container_width=True)

#     st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-title'>📑 Executive Intelligence Summary</div>", unsafe_allow_html=True)
#     st.write(article)
#     st.markdown("</div>", unsafe_allow_html=True)

#     st.download_button(
#         label="⬇ Download Full Report",
#         data=article,
#         file_name="AI_Global_Intelligence_Brief.txt",
#         mime="text/plain",
#         use_container_width=True
#     )

# # ---------------- FOOTER ---------------- #
# st.markdown("""
# <div class='footer'>
# AI Global Intelligence Engine • Autonomous Multi-Agent System • 2026
# </div>
# """, unsafe_allow_html=True)


# # ---------------- SECOND VERSION ---------------- #

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# from agents.contextualist import gather_context
# from agents.scout import analyze_context
# from agents.publisher import generate_article

# st.set_page_config(page_title="AI Daily Global Brief", layout="centered")

# st.title("📰 AI Daily Global Brief Generator")

# if st.button("Generate Daily Report"):

#     with st.spinner("Gathering real-time data..."):
#         context_msg = gather_context()

#     with st.spinner("Analyzing signals..."):
#         scout_msg = analyze_context(context_msg)

#     with st.spinner("Generating AI article..."):
#         article, image_url = generate_article(scout_msg)

#     st.image(image_url)
#     st.subheader("Generated Article")
#     st.write(article)
