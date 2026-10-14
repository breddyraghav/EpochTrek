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

st.set_page_config(page_title="EpochTrek — Living Archive", page_icon="⌛", layout="wide")

# Museum-inspired visual system: ink, parchment, muted brass and editorial type.
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
:root { --paper:#f1eee6; --paper2:#e8e2d6; --ink:#191b18; --muted:#77756d; --brass:#a88b55; --line:rgba(25,27,24,.17); }
.stApp { background:var(--paper); color:var(--ink); }
html, body, [class*="css"], button, input, textarea, select { font-family:'DM Sans',sans-serif; }
.block-container { max-width:1380px; padding:1.4rem 3rem 3rem; }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stToolbar"] { right:1rem; }
#MainMenu, footer {visibility:hidden;}
.archive-nav {display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.45rem 0 1.1rem;border-bottom:1px solid var(--line);margin-bottom:2.1rem;}
.archive-brand {font-family:'Playfair Display',serif;font-size:1.35rem;letter-spacing:.04em;font-weight:700;color:var(--ink);}
.archive-brand span {display:block;font-family:'DM Sans',sans-serif;font-size:.58rem;letter-spacing:.28em;font-weight:600;text-transform:uppercase;color:var(--muted);margin-top:.15rem;}
.nav-meta {font-size:.64rem;letter-spacing:.15em;text-transform:uppercase;color:#5d5b54;text-align:right;}
.hero-shell {position:relative;overflow:hidden;min-height:390px;border-radius:5px;background:linear-gradient(90deg,rgba(15,17,15,.92) 0%,rgba(15,17,15,.76) 43%,rgba(15,17,15,.1) 100%),linear-gradient(0deg,rgba(15,17,15,.48),transparent 60%),url('https://images.unsplash.com/photo-1511818966892-d7d671e672a2?auto=format&fit=crop&w=2200&q=85') center 47%/cover;display:flex;align-items:center;margin-bottom:1.5rem;}
.hero-copy {max-width:650px;padding:3rem 3.5rem;color:#f7f3e9;}
.kicker,.section-kicker {font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:var(--brass);}
.hero-index {font-family:'Playfair Display',serif;font-size:clamp(3.6rem,8vw,6.5rem);line-height:.9;color:rgba(238,230,212,.22);margin:.8rem 0 -.15rem;}
.hero-title {font-family:'Playfair Display',serif;font-size:clamp(2.4rem,5vw,4.5rem);line-height:1.02;letter-spacing:-.035em;color:#fffaf0;margin:0 0 .8rem;}
.hero-sub {max-width:480px;color:rgba(255,250,240,.82);font-size:.93rem;line-height:1.8;}
.hero-note {margin-top:1.6rem;font-size:.62rem;letter-spacing:.18em;text-transform:uppercase;color:#e1d3b7;}
.section-head {display:flex;justify-content:space-between;align-items:end;gap:1rem;border-bottom:1px solid var(--line);padding:1rem 0 .85rem;margin:1.3rem 0 1.2rem;}
.section-title {font-family:'Playfair Display',serif;font-size:1.8rem;line-height:1.15;color:var(--ink);margin:.3rem 0 0;}
.section-number {font-family:'Playfair Display',serif;font-size:2rem;color:var(--brass);}
.intro-copy {font-size:.88rem;line-height:1.8;color:#65635c;max-width:760px;}
[data-testid="stFileUploader"] {background:#e8e2d6;border:1px dashed #a89c83;border-radius:4px;padding:1rem;}
[data-testid="stFileUploader"] section {background:transparent;}
.stButton>button {border-radius:2px;min-height:3.1rem;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;border:1px solid #24251f;background:#24251f;color:#f7f3e9;transition:all .2s;}
.stButton>button:hover {background:#a88b55;border-color:#a88b55;color:#fff;}
.stButton>button:disabled {background:#b9b4a8;color:#716d63;border-color:#b9b4a8;}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:4px!important;border-color:var(--line)!important;background:rgba(255,255,255,.22);}
[data-testid="stImage"] img {border-radius:3px;}
[data-testid="stCaptionContainer"] {color:#77756d;font-size:.72rem;line-height:1.6;}
.stAlert {border-radius:3px;}
.result-panel {padding:1.15rem 1.25rem;border:1px solid var(--line);background:rgba(255,255,255,.25);margin:.35rem 0 .8rem;}
.result-label {font-size:.62rem;letter-spacing:.18em;text-transform:uppercase;color:#8b7448;font-weight:700;margin-bottom:.45rem;}
.result-name {font-family:'Playfair Display',serif;font-size:clamp(1.8rem,3.5vw,3rem);line-height:1.1;color:#20211d;overflow-wrap:anywhere;}
.change-title {font-family:'Playfair Display',serif;font-size:1.2rem;color:#20211d;}
.archive-footer {border-top:1px solid var(--line);margin-top:3rem;padding-top:1rem;display:flex;justify-content:space-between;gap:1rem;color:#77756d;font-size:.65rem;letter-spacing:.08em;text-transform:uppercase;}
hr {border-color:var(--line)!important;}
@media(max-width:760px){.block-container{padding:1rem 1rem 2rem}.hero-shell{min-height:350px}.hero-copy{padding:2rem 1.35rem}.nav-meta{font-size:.55rem}.archive-nav{margin-bottom:1.2rem}.section-title{font-size:1.5rem}.archive-footer{display:block;line-height:2}}
</style>
""", unsafe_allow_html=True)


def get_api_key():
    """Read Gemini key from Streamlit Secrets or an environment variable."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return str(key).strip()
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "").strip()


def extract_json(response_text):
    """Parse JSON returned by Gemini, including optional Markdown fences."""
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
Return ONLY valid JSON with keys: identified (boolean), city, landmark, country, confidence (High/Medium/Low), confidence_reason, visual_clues (array), estimated_period, search_query.
Never claim certainty from weak clues. If not identifiable set identified=false and confidence=Low. Prefer a specific landmark or street. Do not infer an exact year without evidence. Search for a real photograph, not an AI-generated image."""
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    response = client.models.generate_content(
        model=GEMINI_MODEL, contents=[prompt, image_part],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2),
    )
    return extract_json(response.text)


def commons_search(query, limit=8):
    """Search Wikimedia Commons for image files matching a location query."""
    params = {"action":"query","format":"json","generator":"search","gsrsearch":f"{query} filetype:bitmap",
              "gsrnamespace":6,"gsrlimit":limit,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":1400}
    headers = {"User-Agent":"EpochTrek/1.0 (student historical photo comparison project)"}
    response = requests.get(COMMONS_API, params=params, headers=headers, timeout=25)
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
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
        images.append({
            "title":page.get("title","Untitled image").replace("File:",""), "url":url,
            "page_url":info.get("descriptionurl","https://commons.wikimedia.org/"),
            "date":meta_value("DateTimeOriginal") or meta_value("DateTime") or "Date not provided",
            "license":meta_value("LicenseShortName") or "License not listed in metadata",
            "artist":meta_value("Artist") or "Author not listed",
            "description":meta_value("ImageDescription")[:400],
        })
    return images


def analyze_changes(client, old_bytes, old_mime, new_bytes, new_mime, location):
    prompt = f"""Compare two photographs for EpochTrek. First is the user's historical upload; second is a candidate from Wikimedia Commons.
Location hypothesis: {location.get('landmark','Unknown')}, {location.get('city','Unknown')}, {location.get('country','Unknown')}.
Compare only visible evidence. If viewpoints differ or the same place cannot be verified, say so and do not invent changes.
Return ONLY JSON: {{"same_location_assessment":"Likely same place / Possibly same place / Not enough evidence", "summary":"2-3 sentences", "changes":[{{"category":"Architecture","then":"visible old-photo detail","now":"visible candidate-photo detail","confidence":"High/Medium/Low"}}], "caution":"one short limitation statement"}}.
Include 3-5 changes only when supported. Describe visible differences, not unsupported causes. Do not claim the newer image's date unless metadata confirms it."""
    parts = [prompt, types.Part.from_bytes(data=old_bytes, mime_type=old_mime),
             "Candidate image retrieved from Wikimedia Commons:", types.Part.from_bytes(data=new_bytes, mime_type=new_mime)]
    response = client.models.generate_content(
        model=GEMINI_MODEL, contents=parts,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.25),
    )
    return extract_json(response.text)


# Editorial masthead and cinematic landing hero.
st.markdown("""
<div class="archive-nav">
  <div class="archive-brand">EpochTrek<span>Living archive · Then / Now</span></div>
  <div class="nav-meta">A visual journey through time<br>History, preserved in place</div>
</div>
<div class="hero-shell"><div class="hero-copy">
  <div class="kicker">Field notes from the past</div>
  <div class="hero-index">01</div>
  <h1 class="hero-title">Every place<br>holds a memory.</h1>
  <div class="hero-sub">Explore how familiar streets, landmarks and buildings have changed. Begin with an old photograph; let the archive guide the next chapter.</div>
  <div class="hero-note">Observe · Identify · Compare</div>
</div></div>
<div class="intro-copy">EpochTrek combines visual analysis with real archive imagery to build a careful, side-by-side view of a place across time. AI findings are hypotheses—not a substitute for verified historical records.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-head"><div><div class="section-kicker">01 / Begin your search</div><div class="section-title">Bring the past into focus.</div></div><div class="section-number">01</div></div>
""", unsafe_allow_html=True)

left, right = st.columns([1.05, 0.95], gap="large")
with left:
    st.markdown("**YOUR HISTORICAL PHOTOGRAPH**")
    uploaded = st.file_uploader("Choose a photograph", type=["jpg", "jpeg", "png", "webp"],
        help="Landmarks, streets, signs and distinctive buildings provide useful visual clues.")
    st.caption("Accepted formats: JPG, JPEG, PNG and WEBP. A clear, uncropped image usually works best.")
    analyze_clicked = st.button("Identify location & compare  →", type="primary", use_container_width=True, disabled=uploaded is None)
with right:
    if uploaded:
        st.image(uploaded.getvalue(), caption=f"Archive input · {uploaded.name}", use_container_width=True)
    else:
        st.markdown("""
        <div style="height:255px;border:1px solid rgba(25,27,24,.18);background:linear-gradient(135deg,#ddd5c6,#f7f3e9);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:2rem;color:#77756d">
          <div style="font-family:'Playfair Display',serif;font-size:3rem;color:#a88b55">↟</div>
          <div style="font-size:.65rem;letter-spacing:.18em;text-transform:uppercase;font-weight:700">Your photograph appears here</div>
          <div style="font-size:.78rem;margin-top:.7rem;max-width:260px;line-height:1.7">Upload a historical image to begin the location and archive comparison workflow.</div>
        </div>
        """, unsafe_allow_html=True)

if analyze_clicked and uploaded:
    api_key = get_api_key()
    if not api_key:
        st.error("Gemini API key not found. Add GEMINI_API_KEY to Streamlit Secrets or your environment variables.")
        st.stop()
    client = genai.Client(api_key=api_key)
    image_bytes = uploaded.getvalue()
    mime_type = uploaded.type or "image/jpeg"
    try:
        with st.status("Examining the photograph and searching the archive…", expanded=True) as status:
            st.write("Stage 1 of 3 · Reading visual clues")
            location = identify_location(client, image_bytes, mime_type)
            city = location.get("city", "Unknown")
            landmark = location.get("landmark", "Unknown")
            country = location.get("country", "Unknown")
            st.write(f"Location hypothesis: {landmark}, {city}, {country}")
            if not location.get("identified", False) or location.get("confidence", "Low").lower() == "low":
                status.update(label="Location needs stronger visual evidence", state="error", expanded=True)
                st.warning("The photograph could not be identified confidently. Try a clearer image with a distinctive landmark, sign or building.")
                st.json(location)
                st.stop()
            st.write("Stage 2 of 3 · Searching Wikimedia Commons")
            search_query = location.get("search_query") or f"{landmark} {city} {country}"
            images = commons_search(search_query)
            if not images:
                images = commons_search(f"{landmark} {city} {country}")
            if not images:
                status.update(label="No usable archive image found", state="error", expanded=True)
                st.error("Wikimedia Commons returned no usable image. Try a better-known landmark or a clearer photograph.")
                st.stop()
            modern = images[0]
            st.write("Stage 3 of 3 · Comparing visible details")
            modern_response = requests.get(modern["url"], timeout=25, headers={"User-Agent":"EpochTrek/1.0 (student project)"})
            modern_response.raise_for_status()
            modern_bytes = modern_response.content
            lower_url = modern["url"].lower().split("?")[0]
            new_mime = "image/png" if lower_url.endswith(".png") else "image/webp" if lower_url.endswith(".webp") else "image/jpeg"
            comparison = analyze_changes(client, image_bytes, mime_type, modern_bytes, new_mime, location)
            status.update(label="Archive comparison prepared", state="complete", expanded=False)

        st.markdown("""
        <div class="section-head"><div><div class="section-kicker">02 / Place identified</div><div class="section-title">The location record</div></div><div class="section-number">02</div></div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="result-panel"><div class="result-label">Location hypothesis · {location.get("confidence", "Unknown")} confidence</div><div class="result-name">{landmark}</div><div style="margin-top:.5rem;color:#77756d">{city}, {country}</div></div>', unsafe_allow_html=True)
        if location.get("confidence_reason"):
            st.caption(location["confidence_reason"])
        clues = location.get("visual_clues", [])
        if clues:
            st.markdown("**Visual clues noted**")
            st.write(" · ".join(str(item) for item in clues[:5]))

        st.markdown("""
        <div class="section-head"><div><div class="section-kicker">03 / A study in time</div><div class="section-title">Then, beside now.</div></div><div class="section-number">03</div></div>
        """, unsafe_allow_html=True)
        old_col, new_col = st.columns(2, gap="large")
        with old_col:
            st.markdown("**THEN** · YOUR UPLOAD")
            st.image(image_bytes, use_container_width=True)
            st.caption(f"Estimated period: {location.get('estimated_period', 'Unknown')} · AI estimate")
        with new_col:
            st.markdown("**ARCHIVE CANDIDATE** · NOW")
            st.image(modern_bytes, use_container_width=True)
            st.caption(f"{modern['title']} · Image date: {modern['date']}")
            st.markdown(f"[Open archive record and source details ↗]({modern['page_url']})")
            st.caption(f"License: {modern['license']} · Author: {modern['artist']}")

        st.markdown("""
        <div class="section-head"><div><div class="section-kicker">04 / Visible evidence</div><div class="section-title">What appears to have changed?</div></div><div class="section-number">04</div></div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="result-panel"><div class="result-label">Comparison assessment</div><div class="result-name" style="font-size:2rem">{comparison.get("same_location_assessment", "Comparison")}</div><p style="line-height:1.8;color:#5f5d56;margin-bottom:0">{comparison.get("summary", "No summary was returned.")}</p></div>', unsafe_allow_html=True)
        for item in comparison.get("changes", []):
            with st.container(border=True):
                a, b = st.columns([3, 1])
                with a:
                    st.markdown(f'<div class="change-title">{item.get("category", "Visible change")}</div>', unsafe_allow_html=True)
                with b:
                    st.caption(f"Confidence · {item.get('confidence', 'Unknown')}")
                then_col, now_col = st.columns(2, gap="large")
                with then_col:
                    st.caption("THEN")
                    st.write(item.get("then", "Not clear"))
                with now_col:
                    st.caption("NOW")
                    st.write(item.get("now", "Not clear"))
        if comparison.get("caution"):
            st.info(comparison["caution"])
        st.caption("Research note: AI-generated interpretation. The archive image may show a different viewpoint or date. Verify the source before treating a change as historical fact.")
    except requests.RequestException as exc:
        st.error(f"Archive search or image download failed: {exc}. Please retry or choose another landmark photograph.")
    except Exception as exc:
        st.error(f"The analysis could not be completed: {exc}")
        st.caption("Check the API key, Gemini model access and Streamlit logs for details.")

st.markdown("""
<div class="archive-footer"><div>EpochTrek · A living visual archive</div><div>Observe carefully. Compare responsibly.</div></div>
""", unsafe_allow_html=True)