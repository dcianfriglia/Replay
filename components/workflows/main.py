import streamlit as st
from utils.ui_helpers import section_header
from .chain_of_thought import render_chain_of_thought_section
from .iterative import render_iterative_refinement_section
from .few_shot import render_few_shot_section
from .rag import render_rag_section
from .consistency import render_self_consistency_section
from .orchestrator import render_orchestrator_section
from .evaluator_optimizer import render_evaluator_optimizer_section
from .routing import render_routing_section
from .parellalization_ import render_parallelization_section
# from .parallelization_ import render_parallelization_section


def render_workflows_tab():
    """Render the Workflows tab content"""

    section_header("Workflow Configuration")

    workflow_tabs = st.tabs([
        "Chain-of-Thought",
        "Iterative Refinement",
        "Few-Shot Learning",
        "RAG",
        "Self-Consistency",
        "Routing",
        "Parallelization",
        "Orchestrator-Workers",
        "Evaluator-Optimizer"
    ])

    # Chain-of-Thought tab
    with workflow_tabs[0]:
        render_chain_of_thought_section()

    # Iterative Refinement tab
    with workflow_tabs[1]:
        render_iterative_refinement_section()

    # Few-Shot Learning tab
    with workflow_tabs[2]:
        render_few_shot_section()

    # RAG tab
    with workflow_tabs[3]:
        render_rag_section()

    # Self-Consistency tab
    with workflow_tabs[4]:
        render_self_consistency_section()

    # Routing tab
    with workflow_tabs[5]:
        render_routing_section()

    # Parallelization tab
    with workflow_tabs[6]:
        render_parallelization_section()

    # Orchestrator-Workers tab
    with workflow_tabs[7]:
        render_orchestrator_section()

    # Evaluator-Optimizer tab
    with workflow_tabs[8]:
        render_evaluator_optimizer_section()