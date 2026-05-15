<div align="center">

# 🌱 AgriAI — Multi-Agent System for Smart Pesticide Recommendation

### 🧠 AI-Powered Multi-Agent Pipeline for Pesticide Risk Analysis and Eco-Friendly Recommendations

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-Interactive-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Multi--Agent-AI-success?style=for-the-badge"/>
</p>

</div>

---

# 📌 Overview

**AgriAI** is an AI-powered multi-agent system designed to help farmers, agronomists, and decision-makers make smarter and safer pesticide choices.

The platform automatically:

- 🔎 Searches pesticide information online
- 📊 Extracts and structures product details
- ⚠️ Analyzes health and environmental risks using LLMs
- 🌿 Suggests safer biological alternatives
- 📝 Generates structured recommendation reports

The project combines:

- Multi-Agent AI Systems
- Large Language Models (LLMs)
- Web Search Automation
- AI Risk Assessment
- Streamlit Dashboards

to build a practical AI solution for smart agriculture.

---

# 🎯 Problem Statement

Choosing the right pesticide can be difficult and risky due to:

- Limited access to reliable product information
- Difficulty understanding health/environmental risks
- Lack of awareness about biological alternatives
- Time-consuming manual research

AgriAI automates this process using AI-driven agents and intelligent information retrieval.

---

# 🚀 Main Features

✅ AI-powered multi-agent architecture  
✅ Automated pesticide product lookup  
✅ LLM-based risk analysis using Google Gemini  
✅ Biological and eco-friendly alternative recommendations  
✅ Structured report generation  
✅ Interactive Streamlit dashboard  
✅ Secure API key management with `.env`  
✅ Automated web search using SerpAPI  

---

# 🧠 Multi-Agent Architecture

The system is composed of **5 specialized AI agents**, each responsible for a specific task.

| Agent | Role |
|---|---|
| 🔎 Product Lookup Agent | Searches pesticide information using SerpAPI |
| 📊 Data Extraction Agent | Structures and extracts product details |
| ⚠️ Risk Analysis Agent | Uses Gemini LLM for health & environmental analysis |
| 🌿 Alternative Search Agent | Finds safer biological substitutes |
| 📝 Report Generation Agent | Generates final recommendation reports |

---

# ⚙️ System Workflow

<div align="center">

```text
User Input (Pesticide Name)
            ↓
Product Lookup Agent
            ↓
Data Extraction Agent
            ↓
Risk Analysis Agent (Gemini LLM)
            ↓
Alternative Search Agent
            ↓
Report Generation Agent
            ↓
Final Recommendation Report
```

</div>

---

# 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM | Google Gemini |
| Agent Framework | LangChain |
| Search API | SerpAPI |
| Dashboard | Streamlit |
| Data Handling | Pandas |
| Visualization | Matplotlib |
| Environment Management | python-dotenv |

---

# 📂 Project Structure

```bash
AgriAI/
│
├── config/
│   └── settings.py
│
├── dashboard/
│   └── dashboard.py
│
├── src/
│   ├── agents/
│   │   ├── product_lookup.py
│   │   ├── data_extraction.py
│   │   ├── risk_analysis.py
│   │   ├── alternative_search.py
│   │   └── report_generation.py
│   │
│   └── utils/
│       └── google_search.py
│
├── outputs/
│   └── report_glyphosate.txt
│
├── tests/
│   ├── test_alternative_search.py
│   ├── test_data_extraction.py
│   ├── test_product_lookup.py
│   └── test_risk_analysis.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 📸 Application Preview

## 🌿 Smart Pesticide Recommendation Dashboard

<p align="center">
  <img width="1000" src="https://github.com/user-attachments/assets/placeholder-image"/>
</p>

---

# ⚡ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Souadzriouil/AgriAI-Multi-Agent-System-for-Pesticide-Recommendation.git
cd AgriAI-Multi-Agent-System-for-Pesticide-Recommendation
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file at the project root:

```env
SERP_API_KEY=your_serpapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

---

# ▶️ Usage

## Run the CLI Pipeline

```bash
python main.py
```

---

## Run the Streamlit Dashboard

```bash
streamlit run dashboard/dashboard.py
```

---

# 🌐 Access the Dashboard

Open your browser and navigate to:

```bash
http://localhost:8501
```

---

# 📊 Example Output

Example analysis for **Glyphosate**:

```text
⚠️ Risk Analysis:
- Probable human carcinogen
- Harmful to aquatic ecosystems
- Long-term exposure risks

🌿 Recommended Alternatives:
- Neem oil
- Acetic acid-based herbicides
- Corn gluten meal
```

---

# 🧪 Testing

Run all tests:

```bash
python -m pytest tests/
```

Run a specific test:

```bash
python -m pytest tests/test_risk_analysis.py
```

---

# ⚠️ Limitations

- Output quality depends on search result relevance
- LLM responses may require human verification
- Not intended to replace professional agricultural advice
- Currently supports single pesticide analysis

---

# 🔮 Future Improvements

- [ ] Add Retrieval-Augmented Generation (RAG)
- [ ] PDF report export
- [ ] Public cloud deployment
- [ ] Multilingual support (Arabic / French / English)
- [ ] Structured pesticide database
- [ ] Source citation and explainability
- [ ] Advanced dashboard analytics

---

# 💡 Potential Use Cases

This platform can support:

- Smart agriculture systems
- Environmental risk analysis
- Sustainable farming
- Agricultural consulting
- AI-assisted agronomy tools

### Benefits

✅ Faster pesticide analysis  
✅ Improved environmental awareness  
✅ Safer agricultural recommendations  
✅ AI-assisted decision-making  

---

# 👩‍💻 Author

<div align="center">

## Souad Zriouil

### AI Engineer | Data Scientist | Machine Learning | NLP | LLM

<p align="center">
  <a href="https://github.com/Souadzriouil">
    <img src="https://img.shields.io/badge/GitHub-Souadzriouil-181717?style=for-the-badge&logo=github"/>
  </a>

  <a href="https://www.linkedin.com/in/souad-zriouil-54b19b267">
    <img src="https://img.shields.io/badge/LinkedIn-Souad%20Zriouil-0077B5?style=for-the-badge&logo=linkedin"/>
  </a>
</p>

</div>

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🔄 Share it on LinkedIn
- 📌 Add it to your portfolio

<div align="center">

⭐ Star the repo if you like the project!

</div>

---

# 📜 License

This project is intended for educational and portfolio purposes.
