EpochTrek — Journey Through Time 🏛️
Discover how places evolve through history with AI-powered image analysis.
EpochTrek is an AI-powered historical photo comparison application that explores the transformation of landmarks, streets, and buildings over time. Upload a historical photograph, identify its likely location using Google Gemini, find candidate photographs from Wikimedia Commons, and compare visible changes between the two images.
<p align="center">
  <a href="https://epochtrek.streamlit.app/"><strong>🚀 Launch EpochTrek</strong></a>
  &nbsp; · &nbsp;
  <a href="https://github.com/breddyraghav/EpochTrek">View Source Code</a>
</p>

📸 About the Project
Every place has a story. EpochTrek helps uncover it by connecting historical photographs with real images from online archives.
The application combines image analysis provided by Google's Gemini model with image discovery through Wikimedia Commons. It then generates an AI-assisted comparison highlighting visible architectural, environmental, and structural differences.
The goal is to make exploring historical changes more accessible, interactive, and informative.
✨ Features
- AI-Powered Location Identification — Analyze uploaded photographs to estimate the city, landmark, country, and historical period.
- Historical Image Upload — Upload JPG, JPEG, PNG, or WebP photographs.
- Archive Image Search — Search Wikimedia Commons for candidate photographs matching the identified location.
- Then vs. Now Comparison — View the uploaded historical photograph alongside a candidate archive image.
- Visual Change Analysis — Generate an AI-assisted summary of visible differences between photographs.
- Confidence Assessment — Review the AI's confidence and visual clues behind its location hypothesis.
- Image Source Information — Access available image metadata, author information, and licensing details.
- Museum-Inspired Interface — Explore the application through a cinematic, editorial-style design.
🔄 How It Works
1. Upload: Select a historical photograph of a recognizable place.
2. Identify: Gemini analyzes visual clues and proposes a likely location.
3. Discover: EpochTrek searches Wikimedia Commons for relevant photographs.
4. Compare: Gemini analyzes the historical upload and the selected archive image.
5. Explore: Review the location hypothesis, photographs, visible changes, and source information.
🛠️ Technology Stack
Technology	Purpose
Python	Application logic
Streamlit	Interactive web interface
Google Gemini API	Image analysis and location identification
Google Gen AI SDK	Integration with Gemini
Wikimedia Commons API	Image discovery and metadata
Requests	HTTP requests and image retrieval
Git and GitHub	Version control and collaboration
Streamlit Community Cloud	Application deployment


🚀 Live Demo
Try EpochTrek: https://epochtrek.streamlit.app/
No local installation is required to try the hosted application. Availability depends on deployment status and the external APIs it uses.
💻 Run Locally
Prerequisites
- Python 3.10 or a compatible version supported by the dependencies
- Git
- A Google Gemini API key with access to the configured model
1. Clone the repository
git clone https://github.com/breddyraghav/EpochTrek.git
cd EpochTrek
2. Create and activate a virtual environment
Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
4. Configure your Gemini API key
Create .streamlit/secrets.toml and add:
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
Replace the placeholder with your actual key. You can create or manage a key in Google AI Studio.
Security: Never commit a real API key or populated .streamlit/secrets.toml to GitHub. Configure the key separately in Streamlit Community Cloud's Secrets settings.
5. Start EpochTrek
python -m streamlit run app.py
Open the local URL Streamlit prints, usually http://localhost:8501.
☁️ Deployment
EpochTrek is designed for Streamlit Community Cloud.
To deploy your own instance:
1. Sign in to Streamlit Community Cloud with GitHub.
2. Select the breddyraghav/EpochTrek repository.
3. Select the main branch and set the main file to app.py.
4. Add GEMINI_API_KEY in the app's Secrets settings using TOML format.
5. Deploy the application.
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
Keep real credentials out of your repository, logs, and screenshots.
📁 Project Structure
EpochTrek/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── test_gemini.py
└── test_page.py
The exact files in your local checkout may differ. A real secrets.toml should remain private and should not be committed.
🤝 Collaboration & Contributions
Ideas, feedback, bug reports, and contributions are welcome.
Potential areas for collaboration include:
- Improving location estimation and image matching.
- Enhancing the comparison experience and accessibility.
- Refining UI design and mobile layouts.
- Improving testing, error handling, and reliability.
- Expanding documentation and image-source attribution.
Contributing
1. Fork the repository.
2. Create a branch for your change.
3. Implement and test your work.
4. Open a pull request describing the change.
For substantial changes, open an issue first so the approach can be discussed.
Repository: breddyraghav/EpochTrek
⚠️ Limitations
EpochTrek is an exploratory project, not a historical verification system.
- AI location estimates can be inaccurate.
- An archive result may show a different date, viewpoint, or even a different location.
- The retrieved image is not guaranteed to represent the present day.
- AI summaries may omit details or misinterpret visual differences.
Verify locations, dates, and image sources independently before drawing historical conclusions.
🙏 Acknowledgements
- Google Gemini — AI-assisted image analysis.
- Wikimedia Commons — image discovery and media metadata.
- Streamlit — Python web application framework.
👨‍💻 Author
B. Reddy Raghav
Engineering student interested in Python, AI-powered applications, and building practical software projects.
- GitHub: @breddyraghav
- Project: EpochTrek
- Live Demo: epochtrek.streamlit.app
📄 License
No license is currently specified in this README. Add a license file if you want to grant others explicit permission to use, modify, or redistribute this project.
<p align="center">
  <strong>EpochTrek — Explore the past. Understand the present.</strong>
</p>