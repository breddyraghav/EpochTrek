from pathlib import Path
import re
from google import genai

print("EpochTrek - Gemini Diagnostic")
print("=" * 35)

secret_file = Path(".streamlit/secrets.toml")

if not secret_file.exists():
    raise SystemExit("ERROR: secrets.toml was not found.")

content = secret_file.read_text(encoding="utf-8")

match = re.search(
    r'^\s*GEMINI_API_KEY\s*=\s*["\'](.*?)["\']\s*$',
    content,
    re.MULTILINE,
)

if not match or not match.group(1).strip():
    raise SystemExit("ERROR: Check GEMINI_API_KEY in secrets.toml.")

api_key = match.group(1).strip()
client = genai.Client(api_key=api_key)

models = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]

for model in models:
    print(f"\nTesting model: {model}")

    try:
        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: EpochTrek works"
        )

        print("SUCCESS:", model)
        print("Response:", response.text)
        break

    except Exception as error:
        print("FAILED:", type(error).__name__)
        print("Details:", str(error))

else:
    print("\nNeither model succeeded.")
    print("Both requests failed. Check the exact errors above.")