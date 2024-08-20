import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF for PDF handling
from dotenv import load_dotenv
import os
from io import BytesIO
import pandas as pd
import json
from streamlit_lottie import st_lottie 


# Load the environment variables from the .api file
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configure the GenAI API using the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')



def generate_pdf(content, filename):
    # Generate PDF content
    output = BytesIO()
    output.write(content.encode())
    return output

def generate_excel(results):
    df = pd.DataFrame([{
        "filename": r["filename"],
        "match": r["match"],
        "missing_keywords": ", ".join(r["missing_keywords"]),
        "summary": r["summary"]
    } for r in results])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output

def main():
    st.write("<h1><center>Applicant Tracking System</center></h1>", unsafe_allow_html=True)


    with open('src/ATS.json') as anim_source:
        animation = json.load(anim_source)
    st_lottie(animation, 1, True, True, "high", 200, -200)

    
    st.header('', divider='rainbow')

    st.markdown(
    """
    <div style="text-align: center;"> Paste job description</div>
    """,
    unsafe_allow_html=True
    )
    desc = st.text_area("")

    #Upload
    st.markdown(
    """
    <div style="text-align: center;">
        Upload <span style="color: green;">Multiple Resumes</span> and get Analytics details
    </div>
    """,
    unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader("", type="pdf", help="Please Upload PDF files Only", accept_multiple_files=True)
    submit = st.button("Submit")

    # Define custom CSS styles
    st.markdown("""
        <style>
        .card {
            border: 2px solid #000;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        .card-content {
            max-height: 150px;
            overflow-y: auto;
        }
        .percentage-high {
            color: green;
        }
        .percentage-low {
            color: red;
        }
        </style>
        """, unsafe_allow_html=True)

    if submit and uploaded_files:
        results = []

        for uploaded_file in uploaded_files:
            try:
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
                    text = ""
                    for page in pdf:
                        text += page.get_text()

                input_prompt = f'''
                You're a skilled ATS (Applicant Tracking System) Scanner with a deep understanding of tech roles, software development, 
                tech consulting, and understand the ATS role in-depth. Your task is to evaluate the resume against the given description. 
                You must consider that the job market is crowded with applications and you should only pick the best talent. 
                Thus, assign the percentage & MissingKeywords with honesty & accuracy
                resume: {text}
                description: {desc}
                I want an output in one single string of 70 words having the structure: {{"PercentageMatch": "%", "MissingKeywordsintheResume": [], "ProfileSummary": ""}}.
                '''

                with st.spinner(f"Evaluating {uploaded_file.name}..."):
                    response = model.generate_content(input_prompt)
                    response_text = response.text

                    # Parse JSON response
                    try:
                        result_data = json.loads(response_text)
                    except json.JSONDecodeError:
                        result_data = {
                            "PercentageMatch": "N/A",
                            "MissingKeywordsintheResume": ["Parsing Error"],
                            "ProfileSummary": response_text
                        }

                    # Display Results in Cards
                    percentage = result_data.get("PercentageMatch", "N/A")
                    if percentage != "N/A" and isinstance(percentage, str) and percentage.replace('%', '').isdigit():
                        percentage_value = int(percentage.replace('%', ''))
                    else:
                        percentage_value = 0

                    percentage_class = "percentage-low"
                    if percentage_value >= 65:
                        percentage_class = "percentage-high"

                    result = {
                        "filename": uploaded_file.name,
                        "match": percentage,
                        "missing_keywords": result_data.get("MissingKeywordsintheResume", []),
                        "summary": result_data.get("ProfileSummary", "N/A")
                    }
                    results.append(result)

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")

        if results:
            # Display Results in Cards
            st.subheader("ATS Scanner Dashboard")
            cols = st.columns(2)  # Adjust the number of columns as needed
            for index, result in enumerate(results):
                with cols[index % 2]:  # Alternate between columns
                    st.markdown(f"""
                        <div class="card">
                            <h3>{index + 1}. {result['filename']}</h3>
                            <p><strong>Match Percentage:</strong> <span class="{percentage_class}">{result['match']}</span></p>
                            <p><strong>Missing Keywords:</strong></p>
                            <div class="card-content">
                                {"".join(f"<p>- {keyword}</p>" for keyword in result['missing_keywords'])}
                            </div>
                            <p><strong>Profile Summary:</strong></p>
                            <div class="card-content">
                                {result['summary']}
                            </div>
                            <a href="data:application/pdf;base64,{generate_pdf(result['summary'], result['filename']).getvalue().decode('latin1')}" download="{result['filename']}">
                                <button>Download Resume</button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("---")

            # Option to download all results as Excel
            excel_button = st.download_button(
                label="Download All Results as Excel",
                data=generate_excel(results).getvalue(),
                file_name="ATS_Results.xlsx"
            )
        else:
            st.warning("No resumes were processed.")

if __name__ == "__main__":
    main()
