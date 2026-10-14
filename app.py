import json
import os
import re
from html import unescape

import requests
import streamlit as st
from google import genai
from google.genai import types

APP_NAME = "EpochTrek"
GEMINI_MODEL = "gemini-3.5-flash-lite"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

st.set_page_config(
    page_title="EpochTrek | Then vs Now",
    page_icon="🌌",
    layout="wide",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"], button, input, textarea, select {
        font-family: "Times New Roman", Times, serif !important;
    }
    .stApp { background-color: #101820; color: #eaf0f3; }
    .block-container { max-width: 1050px; padding: 2rem 1.25rem 3rem; }
    .brand { font-size: 1.4rem; font-weight: 700; letter-spacing: .12em; color: #ffffff; }
    .eyebrow { color: #b7e4d1; letter-spacing: .12em; text-transform: uppercase; font-size: .75rem; font-weight: 700; }
    .hero { font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.12; font-weight: 700; margin: .65rem 0 .85rem; color: #f5f8f9; }
    .sub { color: #c0cbd1; font-size: 1.05rem; line-height: 1.6; max-width: 700px; }
    .small-label { color: #b7e4d1; font-size: .78rem; letter-spacing: .1em; font-weight: 700; text-transform: uppercase; }
    .result-title { font-size: 1.5rem; font-weight: 700; color: #f4f7f8; overflow-wrap: anywhere; }
    [data-testid="stFileUploader"] { border: 1px dashed #607580; border-radius: 14px; padding: 10px; }
    .stButton > button { background: #b7e4d1; color: #10251e; border-radius: 10px; min-height: 46px; white-space: normal; }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_api_key():
    """Read the Gemini key from Streamlit secrets or an environment variable."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return str(key).strip()
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "").strip()


def extract_json(response_text):
    """Parse JSON returned by Gemini, tolerating optional Markdown fences."""
    text = (response_text or "").strip()
    text = re.sub(r"^\s*```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```\s*$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise ValueError("The AI response was not valid JSON. Please try another image.")
        return json.loads(match.group(0))


def identify_location(client, image_bytes, mime_type):
    prompt = """You are an expert visual geolocation assistant. Analyze the uploaded historical photograph.

Return ONLY valid JSON with these keys:
{
  "identified": true,
  "city": "likely city or Unknown",
  "landmark": "specific landmark or area, or Unknown",
  "country": "country or Unknown",
  "confidence": "High, Medium, or Low",
  "confidence_reason": "short reason based only on visual evidence",
  "visual_clues": ["clue 1", "clue 2"],
  "estimated_period": "approximate decade or Unknown",
  "search_query": "short search phrase for finding a modern photo of this exact location"
}

Never claim certainty from weak clues. If the location is not identifiable, set identified=false and confidence=Low. Prefer a specific landmark or street over just a city. Do not infer an exact year unless visible evidence supports it. Search for a real photograph, not an AI-generated image."""
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[prompt, image_part],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    return extract_json(response.text)


def commons_search(query, limit=8):
    """Search Wikimedia Commons for image files matching a location query."""
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"{query} filetype:bitmap",
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": 1400,
    }
    headers = {"User-Agent": "EpochTrek/1.0 (student historical photo comparison project)"}
    response = requests.get(COMMONS_API, params=params, headers=headers, timeout=25)
    response.raise_for_status()
    payload = response.json()
    pages = payload.get("query", {}).get("pages", {})
    images = []

    for page in pages.values():
        info_list = page.get("imageinfo", [])
        if not info_list:
            continue
        info = info_list[0]
        metadata = info.get("extmetadata", {})
        url = info.get("thumburl") or info.get("url")
        if not url:
            continue

        def meta_value(name):
            return unescape(re.sub(r"<[^>]+>", "", metadata.get(name, {}).get("value", "")))

        images.append(
            {
                "title": page.get("title", "Untitled image").replace("File:", ""),
                "url": url,
                "page_url": info.get("descriptionurl", "https://commons.wikimedia.org/"),
                "date": meta_value("DateTimeOriginal") or meta_value("DateTime") or "Date not provided",
                "license": meta_value("LicenseShortName") or "License not listed in metadata",
                "artist": meta_value("Artist") or "Author not listed",
                "description": meta_value("ImageDescription")[:400],
            }
        )
    return images


def analyze_changes(client, old_bytes, old_mime, new_bytes, new_mime, location):
    prompt = f"""Compare these two photographs for a student project called EpochTrek. The first image is the user's historical upload; the second is a candidate image found on Wikimedia Commons.

Location hypothesis: {location.get('landmark', 'Unknown')}, {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}.

Compare only visible evidence. If the images show different viewpoints or you cannot verify that they depict the same place, say so and do not invent changes.

Return ONLY JSON:
{{
  "same_location_assessment": "Likely same place / Possibly same place / Not enough evidence",
  "summary": "2-3 sentences",
  "changes": [
    {{"category":"Architecture", "then":"visible older-photo detail", "now":"visible newer-photo detail", "confidence":"High/Medium/Low"}}
  ],
  "caution": "one short limitation statement"
}}

Include 3-5 changes only when supported. Describe visible differences, not unsupported claims about why they happened. Do not state the modern image's date unless metadata confirms it."""
    parts = [
        prompt,
        types.Part.from_bytes(data=old_bytes, mime_type=old_mime),
        "Candidate image retrieved from Wikimedia Commons:",
        types.Part.from_bytes(data=new_bytes, mime_type=new_mime),
    ]
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=parts,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.25,
        ),
    )
    return extract_json(response.text)


# Header — native Streamlit elements, no logo
st.markdown("<div class='brand'>EPOCHTREK</div>", unsafe_allow_html=True)
st.caption("THEN VS NOW")
st.write("")
st.markdown("<div class='eyebrow'>A visual journey through time</div>", unsafe_allow_html=True)
st.title("Every place has a story to tell.")
st.write(
    "Upload one old photograph. EpochTrek identifies the likely place, finds a real image "
    "from an online archive, and explains what appears to have changed."
)
st.write("")

with st.container(border=True):
    st.markdown('<div class="small-label">01 / YOUR HISTORICAL PHOTO</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload a historical photograph",
        type=["jpg", "jpeg", "png", "webp"],
        help="Clear photos of landmarks, streets, buildings, and public places work best.",
        label_visibility="collapsed",
    )
    if uploaded:
        st.image(
            uploaded.getvalue(),
            caption=f"Uploaded photograph · {uploaded.name}",
            width=460,
        )
    st.caption("Tip: choose a photo with recognizable buildings, signs, monuments, or street layouts.")
    analyze_clicked = st.button(
        "Identify place & compare with today  →",
        type="primary",
        use_container_width=True,
        disabled=uploaded is None,
    )

if analyze_clicked and uploaded:
    api_key = get_api_key()
    if not api_key:
        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY to "
            ".streamlit/secrets.toml and restart the app."
        )
        st.stop()

    client = genai.Client(api_key=api_key)
    image_bytes = uploaded.getvalue()
    mime_type = uploaded.type or "image/jpeg"

    try:
        with st.status("Reading visual clues in your photograph…", expanded=True) as status:
            st.write("Step 1 of 3 · Identifying the likely location")
            location = identify_location(client, image_bytes, mime_type)
            city = location.get("city", "Unknown")
            landmark = location.get("landmark", "Unknown")
            country = location.get("country", "Unknown")
            st.write(f"Location hypothesis: {landmark}, {city}, {country}")

            if not location.get("identified", False) or location.get("confidence", "Low").lower() == "low":
                status.update(label="Location could not be identified confidently", state="error", expanded=True)
                st.warning(
                    "The visual evidence is not strong enough to identify a reliable location. "
                    "Try a clearer photo showing a landmark, sign, or distinctive building."
                )
                st.json(location)
                st.stop()

            st.write("Step 2 of 3 · Searching Wikimedia Commons for a real image")
            search_query = location.get("search_query") or f"{landmark} {city} {country}"
            images = commons_search(search_query)
            if not images:
                images = commons_search(f"{landmark} {city} {country}")
            if not images:
                status.update(label="No suitable image found", state="error", expanded=True)
                st.error("Wikimedia Commons did not return a usable image. Try a better-known landmark.")
                st.stop()

            modern = images[0]
            st.write("Step 3 of 3 · Comparing the two photographs")
            modern_response = requests.get(
                modern["url"],
                timeout=25,
                headers={"User-Agent": "EpochTrek/1.0 (student project)"},
            )
            modern_response.raise_for_status()
            modern_bytes = modern_response.content
            lower_url = modern["url"].lower().split("?")[0]
            if lower_url.endswith(".png"):
                new_mime = "image/png"
            elif lower_url.endswith(".webp"):
                new_mime = "image/webp"
            elif lower_url.endswith((".jpg", ".jpeg")):
                new_mime = "image/jpeg"
            else:
                new_mime = "image/jpeg"

            comparison = analyze_changes(
                client, image_bytes, mime_type, modern_bytes, new_mime, location
            )
            status.update(label="Comparison ready", state="complete", expanded=False)

        st.markdown("---")
        st.markdown('<div class="eyebrow">02 / LOCATION FOUND</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-title">{landmark}</div>', unsafe_allow_html=True)
        st.markdown(
            f"**{city}, {country}** · Identification confidence: "
            f"**{location.get('confidence', 'Unknown')}**"
        )
        if location.get("confidence_reason"):
            st.caption(location["confidence_reason"])
        clues = location.get("visual_clues", [])
        if clues:
            st.caption("Visual clues: " + " · ".join(str(item) for item in clues[:4]))

        st.markdown("---")
        st.markdown('<div class="eyebrow">03 / THEN VS NOW</div>', unsafe_allow_html=True)
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("**THEN · YOUR UPLOAD**")
            st.image(image_bytes, use_container_width=True)
            st.caption(f"Estimated period: {location.get('estimated_period', 'Unknown')} (AI estimate)")
        with right:
            st.markdown("**NOW · ARCHIVE SEARCH RESULT**")
            st.image(modern_bytes, use_container_width=True)
            st.caption(f"{modern['title']} · Image date: {modern['date']}")
            st.markdown(f"[Open original image and license details ↗]({modern['page_url']})")
            st.caption(f"License: {modern['license']} · Author: {modern['artist']}")

        st.markdown("---")
        st.markdown('<div class="eyebrow">04 / WHAT CHANGED?</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="result-title">{comparison.get("same_location_assessment", "Comparison")}</div>',
            unsafe_allow_html=True,
        )
        st.write(comparison.get("summary", "No summary was returned."))
        for item in comparison.get("changes", []):
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{item.get('category', 'Visible change')}**")
                with c2:
                    st.caption(f"Confidence: {item.get('confidence', 'Unknown')}")
                then_col, now_col = st.columns(2)
                with then_col:
                    st.caption("THEN")
                    st.write(item.get("then", "Not clear"))
                with now_col:
                    st.caption("NOW")
                    st.write(item.get("now", "Not clear"))
        if comparison.get("caution"):
            st.info(comparison["caution"])
        st.caption(
            "AI-generated interpretation. The archive image may be from a different viewpoint or date; "
            "verify the source before treating a change as historical fact."
        )

    except requests.RequestException as exc:
        st.error(f"Image search or download failed: {exc}. Please retry or use a different landmark photo.")
    except Exception as exc:
        st.error(f"The analysis could not be completed: {exc}")
        st.caption("Check the API key, model access, and terminal output for details.")

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#8496a2;font-size:.8rem;">'
    'EpochTrek · A student project exploring how places evolve</div>',
    unsafe_allow_html=True,
)
