import streamlit as st
import google.generativeai as genai
import os
import re
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Sparky - AI Assistant", page_icon="🤖", layout="centered")

# --- Helper Functions ---
def format_chat_history(messages):
    """Formats the chat history into a readable text file format."""
    transcript = "--- Chat Transcript ---\n\n"
    for msg in messages:
        role = "Sparky" if msg.role == "model" else "User"
        text = "".join([part.text for part in msg.parts if hasattr(part, 'text')])
        if text:
            transcript += f"{role}: {text}\n\n"
    return transcript

def extract_python_code(text):
    """Scans the text for Python code blocks and extracts the raw code."""
    # This regex looks for ```python ... ``` blocks
    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)
    # Join multiple code blocks together if the AI generated more than one
    return "\n\n".join(matches) if matches else None

# 2. Configure the API Key securely
API_KEY = os.environ.get("GEMINI_API_KEY") or (st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") else None)
if not API_KEY:
    st.error("API Key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)

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
    
    # Model Parameter Sliders
    st.subheader("Model Parameters")
    temperature = st.slider("Temperature (Creativity)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    max_tokens = st.slider("Max Output Tokens", min_value=100, max_value=8192, value=2048, step=100)
    
    st.divider()
    
    # Google Search Grounding Toggle
    st.subheader("Live Web Data")
    use_search = st.toggle("Enable Google Search Grounding", value=False)
    
    st.divider()
    
    st.subheader("💾 Data & Memory")
    
    # Export Chat Button
    if "chat_session" in st.session_state and st.session_state.chat_session:
        history = st.session_state.chat_session.history
        if len(history) > 0:
            chat_transcript = format_chat_history(history)
            st.download_button(
                label="📥 Export Chat as TXT",
                data=chat_transcript,
                file_name="sparky_chat_transcript.txt",
                mime="text/plain",
                use_container_width=True
            )
            
    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chat_session = None
        st.rerun()

# 4. Set up the Model
tools = 'google_search_retrieval' if use_search else None

model = genai.GenerativeModel(
    model_name='gemini-3.6-flash', 
    system_instruction=persona_options[selected_persona],
    tools=tools,
    generation_config=genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
)

# 5. Initialize Chat Session
if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("🤖 Sparky - AI Assistant")

# Image Uploader (Collapsible)
with st.expander("📎 Attach an Image (Optional)"):
    uploaded_image = st.file_uploader("Upload an image for Sparky to analyze", type=['png', 'jpg', 'jpeg'])

# 6. Display Conversation History
for index, message in enumerate(st.session_state.chat_session.history):
    role = "assistant" if message.role == "model" else "user"
    avatar = "🤖" if role == "assistant" else "👤"
    
    with st.chat_message(role, avatar=avatar):
        full_text = ""
        # Render Text
        for part in message.parts:
            try:
                if part.text:
                    st.markdown(part.text)
                    full_text += part.text
            except Exception:
                pass 
        
        # --- NEW: Code Exporter logic for chat history ---
        if role == "assistant":
            python_code = extract_python_code(full_text)
            if python_code:
                st.download_button(
                    label="🐍 Download Python Code",
                    data=python_code,
                    file_name=f"sparky_script_{index}.py",
                    mime="text/x-python",
                    key=f"download_{index}" # Unique key required by Streamlit
                )

# 7. Suggested Starter Prompts
starter_prompt = None
if len(st.session_state.chat_session.history) == 0:
    st.markdown("#### Try asking Sparky about:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🐍 Write a Python App"):
        starter_prompt = "Write a complete Python script using Tkinter to build a simple calculator app."
    if col2.button("🐛 Debug code"):
        starter_prompt = "How do I fix a 'SyntaxError' in Python?"
    if col3.button("🚀 Brainstorm ideas"):
        starter_prompt = "Give me 3 creative ideas for a tech startup."

# 8. Handle User Input
prompt = st.chat_input("Ask Sparky something...") or starter_prompt

if prompt:
    # Display user prompt
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    message_payload = [prompt]
    if uploaded_image:
        img = Image.open(uploaded_image)
        message_payload.append(img)
        with st.chat_message("user", avatar="👤"):
            st.image(img, caption="Attached Image", width=150)
            
    # Process API call
    try:
        response = st.session_state.chat_session.send_message(message_payload, stream=True)
        
        with st.chat_message("assistant", avatar="🤖"):
            # Stream the response text
            full_response_text = st.write_stream((chunk.text for chunk in response))
            
            # --- NEW: Code Exporter logic for new messages ---
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
        st.error(f"Error communicating with Gemini: {e}")