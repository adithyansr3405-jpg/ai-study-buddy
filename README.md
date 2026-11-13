# 🏛️ Project 10: AI Study Buddy (Notes to Quiz Studio)

> An executive-grade academic revision studio built with Streamlit and Google Gemini 3.5 Flash-Lite. Synthesizes lecture slides, textbook excerpts, and research notes into structured revision summaries, active-recall quizzes with explanations, and dictionary-style terminology glossaries.

---

## 🌟 Executive Overview

**AI Study Buddy** is a classic academic web application designed for students, researchers, and educators. It transforms dense lecture transcripts or multi-page academic PDF documents into structured study packages with interactive assessments, document page-range controls, and an appearance theme switcher.

---

## 🚀 Key Features

- **⚡ High-Yield Revision Studio:** Generates a structured 3-part study curriculum:
  1. **📌 Executive Summary:** 5–6 high-yield key takeaways and core principles.
  2. **🎯 Assessment Quiz (5 MCQs):** 5 multiple-choice questions with collapsible "Answer & Explanation" reveal callouts.
  3. **📖 Key Terminology Glossary:** 3 essential domain terms rendered as classic dictionary-style definition cards.
- **🎨 Built-in Dual Theme Engine:**
  - **Classic Ivory (Light Mode):** Warm alabaster/parchment background (`#F8F6F0`), crisp white cards with slate borders, and royal navy accents (`#1E3A8A`).
  - **Executive Obsidian (Dark Mode):** Deep slate-navy background (`#0F172A`), elevated charcoal cards, and sky-blue accents (`#38BDF8`).
- **📄 Advanced PDF Metrics & Page-Range Selection:**
  - Detects total uploaded pages across PDF documents.
  - Interactive **"Select Pages to Process"** slider to analyze specific page ranges.
  - 3-Column Executive Metrics bar showing:
    1. *Total Pages Uploaded*
    2. *Pages Selected for Analysis*
    3. *Estimated Word Count & Reading Time (at ~250 wpm)*
- **🖥️ Dual View Perspectives:**
  - **3-Column Report View:** Displays Summary, Quiz, and Glossary side-by-side for rapid one-screen reviewing and clean submission screenshots.
  - **Tabbed Study View:** Full-width focused study tabs for in-depth revision.
- **🔒 Zero UI Footprint for API Keys:**
  - Completely hides API key inputs from the interface for clean presentations and screenshot submissions.
  - Loads credentials silently from `.env` or Streamlit Cloud Secrets with an intelligent local study generation fallback.
- **📥 Markdown Export:** One-click download button (`st.download_button`) to export your revision pack as `.md`.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **LLM Engine:** Google Gemini 3.5 Flash-Lite via the official [`google-genai`](https://pypi.org/project/google-genai/) SDK
- **PDF Extraction:** [`pypdf`](https://pypi.org/project/pypdf/)
- **Environment Management:** [`python-dotenv`](https://pypi.org/project/python-dotenv/)

---

## 📦 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-study-buddy-quiz.git
cd ai-study-buddy-quiz
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Optional: Configure API Key in `.env`
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(The application automatically detects the key silently without exposing it on screen).*

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎯 Usage Guide

1. **Select Theme:** Toggle between **Classic Ivory** and **Executive Obsidian** in the sidebar.
2. **Select Input Method:**
   - Click **"📖 Load Sample Notes (ML)"** for an instant 1-click test with ~300 words on Machine Learning Fundamentals, OR
   - Paste custom lecture notes or transcripts into the text area, OR
   - Upload a multi-page PDF document and adjust the page range slider.
3. **Synthesize:** Click **"🚀 Generate Revision Pack"**.
4. **Interact & Review:**
   - Switch between **3-Column Report** and **Tabbed Study** views.
   - Expand the **💡 View Answer & Explanation** callouts under each MCQ question.
   - Click **"📥 Download (.md)"** to save your revision pack.

---

## ☁️ Deployment to Streamlit Cloud

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository, set `app.py` as the main module, and add `GEMINI_API_KEY` under **Advanced Settings > Secrets**.
4. Click **Deploy**!

---

## 📄 License
MIT License. Built for academic learning and revision.
