import streamlit as st
import pandas as pd
from transformers import pipeline

# Load CSV prompts (make sure this CSV exists in the same directory)
try:
    df = pd.read_csv("health_prompts.csv")
except FileNotFoundError:
    st.error("health_prompts.csv not found. Please upload it to run this app.")
    st.stop()

# Set up mock pipelines (using t5-small for simplicity)
medalpaca_pipe = pipeline("text2text-generation", model="t5-small")
pmc_llama_pipe = pipeline("text2text-generation", model="t5-small")

# Streamlit UI
st.title("Health Prompt Data Extraction App")
st.markdown("Compare two medical-focused LLMs: **MedAlpaca** and **PMC-LLaMA** using prompt-based data extraction.")

# Prompt selection
prompt = st.selectbox("Select a health prompt to extract from:", df["prompt"])

# Model choice
model_choice = st.radio("Select a model for extraction:", ["MedAlpaca", "PMC-LLaMA"])

# Run button
if st.button("Extract Information"):
    st.info(f"Running {model_choice} model...")

    if model_choice == "MedAlpaca":
        formatted_prompt = f"Extract medical information from: {prompt}"
        result = medalpaca_pipe(formatted_prompt, max_length=100)[0]["generated_text"]
    else:
        formatted_prompt = f"Answer clearly the medical prompt: {prompt}"
        result = pmc_llama_pipe(formatted_prompt, max_length=100)[0]["generated_text"]

    st.subheader("Model Output:")
    st.write(result)
