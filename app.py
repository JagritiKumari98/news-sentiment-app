import streamlit as st
import requests

# Set Page Configuration
st.set_page_config(page_title="News Sentiment Analyzer", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f8;
        }
        .stApp {
            background-color: #f4f4f8;
            padding: 10px;
        }
        .stButton>button {
            background-color: #0078D7;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }
        .summary-box {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px #ccc;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>📰 News Sentiment Analyzer</div>", unsafe_allow_html=True)

# Dropdown for selecting company
companies = ["Tesla", "Apple", "Microsoft", "Amazon", "Google", "TVS", "Flipkart", "Meesho", "YouTube", "PWC"]
company_name = st.selectbox("🔍 Select a Company", companies)

if st.button("Fetch News & Summarize"):
    st.write(f"📡 Fetching latest news for: **{company_name}**")

    # API Request
    api_url = "http://127.0.0.1:8000/summarize"  # Updated to correct FastAPI port
    payload = {"text": company_name}
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise error for HTTP errors
        data = response.json()
        
        # Ensure "Articles" exists
        if "Articles" not in data or not data["Articles"]:
            st.error("⚠️ No articles found. Try another company.")
            st.stop()

        # Display Articles
        st.subheader("📖 Extracted News Articles:")
        for article in data["Articles"]:
            st.markdown(
                f"""
                <div class='summary-box'>
                    <h4>{article['Title']}</h4>
                    <p>{article['Summary']}</p>
                    <a href="{article['URL']}" target="_blank">🔗 Read More</a>
                    <p>📊 Sentiment: <b>{article['Sentiment']}</b></p>
                </div>
                """, unsafe_allow_html=True
            )

        # Sentiment Analysis Summary
        sentiment_data = data.get("Comparative Sentiment Score", {}).get("Sentiment Distribution", {})
        st.subheader("📊 Sentiment Analysis Overview")
        st.write(f"✅ Positive: {sentiment_data.get('Positive', 0)} articles")
        st.write(f"❌ Negative: {sentiment_data.get('Negative', 0)} articles")
        st.write(f"⚖️ Neutral: {sentiment_data.get('Neutral', 0)} articles")

        # Text-to-Speech (Ensure audio file is retrieved)
        st.subheader("🔊 Listen in Hindi")
        tts_api_url = "http://127.0.0.1:8000/text-to-speech"  # Updated API URL
        tts_payload = {"text": data['Articles'][0]['Summary']}
        
        audio_response = requests.post(tts_api_url, json=tts_payload)

        if audio_response.status_code == 200:
            audio_data = audio_response.json()
            audio_path = audio_data.get("audio_path")

            if audio_path:
                st.audio(audio_path, format="audio/mp3")  # Ensure proper format
            else:
                st.error("⚠️ Audio file not found.")
        else:
            st.error("⚠️ Error generating audio.")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API request failed: {e}")
