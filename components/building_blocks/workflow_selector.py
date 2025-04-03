import streamlit as st
from utils.ui_helpers import section_with_info, workflow_option


def render_workflow_selector():
    """Render the Workflow Selector section"""
    with st.container(border=True):
        section_with_info(
            "Selected Workflow Patterns",
            "Choose workflow patterns to include in your prompt"
        )

        st.markdown("Select the workflow patterns you want to use in your prompt engineering framework:")

        col1, col2 = st.columns(2)

        with col1:
            # Initialize workflow states if not present
            if "thinking_steps_enabled" not in st.session_state:
                st.session_state.thinking_steps_enabled = True

            if "iterative_refinement_enabled" not in st.session_state:
                st.session_state.iterative_refinement_enabled = False

            if "few_shot_enabled" not in st.session_state:
                st.session_state.few_shot_enabled = True

            # Display workflow options - using unique keys for workflow_selector version
            chain_of_thought = workflow_option(
                "Chain-of-Thought",
                "Break complex tasks into logical steps for better reasoning",
                "cot_workflow_selector"  # Changed key to be unique
            )
            # Update the actual session state variable
            st.session_state.thinking_steps_enabled = chain_of_thought

            iterative_refinement = workflow_option(
                "Iterative Refinement",
                "Gradually improve output through multiple generations",
                "iterative_workflow_selector"  # Changed key to be unique
            )
            # Update the actual session state variable
            st.session_state.iterative_refinement_enabled = iterative_refinement

            few_shot = workflow_option(
                "Few-Shot Learning",
                "Use examples to guide the model's understanding",
                "few_shot_workflow_selector"  # Changed key to be unique
            )
            # Update the actual session state variable
            st.session_state.few_shot_enabled = few_shot

        with col2:
            # Initialize additional workflow states if not present
            if "rag_enabled" not in st.session_state:
                st.session_state.rag_enabled = False

            if "self_consistency_enabled" not in st.session_state:
                st.session_state.self_consistency_enabled = False

            if "routing_enabled" not in st.session_state:
                st.session_state.routing_enabled = False

            # Display additional workflow options - using unique keys
            rag = workflow_option(
                "Retrieval-Augmented Generation",
                "Enhance responses with external knowledge",
                "rag_workflow_selector"  # Changed key to be unique
            )
            # Update the actual session state variable
            st.session_state.rag_enabled = rag

            self_consistency = workflow_option(
                "Self-Consistency Checking",
                "Validate outputs against multiple reasoning paths",
                "consistency_workflow_selector"  # Changed key to be unique
            )
            # Update the actual session state variable
            st.session_state.self_consistency_enabled = self_consistency

            routing = workflow_option(
                "Routing",
                "Direct inputs to specialized handlers based on type",
                "routing_workflow_selector"  # Changed key to be unique
            )
            # Update the actual session state variable
            st.session_state.routing_enabled = routing

        # Update selected workflows in session state
        selected_workflows = []
        if chain_of_thought:
            selected_workflows.append("Chain-of-Thought")
        if iterative_refinement:
            selected_workflows.append("Iterative Refinement")
        if few_shot:
            selected_workflows.append("Few-Shot Learning")
        if rag:
            selected_workflows.append("Retrieval-Augmented Generation")
        if self_consistency:
            selected_workflows.append("Self-Consistency Checking")
        if routing:
            selected_workflows.append("Routing")

        st.session_state.selected_workflows = selected_workflows

        # Display hint if no workflows selected
        if not selected_workflows:
            st.warning("Select at least one workflow pattern to be included in your prompt.")