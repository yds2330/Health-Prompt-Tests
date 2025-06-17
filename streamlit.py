import streamlit as st
import pandas as pd
import requests

@st.cache_data
def load_prompts(file_path):
    return pd.read_csv(file_path)

st.title("Health Ailment Prompts")

#upload prompts file
st.sidebar.header("Dataset Options")
file = st.sidebar.file_uploader("Upload Prompts CSV", type=["csv"])
if file:
    prompts_df = load_prompts(file)
else:
    st.warning("Please upload your prompts CSV file to begin.")
    st.stop()

#check for required columns
required_columns = ['prompt', 'health_ailment', 'date']
missing = [col for col in required_columns if col not in prompts_df.columns]
if missing:
    st.error(f"Missing columns in CSV: {', '.join(missing)}")
    st.stop()

#filter non-unique options
health_ailments = prompts_df['health_ailment'].unique()
dates = prompts_df['date'].unique()

selected_ailment = st.sidebar.selectbox("Health Ailment", options=health_ailments)
selected_date = st.sidebar.selectbox("Date", options=dates)

filtered_df = prompts_df[
    (prompts_df['health_ailment'] == selected_ailment) &
    (prompts_df['date'] == selected_date)
]

st.subheader("Filtered Prompts")
st.dataframe(filtered_df[['prompt', 'health_ailment', 'date']])

#prompt details & retrieval
if not filtered_df.empty:
    prompt_row = filtered_df.iloc[0]
    st.markdown("### Prompt Details")
    st.write(f"**Prompt:** {prompt_row['prompt']}")
    st.write(f"**Health Ailment:** {prompt_row['health_ailment']}")
    st.write(f"**Date:** {prompt_row['date']}")

    if st.button("Fetch Data for Prompt"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/retrieve",
                json={"prompt": prompt_row['prompt']}
            )
            if response.status_code == 200:
                st.success("Data fetched successfully from API!")
                st.write(response.json())
            else:
                st.error(f"API returned error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Failed to fetch data from API: {e}")


#upload test results
st.header("Test Results Validation")
test_file = st.file_uploader("Upload Test Results CSV", type=["csv"], key="test_results")
if test_file:
    test_df = pd.read_csv(test_file)
    st.write(test_df.head())
    st.write(f"Total test cases: {len(test_df)}")
    st.write(f"Successful retrievals: {(test_df['result'] == 'success').sum()}")

