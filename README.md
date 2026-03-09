# 🧠 JSO – Agentic Career Intelligence System

An AI-powered career intelligence platform that analyses resumes, matches candidates with relevant jobs, identifies skill gaps, and provides personalised career recommendations — all powered by a **multi-agent RAG architecture** using **Google Gemini**, **ChromaDB**, and **SentenceTransformers**.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=for-the-badge&logo=databricks&logoColor=white)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Agent Pipeline](#-agent-pipeline)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

- **📄 PDF Resume Parsing** – Upload any text-based PDF resume for automatic extraction
- **🤖 Multi-Agent AI Pipeline** – Six specialised agents work together in sequence
- **🔍 RAG-Powered Job Matching** – Semantic vector search using ChromaDB for intelligent job recommendations
- **📊 Match Score Analytics** – Visual gauges and charts showing match percentages
- **🎯 Skill Gap Analysis** – Identifies missing skills and recommends learning paths
- **💡 AI Explanations** – Gemini generates natural-language reasoning for each recommendation
- **🎨 Modern Dark UI** – Premium SaaS-style dashboard built with Streamlit

---

## 🏗 Architecture

The system follows a **multi-agent RAG (Retrieval-Augmented Generation)** architecture:

```
Resume (PDF)
    │
    ▼
┌─────────────────────────┐
│ Resume Intelligence     │ ──▶ Extracts structured profile using Gemini
│ Agent                   │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Embedding Generator     │ ──▶ Indexes job dataset into ChromaDB
│ Agent                   │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ RAG Vector Search       │ ──▶ Semantic similarity search in ChromaDB
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Job Matching Agent      │ ──▶ Ranks jobs by match score (0–100%)
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Skill Gap Analysis      │ ──▶ Finds missing skills + learning paths
│ Agent                   │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Gemini Reasoning Agent  │ ──▶ Generates explanations for each match
└─────────────────────────┘
    │
    ▼
  Dashboard (Streamlit)
```

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **LLM** | Google Gemini (`gemini-flash-latest`) |
| **Vector Database** | ChromaDB (in-memory) |
| **Embeddings** | SentenceTransformers (`all-MiniLM-L6-v2`) |
| **PDF Parsing** | pypdf |
| **Visualisation** | Plotly, Pandas |
| **Environment** | python-dotenv |

---

## 📁 Project Structure

```
JSOO/
├── app.py              # Streamlit dashboard UI
├── rag_engine.py       # Pipeline orchestrator (coordinates all agents)
├── agents.py           # Multi-agent definitions (5 agents + Gemini helper)
├── vector_store.py     # ChromaDB vector store with SentenceTransformer embeddings
├── jobs_dataset.py     # Simulated job dataset (20 diverse job listings)
├── memory.py           # Agent memory system (session-based)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # This file
```

---

## 🚀 Setup & Installation

### Prerequisites

- **Python 3.10+** installed
- A **Google Gemini API Key** ([Get one here](https://aistudio.google.com/apikey))

### Step 1: Clone / Download the Project

```bash
git clone <your-repo-url>
cd JSOO
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` – Web dashboard
- `google-generativeai` – Gemini LLM
- `chromadb` – Vector database
- `sentence-transformers` – Embedding model
- `pypdf` – PDF text extraction
- `pandas`, `numpy` – Data processing
- `plotly` – Interactive charts
- `python-dotenv` – Environment variable management

### Step 3: Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

---

## ⚙ Configuration

| Variable | Description | Required |
|---|---|---|
| `GOOGLE_API_KEY` | Your Google Gemini API key | ✅ Yes |

The API key is loaded from the `.env` file using `python-dotenv`. You can also set it as a system environment variable.

---

## 📖 Usage

1. **Open the app** in your browser (default: `http://localhost:8501`)
2. **Upload your resume** (PDF format) using the sidebar file uploader
3. **Click "🚀 Analyse Resume"** to start the multi-agent pipeline
4. **View results** on the dashboard:
   - **Candidate Profile** – Extracted skills, experience, and summary
   - **Job Recommendations** – Ranked job matches with scores and gauges
   - **Skill Gap Analysis** – Missing skills with recommended learning paths
   - **AI Explanations** – Gemini-generated reasoning for each match
   - **Analytics Charts** – Match score comparisons and skill demand distribution

---

## 🤖 Agent Pipeline

| # | Agent | Responsibility |
|---|---|---|
| 1 | **Resume Intelligence Agent** | Parses PDF and extracts structured candidate profile using Gemini |
| 2 | **Embedding Generator Agent** | Indexes the job dataset into ChromaDB with semantic embeddings |
| 3 | **RAG Vector Search** | Performs cosine similarity search to find relevant jobs |
| 4 | **Job Matching Agent** | Converts distances to match scores and ranks results |
| 5 | **Skill Gap Analysis Agent** | Compares candidate skills vs. job requirements, suggests learning paths |
| 6 | **Gemini Reasoning Agent** | Generates natural-language explanations for each job recommendation |

---

## 🔧 Troubleshooting

| Issue | Solution |
|---|---|
| `GOOGLE_API_KEY not found` | Ensure `.env` file exists with a valid API key |
| `Could not extract text from PDF` | Use a text-based PDF, not a scanned image |
| Module not found errors | Run `pip install -r requirements.txt` |
| Port already in use | Run with `streamlit run app.py --server.port 8502` |
| Slow first run | The SentenceTransformer model (`all-MiniLM-L6-v2`) downloads on first use (~80MB) |

---

## 📄 License

This project is for educational and demonstration purposes.

---

<div align="center">
  <strong>JSO Agentic Career Intelligence System</strong> · Phase-2 Prototype<br>
  Powered by Gemini · ChromaDB · SentenceTransformers · Multi-Agent RAG Architecture
</div>
