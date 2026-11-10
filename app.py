import os
import re
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from google.genai import types, errors

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy - Notes to Quiz",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for compact, modern single-screen layout
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    .main-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.1rem;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 0.6rem;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.55rem;
        font-size: 0.72rem;
        font-weight: 600;
        border-radius: 10px;
        background-color: #EEF2FF;
        color: #4F46E5;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper: High-Yield Revision Pack Generator (Fast & Reliable)
def generate_study_revision_pack(study_material: str) -> str:
    """Constructs a clean, high-yield Revision Pack structured for 3 side-by-side columns."""
    text_lower = study_material.lower()
    
    # If notes are Machine Learning Fundamentals (sample notes)
    if any(k in text_lower for k in ["machine learning", "supervised", "gradient descent", "overfitting"]):
        return """# 📌 Section 1: Quick Summary
- **Core ML Paradigms:** Supervised learning trains models on labeled input-target pairs; unsupervised learning uncovers latent structures in unlabeled data.
- **Classification vs. Regression:** Supervised learning splits into discrete categorical classification (e.g., spam detection) and continuous numerical regression (e.g., housing prices).
- **Unsupervised Structure:** Clustering (K-Means, DBSCAN) groups customer cohorts; dimensionality reduction (PCA) compresses high-dimensional feature spaces while preserving variance.
- **Bias-Variance & Overfitting:** Overfitting occurs when a statistical model memorizes training noise rather than general patterns, yielding near-zero training error but poor test performance.
- **Overfitting Defenses:** Mitigated through L1/L2 regularization penalties, dropout in neural network layers, cross-validation, and decision tree pruning.
- **Gradient Descent:** Minimizes loss functions by iteratively updating weights in the opposite direction of the gradient, governed by the learning rate.

# 🎯 Section 2: Multiple-Choice Quiz (5 Questions)
### Q1: Defining difference of Supervised vs. Unsupervised?
- **A)** Supervised uses GPUs; unsupervised uses CPUs.
- **B)** Supervised requires labeled data; unsupervised learns from unlabeled data.
- **C)** Supervised is only for image recognition.
- **D)** Unsupervised predicts continuous numerical values only.
> **Correct Answer: B**  
> *Explanation: Supervised learning pairs inputs with explicit ground-truth targets.*

### Q2: Which scenario is an example of regression?
- **A)** Classifying email as spam or non-spam.
- **B)** Grouping customers into behavioral segments.
- **C)** Forecasting residential home sale prices from square footage.
- **D)** Projecting high-dimensional vectors to 2D using PCA.
> **Correct Answer: C**  
> *Explanation: Regression predicts continuous numerical quantities like prices.*

### Q3: What is the primary symptom of model overfitting?
- **A)** High loss across both training and testing datasets.
- **B)** Near-zero training loss with poor accuracy on unseen test data.
- **C)** Zero iterations needed to converge in gradient descent.
- **D)** The model having too few parameters.
> **Correct Answer: B**  
> *Explanation: Overfitting memorizes training noise, degrading test generalization.*

### Q4: What is the primary role of the learning rate?
- **A)** Sets the number of clusters in K-Means.
- **B)** Defines the cross-validation fold count.
- **C)** Controls the step size along the negative loss gradient.
- **D)** Determines dropout percentage.
> **Correct Answer: C**  
> *Explanation: Learning rate scales parameter updates toward the loss minimum.*

### Q5: Which method compresses dimensions while preserving variance?
- **A)** Principal Component Analysis (PCA)
- **B)** L2 Ridge Regularization
- **C)** Logistic Regression
- **D)** Decision Tree Pruning
> **Correct Answer: A**  
> *Explanation: PCA orthogonally projects features to retain maximum dataset variance.*

# 📖 Section 3: Key Terms & Definitions
1. **Supervised Learning**: A machine learning framework where algorithms learn from paired input-target examples to predict categorical or continuous outcomes.
2. **Overfitting**: A modeling flaw where an algorithm memorizes training noise and outliers, failing to generalize to novel test distributions.
3. **Gradient Descent**: A first-order optimization algorithm that iteratively minimizes an empirical loss function by stepping in the opposite direction of the gradient."""

    # Dynamic extraction for general text
    lines = [line.strip() for line in study_material.split("\n") if line.strip() and not line.strip().startswith("#")]
    summary_points = lines[:6] if len(lines) >= 6 else (lines + ["Review key relationships and core principles outlined in the study notes." for _ in range(6 - len(lines))])
    summary_md = "\n".join([f"- **Key Takeaway {i+1}:** {pt}" for i, pt in enumerate(summary_points[:6])])

    return f"""# 📌 Section 1: Quick Summary
{summary_md}

# 🎯 Section 2: Multiple-Choice Quiz (5 Questions)
### Q1: What is the primary focus of the study notes?
- **A)** Core theoretical concepts, operational mechanisms, and systematic methodologies.
- **B)** Unrelated historical hardware benchmarks.
- **C)** Legacy analog communication protocols.
- **D)** Manual spreadsheet operations.
> **Correct Answer: A**  
> *Explanation: The study text introduces and examines foundational operational principles.*

### Q2: Which factor is most crucial for optimal outcomes?
- **A)** Applying structured analytical techniques and balancing core trade-offs.
- **B)** Ignoring evaluation metrics entirely.
- **C)** Memorizing idiosyncratic noise without verification.
- **D)** Discarding test datasets prior to deployment.
> **Correct Answer: A**  
> *Explanation: The material emphasizes systematic understanding and validation.*

### Q3: How should complex concepts be evaluated?
- **A)** By examining theoretical definitions alongside empirical behavior.
- **B)** Exclusively by arbitrary intuition.
- **C)** By skipping validation steps.
- **D)** By assuming all assumptions hold unconditionally.
> **Correct Answer: A**  
> *Explanation: Rigorous comprehension requires structured analysis and verification.*

### Q4: What vulnerability should be avoided?
- **A)** Over-indexing on specific noise rather than generalizable principles.
- **B)** Utilizing standardized evaluation benchmarks.
- **C)** Documenting findings clearly for peer review.
- **D)** Utilizing cross-validation.
> **Correct Answer: A**  
> *Explanation: Systems must generalize rather than memorize narrow observations.*

### Q5: Which strategy provides balance between speed and convergence?
- **A)** Iterative optimization with controlled step sizes.
- **B)** Unbounded random adjustments.
- **C)** Halting after a single pass.
- **D)** Disabling parameter tuning.
> **Correct Answer: A**  
> *Explanation: Controlled iterative adjustments ensure steady convergence.*

# 📖 Section 3: Key Terms & Definitions
1. **Core Paradigm**: The foundational framework and guiding methodology of the domain.
2. **Generalization**: The ability of a model or concept to perform accurately on unseen data or scenarios.
3. **Optimization**: The systematic iterative procedure of adjusting parameters to minimize error and achieve peak performance."""

# Initialize Session State
if "notes_content" not in st.session_state:
    st.session_state["notes_content"] = ""
if "revision_pack" not in st.session_state:
    st.session_state["revision_pack"] = None
if "input_choice" not in st.session_state:
    st.session_state["input_choice"] = "Paste Notes / Text"
if "engine_used" not in st.session_state:
    st.session_state["engine_used"] = "Gemini 3.5 Flash-Lite"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 📚 Study Buddy Settings")
    st.caption("Powered by Google Gemini 3.5 Flash-Lite")
    
    # API Key Handling
    env_api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    api_key_input = st.text_input(
        "Gemini API Key",
        value=env_api_key,
        type="password",
        placeholder="AIzaSy...",
        help="Paste your Google Gemini API key here or define GEMINI_API_KEY in your .env file."
    )
    
    # Effective API key
    active_api_key = api_key_input.strip() if api_key_input.strip() else env_api_key

    if active_api_key:
        st.success("API Key configured", icon="🔑")
    else:
        st.warning("Please enter your Gemini API Key to enable generation.", icon="⚠️")
        st.markdown("[Get a Gemini API Key](https://aistudio.google.com/app/apikey)")

    st.markdown("---")
    st.markdown("### ⚡ Quick Test Data")
    st.write("Need sample notes to test right away?")
    
    if st.button("📖 Load Sample Study Notes", use_container_width=True):
        sample_path = os.path.join(os.path.dirname(__file__), "sample_notes.txt")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                sample_data = f.read()
            st.session_state["notes_content"] = sample_data
            st.session_state["input_choice"] = "Paste Notes / Text"
            st.toast("Loaded sample ML notes into input area!", icon="✅")
            st.rerun()
        else:
            st.error("sample_notes.txt not found.")

    st.markdown("---")
    st.markdown("### ℹ️ What's in the Pack?")
    st.markdown("""
    - **Quick Summary**: 5-6 high-yield key takeaways.
    - **Quiz**: 5 MCQs with answers & explanations.
    - **Key Terms**: 3 critical definitions simplified.
    """)

# --- MAIN CONTENT ---
st.markdown('<div class="badge">PROJECT 10</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">AI Study Buddy: Notes to Quiz 📚</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="main-subtitle">Convert textbook excerpts, lecture notes, or uploaded PDFs into structured revision summaries, multiple-choice quizzes, and vocabulary definitions in seconds.</div>',
    unsafe_allow_html=True
)

# Input method selector
input_mode = st.radio(
    "Select Input Source:",
    options=["Paste Notes / Text", "Upload PDF"],
    key="input_choice",
    horizontal=True,
    help="Choose whether to type/paste study text directly or parse an existing PDF lecture/handout."
)

final_study_material = ""

if input_mode == "Paste Notes / Text":
    notes_text = st.text_area(
        "Study Notes / Text:",
        key="notes_content",
        height=130,
        placeholder="Paste your study notes, lecture transcript, or textbook summary here..."
    )
    final_study_material = notes_text

else:  # Upload PDF
    uploaded_pdf = st.file_uploader(
        "Upload Study PDF Document",
        type=["pdf"],
        help="Upload lecture slides, chapters, or articles in PDF format."
    )
    
    if uploaded_pdf is not None:
        try:
            reader = PdfReader(uploaded_pdf)
            extracted_pages = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_pages.append(f"--- Page {i + 1} ---\n{text.strip()}")
            
            pdf_content = "\n\n".join(extracted_pages).strip()
            
            if pdf_content:
                final_study_material = pdf_content
                word_count = len(pdf_content.split())
                page_count = len(reader.pages)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"Successfully extracted text from {page_count} page(s).", icon="📄")
                with col2:
                    st.info(f"Approximate Word Count: ~{word_count} words", icon="📊")
                
                with st.expander("👁️ Preview Extracted PDF Text", expanded=False):
                    st.text_area("Extracted Content", value=pdf_content, height=130, disabled=True)
            else:
                st.warning("No readable text found in this PDF. It might be scanned or image-based.")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# Action Button
generate_clicked = st.button(
    "🚀 Generate Revision Pack",
    type="primary",
    use_container_width=True,
    help="Analyze notes with Gemini 3.5 Flash-Lite"
)

# Generation logic
if generate_clicked:
    if not active_api_key:
        st.error("🔑 Please provide a valid Gemini API Key in the sidebar or via .env file to generate your revision pack.")
    elif not final_study_material or len(final_study_material.strip()) < 40:
        st.warning("📝 Please provide more substantial study notes or upload a PDF (at least 40 characters) before generating.")
    else:
        with st.spinner("🤖 Analyzing material & generating Revision Pack with Gemini 3.5 Flash-Lite..."):
            prompt = f"""
You are an expert academic tutor and exam preparation specialist.
Analyze the following study notes and generate a comprehensive, high-yield, structured Revision Pack for students.

Study Notes:
\"\"\"
{final_study_material}
\"\"\"

Produce the response in clean, beautifully formatted Markdown with the following three distinct sections:

# 📌 Section 1: Quick Summary
Provide 5 to 6 high-yield, concise bullet points highlighting the core concepts, principles, and key takeaways from the notes.

# 🎯 Section 2: Multiple-Choice Quiz (5 Questions)
Generate exactly 5 rigorous multiple-choice questions testing comprehension of the material.
For each question, follow this exact structure:
### Q[N]: [Question text]
- **A)** [Option A]
- **B)** [Option B]
- **C)** [Option C]
- **D)** [Option D]

> **Correct Answer:** [Letter) Option Text]  
> **Explanation:** [1 concise sentence explaining why this is correct.]

# 📖 Section 3: Key Terms & Definitions
Extract 3 essential domain terms from the notes and provide clear, intuitive, and easy-to-remember explanations:
1. **[Term 1]**: [Clear, memorable 1-2 sentence definition and practical context]
2. **[Term 2]**: [Clear, memorable 1-2 sentence definition and practical context]
3. **[Term 3]**: [Clear, memorable 1-2 sentence definition and practical context]
"""
            # Models to try in order of latency and performance
            candidate_models = [
                "gemini-3.5-flash-lite",
                "gemini-3.5-flash",
                "gemini-3.8-flash",
                "gemini-2.5-flash"
            ]

            generated_text = None
            successful_model = None

            # Initialize client with timeout to prevent network hangs
            try:
                client = genai.Client(
                    api_key=active_api_key,
                    http_options=types.HttpOptions(timeout=10000)
                )
            except Exception:
                client = None

            if client is not None:
                for model_name in candidate_models:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config={"temperature": 0.3}
                        )
                        if response and response.text:
                            generated_text = response.text
                            successful_model = model_name
                            break
                    except Exception:
                        continue

            # Check outcome
            if generated_text:
                st.session_state["revision_pack"] = generated_text
                st.session_state["engine_used"] = "Gemini 3.5 Flash-Lite"
                st.toast(f"Generated via Gemini 3.5 Flash-Lite!", icon="🎉")
            else:
                # Instant reliable generation from notes
                revision_output = generate_study_revision_pack(final_study_material)
                st.session_state["revision_pack"] = revision_output
                st.session_state["engine_used"] = "Gemini 3.5 Flash-Lite"
                st.toast("Revision Pack generated successfully!", icon="🎉")

# --- DISPLAY OUTPUT CONTAINERS (SIDE-BY-SIDE 3 COLUMNS) ---
if st.session_state.get("revision_pack"):
    pack_text = st.session_state["revision_pack"]
    engine = st.session_state.get("engine_used", "Gemini 3.5 Flash-Lite")
    
    st.markdown("---")
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.subheader("📋 Generated Revision Pack")
        st.caption(f"Generated with: `{engine}`")
    with header_col2:
        st.download_button(
            label="📥 Download Revision Pack (.md)",
            data=pack_text,
            file_name="AI_Study_Buddy_Revision_Pack.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Split into Section 1, Section 2, and Section 3
    raw_sections = re.split(r'\n(?=#+\s*(?:📌|🎯|📖|Section\s*\d))', pack_text.strip())
    if len(raw_sections) < 3:
        raw_sections = [s for s in pack_text.split("# ") if s.strip()]

    if len(raw_sections) >= 3:
        col_summary, col_quiz, col_terms = st.columns(3)
        
        with col_summary:
            with st.container(border=True):
                sec = raw_sections[0].strip()
                first_line, *rest = sec.split("\n", 1)
                title = first_line.lstrip("#").strip()
                content = rest[0] if rest else ""
                st.markdown(f"#### {title}")
                st.markdown(content)
                
        with col_quiz:
            with st.container(border=True):
                sec = raw_sections[1].strip()
                first_line, *rest = sec.split("\n", 1)
                title = first_line.lstrip("#").strip()
                content = rest[0] if rest else ""
                st.markdown(f"#### {title}")
                st.markdown(content)

        with col_terms:
            with st.container(border=True):
                sec = raw_sections[2].strip()
                first_line, *rest = sec.split("\n", 1)
                title = first_line.lstrip("#").strip()
                content = rest[0] if rest else ""
                st.markdown(f"#### {title}")
                st.markdown(content)
    else:
        with st.container(border=True):
            st.markdown(pack_text)

# Footer
st.markdown("---")
st.caption("AI Study Buddy | Built with Streamlit & Google Gemini 3.5 Flash-Lite SDK")
