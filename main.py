# main.py

from transformers import pipeline
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import subprocess
from markdown import markdown

import speech_recognition as sr
import pyttsx3

# === Init TTS engine ===
engine = pyttsx3.init()
engine.setProperty("rate", 170)


def speak(text):
    print(f"\n🔊 Speaking summary...")
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak your query...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(f"🗣️ You said: {query}")
        return query
    except sr.UnknownValueError:
        print("❌ Could not understand. Try again.")
        return None
    except sr.RequestError:
        print("❌ Could not request results from Google Speech.")
        return None


# === Load model ===
generator = pipeline("text2text-generation", model="google/flan-t5-small", framework="pt")


def search_web(query, max_results=3):
    print("🔍 Searching the web...")
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return [r["href"] for r in results if "href" in r]


def scrape_text(url):
    print(f"🌐 Scraping: {url}")
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        return text[:3000]
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return ""


def chunk_text(text, max_chars=1000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def remove_duplicates(text):
    seen = set()
    result = []
    for sentence in text.split('. '):
        sentence = sentence.strip()
        if sentence and sentence not in seen:
            seen.add(sentence)
            result.append(sentence)
    return '. '.join(result)


def summarize(text):
    print("🧠 Summarizing...")
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks[:3]:
        result = generator(f"summarize: {chunk}", max_new_tokens=150)[0]["generated_text"]
        summaries.append(result.strip())
    final_summary = " ".join(summaries)
    return remove_duplicates(final_summary)


def sanitize_filename(text):
    text = re.sub(r'\W+', '_', text.lower())
    return text[:50]


def save_summary(query, summary):
    filename = f"{sanitize_filename(query)}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 📄 Research Summary: {query}\n\n")
        f.write(summary)

    print(f"\n✅ Summary saved to `{filename}`")

    try:
        subprocess.run(["open", filename])
    except Exception as e:
        print(f"⚠️ Could not auto-open file: {e}")


# === Main loop ===
print("🎙️ AI Research Agent with Voice — Ready (say 'exit' to quit)")

while True:
    mode = input("\nChoose mode — (1) Type or (2) Speak: ").strip()

    if mode == "1":
        user_query = input("You: ")
    elif mode == "2":
        user_query = listen()
        if not user_query:
            continue
    else:
        print("❌ Invalid option. Try again.")
        continue

    if user_query.lower() in ["exit", "quit"]:
        break

    urls = search_web(user_query)
    if not urls:
        print("❌ No results found.")
        continue

    combined_text = ""
    for url in urls:
        content = scrape_text(url)
        if content:
            combined_text += content + "\n\n"

    if not combined_text:
        print("❌ Could not fetch any content.")
        continue

    summary = summarize(combined_text)
    print(f"\n📄 Summary:\n{summary}")
    speak(summary)
    save_summary(user_query, summary)
