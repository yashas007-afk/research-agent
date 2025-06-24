# 🧠 Terminal AI Research Agent

A minimal AI-powered assistant that runs in the terminal and helps you generate research summaries from any natural language topic. Built using Hugging Face Transformers and the FLAN-T5 model.

---

## 🚀 Features

- ✅ Terminal-based interface (no web UI)
- 🤖 Uses `flan-t5-small` model from Hugging Face
- 📄 Generates clear, concise summaries
- 💻 CPU-compatible (no GPU required)
- 🧩 Simple and extendable codebase (`main.py`)

---

## 📦 Requirements

Install the required Python package:

```bash
pip install transformers
python main.py

Ask your AI Assistant (or type 'exit'): tell me about M3 chip in apple products

📄 AI: The M3 chip is Apple’s advanced silicon designed using a 3nm process. It improves speed, battery efficiency, and is optimized for AI workloads in the latest Macs.

main.py       # The AI assistant script
README.md     # This file


You can change the model or prompt format by editing this line in main.py
generator = pipeline("text2text-generation", model="google/flan-t5-small")

