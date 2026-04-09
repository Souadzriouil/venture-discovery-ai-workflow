# 🚀 Venture Discovery AI Workflow

## 📌 Overview

This project presents an **AI-powered Venture Discovery Pipeline** designed to automate the process of **generating, analyzing, and evaluating startup ideas** using Large Language Models (LLMs) and Low-Code/No-Code (LCNC) platforms.

Developed as part of a **Master’s Thesis in Artificial Intelligence**, this system aims to democratize access to AI-driven business insights for entrepreneurs, startups, and innovation teams.

📄 Full Thesis: [Download Report](./Rapport_MFE.pdf)

---

## 🎯 Problem Statement

Venture discovery is a **complex and resource-intensive process** that requires:

- Market research  
- Competitor analysis  
- Feasibility evaluation  

Traditional approaches are:

- ❌ Time-consuming  
- ❌ Require strong expertise  
- ❌ Not accessible to non-technical users  

➡️ This project proposes an **end-to-end AI workflow** that automates and simplifies this process using low-code / no-code tools.

---

## 🧠 Project Objectives

- Generate innovative startup ideas using AI  
- Automate **market research and data collection**  
- Evaluate ideas using structured metrics (TAM, growth, etc.)  
- Rank and prioritize business opportunities  
- Identify **market gaps (white space)**  
- Provide actionable **business insights**  
- Enable usage through **low-code / no-code platforms**

---

## ⚙️ System Architecture

<img width="768" height="746" alt="pipeline" src="https://github.com/user-attachments/assets/a1a1eb43-ea49-4d79-b8e1-8d825d03e41a" />


### 🔹 Pipeline Steps

1. **User Input**
   - Define industry or domain
   - Optional company context

2. **Query Expansion**
   - Generate optimized search queries using LLMs

3. **Web Search & Data Retrieval**
   - Collect market trends, competitors, and insights

4. **Summarization**
   - Convert raw data into structured knowledge

5. **Idea Generation**
   - Generate multiple startup ideas

6. **Feasibility Scoring**
   - Evaluate ideas using:
     - TAM / SAM / SOM  
     - Growth potential (CAGR)  
     - Strategic fit  

7. **Solution Insights**
   - Value proposition  
   - Key features  
   - Go-to-market strategy  

8. **White-Space Analysis**
   - Identify market gaps  
   - Compare competitors  

9. **Final Output**
   - Structured JSON with ranked ideas and insights  

---

## 🧩 Platforms Used

The system was implemented and evaluated across multiple platforms:

- 🔗 **n8n** → Workflow orchestration  
- 🔗 **RAGFlow** → Retrieval & knowledge grounding  
- 🔗 **Dify** → Prompt management & evaluation  
- 🔗 **CrewAI** → Multi-agent reasoning  

Each platform provides different trade-offs between performance, usability, and scalability.

---

## 🧪 Evaluation Approach

### 🔹 Quantitative Metrics
- Latency  
- Token usage  
- Workflow complexity  
- JSON validity  

### 🔹 Qualitative Metrics
- Accessibility  
- Stability  
- Ecosystem maturity  

📊 Results show that **no single platform is universally optimal** — the choice depends on the use case and technical requirements.

---

## 🚀 Features

- ✅ AI-powered startup idea generation  
- ✅ Automated market research  
- ✅ Multi-agent reasoning workflows  
- ✅ Feasibility scoring system  
- ✅ White-space analysis  
- ✅ Structured JSON output  
- ✅ Low-code / no-code implementation  

---

## ▶️ How to Run

### 1. Clone the repository

git clone https://github.com/Souadzriouil/venture-discovery-ai-workflow.git  
cd venture-discovery-ai-workflow  

---

## 🧪 Use Cases

- 💡 Startup idea generation  
- 📊 Market opportunity analysis  
- 🧠 AI-driven business strategy  
- 🚀 Innovation automation  

---

## 👩‍💻 Author

**Souad Zriouil**  
AI Engineer | Data Scientist | Machine Learning | NLP | LLM  

📍 Settat, Morocco  
📧 souadzriouil02@gmail.com  
🔗 LinkedIn: www.linkedin.com/in/souad-zriouil-54b19b267  

---

## ⭐ Support

If you like this project, don’t forget to ⭐ the repository!
