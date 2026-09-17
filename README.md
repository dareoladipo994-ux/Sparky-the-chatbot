# 🤖 Sparky - Multimodal AgentRouter AI Assistant

Sparky is a full-featured, interactive chatbot web application built with **Streamlit** and powered by the **AgentRouter Gateway**. By leveraging an OpenAI-compatible client interface, Sparky can instantly route requests to the world's most powerful frontier AI models—including **ChatGPT 6, Claude 4.5, and Gemini 3.8**—all through a single API key.

![Python](https://shields.io)
![Streamlit](https://shields.io)
![AgentRouter](https://shields.io)

---

## ✨ Features

* **🌐 Gateway Unified Model Routing:** Seamlessly switch between the latest AI models (like `chatgpt-6-pro`, `claude-sonnet-4-5`, and `gemini-3.8-flash`) natively via the AgentRouter proxy.
* **🎭 Dynamic Persona Switcher:** Easily toggle Sparky between different roles (Code Reviewer, Copywriter, App Architect, etc.) to inject custom system architectures.
* **🖼️ Standardized Multimodal Processing:** Upload images directly through the chat interface. The application automatically converts images into base64 data payloads, making them fully compatible with multi-modal gateway endpoints.
* **🐍 Automatic Python Code Exporter:** Sparky parses incoming assistant streaming texts for Python code blocks and provides instant, dedicated `.py` file download buttons.
* **🎛️ Model Customization Sliders:** Fine-tune response outputs with real-time temperature (creativity) and max token boundaries.
* **📥 Export Chat Transcript:** Render and download full conversational turns as clean, structured `.txt` files.

---

## 🚀 Quickstart & Installation

Ensure you have Python 3.9 or higher installed, then run the following commands in your terminal to get everything set up:

```bash
# 1. Clone the repository and navigate into the folder
git clone https://github.com
cd sparky-gemini-chatbot

# 2. Install the updated dependencies
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Before running the application, you must provide your AgentRouter credential token. You can configure this using any of the following methods:

### Method A: Local `.env` File (Recommended)
Create a file named `.env` in your project root directory and add your key:
```text
AGENTROUTER_API_KEY="your_actual_agentrouter_key_here"
```

### Method B: Temporary Terminal Session
Run the export command directly in your terminal before launching the application.

* **macOS / Linux:**
  ```bash
  export AGENTROUTER_API_KEY="your_actual_agentrouter_key_here"
  ```
* **Windows (Command Prompt):**
  ```cmd
  set AGENTROUTER_API_KEY="your_actual_agentrouter_key_here"
  ```
* **Windows (PowerShell):**
  ```powershell
  \$env:AGENTROUTER_API_KEY="your_actual_agentrouter_key_here"
  ```

---

## 🏃‍♂️ Running the Application

Once your dependencies are installed and your API key environment variable is established, fire up the application:

```bash
streamlit run app.py
```

---

## 📝 License
This project is open-source and available under the MIT License.
