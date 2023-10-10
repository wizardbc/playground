# ChatGPT Playground
Put your OpenAI API Key in `.streamlit/secrets.toml`.
```config
OPENAI_API_KEY = "YOUR_API_KEY"
```
Run streamlit app.
```bash
pip install -r requirements.txt
streamlit run chatbot.py
```
Dependency: `openai`, `streamlit`.