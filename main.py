from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from openai import OpenAI
import os
import re
import base64
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Sparky - AI Assistant", page_icon="🤖", layout="centered")

# --- Helper Functions ---
def format_chat_history(messages):
    """Formats the chat history into a readable text file format."""
    transcript = "--- Chat Transcript ---\n\n"
    for msg in messages:
        if msg["role"] == "system":
            continue
        role = "Sparky" if msg["role"] == "assistant" else "User"
        # Handle string or list-based content (multimodal structure) Safely
        if isinstance(msg["content"], list):
            text_pieces = [part["text"] for part in msg["content"] if part.get("type") == "text"]
            text = " ".join(text_pieces)
        else:
            text = msg["content"]
            
        transcript += f"{role}: {text}\n\n"
    return transcript

def extract_python_code(text):
    """Scans the text for Python code blocks and extracts the raw code."""
    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n\n".join(matches) if matches else None

def encode_image_to_base64(uploaded_file):
    """Converts a Streamlit uploaded image file into a base64 string for OpenAI multi-modal specification."""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Convert to RGB if palette-based (PNG) to ensure standard JPEG compression works
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    return None

# 2. Configure the AgentRouter API Key securely
API_KEY = os.environ.get("AGENTROUTER_API_KEY") or (st.secrets.get("AGENTROUTER_API_KEY") if hasattr(st, "secrets") else None)
if not API_KEY:
    st.error("AgentRouter API Key not found. Please set the AGENTROUTER_API_KEY environment variable.")
    st.stop()

# Initialize Client pointing to the standardized AgentRouter API Endpoint
client = OpenAI(
    base_url="https://agentrouter.org/v1",
    api_key=API_KEY
)

# 3. Sidebar Settings & Controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Persona Selector with Sparky as the core identity
    persona_options = {
        "Sparky (Default)": "You are Sparky, a helpful, friendly, witty, and highly capable AI assistant.",
        "Code Reviewer Sparky": "You are Sparky acting as a senior software engineer. Review code, find bugs, and suggest optimizations.",
        "Creative Writer Sparky": "You are Sparky acting as a creative copywriter. Write engaging, imaginative content.",
        "App Architect Sparky": "You are Sparky acting as an app architect. Write clean Python code for the user to download."
    }
    selected_persona = st.selectbox("Select Persona", options=list(persona_options.keys()))
    
    st.divider()
    
    # Model Catalog Grouping
    st.subheader("Model Routing")
    model_choice = st.selectbox(
        "Select Model Target",
        options=[
            "chatgpt-6-pro",      # OpenAI Latest Pro Astra Release
            "chatgpt-6-astra",    # OpenAI Standard High-Velocity
            "claude-sonnet-4-5",  # Anthropic Core Flagship Agentic Model
            "claude-opus-4-5",    # Anthropic Heavy Reasoning
            "gemini-3.8-flash",   # Google Latest Flash Multimodal Engine
            "deepseek-v4-pro"     # DeepSeek Flagship Reasoning Choice
        ]
    )
    
    # Model Parameter Sliders
    st.subheader("Model Parameters")
    temperature = st.slider("Temperature (Creativity)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    max_tokens = st.slider("Max Output Tokens", min_value=100, max_value=8192, value=2048, step=100)
    
    st.divider()
    st.subheader("💾 Data & Memory")
    
    # Export Chat Button
    if "chat_history" in st.session_state and len(st.session_state.chat_history) > 0:
        chat_transcript = format_chat_history(st.session_state.chat_history)
        st.download_button(
            label="📥 Export Chat as TXT",
            data=chat_transcript,
            file_name="sparky_chat_transcript.txt",
            mime="text/plain",
            use_container_width=True
        )
            
    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# 4. Initialize Chat Session State Array if not existing
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 Sparky - AI Assistant")

# Image Uploader (Collapsible) - Restored with new processing backend
with st.expander("📎 Attach an Image (Optional)"):
    uploaded_image = st.file_uploader("Upload an image for Sparky to analyze", type=['png', 'jpg', 'jpeg'])

# 5. Display Conversation History
for index, message in enumerate(st.session_state.chat_history):
    if message["role"] == "system":
        continue
        
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        # Handle printing content cleanly depending on structure (Text vs Multimodal Content List)
        if isinstance(message["content"], list):
            for part in message["content"]:
                if part["type"] == "text":
                    st.markdown(part["text"])
                elif part["type"] == "image_url":
                    # Re-display images saved in state using the raw base64 string
                    st.image(part["image_url"]["url"], width=150, caption="Uploaded context")
        else:
            st.markdown(message["content"])
        
        # Code Exporter logic for legacy turns
        if message["role"] == "assistant":
            python_code = extract_python_code(message["content"] if isinstance(message["content"], str) else "")
            if python_code:
                st.download_button(
                    label="🐍 Download Python Code",
                    data=python_code,
                    file_name=f"sparky_script_{index}.py",
                    mime="text/x-python",
                    key=f"download_{index}"
                )

# 6. Suggested Starter Prompts
starter_prompt = None
if len([m for m in st.session_state.chat_history if m["role"] != "system"]) == 0:
    st.markdown("#### Try asking Sparky about:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🐍 Write a Python App"):
        starter_prompt = "Write a complete Python script using Tkinter to build a simple calculator app."
    if col2.button("🐛 Debug code"):
        starter_prompt = "How do I fix a 'SyntaxError' in Python?"
    if col3.button("🚀 Brainstorm ideas"):
        starter_prompt = "Give me 3 creative ideas for a tech startup."

# 7. Handle User Input
prompt = st.chat_input("Ask Sparky something...") or starter_prompt

if prompt:
    # 1. Prepare modern message payload list
    content_payload = [{"type": "text", "text": prompt}]
    
    # Process image attachment into standard base64 data URL formatting if present
    base64_image = encode_image_to_base64(uploaded_image)
    if base64_image:
        content_payload.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    # Render User Turn Immediately into current window view
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        if uploaded_image:
            st.image(uploaded_image, caption="Attached Image", width=150)
            
    # Compile message stack for API delivery (injecting system architecture rule cleanly at the top)
    api_messages = [{"role": "system", "content": persona_options[selected_persona]}]
    for turn in st.session_state.chat_history:
        api_messages.append(turn)
    
    # Add new user interaction package
    api_messages.append({"role": "user", "content": content_payload})
    st.session_state.chat_history.append({"role": "user", "content": content_payload})
            
    # 8. Process Gateway Generation stream
    try:
        with st.chat_message("assistant", avatar="🤖"):
            response_stream = client.chat.completions.create(
                model=model_choice,
                messages=api_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Generator helper to capture delta values coming over the network thread
            def stream_generator():
                for chunk in response_stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            yield delta

            full_response_text = st.write_stream(stream_generator())
            
        # Commit assistant response text back to internal state list
        st.session_state.chat_history.append({"role": "assistant", "content": full_response_text})
        
        # --- Code Exporter logic for newest turn ---
        python_code = extract_python_code(full_response_text)
        if python_code:
            st.download_button(
                label="🐍 Download Python Code",
                data=python_code,
                file_name="sparky_script_new.py",
                mime="text/x-python",
                key="download_newest"
            )
            
    except Exception as e:
        st.error(f"Error communicating with AgentRouter: {e}")
