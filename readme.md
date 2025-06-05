# IMDb Chatbot: Interactive Setup Guide

Welcome! This guide will walk you through setting up and running the IMDb Chatbot locally. Just follow each step below. If something doesn’t work, check off the step to see where you might need to revisit.

---

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [1. Create a Virtual Environment](#1-create-a-virtual-environment)
3. [2. Install Dependencies](#2-install-dependencies)
4. [3. Download and Prepare IMDb Data](#3-download-and-prepare-imdb-data)
5. [4. Create a `.env` File](#4-create-a-env-file)
6. [5. Run the FastAPI Server](#5-run-the-fastapi-server)
7. [6. Test the `/chat` Endpoint](#6-test-the-chat-endpoint)

---

## 🔧 Prerequisites

* **Python 3.9+** installed on your system
* **Git** (optional, if you’re cloning from a repo)
* **Neo4j 4.x or 5.x** installed and running (`bolt://localhost:7687` by default)
* (Optional) **Docker** if you prefer running Neo4j in a container
* **curl** or **Postman** (for testing the API)

---

## 1. Create a Virtual Environment

1. Open a terminal and navigate to your project’s root folder (where `main.py` lives).

2. Create a new virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   * **macOS / Linux**:

     ```bash
     source .venv/bin/activate
     ```

   * **Windows (PowerShell)**:

     ```powershell
     .venv\Scripts\Activate.ps1
     ```

4. Confirm you’re in the virtual environment (you should see `(venv)` or `(.venv)` in your prompt).

---

## 2. Install Dependencies

With the virtual environment activated, install all required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Download and Prepare IMDb Data

You need four TSV files from the official IMDb datasets:

1. **title.basics.tsv.gz**
2. **title.ratings.tsv.gz**
3. **name.basics.tsv.gz**
4. **title.principals.tsv.gz**

### 3.1 Download the ZIPs

Visit the IMDb Bulk Data page:

> **Link:** [https://datasets.imdbws.com/](https://datasets.imdbws.com/)

Download these four files into your project’s `data/` directory (create it if it doesn’t exist):

```
your-project/
├── app/
│   └── (code files...)
└── data/
    ├── title.basics.tsv.gz
    ├── title.ratings.tsv.gz
    ├── name.basics.tsv.gz
    └── title.principals.tsv.gz
```

### 3.2 Extract the TSVs

In your terminal (while in the `data/` folder):

```bash
cd data/

# macOS / Linux:
gunzip title.basics.tsv.gz
gunzip title.ratings.tsv.gz
gunzip name.basics.tsv.gz
gunzip title.principals.tsv.gz

# Windows (PowerShell):
# Right-click each .gz file and choose “Extract Here” (or use 7-Zip).
```

After extraction, you should see:

```
data/
├── title.basics.tsv
├── title.ratings.tsv
├── name.basics.tsv
└── title.principals.tsv
```

---

## 4. Create a `.env` File

At the root of your project (next to `main.py`), create a file named `.env` and open it in your editor.

Fill it with the following environment variables (replace the placeholders with your actual keys/passwords):

```env
# Neo4j Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Zep Cloud (for memory)
ZEP_URL=https://api.zep.yourdomain.com
ZEP_API_KEY=your_zep_cloud_api_key

# OpenAI (if using OpenAI for LLM)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Ollama (if using Ollama instead of OpenAI)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:1b
```

> **Note:**
>
> * If you plan to use **OpenAI**, set only `OPENAI_API_KEY`.

---

## 5. Run the FastAPI Server

Make sure your virtual environment is still activated and Neo4j is running. Then, from the project root, run:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

* `main:app` points to the `app = FastAPI()` object inside `main.py`.
* `--reload` enables hot-reloading when code changes.
* By default, it listens on **[http://localhost:8000](http://localhost:8000)**.

You should see logs like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using statreload
INFO:     Started server process [12346]
...
```

---

## 6. Test the `/chat` Endpoint

You have two quick ways to test:

### 6.1 Using `curl` (macOS / Linux)

Open a new terminal (do not stop Uvicorn) and run:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test_session_1","user_message":"Which Nolan movies are rated above 8?"}'
```

You should get back a JSON response similar to:

```json
{
  "reply": "Here are Christopher Nolan’s top-rated movies:\n- Inception (2010) — Rating: 8.8\n- The Dark Knight (2008) — Rating: 9.0\n- Interstellar (2014) — Rating: 8.6\n…"
}
```

---

### 6.2 Using Postman

1. Open Postman and create a new **POST** request.
2. Set the URL to:

   ```
   http://localhost:8000/chat
   ```
3. Under the **Headers** tab, add:

   ```
   Content-Type: application/json
   ```
4. Under the **Body** tab, select **raw** and choose **JSON**. Paste the payload:

   ```json
   {
     "session_id": "test_session_1",
     "user_message": "Which Nolan movies are rated above 8?"
   }
   ```
5. Click **Send**. You should see the JSON response in Postman’s response pane.

---

Once you’ve followed all steps above, your IMDb Chatbot should be fully functional:

* It ingests structured (and optional unstructured) data into Neo4j via Graphiti.
* It uses Zep Cloud to store “last-turn” context.
* It calls your chosen LLM (OpenAI or Ollama) to transform queries → Cypher and generate final responses.
* You can now chat with the system by sending JSON to `http://localhost:8000/chat`. Good luck—and happy chatting!
