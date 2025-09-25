import streamlit as st
import google.generativeai as genai
import json

# =========================
# --- GEMINI CONFIG ---
# =========================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    _ = genai.list_models()
except KeyError:
    st.error("🚨 GEMINI_API_KEY not found in Streamlit Secrets. Please configure it for deployment.")
    st.stop()
except Exception as e:
    st.error(f"❌ Gemini API configuration failed: {e}")
    st.stop()


# =========================
# --- CORE FUNCTION ---
# =========================
@st.cache_data(show_spinner=False)
def generate_persona_prompt(role, task, tone, model_name):
    """Generates a high-quality system prompt and returns both the result and the instruction used."""
    system_instruction = f"""
    You are an expert Prompt Engineer. Your task is to generate the most effective and detailed 'System Prompt'
    possible for a large language model. This prompt must be ready to copy/paste and will define the LLM's
    behavior, knowledge base, constraints, and output format for a highly specific task.

    --- USER-DEFINED PARAMETERS ---
    1. **ROLE:** '{role}'
    2. **PRIMARY TASK:** '{task}'
    3. **TONE/STYLE:** '{tone}'

    --- INSTRUCTIONS FOR YOU ---
    1. **Persona Definition:** Start with a declarative statement establishing the LLM's identity based on the ROLE.
    2. **Goal & Task:** Clearly state the PRIMARY TASK and the desired outcome.
    3. **Constraints:** List at least 3 critical constraints for the LLM to follow.
    4. **Output Format:** Specify the exact format for the LLM's final response.
    5. **Final Instruction:** End with a clear instruction on handling ambiguity.
    6. **Crucial:** DO NOT add any preamble or explanation. Just output the final, copy-paste-ready System Prompt.
    """
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(system_instruction)
    return response.text, system_instruction


# =========================
# --- PAGE NAVIGATION ---
# =========================
st.set_page_config(
    page_title="Persona Prompt Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Use session_state to store current page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "Home"
if st.sidebar.button("⚡ Generator"):
    st.session_state.page = "Generator"


# =========================
# --- PAGE 1: HOME ---
# =========================
if st.session_state.page == "Home":
    st.title("🧙 Persona Prompt Generator")
    st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=200)

    st.markdown("""
    ### Welcome! 👋  
    This tool helps you instantly generate **high-quality System Prompts** for LLMs.  
    Define a role, a task, and a tone/style — and get a copy-paste-ready prompt.  

    ✅ Useful for RAG pipelines  
    ✅ Great for AI agents  
    ✅ Saves hours of manual prompt crafting  
    """)

    if st.button("🚀 Let's Go!", type="primary"):
        st.session_state.page = "Generator"
        st.rerun()


# =========================
# --- PAGE 2: GENERATOR ---
# =========================
elif st.session_state.page == "Generator":
    # Sidebar Settings
    with st.sidebar:
        st.title("⚙️ Configuration")
        st.markdown("### Model Settings")
        model_choice = st.selectbox(
            "Select Gemini Model:",
            options=["gemini-2.5-flash", "gemini-2.5-pro"],
            help="Flash = faster/cheaper, Pro = deeper reasoning.",
            key="model_choice"
        )
        show_raw_prompt = st.toggle(
            "Show Raw System Instruction",
            value=False,
            key="show_raw_prompt"
        )
        st.info("💡 Use 'gemini-2.5-pro' for the most detailed prompts.")

    # Header
    st.title("⚡ Persona Prompt Generator")
    st.markdown("Fill in the fields below to create your custom System Prompt.")

    # --- FORM ---
    with st.form("prompt_form"):
        st.markdown("### Define the Persona")
        col1, col2 = st.columns([1, 1])

        # Predefined Role Options
        role_options = [
            "Senior Financial Analyst",
            "Creative Director",
            "History Professor",
            "Cybersecurity Expert",
            "Health & Fitness Coach",
            "Custom (Type Your Own)"
        ]
        with col1:
            role_choice = st.selectbox("1. AI's **ROLE**:", role_options)
            if role_choice == "Custom (Type Your Own)":
                role_input = st.text_input("Enter Custom Role:", value="")
            else:
                role_input = role_choice

        # Predefined Tone Options
        tone_options = [
            "Ultra-precise and skeptical",
            "Formal and objective",
            "Casual and friendly",
            "Motivational and inspiring",
            "Dark and suspenseful",
            "Custom (Type Your Own)"
        ]
        with col2:
            tone_choice = st.selectbox("3. **TONE/STYLE**:", tone_options)
            if tone_choice == "Custom (Type Your Own)":
                tone_input = st.text_input("Enter Custom Tone/Style:", value="")
            else:
                tone_input = tone_choice

        # Task input
        task_input = st.text_area(
            "2. **PRIMARY TASK**:",
            value="Analyze the Q3 earnings report and identify 3 key risks and 2 growth opportunities.",
            height=120
        )

        submit_button = st.form_submit_button("✨ Generate My System Prompt", type="primary")

    # --- GENERATION LOGIC ---
    if submit_button:
        if not all([role_input, task_input, tone_input]):
            st.error("⚠️ Please fill out all fields.")
        else:
            with st.spinner(f"Generating System Prompt using **{model_choice}**..."):
                try:
                    final_prompt, raw_instruction = generate_persona_prompt(
                        role_input, task_input, tone_input, model_choice
                    )

                    output_tab, info_tab = st.tabs(["💡 Generated System Prompt", "⚙️ Debug Info"])

                    with output_tab:
                        st.subheader("✅ Copy-Paste-Ready Prompt")

                        # Show nicely formatted code block
                        st.code(final_prompt, language="text")

                        # Copy-to-Clipboard Button
                        safe_prompt = json.dumps(final_prompt)
                        copy_button_html = f"""
                        <div style="margin-top:10px; margin-bottom:20px;">
                            <button onclick='navigator.clipboard.writeText({safe_prompt});'
                                    style="padding:10px 16px; border:none; border-radius:8px;
                                           background:#4CAF50; color:white; font-size:16px; cursor:pointer;">
                                📋 Copy Prompt
                            </button>
                        </div>
                        """
                        st.markdown(copy_button_html, unsafe_allow_html=True)

                        st.success("🎉 Success! Your prompt is ready.")

                    with info_tab:
                        st.subheader("Generation Details")
                        st.markdown(f"**Model Used:** `{model_choice}`")
                        if show_raw_prompt:
                            st.markdown("#### Raw Instruction Sent to Gemini:")
                            st.code(raw_instruction, language="text")
                        else:
                            st.info("Toggle 'Show Raw System Instruction' in the sidebar to view it.")

                except Exception as e:
                    st.exception(e)
                    st.error("❌ An error occurred during generation.")
