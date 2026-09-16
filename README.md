# 🤖 Sparky - Multimodal Gemini AI Assistant

Sparky is a full-featured, interactive chatbot web application powered by **Google Gemini 3.0 Flash** and built with **Streamlit**. It features multimodal capabilities (image analysis), dynamic persona switching, Google Search grounding, custom model controls, chat exporting, and a built-in Python Code Exporter.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-8E75B2?style=flat&logo=googlegemini&logoColor=white)

---

## ✨ Features

* **⚡ Gemini 3.0 Flash Powered:** Ultra-fast, real-time streaming responses.
* **🎭 Dynamic Persona Switcher:** Easily toggle Sparky between different roles (Code Reviewer, Copywriter, App Architect, etc.).
* **🖼️ Multimodal Capabilities:** Upload images alongside text prompts for vision analysis.
* **🌐 Google Search Grounding:** Toggle live web search on/off for real-time internet data.
* **🐍 Automatic Python Code Exporter:** Sparky detects generated Python code and provides an instant `.py` download button.
* **🎛️ Model Customization Sliders:** Adjust temperature (creativity) and max output tokens.
* **📥 Export Chat Transcript:** Download full conversation histories as clean `.txt` files.

---

## 🚀 Quickstart & Installation

Ensure you have Python 3.9 or higher installed, then run the following commands in your terminal to get everything set up at once:

```bash
# 1. Clone the repository and navigate into the folder
git clone [https://github.com/your-username/sparky-gemini-chatbot.git](https://github.com/your-username/sparky-gemini-chatbot.git)
cd sparky-gemini-chatbot

# 2. Install the required dependencies
pip install -r requirements.txt

# 3. Set your API Key (Replace with your actual key from Google AI Studio)
# For macOS / Linux:
export GEMINI_API_KEY="your_actual_api_key_here"

# For Windows (Command Prompt):
 setx GEMINI_API_KEY "your_actual_api_key_here"

# 4. Start the application
streamlit run app.py

📝 License
This project is open-source and available under the MIT License. 