import streamlit as st
import pandas as pd
import requests
import json
import time
from bs4 import BeautifulSoup

# --- CONFIG & UI ---
st.set_page_config(page_title="Autonomous SEO Strategist", layout="wide")

def get_google_data(query):
    """Mines the semantic universe for a seed topic."""
    # Google Autocomplete (Semantic Universe)
    suggest_url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={query}"
    
    # People Also Ask / Search Results (Intent & Questions)
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        suggestions = json.loads(requests.get(suggest_url).text)[1]
        
        # Simple Scrape for Questions (PAA)
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        questions = [q.text for q in soup.find_all(['h3', 'span']) if "?" in q.text][:10]
        
        return suggestions, questions
    except:
        return [], []

def extract_entities(text_list):
    """Simulates NLP Entity extraction by identifying recurring technical nouns."""
    stop_words = ["how", "to", "the", "and", "best", "for", "with", "guide"]
    words = " ".join(text_list).lower().split()
    entities = [w.capitalize() for w in words if len(w) > 4 and w not in stop_words]
    return list(set(entities))[:15]

# --- MAIN DASHBOARD ---
st.title("🧠 Autonomous SEO Strategy Agent")
st.markdown("Enter a keyword to trigger a **Semantic Research Cycle**.")

seed_keyword = st.text_input("Enter Seed Keyword (e.g., 'Specialty Coffee'):", "")

if st.button("🚀 Start Autonomous Research"):
    if not seed_keyword:
        st.warning("Please enter a keyword.")
    else:
        # STEP 1: MINING
        with st.status("🔍 Scout Agent: Mining Semantic Universe...", expanded=True) as status:
            st.write("Fetching Autocomplete suggestions...")
            suggestions, questions = get_google_data(seed_keyword)
            time.sleep(1)
            
            st.write("Extracting recurring Entities and Nouns...")
            entities = extract_entities(suggestions + questions)
            status.update(label="Research Complete!", state="complete")

        # DISPLAY RESULTS
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Knowledge Domain Entities")
            st.info("These are the core 'Nouns' that define your topical authority.")
            st.write(entities)
            
        with col2:
            st.subheader("❓ User Questions (PAA)")
            st.write(questions)

        # STEP 2: STRATEGY & ROADMAP
        st.divider()
        st.subheader("📅 6-Month Topical Wave Roadmap")
        st.caption("Strategic grouping of topics to build 'Source of Truth' status.")
        
        roadmap_data = []
        for i, topic in enumerate(suggestions[:18]):
            month = (i // 3) + 1
            roadmap_data.append({
                "Month": f"Month {month}",
                "Topic": topic,
                "Intent": "Informational" if "?" in topic else "Commercial",
                "Weight": "Pillar" if i < 3 else "Supporting",
                "Priority": "🔥 Critical" if month == 1 else "Normal"
            })
        
        df = pd.DataFrame(roadmap_data)
        st.table(df)

        # STEP 3: EXPORT
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Strategy to CSV", csv, "seo_strategy.csv", "text/csv")
