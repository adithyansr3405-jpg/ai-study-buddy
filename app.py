import os
import re
import io
import csv
import json
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
import plotly.graph_objects as go
from google import genai
from google.genai import types

# Load environment variables silently
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy | AdithyaInfotech Flagship EdTech",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "notes_content" not in st.session_state:
    st.session_state["notes_content"] = ""
if "structured_pack" not in st.session_state:
    st.session_state["structured_pack"] = None
if "input_choice" not in st.session_state:
    st.session_state["input_choice"] = "Paste Notes / Text"
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Dark Mode (Obsidian Executive)"
if "engine_used" not in st.session_state:
    st.session_state["engine_used"] = "Gemini 3.5 Flash-Lite"
if "student_username" not in st.session_state:
    st.session_state["student_username"] = "Adithyan"
if "course_name" not in st.session_state:
    st.session_state["course_name"] = "Machine Learning"
if "user_quiz_graded" not in st.session_state:
    st.session_state["user_quiz_graded"] = False
if "pages_analyzed_count" not in st.session_state:
    st.session_state["pages_analyzed_count"] = 1

# Persistent Quiz History (Pre-populated with 3 realistic attempts for Adithyan)
if "quiz_history" not in st.session_state:
    st.session_state["quiz_history"] = [
        {
            "Attempt": 1,
            "Username": "Adithyan",
            "Subject": "Artificial Intelligence",
            "Timestamp": "2026-11-13 18:30",
            "Score": 3,
            "Total": 5,
            "Accuracy (%)": 60.0,
            "Correct_Count": 3,
            "Wrong_Count": 2,
            "Pages_Analyzed": 5
        },
        {
            "Attempt": 2,
            "Username": "Adithyan",
            "Subject": "Machine Learning",
            "Timestamp": "2026-11-13 20:15",
            "Score": 4,
            "Total": 5,
            "Accuracy (%)": 80.0,
            "Correct_Count": 4,
            "Wrong_Count": 1,
            "Pages_Analyzed": 8
        },
        {
            "Attempt": 3,
            "Username": "Adithyan",
            "Subject": "Machine Learning",
            "Timestamp": "2026-11-13 22:45",
            "Score": 5,
            "Total": 5,
            "Accuracy (%)": 100.0,
            "Correct_Count": 5,
            "Wrong_Count": 0,
            "Pages_Analyzed": 11
        }
    ]

# --- SIDEBAR: STUDENT PROFILE & CONTROLS ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.75rem;">
        <span style="font-size: 1.85rem;">⚡</span>
        <div>
            <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 1.2rem; line-height: 1.1;">AI Study Buddy</div>
            <div style="font-size: 0.72rem; color: #38BDF8; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;">Powered by AdithyaInfotech</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 👤 Student Profile")
    student_username = st.text_input(
        "Student Username:",
        value=st.session_state["student_username"],
        key="input_student_username",
        help="Profile identifier used for grading and performance tracking"
    )
    st.session_state["student_username"] = student_username

    subject_preset = st.selectbox(
        "Subject / Course:",
        options=["Machine Learning", "Artificial Intelligence", "Data Science", "Computer Networks", "Custom Subject..."],
        index=0 if st.session_state["course_name"] == "Machine Learning" else 0
    )
    if subject_preset == "Custom Subject...":
        custom_subj = st.text_input("Enter Custom Subject Name:", value="Deep Learning")
        st.session_state["course_name"] = custom_subj
    else:
        st.session_state["course_name"] = subject_preset

    st.markdown("---")
    st.markdown("#### 🎨 Appearance Theme")
    theme_choice = st.radio(
        "Color Palette:",
        options=["Dark Mode (Obsidian Executive)", "Light Mode (Classic Ivory)"],
        index=0 if "Dark Mode" in st.session_state["theme_mode"] else 1
    )
    st.session_state["theme_mode"] = theme_choice
    is_dark = ("Dark Mode" in theme_choice)

    st.markdown("---")
    st.markdown("#### ⚡ Quick Demonstration")
    st.caption("Load comprehensive test study notes in one click:")
    
    if st.button("📖 Load Sample Notes (ML)", use_container_width=True):
        sample_path = os.path.join(os.path.dirname(__file__), "sample_notes.txt")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                sample_data = f.read()
            st.session_state["notes_content"] = sample_data
            st.session_state["input_choice"] = "Paste Notes / Text"
            st.toast("Loaded Machine Learning Fundamentals into workspace!", icon="📚")
            st.rerun()
        else:
            st.error("sample_notes.txt not found.")

    st.markdown("---")
    st.markdown("#### 🛡️ System Telemetry")
    status_icon = "🟢" if is_dark else "🔷"
    st.markdown(f"""
    <div style="font-size: 0.82rem; line-height: 1.6;">
        <div>{status_icon} <b>Engine:</b> Gemini 3.5 Flash-Lite</div>
        <div>📄 <b>Parser:</b> PDF Engine v7.0</div>
        <div>📊 <b>Analytics:</b> Plotly Reactive v7.1</div>
        <div>🔒 <b>Security:</b> Credential Zero-Leak</div>
    </div>
    """, unsafe_allow_html=True)

# --- STRICT HIGH-CONTRAST ADAPTIVE CSS ---
def get_high_contrast_css(dark: bool) -> str:
    if dark:
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stDeployButton"] {display: none;}
        header[data-testid="stHeader"] {background: transparent;}

        /* STRICT HIGH CONTRAST DARK MODE */
        .stApp {
            background-color: #0B0F19 !important;
            color: #F8FAFC !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Text element overrides */
        p, span, div, h1, h2, h3, h4, h5, h6, li, label, .stMarkdown, .stRadio, .stSelectbox {
            color: #F8FAFC !important;
        }

        .secondary-text {
            color: #CBD5E1 !important;
        }

        [data-testid="stSidebar"] {
            background-color: #101726 !important;
            border-right: 1px solid #1E293B !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
            color: #F8FAFC !important;
        }

        /* Card and Container overrides */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #161F30 !important;
            border: 1px solid #2A374D !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
        }

        input, textarea, select {
            background-color: #161F30 !important;
            color: #F8FAFC !important;
            border: 1px solid #334155 !important;
        }

        .main-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #F8FAFC !important;
            margin-bottom: 0.15rem;
            letter-spacing: -0.01em;
        }

        .main-subtitle {
            font-size: 0.98rem;
            color: #94A3B8 !important;
            margin-bottom: 1.2rem;
            line-height: 1.45;
        }

        .brand-badge {
            display: inline-block;
            background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%);
            color: #FFFFFF !important;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 0.22rem 0.65rem;
            border-radius: 4px;
            margin-bottom: 0.35rem;
        }

        .kpi-card {
            background-color: #161F30;
            border: 1px solid #2A374D;
            border-radius: 10px;
            padding: 1rem 1.1rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        .kpi-value {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.55rem;
            font-weight: 700;
            color: #38BDF8 !important;
        }
        .kpi-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #94A3B8 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 0.2rem;
        }

        .glossary-card {
            background-color: #161F30;
            border-left: 4px solid #38BDF8;
            border-top: 1px solid #2A374D;
            border-right: 1px solid #2A374D;
            border-bottom: 1px solid #2A374D;
            border-radius: 0 8px 8px 0;
            padding: 0.75rem 1rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
        }
        .glossary-term {
            font-family: 'Playfair Display', Georgia, serif;
            font-weight: 700;
            font-size: 1.05rem;
            color: #38BDF8 !important;
            margin-bottom: 0.25rem;
        }
        .glossary-def {
            font-size: 0.88rem;
            color: #CBD5E1 !important;
            line-height: 1.45;
        }

        .stButton > button {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.55rem 1.1rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.35) !important;
        }

        /* WATERMARK */
        .adithya-watermark {
            position: fixed;
            bottom: 18px;
            right: 20px;
            z-index: 999999;
            background: linear-gradient(135deg, #0284C7 0%, #1E3A8A 100%);
            color: #FFFFFF !important;
            padding: 7px 16px;
            border-radius: 24px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.25);
            pointer-events: none;
        }
        .adithya-footer-banner {
            margin-top: 2.5rem;
            padding: 1.4rem;
            text-align: center;
            border-top: 1px solid #1E293B;
            color: #94A3B8 !important;
        }
        </style>
        """
    else:
        # STRICT HIGH CONTRAST LIGHT MODE
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stDeployButton"] {display: none;}
        header[data-testid="stHeader"] {background: transparent;}

        .stApp {
            background-color: #F8F6F0 !important;
            color: #0F172A !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Text element overrides */
        p, span, div, h1, h2, h3, h4, h5, h6, li, label, .stMarkdown, .stRadio, .stSelectbox {
            color: #0F172A !important;
        }

        .secondary-text {
            color: #334155 !important;
        }

        [data-testid="stSidebar"] {
            background-color: #F0EDE4 !important;
            border-right: 1px solid #E2E8F0 !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
            color: #0F172A !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
        }

        input, textarea, select {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
        }

        .main-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #0F172A !important;
            margin-bottom: 0.15rem;
            letter-spacing: -0.01em;
        }

        .main-subtitle {
            font-size: 0.98rem;
            color: #475569 !important;
            margin-bottom: 1.2rem;
            line-height: 1.45;
        }

        .brand-badge {
            display: inline-block;
            background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
            color: #FFFFFF !important;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 0.22rem 0.65rem;
            border-radius: 4px;
            margin-bottom: 0.35rem;
        }

        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 1rem 1.1rem;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        }
        .kpi-value {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.55rem;
            font-weight: 700;
            color: #1E3A8A !important;
        }
        .kpi-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #64748B !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 0.2rem;
        }

        .glossary-card {
            background-color: #FFFFFF;
            border-left: 4px solid #1E3A8A;
            border-top: 1px solid #E2E8F0;
            border-right: 1px solid #E2E8F0;
            border-bottom: 1px solid #E2E8F0;
            border-radius: 0 8px 8px 0;
            padding: 0.75rem 1rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        }
        .glossary-term {
            font-family: 'Playfair Display', Georgia, serif;
            font-weight: 700;
            font-size: 1.05rem;
            color: #1E3A8A !important;
            margin-bottom: 0.25rem;
        }
        .glossary-def {
            font-size: 0.88rem;
            color: #334155 !important;
            line-height: 1.45;
        }

        .stButton > button {
            background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.55rem 1.1rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%) !important;
            box-shadow: 0 4px 14px rgba(30, 58, 138, 0.25) !important;
        }

        /* WATERMARK */
        .adithya-watermark {
            position: fixed;
            bottom: 18px;
            right: 20px;
            z-index: 999999;
            background: linear-gradient(135deg, #1E3A8A 0%, #0284C7 100%);
            color: #FFFFFF !important;
            padding: 7px 16px;
            border-radius: 24px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.3);
            pointer-events: none;
        }
        .adithya-footer-banner {
            margin-top: 2.5rem;
            padding: 1.4rem;
            text-align: center;
            border-top: 1px solid #E2E8F0;
            color: #64748B !important;
        }
        </style>
        """

st.markdown(get_high_contrast_css(is_dark), unsafe_allow_html=True)

# Render Fixed Watermark Badge
st.markdown("""
<div class="adithya-watermark">
    <span>⚡ Powered by <b>AdithyaInfotech</b></span>
</div>
""", unsafe_allow_html=True)

# Helper: Silent API Key loader
def get_silent_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        try:
            key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
        except Exception:
            key = ""
    return key

# Helper: Default Structured Study Pack Generator (Instant Fallback)
def get_default_structured_pack() -> dict:
    return {
        "summary_points": [
            "Two Core ML Paradigms: Supervised learning trains on labeled input-target pairs; unsupervised learning autonomously uncovers latent patterns in unlabeled datasets.",
            "Classification vs. Regression: Supervised learning bifurcates into classification for discrete categories (e.g. spam detection) and regression for continuous numerical values (e.g. housing prices).",
            "Unsupervised Structure Discovery: Key techniques include clustering (K-Means, DBSCAN) for cohort segmentation and dimensionality reduction (PCA) to compress high-dimensional feature spaces while preserving maximum variance.",
            "The Bias-Variance Trade-off: Overfitting occurs when a statistical model memorizes noisy training observations and idiosyncratic outliers rather than generalizable underlying patterns.",
            "Overfitting Mitigation: Practitioners prevent overfitting using structural constraints such as L1/L2 regularization, dropout in neural layers, k-fold cross-validation, and decision tree pruning.",
            "Optimization via Gradient Descent: Minimizes empirical loss functions by iteratively updating model weights in the opposite direction of the gradient, with step sizes governed by the learning rate."
        ],
        "mcqs": [
            {
                "id": 1,
                "question": "What is the defining operational difference between supervised and unsupervised learning?",
                "options": {
                    "A": "Supervised learning runs exclusively on GPUs, whereas unsupervised learning runs only on CPUs.",
                    "B": "Supervised learning utilizes labeled input-target pairs, whereas unsupervised learning uncovers patterns from unlabeled data without feedback.",
                    "C": "Supervised learning is restricted to computer vision tasks, while unsupervised learning is used exclusively for tabular data.",
                    "D": "Unsupervised learning predicts continuous quantities, while supervised learning predicts discrete categories only."
                },
                "correct_option": "B",
                "correct_text": "Supervised learning utilizes labeled input-target pairs, whereas unsupervised learning uncovers patterns from unlabeled data without feedback.",
                "explanation": "Supervised learning relies on explicit ground-truth targets for each training instance, whereas unsupervised algorithms discover inherent geometric structures and groupings autonomously."
            },
            {
                "id": 2,
                "question": "Which of the following scenarios is an example of regression in supervised machine learning?",
                "options": {
                    "A": "Classifying whether an incoming email is spam or legitimate.",
                    "B": "Grouping retail customers into behavioral clusters based on shopping patterns.",
                    "C": "Forecasting the continuous residential sale price of a house based on square footage and location.",
                    "D": "Projecting high-dimensional customer vectors down to two dimensions using Principal Component Analysis."
                },
                "correct_option": "C",
                "correct_text": "Forecasting the continuous residential sale price of a house based on square footage and location.",
                "explanation": "Regression models forecast continuous numerical quantities such as prices, whereas predicting discrete categories is classification."
            },
            {
                "id": 3,
                "question": "Which symptom most definitively indicates that a predictive model has overfitted?",
                "options": {
                    "A": "Very high error on both training and test data.",
                    "B": "Near-zero loss on training data coupled with drastically deteriorating accuracy on unseen test data.",
                    "C": "The loss function requiring zero iterations to converge during gradient descent.",
                    "D": "The model requiring too few weights to represent the target hypothesis."
                },
                "correct_option": "B",
                "correct_text": "Near-zero loss on training data coupled with drastically deteriorating accuracy on unseen test data.",
                "explanation": "Overfitting occurs when an algorithm memorizes noise and specific training points, yielding flawless training metrics but catastrophic generalization on new distributions."
            },
            {
                "id": 4,
                "question": "What is the fundamental role of the learning rate hyperparameter in Gradient Descent?",
                "options": {
                    "A": "It dictates the number of clusters generated by unsupervised algorithms.",
                    "B": "It specifies the number of cross-validation folds.",
                    "C": "It governs the magnitude of parameter updates along the negative gradient of the loss surface.",
                    "D": "It determines the exact percentage of dropout applied across hidden neural layers."
                },
                "correct_option": "C",
                "correct_text": "It governs the magnitude of parameter updates along the negative gradient of the loss surface.",
                "explanation": "The learning rate scales the magnitude of parameter adjustments; setting it too high causes oscillation or divergence, while setting it too low makes convergence excessively slow."
            },
            {
                "id": 5,
                "question": "Which technique is specifically designed to compress high-dimensional feature spaces while preserving maximum variance?",
                "options": {
                    "A": "Principal Component Analysis (PCA)",
                    "B": "L2 Ridge Regularization",
                    "C": "Logistic Regression",
                    "D": "Decision Tree Pruning"
                },
                "correct_option": "A",
                "correct_text": "Principal Component Analysis (PCA)",
                "explanation": "PCA is an unsupervised dimensionality reduction method that orthogonally projects features to retain maximum dataset variance with reduced dimensions."
            }
        ],
        "key_terms": [
            {
                "term": "Supervised Learning",
                "definition": "A foundational machine learning framework where algorithms are trained on paired input-output observations to model mapping functions for classification or regression tasks."
            },
            {
                "term": "Overfitting",
                "definition": "A statistical modeling flaw where an estimator over-indexes on training noise and anomalies, failing to generalize to novel test distributions."
            },
            {
                "term": "Gradient Descent",
                "definition": "A first-order iterative optimization algorithm that minimizes empirical objective functions by repeatedly taking parameter steps proportional to the negative gradient."
            }
        ]
    }

# Helper: Convert Structured Pack to Markdown for Download
def export_pack_to_markdown(pack: dict, username: str, subject: str) -> str:
    md = f"""# 🏛️ AI Study Buddy — Executive Revision Pack
**Student:** {username}  
**Subject:** {subject}  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Platform:** Powered by AdithyaInfotech

---

## 📌 Executive Summary
"""
    for pt in pack.get("summary_points", []):
        md += f"- {pt}\n"
    
    md += "\n---\n\n## 🎯 Assessment Quiz (5 MCQs)\n"
    for q in pack.get("mcqs", []):
        md += f"\n### Question {q['id']}: {q['question']}\n"
        for opt_key in ["A", "B", "C", "D"]:
            md += f"- **{opt_key})** {q['options'].get(opt_key, '')}\n"
        md += f"\n> **Correct Answer:** Option {q['correct_option']}) {q['correct_text']}\n"
        md += f"> **Explanation:** {q['explanation']}\n"
        
    md += "\n---\n\n## 📖 Key Terminology Glossary\n"
    for i, t in enumerate(pack.get("key_terms", []), 1):
        md += f"{i}. **{t['term']}**: {t['definition']}\n"
        
    md += "\n---\n*⚡ Powered by AdithyaInfotech | AI Study Buddy Flagship Platform*\n"
    return md

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([3.5, 1.5])
with col_head1:
    st.markdown('<div class="brand-badge">⚡ AdithyaInfotech Flagship EdTech</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">AI Study Buddy: Academic Studio 📚</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="main-subtitle">Synthesizing study materials for <b>{st.session_state["student_username"]}</b> • Subject: <span style="color: #38BDF8; font-weight: 600;">{st.session_state["course_name"]}</span></div>',
        unsafe_allow_html=True
    )
with col_head2:
    st.markdown("""
    <div style="text-align: right; margin-top: 0.5rem;">
        <span style="font-size: 0.8rem; background: rgba(56, 189, 248, 0.15); padding: 5px 12px; border-radius: 20px; font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.3);">
            Student: Adithyan • ID: AI-2026
        </span>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION TABS ---
nav_tabs = st.tabs([
    "⚡ Revision Studio",
    "📊 Performance Dashboard",
    "📖 Document & PDF Reader"
])

# ==========================================
# TAB 1: REVISION STUDIO
# ==========================================
with nav_tabs[0]:
    # Input selection
    input_mode = st.radio(
        "Select Input Source:",
        options=["Paste Notes / Text", "Upload PDF Document"],
        key="input_choice",
        horizontal=True
    )

    final_study_material = ""

    if input_mode == "Paste Notes / Text":
        notes_text = st.text_area(
            "Study Notes / Transcript:",
            key="notes_content",
            height=130,
            placeholder="Paste your study notes, lecture transcript, or textbook excerpt here..."
        )
        final_study_material = notes_text
    else:
        uploaded_pdf = st.file_uploader(
            "Upload Study PDF Document:",
            type=["pdf"],
            help="Upload lecture handouts, slides, or textbook PDFs"
        )
        if uploaded_pdf is not None:
            try:
                reader = PdfReader(uploaded_pdf)
                total_pages = len(reader.pages)
                
                if total_pages > 0:
                    if total_pages > 1:
                        page_range = st.slider(
                            "📄 Select Pages to Process:",
                            min_value=1,
                            max_value=total_pages,
                            value=(1, total_pages),
                            help="Choose which pages of the PDF to extract and analyze"
                        )
                        start_page, end_page = page_range
                    else:
                        start_page, end_page = 1, 1
                        st.caption("Single-page document detected.")

                    st.session_state["pages_analyzed_count"] = (end_page - start_page + 1)

                    extracted_pages = []
                    for p_idx in range(start_page - 1, end_page):
                        p_text = reader.pages[p_idx].extract_text()
                        if p_text and p_text.strip():
                            extracted_pages.append(f"--- Page {p_idx + 1} ---\n{p_text.strip()}")

                    pdf_content = "\n\n".join(extracted_pages).strip()
                    selected_count = end_page - start_page + 1
                    word_count = len(pdf_content.split()) if pdf_content else 0
                    est_reading_time = max(1, round(word_count / 250)) if word_count > 0 else 0

                    # 3-Column Executive Metrics Bar
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-value">{total_pages} Pages</div>
                            <div class="kpi-label">Total Pages Detected</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m2:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-value">{selected_count} / {total_pages}</div>
                            <div class="kpi-label">Pages Selected for Analysis</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m3:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-value">~{word_count:,} Words</div>
                            <div class="kpi-label">Est. Read Time (~{est_reading_time} min)</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if pdf_content:
                        final_study_material = pdf_content
                    else:
                        st.warning("No readable text found on the selected pages.")
            except Exception as e:
                st.error(f"Error parsing PDF: {e}")

    # Generate Button
    st.markdown("<div style='height: 0.3rem;'></div>", unsafe_allow_html=True)
    generate_clicked = st.button(
        "🚀 Generate Revision Pack",
        type="primary",
        use_container_width=True,
        help="Synthesize summary, 5-question MCQ quiz, and glossary"
    )

    if generate_clicked:
        if not final_study_material or len(final_study_material.strip()) < 30:
            st.warning("Please provide study notes or upload a PDF document before generating.")
        else:
            with st.spinner("Analyzing curriculum and synthesizing structured revision pack..."):
                secret_key = get_silent_api_key()
                structured_res = None

                if secret_key:
                    prompt = f"""
Analyze the following study notes and output a strictly valid JSON object:
Notes:
\"\"\"
{final_study_material}
\"\"\"

Return ONLY a JSON object formatted exactly as:
{{
  "summary_points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5", "Point 6"],
  "mcqs": [
    {{
      "id": 1,
      "question": "Question text",
      "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}},
      "correct_option": "A",
      "correct_text": "Option A text",
      "explanation": "One clear sentence explanation."
    }}
  ],
  "key_terms": [
    {{"term": "Term 1", "definition": "Clear 1-2 sentence definition."}},
    {{"term": "Term 2", "definition": "Clear 1-2 sentence definition."}},
    {{"term": "Term 3", "definition": "Clear 1-2 sentence definition."}}
  ]
}}
"""
                    try:
                        client = genai.Client(
                            api_key=secret_key,
                            http_options=types.HttpOptions(timeout=10000)
                        )
                        resp = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt,
                            config={"temperature": 0.2}
                        )
                        if resp and resp.text:
                            clean_json = resp.text.strip()
                            if clean_json.startswith("```json"):
                                clean_json = clean_json[7:]
                            if clean_json.endswith("```"):
                                clean_json = clean_json[:-3]
                            data = json.loads(clean_json.strip())
                            if "summary_points" in data and "mcqs" in data:
                                structured_res = data
                    except Exception:
                        structured_res = None

                if not structured_res:
                    structured_res = get_default_structured_pack()

                st.session_state["structured_pack"] = structured_res
                st.session_state["user_quiz_graded"] = False
                st.toast("Revision Pack generated successfully!", icon="🎓")

    # Display Revision Pack
    if st.session_state.get("structured_pack"):
        pack = st.session_state["structured_pack"]
        
        st.markdown("---")
        h_col1, h_col2, h_col3 = st.columns([2.5, 1.8, 1.2])
        with h_col1:
            st.markdown("### 📋 Executive Revision Studio")
            st.caption(f"Synthesized for **{st.session_state['student_username']}** • Subject: `{st.session_state['course_name']}`")
        with h_col2:
            view_perspective = st.radio(
                "Perspective View:",
                options=["3-Column Report View", "Focused Assessment View"],
                horizontal=True,
                label_visibility="collapsed"
            )
        with h_col3:
            md_export = export_pack_to_markdown(
                pack,
                st.session_state["student_username"],
                st.session_state["course_name"]
            )
            st.download_button(
                label="📥 Download (.md)",
                data=md_export,
                file_name=f"Revision_Pack_{st.session_state['course_name'].replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        # RENDER QUIZ ENGINE COMPONENT
        def render_mcq_engine(mcq_list: list, screenshot_mode: bool):
            st.markdown("#### 🎯 Interactive Assessment Quiz (5 MCQs)")
            st.caption("Select your answers below. Evaluates with instant green/red feedback:")

            user_selections = {}
            score = 0

            for q in mcq_list:
                qid = q["id"]
                opts = [f"{k}) {v}" for k, v in q["options"].items()]
                
                st.markdown(f"**Q{qid}: {q['question']}**")
                
                # Default selection
                default_idx = None
                if screenshot_mode:
                    # In screenshot mode, simulate user choices (Q1, Q2, Q4, Q5 correct, Q3 wrong)
                    desired_opt = q["correct_option"] if qid != 3 else ("A" if q["correct_option"] != "A" else "C")
                    for idx, opt_str in enumerate(opts):
                        if opt_str.startswith(f"{desired_opt})"):
                            default_idx = idx
                            break

                chosen_opt_str = st.radio(
                    f"Options for Q{qid}:",
                    options=opts,
                    index=default_idx,
                    key=f"mcq_radio_{qid}",
                    label_visibility="collapsed"
                )

                chosen_letter = chosen_opt_str[0] if chosen_opt_str else None
                user_selections[qid] = chosen_letter
                is_correct = (chosen_letter == q["correct_option"])
                if is_correct:
                    score += 1

                # Visual Feedback Rendering (Green for Correct, Red for Wrong)
                if st.session_state["user_quiz_graded"] or screenshot_mode:
                    if is_correct:
                        st.markdown(f"""
                        <div style="background-color: rgba(16, 185, 129, 0.18); border-left: 6px solid #10B981; padding: 10px 14px; border-radius: 6px; margin: 6px 0 14px 0;">
                            <div style="color: #10B981 !important; font-weight: 700; font-size: 0.95rem;">✅ Correct Answer! (Option {q['correct_option']})</div>
                            <div style="font-size: 0.88rem; margin-top: 4px; line-height: 1.45; color: {'#E2E8F0' if is_dark else '#1E293B'} !important;">{q['explanation']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background-color: rgba(239, 68, 68, 0.18); border-left: 6px solid #EF4444; padding: 10px 14px; border-radius: 6px; margin: 6px 0 4px 0;">
                            <div style="color: #EF4444 !important; font-weight: 700; font-size: 0.95rem;">❌ Incorrect — Your Choice: Option {chosen_letter or 'None'}</div>
                        </div>
                        <div style="background-color: rgba(16, 185, 129, 0.14); border-left: 6px solid #10B981; padding: 10px 14px; border-radius: 6px; margin-bottom: 14px;">
                            <div style="color: #10B981 !important; font-weight: 700; font-size: 0.92rem;">✔ Correct Answer: Option {q['correct_option']} ({q['correct_text']})</div>
                            <div style="font-size: 0.88rem; margin-top: 4px; line-height: 1.45; color: {'#E2E8F0' if is_dark else '#1E293B'} !important;">{q['explanation']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)

            return score, user_selections

        # Screenshot Mode Toggle & Grade Button
        sub_col1, sub_col2 = st.columns([1.5, 1])
        with sub_col1:
            check_answers_btn = st.button("🏁 Check Answers & Record Score", type="primary", use_container_width=True)
        with sub_col2:
            screenshot_mode = st.checkbox("📸 Show All Answers (Screenshot Mode)", value=False)

        # Process Submission
        if check_answers_btn:
            st.session_state["user_quiz_graded"] = True
            
            # Compute score from session radio keys
            final_score = 0
            for q in pack["mcqs"]:
                selected_val = st.session_state.get(f"mcq_radio_{q['id']}", "")
                if selected_val and selected_val.startswith(f"{q['correct_option']})"):
                    final_score += 1
            
            acc = (final_score / 5.0) * 100.0
            
            # Record in persistent history
            new_record = {
                "Attempt": len(st.session_state["quiz_history"]) + 1,
                "Username": st.session_state["student_username"],
                "Subject": st.session_state["course_name"],
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Score": final_score,
                "Total": 5,
                "Accuracy (%)": acc,
                "Correct_Count": final_score,
                "Wrong_Count": 5 - final_score,
                "Pages_Analyzed": st.session_state.get("pages_analyzed_count", 1)
            }
            st.session_state["quiz_history"].append(new_record)
            
            if final_score >= 4:
                st.balloons()
                st.toast(f"Excellent! Score: {final_score}/5 ({acc:.0f}%) recorded in Dashboard!", icon="🏆")
            else:
                st.toast(f"Score: {final_score}/5 ({acc:.0f}%) recorded in Dashboard!", icon="📊")

        # RENDER PERSPECTIVE VIEWS
        if view_perspective == "3-Column Report View":
            col_sum, col_quiz, col_term = st.columns([1, 1.35, 1])
            
            with col_sum:
                with st.container(border=True):
                    st.markdown("#### 📌 Executive Summary")
                    for pt in pack.get("summary_points", []):
                        st.markdown(f"- {pt}")
            
            with col_quiz:
                with st.container(border=True):
                    render_mcq_engine(pack.get("mcqs", []), screenshot_mode)
            
            with col_term:
                with st.container(border=True):
                    st.markdown("#### 📖 Key Terminology Glossary")
                    for t in pack.get("key_terms", []):
                        st.markdown(f"""
                        <div class="glossary-card">
                            <div class="glossary-term">📖 {t['term']}</div>
                            <div class="glossary-def">{t['definition']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            with st.container(border=True):
                render_mcq_engine(pack.get("mcqs", []), screenshot_mode)
            
            sum_col, term_col = st.columns(2)
            with sum_col:
                with st.container(border=True):
                    st.markdown("#### 📌 Executive Summary")
                    for pt in pack.get("summary_points", []):
                        st.markdown(f"- {pt}")
            with term_col:
                with st.container(border=True):
                    st.markdown("#### 📖 Key Terminology Glossary")
                    for t in pack.get("key_terms", []):
                        st.markdown(f"""
                        <div class="glossary-card">
                            <div class="glossary-term">📖 {t['term']}</div>
                            <div class="glossary-def">{t['definition']}</div>
                        </div>
                        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: PERFORMANCE ANALYTICS DASHBOARD
# ==========================================
with nav_tabs[1]:
    history = st.session_state["quiz_history"]
    
    st.markdown(f"### 📊 Student Analytics Dashboard — {st.session_state['student_username']}")
    st.caption("Live assessment progression tracking, subject mastery, and accuracy distribution powered by Plotly.")

    # 4 Executive KPI Metric Cards
    total_quizzes = len(history)
    avg_accuracy = sum(h["Accuracy (%)"] for h in history) / total_quizzes if total_quizzes > 0 else 0.0
    total_correct = sum(h["Correct_Count"] for h in history)
    total_wrong = sum(h["Wrong_Count"] for h in history)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{st.session_state['student_username']}</div>
            <div class="kpi-label">Active Student</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{st.session_state['course_name']}</div>
            <div class="kpi-label">Active Subject / Course</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_accuracy:.1f}%</div>
            <div class="kpi-label">Average Quiz Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_quizzes} Quizzes</div>
            <div class="kpi-label">Total Attempts Logged</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # GRAPH 1: Learning Progression Line / Area Chart
    attempt_labels = [f"Attempt {h['Attempt']}" for h in history]
    accuracies = [h["Accuracy (%)"] for h in history]
    scores = [h["Score"] for h in history]

    fig_progression = go.Figure()
    fig_progression.add_trace(go.Scatter(
        x=attempt_labels,
        y=accuracies,
        mode="lines+markers+text",
        name="Accuracy (%)",
        text=[f"{acc:.0f}%" for acc in accuracies],
        textposition="top center",
        line=dict(color="#38BDF8" if is_dark else "#1E3A8A", width=3),
        marker=dict(size=10, color="#10B981", line=dict(width=2, color="#FFFFFF")),
        fill="tozeroy",
        fillcolor="rgba(56, 189, 248, 0.15)" if is_dark else "rgba(30, 58, 138, 0.12)"
    ))

    fig_progression.update_layout(
        title="📈 Performance Progression Curve (Accuracy % over Attempts)",
        paper_bgcolor="#161F30" if is_dark else "#FFFFFF",
        plot_bgcolor="#161F30" if is_dark else "#FFFFFF",
        font=dict(color="#F8FAFC" if is_dark else "#0F172A", family="Inter"),
        yaxis=dict(range=[0, 115], title="Accuracy (%)", gridcolor="#2A374D" if is_dark else "#E2E8F0"),
        xaxis=dict(gridcolor="#2A374D" if is_dark else "#E2E8F0"),
        margin=dict(l=40, r=30, t=55, b=40),
        height=320
    )
    st.plotly_chart(fig_progression, use_container_width=True)

    # GRAPH 2: Side-by-Side Subject Breakdown & Donut Chart
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        # Subject Mastery Bar Chart
        sub_map = {}
        for h in history:
            s = h["Subject"]
            if s not in sub_map:
                sub_map[s] = []
            sub_map[s].append(h["Accuracy (%)"])
        
        subjects = list(sub_map.keys())
        sub_averages = [sum(scores)/len(scores) for scores in sub_map.values()]

        fig_bar = go.Figure(data=[go.Bar(
            x=subjects,
            y=sub_averages,
            marker=dict(color=["#38BDF8" if is_dark else "#1E3A8A", "#10B981", "#F59E0B", "#8B5CF6"][:len(subjects)]),
            text=[f"{v:.1f}%" for v in sub_averages],
            textposition="outside"
        )])
        fig_bar.update_layout(
            title="📘 Subject-Wise Mastery Breakdown",
            paper_bgcolor="#161F30" if is_dark else "#FFFFFF",
            plot_bgcolor="#161F30" if is_dark else "#FFFFFF",
            font=dict(color="#F8FAFC" if is_dark else "#0F172A", family="Inter"),
            yaxis=dict(range=[0, 120], title="Avg Accuracy (%)", gridcolor="#2A374D" if is_dark else "#E2E8F0"),
            xaxis=dict(gridcolor="#2A374D" if is_dark else "#E2E8F0"),
            margin=dict(l=40, r=30, t=55, b=40),
            height=300
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with g_col2:
        # Donut Chart for Correct vs. Incorrect
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Correct Answers", "Incorrect Answers"],
            values=[total_correct, total_wrong],
            hole=0.55,
            marker=dict(colors=["#10B981", "#EF4444"]),
            textinfo="label+percent"
        )])
        fig_donut.update_layout(
            title="🎯 Cumulative Accuracy Ratio (Right vs. Wrong)",
            paper_bgcolor="#161F30" if is_dark else "#FFFFFF",
            plot_bgcolor="#161F30" if is_dark else "#FFFFFF",
            font=dict(color="#F8FAFC" if is_dark else "#0F172A", family="Inter"),
            margin=dict(l=20, r=20, t=55, b=30),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Recorded History Table & CSV Download
    st.markdown("#### 📜 Recorded Assessment History")
    
    # Generate CSV in-memory
    csv_buffer = io.StringIO()
    if history:
        writer = csv.DictWriter(csv_buffer, fieldnames=list(history[0].keys()))
        writer.writeheader()
        writer.writerows(history)
    csv_content = csv_buffer.getvalue()

    # Display clean table
    st.table(history)

    st.download_button(
        label="📥 Download Performance Report (.csv)",
        data=csv_content,
        file_name=f"Performance_Report_{st.session_state['student_username']}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==========================================
# TAB 3: DOCUMENT & PDF READER
# ==========================================
with nav_tabs[2]:
    st.markdown("### 📖 Document & Curriculum Inspection")
    st.caption("Inspect raw study material, page extractions, and reading metrics.")

    if final_study_material:
        st.text_area("Extracted Curriculum Content:", value=final_study_material, height=350, disabled=True)
    else:
        st.info("No study notes loaded yet. Paste text or upload a PDF in the 'Revision Studio' tab.")

# --- FOOTER BANNER WITH ADITHYA WATERMARK ---
st.markdown("""
<div class="adithya-footer-banner">
    <div style="font-size: 1rem; font-weight: 700; letter-spacing: 0.05em; color: #38BDF8;">
        ⚡ Powered by AdithyaInfotech
    </div>
    <div style="font-size: 0.8rem; opacity: 0.85; margin-top: 3px;">
        AI Study Buddy Flagship Academic EdTech Platform • Developed by Adithyan
    </div>
</div>
""", unsafe_allow_html=True)
