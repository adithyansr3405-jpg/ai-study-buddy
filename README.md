# 📚 Project 10: AI Study Buddy (Notes to Quiz)

> Transform study notes, textbook excerpts, and lecture PDFs into structured revision summaries, multiple-choice quizzes, and key vocabulary definitions in seconds — powered by Google Gemini 3.5 Flash-Lite.

---

## 🌟 Overview

**AI Study Buddy** is an intelligent academic revision tool built with Streamlit and Google's official `google-genai` SDK. It empowers students and educators to turn complex study notes or multi-page PDF documents into comprehensive revision packs featuring high-yield summaries, 5 multiple-choice questions with answer keys and explanations, and core term definitions.

---

## 🚀 Key Features

- **⚡ Instant Revision Pack Generation:** Generates a structured 3-part study package:
  1. **📌 Quick Summary:** 5–6 high-yield bullet points capturing core principles.
  2. **🎯 Multiple-Choice Quiz:** 5 challenging MCQs with options A–D, answer keys, and 1-sentence explanations.
  3. **📖 Key Terms & Definitions:** 3 essential vocabulary terms with concise definitions.
- **🖥️ Compact 3-Column Single-Screen Layout:** Displays all 3 sections side-by-side using `st.columns(3)` for immediate visibility and seamless screenshot capture.
- **📄 Dual Input Modes:**
  - **Paste Notes / Text:** Directly paste lecture transcripts, articles, or notes.
  - **Upload PDF:** Extract text across multiple pages from PDF handouts or lecture slides via `pypdf`.
- **📖 One-Click Sample Notes:** Pre-loaded with a ~300-word passage on *Machine Learning Fundamentals (Supervised vs. Unsupervised Learning, Overfitting, and Gradient Descent)* for instant testing.
- **🔐 Secure API Key Management:** Supports both `.env` configuration and dynamic in-app entry via a masked password input field.
- **📥 Markdown Export:** One-click download button (`st.download_button`) to save your complete revision pack as a `.md` file.

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

### 3. Configure Your Gemini API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(Alternatively, you can paste your API key directly into the sidebar at runtime).*

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎯 Usage Guide

1. **Enter API Key:** Paste your Gemini API key in the sidebar (if not already set in `.env`).
2. **Select Input Source:**
   - Click **"📖 Load Sample Study Notes"** in the sidebar for instant testing, OR
   - Paste custom notes into the text area, OR
   - Upload a lecture PDF file.
3. **Generate:** Click **"🚀 Generate Revision Pack"**.
4. **Revise & Export:** Review the 3 side-by-side columns and click **"📥 Download Revision Pack (.md)"** to save offline.

---

## ☁️ Deployment

### Streamlit Community Cloud (1-Click Deployment)
1. Fork or push this repository to your GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository, select `app.py` as the main file path, and add `GEMINI_API_KEY` under **Advanced Settings > Secrets**.
4. Click **Deploy**!

---

## 📄 License
MIT License. Built for academic and educational learning purposes.
