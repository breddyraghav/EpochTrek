# EpochTrek

**Explore the past. Understand the present.**

EpochTrek is an AI-powered historical photo explorer that identifies locations in old photographs, finds reference images from Wikimedia Commons, and compares visible changes using Google Gemini.

[**Live Demo**](https://epochtrek.streamlit.app) · [**GitHub**](https://github.com/breddyraghav/EpochTrek)

## Features

- **Location Detection** — Estimate a photograph's location and historical period using AI.
- **Image Discovery** — Find candidate reference images from Wikimedia Commons.
- **Visual Comparison** — Summarize visible differences between photographs.
- **Source Attribution** — Access available image metadata and licensing information.

## Tech Stack

Python · Streamlit · Google Gemini · Wikimedia Commons API

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/breddyraghav/EpochTrek.git
cd EpochTrek
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your API key**

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Get an API key from [Google AI Studio](https://aistudio.google.com/).

**5. Run the application**

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## Limitations

- Location estimates and change summaries may be inaccurate.
- Reference images are not guaranteed to show the same location or viewpoint.
- Image dates and licensing must be verified from the original source.

EpochTrek is an exploratory project, not a substitute for verified historical research.

## Author

**B. Reddy Raghav**

[GitHub](https://github.com/breddyraghav)

## License

No license is currently included. All rights to the source code remain subject to applicable law unless a license is added.

---

*Every photograph is a fragment of history.*
