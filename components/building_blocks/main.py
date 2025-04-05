import streamlit as st
from utils.ui_helpers import section_header
from .context import render_context_section
from .task import render_task_section
from .io_format import render_input_format_section, render_output_section
from .examples import render_examples_section
from .evaluation import render_evaluation_section
from .workflow_selector import render_workflow_selector
from .agent_selector import render_agent_selector
# Import new building blocks
from .enhanced_building_blocks import (
    render_content_intent_section,
    render_content_setup_section,
    render_design_requirements_section
)
# Import data injection module
from .data_injection import render_data_injection_section


def render_building_blocks_tab():
    """Render the Building Blocks tab content"""

    section_header("Prompt Building Blocks")

    # Create tab selection for building block categories
    block_category = st.radio(
        "Building Block Categories",
        ["Basic", "Enhanced", "Data & Examples", "Workflows & Agents"],
        horizontal=True,
        key="building_block_category"
    )

    if block_category == "Basic":
        # Original basic building blocks
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

    elif block_category == "Enhanced":
        # New enhanced building blocks
        col1, col2 = st.columns(2)

        with col1:
            render_content_intent_section()
            render_design_requirements_section()

        with col2:
            render_content_setup_section()

    elif block_category == "Data & Examples":
        # Data injection section
        render_data_injection_section()

    else:  # Workflows & Agents
        # Workflow and agent selectors
        render_workflow_selector()
        render_agent_selector()