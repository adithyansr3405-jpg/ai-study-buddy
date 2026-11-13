# ⚡ AI Study Buddy — Flagship Academic EdTech Platform

> **Powered by AdithyaInfotech** | Advanced Interactive Learning, Performance Analytics & Active-Recall Assessment Studio.  
> Developed for **Project 10: AI Study Buddy (Notes to Quiz)**.

---

## 🌟 Executive Overview

**AI Study Buddy** is a flagship academic EdTech platform built with **Streamlit**, **Plotly**, and **Google Gemini 3.5 Flash-Lite**. It transforms dense academic notes, textbooks, and multi-page PDFs into structured high-yield revision summaries, interactive multiple-choice assessments with real-time green/red visual grading, and dictionary-style terminology glossaries.

The platform includes a **Performance Analytics Dashboard** that tracks student learning progression, subject mastery curves, and cumulative accuracy over time with full `.csv` and `.md` export capabilities.

---

## 🚀 Flagship Features

### 1. 🎯 Interactive Green/Red MCQ Assessment Engine
- **Instant Visual Grading**:
  - **Correct Answers**: Highlighted in vibrant **Emerald Green** with solution explanation (`✅ Correct Answer!`).
  - **Incorrect Answers**: Highlighted in vibrant **Crimson Red** showing user's choice (`❌ Incorrect — Your Choice`), immediately followed by the **Correct Answer Reveal Box**.
- **Screenshot Mode ("Show All Answers")**: One-click toggle revealing all evaluated states and explanations simultaneously for submission screenshots.
- **Scorecard Recording**: Calculates accuracy % and score out of 5, logging every attempt persistently into the student's analytics history.

### 2. 📊 Performance Analytics Dashboard (Plotly Reactive)
- **4 Executive KPI Metrics**: Active Student Profile, Current Subject, Average Accuracy %, and Total Logged Attempts.
- **Learning Progression Curve**: Theme-aware Plotly line/area chart visualizing score trends and accuracy percentages over sequential attempts.
- **Subject-Wise Mastery Breakdown**: Interactive bar chart comparing student mastery across multiple academic disciplines.
- **Cumulative Accuracy Ratio**: Precision donut chart displaying total correct vs. incorrect answers.
- **Report Export**: One-click **"📥 Download Performance Report (.csv)"** for academic records.

### 3. 👤 Student Profile & Subject Tracking
- Editable **Student Username** (default: `Adithyan`) and **Subject/Course Name** selector with presets (*Machine Learning*, *Artificial Intelligence*, *Data Science*, *Computer Networks*) or custom entry.

### 4. 🎨 Strict High-Contrast Adaptive Theme Engine
- **Dark Mode (Obsidian Executive)**: Deep slate-obsidian canvas (`#0B0F19`), dark charcoal cards (`#161F30`), and crisp off-white typography (`#F8FAFC`).
- **Light Mode (Classic Ivory)**: Warm parchment canvas (`#F8F6F0`), crisp white cards (`#FFFFFF`), and deep ink black typography (`#0F172A`).
- Editorial serif headings (`Playfair Display` / `Georgia`) paired with clean modern body typography (`Inter`).

### 5. 📄 Advanced PDF Metrics & Page-Range Extraction
- Automatic detection of total uploaded PDF pages via `pypdf`.
- Interactive page-range slider to extract and analyze specific chapters or sections.
- 3-Column Executive Metrics bar tracking Total Pages, Selected Pages, Word Count, and Estimated Reading Time (~250 wpm).

### 6. ⚡ Watermark & Branding
- Persistent floating badge at bottom-right: `⚡ Powered by AdithyaInfotech`.
- Classic footer banner across all application views and in all exported reports.

---

## 🛠️ Tech Stack

- **Application Framework:** [Streamlit](https://streamlit.io/)
- **Visual Analytics:** [Plotly Graph Objects](https://plotly.com/python/)
- **Data Engineering:** Python CSV & Pandas DataFrames
- **AI Synthesis Engine:** Google Gemini 3.5 Flash-Lite via the official [`google-genai`](https://pypi.org/project/google-genai/) SDK
- **PDF Extraction:** [`pypdf`](https://pypi.org/project/pypdf/)
- **Environment Management:** [`python-dotenv`](https://pypi.org/project/python-dotenv/)

---

## 📦 Local Installation & Setup

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
*(The platform loads credentials silently with zero UI exposure and automatically activates an intelligent study generation engine if no key is present).*

### 4. Run the Platform
```bash
streamlit run app.py
```
Access the application in your browser at `http://localhost:8501`.

---

## 🎯 Quick Demonstration Flow (For Evaluation & Screenshots)

1. Open the app in your browser ([http://localhost:8501](http://localhost:8501) or live public tunnel).
2. Click **"📖 Load Sample Notes (ML)"** in the sidebar.
3. Click **"🚀 Generate Revision Pack"** in the **Revision Studio** tab.
4. Interact with the **Assessment Quiz**:
   - Check answers using **"🏁 Check Answers & Record Score"** to see vibrant green and red evaluation boxes.
   - Or toggle **"📸 Show All Answers (Screenshot Mode)"** to display all 5 graded questions on screen at once.
5. Switch to the **"📊 Performance Dashboard"** tab to view the executive KPIs, progression curve, subject mastery bar chart, donut ratio, and recorded history table.
6. Click **"📥 Download (.md)"** or **"📥 Download Performance Report (.csv)"** to export your study materials.

---

## 📄 License & Attribution
MIT License • Built by **Adithyan** • Powered by **AdithyaInfotech**.
