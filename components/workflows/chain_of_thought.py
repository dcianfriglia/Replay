import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_chain_of_thought_section():
    """Render the Chain-of-Thought workflow configuration section"""

    st.markdown("### Chain-of-Thought Workflow")

    st.markdown("""
    Chain-of-Thought breaks complex tasks into logical reasoning steps. 
    This workflow helps models work through multi-step reasoning by explicitly following 
    a sequence of steps, leading to more accurate and transparent results.
    """)

    # Render workflow diagram
    from .workflow_diagrams.chain_of_thought import render_chain_of_thought_diagram
    render_chain_of_thought_diagram()

    # Enable/disable toggle - using a callback to update the session state
    # Initialize the value if it doesn't exist
    if "thinking_steps_enabled" not in st.session_state:
        st.session_state.thinking_steps_enabled = True

    def on_toggle_change():
        # This is a callback that runs when the toggle changes
        # Update the main session state variable from the widget-specific one
        st.session_state.thinking_steps_enabled = st.session_state.cot_component_toggle

    # Use the toggle with a unique key that doesn't conflict with session state variable
    thinking_steps_enabled = st.toggle(
        "Enable Chain-of-Thought",
        value=st.session_state.thinking_steps_enabled,
        help="When enabled, the prompt will include step-by-step reasoning instructions",
        key="cot_component_toggle",  # Unique key different from session state variable
        on_change=on_toggle_change
    )

    if thinking_steps_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Thinking steps configuration
            st.markdown("#### Thinking Steps")

            # Initialize thinking steps if not present
            if "chain_of_thought_steps" not in st.session_state:
                st.session_state.chain_of_thought_steps = [
                    "Analyze requirements and current situation",
                    "Research key concepts relevant to the specific case",
                    "Outline content structure with clear sections",
                    "Draft content sections with practical examples",
                    "Review for consistency and completeness"
                ]

            # Display and manage thinking steps
            for i, step in enumerate(st.session_state.chain_of_thought_steps):
                cols = st.columns([10, 1])

                with cols[0]:
                    updated_step = st.text_input(f"Step {i + 1}", value=step, key=f"step_{i}")
                    st.session_state.chain_of_thought_steps[i] = updated_step

                with cols[1]:
                    if i > 0 and st.button("↑", key=f"cot_move_up_{i}"):
                        # Swap with previous step
                        st.session_state.chain_of_thought_steps[i], st.session_state.chain_of_thought_steps[i - 1] = \
                            st.session_state.chain_of_thought_steps[i - 1], st.session_state.chain_of_thought_steps[i]
                        st.rerun()

                    if i < len(st.session_state.chain_of_thought_steps) - 1 and st.button("↓", key=f"cot_move_down_{i}"):
                        # Swap with next step
                        st.session_state.chain_of_thought_steps[i], st.session_state.chain_of_thought_steps[i + 1] = \
                            st.session_state.chain_of_thought_steps[i + 1], st.session_state.chain_of_thought_steps[i]
                        st.rerun()

                    if len(st.session_state.chain_of_thought_steps) > 1 and st.button("×", key=f"cot_delete_{i}"):
                        # Remove this step
                        st.session_state.chain_of_thought_steps.pop(i)
                        st.rerun()

            # Add step button
            if st.button("+ Add Step", key="cot_add_step_btn"):
                st.session_state.chain_of_thought_steps.append(
                    f"New step {len(st.session_state.chain_of_thought_steps) + 1}")
                st.rerun()

        with col2:
            # Advanced settings
            st.markdown("#### Advanced Settings")

            cot_style = st.radio(
                "Reasoning Style",
                ["Sequential", "Branching", "Recursive"],
                index=0,
                help="How the chain of thought steps should be structured"
            )

            if cot_style == "Branching":
                st.info("Branching style allows for decision points and alternative paths in reasoning.")
            elif cot_style == "Recursive":
                st.info("Recursive style allows steps to be broken down into sub-steps when needed.")

            # Verbosity control
            st.select_slider(
                "Reasoning Verbosity",
                options=["Minimal", "Balanced", "Detailed", "Comprehensive"],
                value="Balanced",
                help="How detailed the step-by-step reasoning should be"
            )

            # Output handling
            st.radio(
                "Output Format",
                ["Show final result only", "Include reasoning steps", "Numbered steps with result"],
                index=1,
                help="How to format the final output with respect to reasoning steps"
            )

            # Additional settings
            st.checkbox(
                "Allow backtracking",
                value=True,
                help="Permit the model to revise earlier steps if needed"
            )

            st.checkbox(
                "Explicit verification",
                value=True,
                help="Add a verification step to check the reasoning"
            )

        # Example implementation
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of Chain-of-Thought workflow
def chain_of_thought_workflow(input_query, thinking_steps):
    # Format the thinking steps
    formatted_steps = "\\n".join([f"{i+1}. {step}" for i, step in enumerate(thinking_steps)])

    # Build the CoT prompt
    cot_prompt = f\"\"\"
    Please solve the following task step-by-step:

    {input_query}

    Think through this carefully using the following steps:
    {formatted_steps}

    For each step, show your reasoning explicitly before moving to the next step.
    After completing all steps, provide your final answer.
    \"\"\"

    # Make the LLM call
    response = llm_call(cot_prompt)

    return response
            """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Complex reasoning tasks requiring multiple steps
            * Math problems and logical puzzles
            * Decision-making scenarios with multiple factors
            * Analysis tasks requiring structured thinking
            * Content creation needing methodical development

            **Real-World Examples:**

            * Financial analysis requiring step-by-step calculations
            * Legal reasoning through case elements and precedents
            * Technical troubleshooting following logical diagnostics
            * Essay writing with clear thesis development
            * Code development following a structured approach
            """)

            # Citation from research
            st.info("""
            *"Chain-of-Thought prompting enables models to break down complex problems into intermediate steps. 
            Research shows that explicitly prompting the model to 'think step by step' significantly 
            improves performance on reasoning tasks, sometimes by 20-40% on challenging problems."*

            — Wei et al., "Chain of Thought Prompting Elicits Reasoning in Large Language Models"
            """)