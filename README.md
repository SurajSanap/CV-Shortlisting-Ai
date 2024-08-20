# CV-Shortlisting-Ai

This project is an CV-Shortlisting-Ai that analyzes multiple resumes against a provided job description. It evaluates the match percentage, identifies missing keywords, and provides a summary for each resume. The results can be downloaded as a PDF or an Excel file.

## Features

- Upload multiple PDF resumes.
- Compare resumes with a provided job description.
- Get match percentage, missing keywords, and a summary for each resume.
- Display results in a user-friendly dashboard with styled cards.
- Download individual summaries as PDF.
- Download all results as an Excel file.

## Requirements

- Python 3.7 or higher

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ats-resume-analyzer.git
    cd ats-resume-analyzer
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.api` file in the root directory of the project and add your Google API key:

    ```bash
    GOOGLE_API_KEY=your-google-api-key
    ```

## Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run ats_resume_analyzer.py
    ```

2. **Navigate to the provided URL in your web browser.**

3. **Paste the job description and upload the resumes you want to analyze.**

4. **Click "Submit" to start the analysis.**

5. **View the analysis results in the dashboard and download them as needed.**

## Project Structure

- `ats_resume_analyzer.py`: Main application script.
- `.api`: Environment file for storing the Google API key.
- `requirements.txt`: File listing all the dependencies required to run the project.
- `src/ATS.json`: JSON file containing the Lottie animation used in the app.

## Dependencies

The project relies on the following Python packages:

- `streamlit`: Web application framework.
- `google-generativeai`: API client for Google Generative AI.
- `pymupdf`: For handling PDF files.
- `python-dotenv`: For loading environment variables from `.api` files.
- `pandas`: For handling data and exporting results to Excel.
- `openpyxl`: Excel file manipulation library.
- `streamlit-lottie`: For integrating Lottie animations in Streamlit.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Generative AI](https://ai.google/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Lottie Animations](https://lottiefiles.com/)


