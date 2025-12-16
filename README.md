# 🌲 California Parks & Outdoors Virtual Assistant  
*A CMPE 259 Final Project by Paul Junver Soriano*

## 📌 Overview  
The **California Parks & Outdoors Virtual Assistant** is an intelligent conversational agent that helps users explore California state parks, outdoor activities, and real-time weather conditions. It combines **Retrieval-Augmented Generation (RAG)**, **live weather APIs**, and **LLM reasoning** to deliver grounded, accurate, and context-aware responses.

This project compares two language models—**Mistral-7B v0.2** and **Llama-3.3-70B**—while analyzing how prompting techniques influence their performance, speed, and robustness.  

---

## 🚀 Features

### 🔍 Retrieval-Augmented Generation (RAG)
- Stores **283+ California state parks** in a FAISS vector database.  
- Retrieves relevant park information for each query to ensure factual accuracy.  
- Uses a **two-step RAG chain** to reduce inference latency.  

### 🌦 Live Weather Integration  
- Weather data is fetched using the **OpenMeteo API**.  
- Supports:
  - Current weather  
  - 10-day forecast  
- Automatically triggers when queries contain weather-related keywords.

### 🤖 Large Language Model Comparison  
Two models were tested and benchmarked:
- **Mistral-7B v0.2**  
- **Llama-3.3-70B**  

Both accessed through HuggingFace inference endpoints.

### 🧠 Intelligent System Architecture  
User queries are processed using:
1. Vector database retrieval  
2. Weather detection (regex-based)  
3. Prompt generation  
4. A single-pass LLM inference  

---

## 🗂 Dataset  
The dataset consists of **California State Parks official data**, including:
- Park names  
- Descriptions  
- Details & facilities  
- Activity lists  
- Source URL metadata  

---

## 💬 Query Categories  
The VA is evaluated on **20 diverse test queries**, grouped into four categories:

- **S — Simple (factual queries)**  
- **W — Weather**  
- **C — Complex (multi-step instructions)**  
- **R — Reasoning-based**  

---

## 🔒 Security Evaluation  
Five adversarial prompts tested the VA for:
- Prompt injection  
- Retrieval overrides  
- Sensitive data extraction  
- System prompt leakage  
- API key leakage  

---

## 🧪 Prompting Techniques Explored  

### 1️⃣ Chain-of-Thought (CoT)
- Helps smaller models (Mistral-7B) reason more clearly.  
- Reduced response times for Mistral-7B.  
- Slightly slowed Llama-70B.

### 2️⃣ Meta-Prompting
- Adds explicit safety & refusal instructions.  
- Improved harmful-prompt rejection for Llama-70B.  
- Reduced latency for Mistral-7B.

### 3️⃣ Self-Reflection
- Models evaluate and refine their own initial answer.  
- Increased response times.  
- Improved clarity and definitiveness.

---

## 📈 Summary of Findings  

### ⏱ Performance & Latency
- **Llama-70B consistently faster**.  
- Mistral-7B latency varies heavily.

### 📝 Output Size
- Comparable token counts between models.  
- Complex queries produce longer outputs.

### ⚠ Safety & Guardrails
- Both models are vulnerable without meta-prompting.

---

## 🛠 Repository Structure  
```plaintext
cmpe-259-project/
│── data/                               # Park dataset and FAISS vectors
│── evaluations/                        # LLM responses (stored to reduce API calls)
│── notebooks/                          # Jupyter/Google Colab notebooks used for the project
    │── parks_virtual_assistant.ipynb   # MAIN COLAB NOTEBOOK
│── src/                                # Contains Python scripts for utility
│── README.md                           # Project documentation (this file)
```

---

## ▶️ Getting Started

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Set Up Environment Variables**
```bash
HF_API_KEY=your_huggingface_key
OPEN_METEO_ENDPOINT=https://api.open-meteo.com/v1/forecast
```

### **3. Run the Virtual Assistant**
```bash
python app.py
```

### **4. Example Queries**
```text
"List parks with accessible trails."
"What's the weather like in Emerald Bay?"
"Plan a 2-day itinerary at Pismo Beach."
```

---

## 🔮 Future Improvements  
- Expand dataset (NPS, regional parks, AllTrails).  
- Add automated evaluation (LLM-as-a-Judge).  
- Increase the number of queries tested.  

---

## 🙌 Acknowledgments  
Thanks to **CMPE 259 — Natural Language Processing** for guidance and support.
