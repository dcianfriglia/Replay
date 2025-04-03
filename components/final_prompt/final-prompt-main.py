import streamlit as st
from utils.ui_helpers import section_header
from .structure import render_prompt_structure
from .preview import render_prompt_preview


def render_final_prompt_tab():
    """Render the Final Prompt tab content"""

    section_header("Final Prompt")

    st.markdown("""
    This tab allows you to view and customize the final prompt structure based on your selected
    building blocks, workflows, and agents. You can rearrange sections, enable or disable specific
    components, and generate the final prompt for use with an LLM.
    """)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Render the prompt structure manager
        render_prompt_structure()
    
    with col2:
        # Render the prompt preview and actions
        render_prompt_preview()
    
    # Add button to generate content
    st.divider()
    
    col_a, col_b, col_c = st.columns([2, 2, 1])
    
    with col_a:
        st.button("Copy Prompt to Clipboard", type="secondary", use_container_width=True,
                 on_click=lambda: st.session_state.update({"copy_to_clipboard": True}))
    
    with col_b:
        st.button("Save as Template", type="secondary", use_container_width=True,
                 on_click=lambda: st.session_state.update({"save_as_template": True}))
    
    with col_c:
        st.button("Generate Content", type="primary", use_container_width=True,
                 on_click=lambda: st.session_state.update({"generated": True}))