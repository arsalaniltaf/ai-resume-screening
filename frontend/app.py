import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://backend:8000/rank"

st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("🤖 AI Resume Screening & Ranking System")
st.markdown(
    "Upload resumes and compare them against a job description using semantic similarity."
)

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    job_description = st.text_area("📌 Enter Job Description", height=250)

with col2:
    st.markdown("### 💡 Instructions")
    st.markdown("""
    - Enter job description  
    - Upload resumes  
    - Click **Rank Candidates**  
    - View candidate match scores and matched keywords  
    """)

uploaded_files = st.file_uploader(
    "📄 Upload Resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if st.button("🚀 Rank Candidates"):

    if not job_description:
        st.warning("Please enter a job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes..."):

            files = []
            for file in uploaded_files:
                files.append(
                    ("resumes", (file.name, file.getvalue(), file.type))
                )

            data = {
                "job_description": job_description
            }

            try:
                response = requests.post(
                    BACKEND_URL,
                    files=files,
                    data=data
                )

                if response.status_code == 200:
                    results = response.json().get("rankings", [])

                    if results:

                        st.success("Ranking Complete ✅")

                        # Convert to DataFrame
                        df = pd.DataFrame(results)

                        # Keep numeric version for progress bars
                        df_numeric = df.copy()

                        # Add ranking index
                        df.index = df.index + 1
                        df.index.name = "Rank"

                        # Format score as percentage
                        df["score"] = df["score"].round(2).astype(str) + " %"

                        st.dataframe(df[["candidate", "score"]], use_container_width=True)

                        st.markdown("## 📊 Detailed Results")

                        for idx, row in df_numeric.iterrows():

                            st.markdown(f"### {idx+1}. {row['candidate']}")
                            st.markdown(f"**Match Score:** {round(row['score'], 2)} %")
                            st.progress(row["score"] / 100)

                            matched = row.get("matched_keywords", [])

                            if matched:
                                st.markdown("**Matched Keywords:**")
                                st.write(", ".join(matched))
                            else:
                                st.markdown("No strong keyword matches found.")

                            st.divider()

                    else:
                        st.error("No results returned from backend.")

                else:
                    st.error("Backend error occurred.")

            except Exception as e:
                st.error(f"Connection failed: {e}")
