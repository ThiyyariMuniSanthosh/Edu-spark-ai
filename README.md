# EduSpark AI: Stage 1 (Doubt Solver)

Ask study doubts by text, upload a PDF to get answers from your material, ask follow-up questions, and get explanations in English, Telugu, Hindi, Tamil, Kannada, or Malayalam.

This is Stage 1 of the EduSpark AI spec. Not included yet: accounts and login, saved history, teacher and admin features, image questions, notes, quizzes, and the study planner.

## Run on Replit
1. Create a new Python Repl and upload these files, or import the folder from GitHub.
2. Open Tools > Secrets and add `GEMINI_API_KEY` with a key from Google AI Studio.
3. Press Run and open the preview.

If Replit reports a port problem, open the Ports tab and make the port there match `.replit` and the run command (8080).

## Deploy on Streamlit Community Cloud (free)
1. Push this folder to a GitHub repository. Do not commit your key.
2. Go to share.streamlit.io, choose New app, select the repository, and set the main file to `app.py`.
3. Under Advanced settings > Secrets, add: `GEMINI_API_KEY = "your-key-here"`
4. Deploy. Streamlit gives you a public link like `https://your-name.streamlit.app`.

## Run on your computer
```
pip install -r requirements.txt
export GEMINI_API_KEY=your-key-here      (Windows: set GEMINI_API_KEY=your-key-here)
streamlit run app.py
```

## Limits
- Gemini free-tier quotas are set by Google and change over time. Check Google's Gemini API rate-limit docs before a demo. When a limit is hit, the app says so.
- PDFs must have selectable text, be 10 MB or less, and have 200 pages or fewer. Scanned PDFs need OCR, which is not in this version.
- AI answers can be wrong. Check important ones against your textbook.
- Chat history lasts only for the current browser session.
