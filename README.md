Gen AI Multi-Modal Chatbot

This is a Flask-based web application that integrates various AI models to provide a multi-modal chat experience. It allows users to generate text, create images, and translate languages within a unified interface.

## 🚀 Features

* **Text Generation**: Uses the **Mistral-Nemo-Instruct** model via Hugging Face to generate concise, bullet-point descriptions based on user prompts.
* **Image Generation**: Uses the **FLUX.1-dev** model via Hugging Face to generate images from text descriptions.
* **Language Translation**: Automatically detects input languages and translates them to English using `deep-translator`.
* **Dynamic UI**: A clean, responsive web interface that allows users to choose the type of response (Text, Image, or Translate) after sending a message.
* **Visual Cues**: Messages change background color based on text length.

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

* Python 3.7+
* pip (Python package manager)
* A **Hugging Face Account** (to obtain an API Token)

## 📦 Installation

1.  **Clone the repository** (or download the files to a folder).

2.  **Install the required dependencies**.
    Run the following command in your terminal to install the necessary Python libraries:

    ```bash
    pip install flask requests pillow deep-translator langdetect
    ```

## ⚙️ Configuration

To make the AI features work, you need to configure your API token.

1.  Open `app.py`.
2.  Locate the `headers` dictionary near the top of the file:
    ```python
    headers = {"Authorization": "Hugging Face Token"}
    ```
3.  Replace `"Hugging Face Token"` with your actual **Hugging Face Access Token**.
    * *Note: You can get a token by going to your Hugging Face Settings -> Access Tokens.*
    * *Your code should look like this example:* `headers = {"Authorization": "Bearer hf_xyz123..."}`

> **Security Note**: It is recommended to use environment variables (like a `.env` file) to hide your API keys in production, rather than hardcoding them in the file.

## 🏃‍♂️ Usage

1.  **Start the Application**:
    Run the following command in your terminal:
    ```bash
    python app.py
    ```

2.  **Access the Interface**:
    Open your web browser and navigate to:
    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

3.  **Interact**:
    * Type a message in the input box and click **Send**.
    * Three buttons will appear: **Text**, **Image**, and **Translate**.
    * Click the desired action to process your request.

## 📂 Project Structure

```text
/
├── app.py                # Main Flask application backend
├── .env                  # Environment variables (optional setup)
└── templates/
    └── index.html        # Frontend HTML/CSS/JS interface

🧩 Technologies Used
Backend: Flask (Python)

Frontend: HTML5, CSS3, JavaScript

AI Models:

Text: mistralai/Mistral-Nemo-Instruct-2407

Image: black-forest-labs/FLUX.1-dev

Utilities: deep_translator, langdetect, PIL (Pillow)
