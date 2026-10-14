# EpochTrek — Journey Through Time

### Rediscover the Past. Explore the Present.

EpochTrek is an AI-powered web application that explores how places change over time through historical photographs. Using Google's Gemini AI and Wikimedia Commons, it estimates the location of an uploaded image, searches for a relevant comparison photograph, and generates an AI-assisted summary of visible changes.

<p align="center">
  <a href="https://epochtrek.streamlit.app/">
    <strong>Launch EpochTrek →</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="https://github.com/breddyraghav/EpochTrek">
    View Source Code
  </a>
</p>

---

## Overview

Places evolve. Buildings are reconstructed, streets transform, and landmarks change with time. Historical photographs preserve moments from the past, but understanding how those places look today can be difficult.

**EpochTrek bridges that gap** by combining AI-assisted image analysis with image search to create a visual Then & Now experience.

Upload a historical photograph, explore its estimated location, compare it with a potentially relevant image, and examine an AI-generated summary of visible differences.

## Key Features

- **Historical Photo Upload** — Upload a photograph of a recognizable landmark, building, street, or place.
- **AI-Powered Location Estimation** — Uses Google's Gemini model to estimate the likely location shown in the photograph.
- **Image Discovery** — Searches Wikimedia Commons for a suitable comparison image.
- **Then & Now Comparison** — View the uploaded historical photograph alongside the retrieved image.
- **AI-Assisted Change Summary** — Generate a description of visible differences between the two photographs.
- **Interactive Web Application** — Access the project through a Streamlit-powered interface.
- **Cloud Accessibility** — Explore the deployed application directly from your browser.

## Live Demo

**Try EpochTrek:** https://epochtrek.streamlit.app/

No local installation is required to access the hosted application. Availability and functionality depend on the deployment and external API services.

## How It Works

The application follows a five-step workflow:

1. **Upload** — Provide a historical photograph.
2. **Analyze** — Gemini examines the image and estimates its likely location.
3. **Discover** — The application searches Wikimedia Commons for a potential comparison image.
4. **Compare** — Review the historical photograph and the retrieved image.
5. **Understand** — Explore the AI-assisted summary of visible changes.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface and application deployment |
| Google Gemini API | AI-assisted image interpretation and analysis |
| Wikimedia Commons API | Search for comparison images |
| Requests | HTTP communication with external services |

## Getting Started

Run EpochTrek locally by following the steps below.

### Prerequisites

- Python 3.10 or newer
- Git
- A Google Gemini API key

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 1. Clone the repository

```bash
git clone https://github.com/breddyraghav/EpochTrek.git
cd EpochTrek
```

### 2. Create a virtual environment

**Windows — PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a file named `secrets.toml` inside the `.streamlit` directory.

Add the following configuration:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your actual API key.

The local configuration path should be:

```text
.streamlit/secrets.toml
```

**Security:** Never commit your actual API key to GitHub. Keep the local secrets file private and configure secrets separately when deploying the application.

### 4. Run the application

**Windows**

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS / Linux**

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit, usually:

http://localhost:8501

Upload a historical photograph and follow the instructions displayed in the application.

## Deployment

EpochTrek is hosted using [Streamlit Community Cloud](https://share.streamlit.io/).

To deploy your own instance:

1. Sign in to Streamlit Community Cloud using GitHub.
2. Select the `breddyraghav/EpochTrek` repository.
3. Choose the `main` branch.
4. Set the main file path to `app.py`.
5. Add the `GEMINI_API_KEY` value under **Advanced settings → Secrets**.
6. Deploy the application.

Use TOML format for the secret:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Never publish your real API key in source code, screenshots, or repository files.

## Project Structure

```text
EpochTrek/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    ├── config.toml
    └── secrets.toml.example
```

The actual `secrets.toml` file is created locally or configured through the deployment platform and should not be committed.

## Collaboration & Contributions

Contributions, suggestions, and ideas are welcome.

EpochTrek can benefit from improvements in AI, image retrieval, historical research, interface design, testing, and documentation.

### Areas for Collaboration

- Improving location estimation and image matching
- Enhancing visual comparison and change summaries
- Refining the user interface and accessibility
- Improving performance, error handling, and reliability
- Expanding testing and documentation

### How to Contribute

1. Fork the repository.
2. Create a branch for your changes.
3. Implement and test your improvements.
4. Submit a pull request with a clear description of your contribution.

For substantial changes, open an issue first to discuss the proposed solution.

**Repository:** [breddyraghav/EpochTrek](https://github.com/breddyraghav/EpochTrek)

## Limitations

EpochTrek is an exploratory application, not a historical verification system.

- AI-generated location estimates may be inaccurate.
- A retrieved image may depict a different year, location, or viewpoint.
- A comparison image is not necessarily a current photograph.
- AI-generated summaries may overlook details or misinterpret visual differences.

Always verify dates, locations, and image sources independently before drawing historical conclusions.

## Acknowledgements

- [Google Gemini](https://ai.google.dev/) — AI-assisted image analysis.
- [Wikimedia Commons](https://commons.wikimedia.org/) — image search and media resources.
- [Streamlit](https://streamlit.io/) — Python web application framework.

---

<p align="center">
  <strong>EpochTrek</strong><br>
  <em>Connecting the past with the present through AI.</em><br><br>
  <a href="https://epochtrek.streamlit.app/">Live Demo</a> ·
  <a href="https://github.com/breddyraghav/EpochTrek">GitHub Repository</a>
</p>