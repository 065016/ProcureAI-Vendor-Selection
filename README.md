# ProcureAI
AI-powered vendor selection decision-support prototype.

## Run
`pip install -r requirements.txt`
`streamlit run app.py`

## Gemini
Set `GEMINI_API_KEY` and optionally `GEMINI_MODEL` in Streamlit Secrets/environment. No key is stored in the repository.

## Data
`sample_vendors_10.csv`, `sample_vendors_250.csv`, `test_vendors_invalid.csv` are synthetic.

## Deployment
Deploy `app.py` to Streamlit Community Cloud, configure Secrets, then verify the live URL before submission.
