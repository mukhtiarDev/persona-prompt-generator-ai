🧙 Persona Prompt Generator

Streamlit App - (https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
(https://mukhtiarDev-persona-prompt-generator-ai.streamlit.app/)

## ✨ Overview

The Persona Prompt Generator-- is a unique Gen AI application built with Streamlit and the Gemini API. Its purpose is to solve the common challenge of writing effective "System Prompts" for large language models (LLMs).

Instead of starting from a blank page, users define a --Role--, --Task--, and --Tone--, and the app uses a powerful meta-prompt to generate a highly-structured, copy-paste-ready System Prompt.

This is ideal for enhancing RAG (Retrieval Augmented Generation) pipelines, complex reasoning tasks, and ensuring consistent LLM behavior.

## ⚙️ Core Technology

- --App Framework:-- [Streamlit](https://streamlit.io/) (for fast, elegant UI)
- --LLM Model:-- Gemini API (`gemini-2.5-flash`)
- --Hosting:-- Streamlit Community Cloud (free, scalable deployment)

## 🚀 How to Use

1.  --Define the Role:-- What persona should the AI adopt? (e.g., -Senior Financial Analyst-)
2.  --Define the Task:-- What is the primary goal? (e.g., -Analyze the Q3 report and identify 3 key risks.-)
3.  --Define the Tone:-- What style should the output follow? (e.g., -Ultra-precise and skeptical-)

The application will output a detailed prompt ready for use as the `system_instruction` parameter in any LLM API call.

## 🛠️ Local Setup

To run this app locally:

1.  --Clone the Repository:--
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR-USERNAME]/ai-prompt-generator.git
    cd ai-prompt-generator
    ```
2.  --Install Dependencies:--
    ```bash
    pip install -r requirements.txt
3.  --Install correct packages:--
    ```
4.  --Set Environment Variable:-- Create a file named `.streamlit/secrets.toml` and add your API key (This simulates Streamlit Secrets locally):
    ```toml
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
5.  --Run the App:--
    ```bash
    streamlit run app.py
    ```