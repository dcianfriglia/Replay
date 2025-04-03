import streamlit as st
from utils.ui_helpers import section_header
from models.prompt_generator import simulate_content_generation
from .metrics import render_quality_metrics
from .feedback import render_feedback_section


def render_content_display():
    """Render the Content Display section for generated content"""
    
    st.markdown("---")
    section_header("Generated Content")
    
    # Check if content is available or needs to be generated
    if "result_content" not in st.session_state:
        # Simulate or call API to generate content
        st.session_state.result_content = simulate_content_generation()
    
    # Display regenerate option
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("This content was generated based on your prompt configuration.")
    
    with col2:
        if st.button("Regenerate", type="secondary", use_container_width=True):
            # Clear the current result and generate new content
            if "result_content" in st.session_state:
                del st.session_state.result_content
            st.rerun()
    
    # Display the generated content in a markdown box
    with st.container(border=True, height=400):
        st.markdown(st.session_state.result_content)
    
    # Action buttons for the content
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.download_button(
            "Download Content",
            data=st.session_state.result_content,
            file_name="generated_content.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col_b:
        st.button("Copy to Clipboard", use_container_width=True)
    
    with col_c:
        st.button("Refine Content", type="primary", use_container_width=True,
                 on_click=lambda: st.session_state.update({"refine_content": True}))
    
    # Display quality metrics
    render_quality_metrics(st.session_state.result_content)
    
    # Display feedback section
    render_feedback_section()