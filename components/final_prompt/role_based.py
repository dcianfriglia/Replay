import streamlit as st
from utils.ui_helpers import subsection_header
from models.prompt_generator import generate_system_prompt, generate_user_prompt


def render_role_based_prompts():
    """Render the Role-Based Prompts section for system and user prompts"""

    # Initialize role-based preferences if not present
    if "system_prompt_sections" not in st.session_state:
        st.session_state.system_prompt_sections = {
            "Context & Background": True,
            "Persona Definition": True,
            "Tone & Voice": True,
            "Domain Expertise": True,
            "Constraints & Limitations": True,
            "Evaluation Criteria": False,
            "Self-Review Requirements": False
        }

    if "user_prompt_sections" not in st.session_state:
        st.session_state.user_prompt_sections = {
            "Task Definition": True,
            "Input Data Format": True,
            "Output Requirements": True,
            "Examples (Few-Shot Learning)": True,
            "Chain-of-Thought Instructions": True,
            "Fact Checking Instructions": False
        }

    subsection_header("Role-Based Prompt Configuration")

    st.markdown("""
    Organize your prompt into System and User components:
    - **System Prompt**: Sets the AI's persona, knowledge, constraints, and behavior
    - **User Prompt**: Contains the specific task, inputs, requirements, and examples
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### System Prompt Components")
        st.markdown("*Defines the AI assistant's personality and behavior*")

        # System prompt sections
        for section, included in st.session_state.system_prompt_sections.items():
            st.session_state.system_prompt_sections[section] = st.checkbox(
                section,
                value=included,
                key=f"system_{section}"
            )

        # System prompt preview
        with st.expander("System Prompt Preview", expanded=False):
            system_prompt = generate_system_prompt()
            st.code(system_prompt, language="markdown")

    with col2:
        st.markdown("### User Prompt Components")
        st.markdown("*Contains the specific task and requirements*")

        # User prompt sections
        for section, included in st.session_state.user_prompt_sections.items():
            st.session_state.user_prompt_sections[section] = st.checkbox(
                section,
                value=included,
                key=f"user_{section}"
            )

        # User prompt preview
        with st.expander("User Prompt Preview", expanded=False):
            user_prompt = generate_user_prompt()
            st.code(user_prompt, language="markdown")

    # Add custom sections
    st.markdown("### Add Custom Sections")

    custom_cols = st.columns([2, 2, 1])
    with custom_cols[0]:
        custom_section = st.text_input("Custom Section Name", key="custom_role_section_name")

    with custom_cols[1]:
        role_type = st.selectbox("Add to", ["System Prompt", "User Prompt"], key="custom_role_section_type")

    with custom_cols[2]:
        if st.button("Add Section", key="add_role_section_btn"):
            if custom_section:
                if role_type == "System Prompt":
                    st.session_state.system_prompt_sections[custom_section] = True
                else:
                    st.session_state.user_prompt_sections[custom_section] = True
                st.rerun()

    # Combined preview
    with st.expander("Complete Prompt Preview", expanded=True):
        # Format the complete prompt
        system_prompt = generate_system_prompt()
        user_prompt = generate_user_prompt()

        col_sys, col_user = st.columns(2)

        with col_sys:
            st.markdown("**System Prompt:**")
            st.code(system_prompt, language="markdown")

        with col_user:
            st.markdown("**User Prompt:**")
            st.code(user_prompt, language="markdown")

        # Store in session state for other components to use
        st.session_state.final_system_prompt = system_prompt
        st.session_state.final_user_prompt = user_prompt