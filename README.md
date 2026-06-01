# 🌍 Free Multilingual RAG Translation Agent

A free multilingual Translation RAG (Retrieval-Augmented Generation) application built with Streamlit, Deep Translator, Sentence Transformers, and a local vector store.

This project translates text between multiple languages, stores translations as embeddings, and retrieves relevant past translations using semantic search.

---

## 🚀 Features

* 🌍 Translate text into multiple languages
* 🔍 Automatic language detection
* 🧠 Local embedding generation using Sentence Transformers
* 📚 Retrieval-Augmented Generation (RAG) memory
* ⚡ Semantic similarity search
* 💾 In-memory vector storage
* 🎨 Clean Streamlit user interface
* 🆓 Completely free (No Gemini API required)

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Deep Translator
* Sentence Transformers
* NumPy
* LangDetect

---

## 📂 Project Structure

```text
Translation-RAG-Agent/
│
├── app.py
├── agent.py
├── rag_store.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/Translation-RAG-Agent.git

cd Translation-RAG-Agent
```

### 2. Create Virtual Environment

```bash
conda create -n rag python=3.11

conda activate rag
```

Or:

```bash
python -m venv rag

rag\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

## 🌎 Supported Languages

* English
* Urdu
* German
* French
* Spanish
* Arabic
* Hindi
* Japanese
* Chinese
* Russian
* Turkish
* Italian
* Korean

---

## 🧠 How RAG Works

1. User enters text.
2. Language is automatically detected.
3. Text is translated using Google Translator.
4. Original text and translation are combined.
5. Combined text is converted into embeddings.
6. Embeddings are stored in memory.
7. Future queries retrieve semantically similar chunks.
8. Retrieved chunks provide contextual memory.

---

## 📊 RAG Components

### Embedding Model

```python
all-MiniLM-L6-v2
```

Used for:

* Semantic Search
* Similarity Retrieval
* Vector Embeddings

### Similarity Metric

```python
Cosine Similarity
```

Used to rank relevant stored chunks.

---

## ✨ Example

### Input

```text
Hello, how are you?
```

### Target Language

```text
Urdu
```

### Output

```text
ہیلو، آپ کیسے ہیں؟
```

---

## 🔥 Future Improvements

* Persistent Vector Database
* ChromaDB Integration
* FAISS Indexing
* PDF Translation
* Document Upload
* Translation History Export
* Voice Translation
* LLM Integration

---

## 📜 License

MIT License
