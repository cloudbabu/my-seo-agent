import streamlit as st
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup

st.set_page_config(page_title="Autonomous SEO Agent", layout="wide")

def get_google_suggestions(query):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={query}"
    try:
        r = requests.get(url, timeout=5)
        return json.loads(r.text)[1]
    except:
        return ["Error fetching data"]

st.title("🚀 Koray-Style Semantic SEO Agent")
st.write("Input a topic to generate a 6-month semantic roadmap.")

topic = st.text_input("Enter Topic", "Specialty Coffee")

if st.button("Generate Strategy"):
    with st.spinner("Mining Entities..."):
        queries = get_google_suggestions(topic)
        
        # Build roadmap logic
        data = []
        for i, q in enumerate(queries[:18]): # Top 18 queries
            month = (i // 3) + 1
            data.append({
                "Month": f"Month {month}",
                "Topic": q,
                "Type": "Pillar" if i < 3 else "Supporting Cluster",
                "Priority": "High" if month <= 2 else "Medium"
            })
        
        df = pd.DataFrame(data)
        st.table(df)
        
        csv = df.to_csv().encode('utf-8')
        st.download_button("Download CSV", csv, "roadmap.csv", "text/csv")