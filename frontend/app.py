import streamlit as st
import requests
import json

# Backend URL
API_URL = "http://localhost:8000/generate"

st.set_page_config(page_title="ViralFlow AI", layout="wide", page_icon="🚀")

# Custom CSS for better UI
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    /* Image Gallery Styling */
    div[data-testid="stImage"] > img {
        height: 300px !important;
        object-fit: cover !important;
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    div[data-testid="stImage"] > img:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing results
if "results" not in st.session_state:
    st.session_state.results = None

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["Content Generator", "Visuals Gallery"])

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Configuration")

# --- Page 1: Content Generator ---
if page == "Content Generator":
    st.title("🚀 ViralFlow AI")
    st.subheader("The Omni-Channel Content Engine")
    st.markdown("Transform a single idea into optimized, platform-specific content for **Twitter, LinkedIn, Instagram**, and more—complete with trending hashtags, scheduling insights, and AI-curated visuals. ✨")

    # Inputs
    base_content = st.text_area("✍️ Enter your content idea or draft:", height=150)
    
    platforms = st.sidebar.multiselect(
        "Select Platforms",
        ["twitter", "instagram", "linkedin", "youtube", "blog"],
        default=["twitter", "linkedin"]
    )
    
    tone = st.sidebar.selectbox(
        "Select Tone",
        ["Professional", "Casual", "Humorous", "Inspirational", "Educational", "Sales-oriented"],
        index=0
    )

    if st.button("✨ Generate Content", type="primary"):
        if not base_content:
            st.warning("Please enter some content first.")
        else:
            with st.spinner("🤖 AI Agents are working... (Researching, Writing, Optimizing, Searching Visuals)"):
                try:
                    payload = {
                        "base_content": base_content,
                        "platforms": platforms,
                        "tone": tone
                    }
                    response = requests.post(API_URL, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Store results in session state
                    st.session_state.results = data
                    st.success("Content Generated Successfully! Check the Visuals Gallery for images.")
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to backend: {e}")

    # Display Results (if available)
    if st.session_state.results:
        data = st.session_state.results
        st.markdown("---")
        
        # Platform Icons
        PLATFORM_ICONS = {
            "twitter": "🐦",
            "instagram": "📸",
            "linkedin": "💼",
            "youtube": "▶️",
            "blog": "✍️"
        }
        
        # Create tabs for platforms
        if "platform_outputs" in data:
            platform_tabs = st.tabs([f"{PLATFORM_ICONS.get(p, '📱')} {p.capitalize()}" for p in data["platform_outputs"].keys()])
            
            for i, (platform, content) in enumerate(data["platform_outputs"].items()):
                with platform_tabs[i]:
                    st.subheader(f"{PLATFORM_ICONS.get(platform, '📱')} {platform.capitalize()} Draft")
                    st.text_area("Content", content, height=200, key=f"content_{platform}")
                    
                    # Hashtags
                    if "hashtags" in data and platform in data["hashtags"]:
                        tags = " ".join(data["hashtags"][platform])
                        st.info(f"**Hashtags:** {tags}")
                        
                    # Schedule
                    if "schedules" in data and platform in data["schedules"]:
                        time = data["schedules"][platform]
                        st.warning(f"📅 **Best Posting Time:** {time}")
                        
                    st.download_button(
                        label="⬇️ Download JSON",
                        data=json.dumps({
                            "content": content,
                            "hashtags": data.get("hashtags", {}).get(platform, []),
                            "schedule": data.get("schedules", {}).get(platform, "")
                        }, indent=2),
                        file_name=f"{platform}_content.json",
                        mime="application/json"
                    )

# --- Page 2: Visuals Gallery ---
elif page == "Visuals Gallery":
    st.title("🎨 Visuals Gallery")
    st.markdown("Here are the AI-suggested images for your content.")
    
    if st.session_state.results:
        # Refresh Button
        if st.button("🔄 Refresh Visuals"):
            metadata = st.session_state.results.get("metadata", {})
            if metadata:
                with st.spinner("Refreshing visuals..."):
                    try:
                        payload = {
                            "topic": metadata.get("topic", ""),
                            "keywords": metadata.get("keywords", [])
                        }
                        response = requests.post("http://localhost:8000/regenerate_visuals", json=payload)
                        if response.status_code == 200:
                            new_visuals = response.json().get("visuals", [])
                            st.session_state.results["visuals"] = new_visuals
                            st.success("Visuals refreshed!")
                            st.rerun()
                        else:
                            st.error("Failed to refresh visuals.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("No metadata available to refresh visuals.")

        visuals = st.session_state.results.get("visuals", [])
        
        if visuals:
            # Create rows of 2 images each
            for i in range(0, len(visuals), 2):
                cols = st.columns(2)
                # Get the slice of 2 images for this row
                row_visuals = visuals[i:i+2]
                
                for j, img_url in enumerate(row_visuals):
                    idx = i + j
                    with cols[j]:
                        st.image(img_url, use_container_width=True)
                        
                        # Download Button Logic
                        try:
                            # We need to fetch the image to download it
                            # Use a unique key for each button to avoid conflicts
                            if st.button(f"⬇️ Download Image {idx+1}", key=f"btn_dl_{idx}"):
                                with st.spinner("Downloading..."):
                                    r = requests.get(img_url)
                                    if r.status_code == 200:
                                        st.download_button(
                                            label="⬇️ Click to Save",
                                            data=r.content,
                                            file_name=f"visual_{idx+1}.jpg",
                                            mime="image/jpeg",
                                            key=f"dl_final_{idx}"
                                        )
                                    else:
                                        st.error("Could not fetch image.")
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.info("No visuals found. Try generating content first or check your Serper API key.")
    else:
        st.warning("No content generated yet. Go to the 'Content Generator' page to start.")

# Footer in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("###### ⚡ Powered by LangGraph, Groq & Tavily")
