# EpochTrek — Journey Through Time

This guide is written for a Windows laptop using VS Code. Follow the steps in order.

## A. Open the correct folder

1. Download and extract `epochtrek-starter.zip`.
2. In VS Code select **File → Open Folder**.
3. Open the folder named **epochtrek** (the folder that contains `app.py` and `requirements.txt`).
4. Select **Terminal → New Terminal**.

## B. Check Python

In the VS Code terminal, run:

```powershell
py --version
```

You should see Python 3.10 or newer. If `py` is not recognized, install Python from https://www.python.org/downloads/ and tick **Add python.exe to PATH** during setup. Restart VS Code after installation.

## C. Set up the project

Run these commands one at a time in the VS Code terminal:

```powershell
py -m venv .venv
```

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
```

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

These commands do not require activating the virtual environment. Wait for each command to finish before running the next.

## D. Add your Gemini key

1. In VS Code Explorer, open the `.streamlit` folder.
2. Create a new file inside it named exactly `secrets.toml` (not `secrets.toml.txt`).
3. Paste the following and replace the text inside quotes with your key from https://aistudio.google.com/apikey:

```toml
GEMINI_API_KEY = "PASTE_YOUR_REAL_KEY_HERE"
```

4. Save the file. Never share the key or commit `secrets.toml` to GitHub. The `.gitignore` file excludes it.

## E. Run EpochTrek locally

In the VS Code terminal, run:

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

Your browser should open. If it does not, open http://localhost:8501. Upload a clear old photo of a recognizable landmark, then click **Identify place & compare with today**. Keep the terminal open while using the app. To stop it, click the terminal and press `Ctrl+C`.

## F. If something goes wrong

- **`py` is not recognized**: install Python and restart VS Code.
- **`No module named streamlit`**: run the install commands in section C again.
- **Gemini API key not found**: confirm `.streamlit/secrets.toml` exists in this project and its line is `GEMINI_API_KEY = "..."`; then stop and restart Streamlit.
- **Invalid API key / permission / quota error**: recheck the key in AI Studio and account/model limits. Do not post the key in a screenshot.
- **No image found**: try a more recognizable landmark. Wikimedia Commons may not have a suitable matching image.
- **PowerShell command confusion**: paste one command at a time into VS Code's terminal, not into a Python `>>>` prompt.

If you get an error, copy the full red error text from the VS Code terminal and send it, but remove any API key first.

## G. Push to GitHub (after local run works)

1. Create an empty repository named `epochtrek` at https://github.com/new.
2. In VS Code's terminal, make sure you are in the folder containing `app.py`.
3. Run these commands one at a time, replacing `YOUR_USERNAME` with your GitHub username:

```bash
git init
git add .
git status
```

Check that `.streamlit/secrets.toml` is NOT listed. If it is listed, stop and do not commit.

```bash
git commit -m "Build EpochTrek historical photo comparison app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/epochtrek.git
git push -u origin main
```

If Git asks you to configure your name/email, follow the message it prints and then repeat the commit.

## H. Deploy with Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app**. Select your `epochtrek` repository, branch `main`, and file path `app.py`.
3. Open **Advanced settings → Secrets** and paste the same TOML setting from section D, with your real key.
4. Choose a supported Python version (3.11 or 3.12) if prompted, then deploy.
5. Keep the local `secrets.toml` private; only enter the secret through Streamlit's Secrets interface.

## Project files

```text
epochtrek/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    ├── config.toml
    ├── secrets.toml.example
    └── secrets.toml       # create this yourself; do not upload it
```

## Important note about results

The app uses AI to estimate the location and Wikimedia Commons to search for a comparison image. The second image may not be a recent photo or the exact same viewpoint. Always check its source and treat AI-generated differences as suggestions, not verified history.
