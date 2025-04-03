import streamlit as st
from utils.ui_helpers import section_header
from .context import render_context_section
from .task import render_task_section
from .io_format import render_input_format_section, render_output_section
from .examples import render_examples_section
from .evaluation import render_evaluation_section
from .workflow_selector import render_workflow_selector
from .agent_selector import render_agent_selector


def render_building_blocks_tab():
    """Render the Building Blocks tab content"""

    section_header("Prompt Building Blocks")

    col1, col2 = st.columns(2)

    with col1:
        render_context_section()
        render_input_format_section()

    with col2:
        render_task_section()
        render_output_section()

    col3, col4 = st.columns(2)

    with col3:
        render_examples_section()

    with col4:
        render_evaluation_section()

    render_workflow_selector()
    render_agent_selector()