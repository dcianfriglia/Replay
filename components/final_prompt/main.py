import streamlit as st
from utils.ui_helpers import section_header
from .structure import render_prompt_structure
from .preview import render_prompt_preview
from .role_based import render_role_based_prompts
from .execute_prompt import render_execution_controls


def render_final_prompt_tab():
    """Render the Final Prompt tab content"""

    section_header("Final Prompt")

    st.markdown("""
    This tab allows you to finalize your prompt structure, split content between system and user roles,
    and test your prompt against different models with various parameters.
    """)

    # Create tabs for different prompt organization approaches
    prompt_tabs = st.tabs([
        "Role-Based Prompts",
        "Structure Manager",
        "Raw Prompt Editor"
    ])

    # Tab 1: Role-Based Prompts (System/User)
    with prompt_tabs[0]:
        render_role_based_prompts()

    # Tab 2: Prompt Structure Manager (Original functionality)
    with prompt_tabs[1]:
        col1, col2 = st.columns([1, 1])

        with col1:
            # Render the prompt structure manager
            render_prompt_structure()

        with col2:
            # Render the prompt preview and actions
            render_prompt_preview()

    # Tab 3: Raw Prompt Editor
    with prompt_tabs[2]:
        if "raw_system_prompt" not in st.session_state:
            st.session_state.raw_system_prompt = "You are a helpful AI assistant with expertise in the requested domain."

        if "raw_user_prompt" not in st.session_state:
            st.session_state.raw_user_prompt = "Please provide information about the following topic:"

        col1, col2 = st.columns([1, 1])

        with col1:
            st.session_state.raw_system_prompt = st.text_area(
                "System Prompt (Instructions for the AI)",
                value=st.session_state.raw_system_prompt,
                height=200
            )

        with col2:
            st.session_state.raw_user_prompt = st.text_area(
                "User Prompt (The user's query)",
                value=st.session_state.raw_user_prompt,
                height=200
            )

    st.divider()

    # Add execution controls (model selection, parameters, run button)
    render_execution_controls()