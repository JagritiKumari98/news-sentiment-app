import streamlit as st
import requests

# ---- Apply Custom CSS Styling ----
st.markdown(
    """
    <style>
    /* Background Color */
    .stApp {
        background-color: #f0f2f6;
    }

    /* Title Style */
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #3366cc;
        text-align: center;
    }

    /* Text Input Box */
    .stTextInput {
        background-color: white;
        border: 2px solid #3366cc;
        padding: 10px;
        border-radius: 5px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        transition: 0.3s;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- UI Title ----
st.markdown('<p class="title">📰 News Sentiment Analyzer</p>', unsafe_allow_html=True)

# ---- Company Selection with Dropdown ----
company_list = ["Tesla", "Microsoft", "Google", "Amazon", "Apple", "TVS", "Flipkart", "Meesho", "Youtube", "PWC"]
company_name = st.selectbox("Select a Company", company_list)

if st.button("Fetch News"):
    st.write(f"🔍 Searching news for: {company_name}")

    # API Request to Backend
    api_url = "http://127.0.0.1:5000/summarize"
    payload = {"text": f"{company_name} latest news"}  

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        data = response.json()

        # Display News Summary
        st.subheader(f"**{company_name} News Summary**")
        st.write(f"📖 {data['summary']}")

        # Add Sentiment Analysis
        st.write(f"📊 **Sentiment:** `{data.get('sentiment', 'N/A')}`")

        # Hindi Text-to-Speech
        if st.button("Listen in Hindi 🎙️"):
            st.audio("http://127.0.0.1:5000/audio")  

    else:
        st.error("⚠️ Error fetching news! Try again.")
