import streamlit as st
from utils.ui_helpers import section_with_info


def render_task_section():
    """Render the Task Definition section"""
    with st.container(border=True):
        section_with_info(
            "Task Definition",
            "Clearly define what needs to be accomplished"
        )

        st.text_area(
            "Define the specific task the LLM needs to perform",
            value=st.session_state.task,
            height=150,
            key="task_input",
            on_change=lambda: setattr(st.session_state, "task", st.session_state.task_input)
        )