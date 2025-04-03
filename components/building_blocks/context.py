import streamlit as st
from utils.ui_helpers import section_with_info


def render_context_section():
    """Render the Context & Background section"""
    with st.container(border=True):
        section_with_info(
            "Context & Background",
            "Provide domain knowledge and relevant context for the LLM"
        )

        st.text_area(
            "Provide domain knowledge and relevant context for the LLM",
            value=st.session_state.context,
            height=150,
            key="context_input",
            on_change=lambda: setattr(st.session_state, "context", st.session_state.context_input)
        )