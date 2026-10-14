# EpochTrek — Journey Through Time

**Explore how places have changed over time using AI and historical photographs.**

EpochTrek is a Python-based web application that analyzes historical photographs, estimates their locations using Google's Gemini AI, searches Wikimedia Commons for comparison images, and summarizes visible changes between the past and present.

## Features

- **Historical Photo Upload:** Upload a photograph of an old building, landmark, street, or other recognizable place.
- **AI-Powered Location Identification:** Uses Google's Gemini model to estimate where the photograph was taken.
- **Then & Now Comparison:** Searches Wikimedia Commons for a potential comparison image.
- **Visual Change Analysis:** Generates an AI-assisted summary of visible differences between the two images.
- **Interactive Web Interface:** Provides a simple interface built with Streamlit.
- **Cloud Deployment:** Can be deployed using Streamlit Community Cloud.

## How It Works

1. Upload a historical photograph.
2. Gemini analyzes the image and estimates its likely location.
3. EpochTrek searches Wikimedia Commons for a suitable comparison image.
4. View the historical and comparison images side by side.
5. Read the AI-assisted summary of visible changes.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Google Gemini API | Image interpretation and change summaries |
| Wikimedia Commons API | Comparison image search |
| Requests | HTTP requests and API communication |

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Git
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Clone the Repository

```bash
git clone https://github.com/breddyraghav/EpochTrek.git
cd EpochTrek
```

### 2. Create a Virtual Environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure the Gemini API Key

Create a file named `secrets.toml` inside the `.streamlit` folder.

Your project should contain:

```text
.streamlit/
├── config.toml
├── secrets.toml.example
└── secrets.toml
```

Add the following to `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your actual API key.

**Security:** Never commit, publish, or share your real API key. Keep `secrets.toml` private and use Streamlit Secrets when deploying online.

### 4. Run EpochTrek Locally

**Windows:**

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS or Linux:**

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

http://localhost:8501

Upload a historical photograph and follow the on-screen instructions.

## Deploy on Streamlit Community Cloud

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Sign in with your GitHub account.
3. Create a new app using the repository `breddyraghav/EpochTrek`.
4. Select the `main` branch.
5. Set the main file path to `app.py`.
6. Open **Advanced settings → Secrets**.
7. Add your Gemini API key:

   ```toml
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
   ```

8. Deploy the application.

Keep your API key in Streamlit's Secrets settings rather than storing it in GitHub.

## Troubleshooting

| Problem | Suggested solution |
|---|---|
| Python is not recognized | Install Python and restart your terminal. |
| A package is missing | Run `pip install -r requirements.txt` in your virtual environment. |
| Gemini API key error | Check the `GEMINI_API_KEY` setting in your local secrets file or Streamlit Cloud. |
| API quota or permission error | Check your Google AI Studio project, API key, model access, and usage limits. |
| No suitable comparison image | Try a clearer photograph of a recognizable landmark. |
| Streamlit app does not start | Check the terminal for the full error message and verify the project dependencies. |

Remove any
