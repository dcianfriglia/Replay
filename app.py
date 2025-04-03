import streamlit as st
import os
from utils.state_management import initialize_session_state
from utils.template_manager import list_templates, save_template, load_template
from utils.state_persistence import (
    save_state_to_local_storage,
    load_state_from_local_storage,
    list_saved_states,
    delete_saved_state
)
from components.building_blocks import render_building_blocks_tab
from components.workflows import render_workflows_tab
from components.agents import render_agents_tab
from components.final_prompt import render_final_prompt_tab
from components.content_display import render_content_display

# Set page config
st.set_page_config(
    page_title="LLM Prompt Engineering Framework",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and apply custom CSS
with open(os.path.join(os.path.dirname(__file__), "styles", "main.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_session_management():
    """Render session management UI (save/load state)"""
    with st.expander("Session Management", expanded=False):
        st.markdown("### Save/Load Session")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Save Current Session")
            session_name = st.text_input("Session Name (optional)", key="session_save_name")

            if st.button("Save Session", use_container_width=True):
                filename = save_state_to_local_storage(session_name if session_name else None)
                st.success(f"Session saved as: {os.path.basename(filename)}")

        with col2:
            st.markdown("#### Load Saved Session")
            load_state_from_local_storage()


def main():
    # Initialize session state
    initialize_session_state()

    # Header section
    col_header_left, col_header_right = st.columns([3, 1])
    with col_header_left:
        st.markdown('<div class="main-header">LLM Prompt Engineering Framework</div>', unsafe_allow_html=True)
    with col_header_right:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Save State", use_container_width=True):
                st.session_state.show_save_dialog = True
        with col_b:
            if st.button("Load State", use_container_width=True):
                st.session_state.show_load_dialog = True

    # Show save/load dialogs if requested
    if st.session_state.get("show_save_dialog", False):
        with st.expander("Save Current State", expanded=True):
            session_name = st.text_input("State Name", key="save_state_name")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Save", key="save_state_confirm", use_container_width=True):
                    filename = save_state_to_local_storage(session_name if session_name else None)
                    st.success(f"State saved as: {os.path.basename(filename)}")
                    st.session_state.show_save_dialog = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key="save_state_cancel", use_container_width=True):
                    st.session_state.show_save_dialog = False
                    st.rerun()

    if st.session_state.get("show_load_dialog", False):
        with st.expander("Load Saved State", expanded=True):
            saved_states = list_saved_states()

            if not saved_states:
                st.warning("No saved states found.")
                if st.button("Close", key="load_state_close_empty"):
                    st.session_state.show_load_dialog = False
                    st.rerun()
            else:
                state_options = [f"{state['display_name']} ({state['saved_at'][:10]})" for state in saved_states]
                selected_state_idx = st.selectbox(
                    "Select a saved state to load:",
                    range(len(state_options)),
                    format_func=lambda i: state_options[i],
                    key="load_state_select"
                )

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("Load", key="load_state_confirm", use_container_width=True):
                        if load_state_from_local_storage(saved_states[selected_state_idx]["path"]):
                            st.success("State loaded successfully!")
                            st.session_state.show_load_dialog = False
                            st.rerun()
                with col2:
                    if st.button("Delete", key="delete_state", use_container_width=True):
                        if delete_saved_state(saved_states[selected_state_idx]["path"]):
                            st.warning("State deleted.")
                            st.session_state.show_load_dialog = False
                            st.rerun()
                with col3:
                    if st.button("Cancel", key="load_state_cancel", use_container_width=True):
                        st.session_state.show_load_dialog = False
                        st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="main-header">Framework</div>', unsafe_allow_html=True)

        # Project selector
        st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)
        projects = ["Content Marketing", "Technical Documentation", "Creative Writing", "+ New Project"]
        selected_project = st.selectbox("Select Project", projects, index=0, label_visibility="collapsed")

        # Templates
        st.markdown('<div class="section-header">Templates</div>', unsafe_allow_html=True)
        template_options = list_templates()
        if not template_options:
            template_options = ["Default Template"]
        template_options.append("+ Save Current as Template")
        selected_template = st.selectbox("Templates", template_options, index=0, label_visibility="collapsed")

        if selected_template == "+ Save Current as Template":
            template_name = st.text_input("Template Name")
            if st.button("Save Template") and template_name:
                template_data = {
                    # Collect all session state data to save
                    "context": st.session_state.context,
                    "task": st.session_state.task,
                    "input_format": st.session_state.input_format,
                    "input_description": st.session_state.input_description,
                    "output_format": st.session_state.output_format,
                    "output_tone": st.session_state.output_tone,
                    "output_requirements": st.session_state.output_requirements,
                    "examples": st.session_state.examples,
                    "constraints": st.session_state.constraints,
                    "evaluation_criteria": st.session_state.evaluation_criteria,
                    "selected_workflows": st.session_state.selected_workflows,
                    "selected_agents": st.session_state.selected_agents,
                    "chain_of_thought_steps": st.session_state.chain_of_thought_steps,
                    "prompt_structure": st.session_state.prompt_structure
                }
                saved_path = save_template(template_data, template_name)
                st.success(f"Template saved to {saved_path}")
        elif selected_template in template_options and selected_template != "Default Template":
            if st.button("Load Template"):
                file_path = f"templates/{selected_template.replace(' ', '_')}.json"
                template_data = load_template(file_path)
                for key, value in template_data.items():
                    if key in st.session_state:
                        st.session_state[key] = value
                st.success(f"Loaded template: {selected_template}")

        # Session Management
        render_session_management()

        # Actions
        st.divider()
        if st.button("Generate Content", type="primary", use_container_width=True):
            st.session_state.generated = True
            # In a real implementation, we would use an API call to an LLM service
            if "result_content" not in st.session_state:
                st.session_state.result_content = """## Implementing Agile in Software Development

Agile methodologies have revolutionized software development by emphasizing iterative progress, team collaboration, and customer feedback. This guide will help you understand and implement Agile practices in your organization.

... (content continues)
"""

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Building Blocks", "Workflows", "Agents", "Final Prompt"])

    # Render each tab
    with tab1:
        render_building_blocks_tab()

    with tab2:
        render_workflows_tab()

    with tab3:
        render_agents_tab()

    with tab4:
        render_final_prompt_tab()

    # Show generated content if available
    if "generated" in st.session_state and st.session_state.generated:
        render_content_display()