import streamlit as st
from transformers import pipeline

# ✅ Set page config as the first Streamlit command
st.set_page_config(page_title="AI Text Summarizer", page_icon="📝", layout="wide")

# Load the summarization model
@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")  # 🔄 Better model

summarizer = load_model()

# Function to split long text
def split_text(text, max_chars=800):
    sentences = text.split(". ")
    chunks, chunk = [], ""

    for sentence in sentences:
        if len(chunk) + len(sentence) < max_chars:
            chunk += sentence + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + ". "

    chunks.append(chunk.strip())  # Add last chunk
    return chunks

# App Title
st.title("📝 AI-Powered Text Summarizer")
st.write("Enter a paragraph and get a concise summary!")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    max_len = st.slider("Max Summary Length", 100, 500, 200)  # Increased max length
    min_len = st.slider("Min Summary Length", 20, 150, 50)
    st.markdown("---")
    st.write("Built with ❤️ using Transformers & Streamlit")

# Input Text Box
user_input = st.text_area("✍️ Enter Text to Summarize:", "", height=200)

# Summarization Button
if st.button("🔍 Summarize"):
    if len(user_input) < 20:
        st.warning("⚠️ Please enter at least 20 characters.")
    else:
        with st.spinner("Generating summary... ⏳"):
            text_chunks = split_text(user_input)
            summaries = [summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text'] for chunk in text_chunks]
            final_summary = " ".join(summaries)

        st.subheader("📜 Summary:")
        st.success(final_summary)
