import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_few_shot_section():
    """Render the Few-Shot Learning workflow configuration section"""

    st.markdown("### Few-Shot Learning Workflow")

    st.markdown("""
    Few-Shot Learning uses examples to guide the model's understanding of a task.
    By providing input-output pairs, this workflow helps the model understand patterns,
    formats, and expectations without requiring extensive instructions.
    """)

    # Diagram
    st.image("https://via.placeholder.com/800x200?text=Few-Shot+Learning+Workflow+Diagram",
             caption="Few-Shot Learning workflow showing examples guiding model behavior",
             use_column_width=True)

    # Enable/disable toggle using a callback pattern
    if "few_shot_enabled" not in st.session_state:
        st.session_state.few_shot_enabled = True

    def on_toggle_change():
        # Callback updates the main session state variable from the widget-specific one
        st.session_state.few_shot_enabled = st.session_state.few_shot_component_toggle

    # Use the toggle with a unique key that doesn't conflict with session state variable
    few_shot_enabled = st.toggle(
        "Enable Few-Shot Learning",
        value=st.session_state.few_shot_enabled,
        help="When enabled, examples will be included in prompts to guide model behavior",
        key="few_shot_component_toggle",  # Unique key different from session state variable
        on_change=on_toggle_change
    )

    if few_shot_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Example configuration
            st.markdown("#### Example Configuration")

            example_count = st.selectbox(
                "Number of Examples",
                ["1 Example (Minimal)", "3 Examples (Recommended)", "5 Examples (Comprehensive)"],
                index=1,
                help="Select the number of examples to include"
            )

            st.info("Examples are configured in the Building Blocks tab under 'Examples & Constraints'")

            # Example structure settings
            st.markdown("#### Example Structure")

            st.radio(
                "Example Format",
                ["Input/Output Pairs", "Detailed Step-by-Step", "Question/Answer Format", "Custom Format"],
                index=0,
                help="Choose how examples are structured and presented"
            )

            st.checkbox(
                "Include explanations with examples",
                value=False,
                help="Add explanations of why each example is correct"
            )

            st.checkbox(
                "Show progressive complexity",
                value=True,
                help="Order examples from simple to complex"
            )

        with col2:
            # Advanced settings
            st.markdown("#### Advanced Settings")

            st.selectbox(
                "Example Selection Strategy",
                ["Manual Selection", "Similarity-Based", "Diverse Coverage", "Dynamic Selection"],
                index=0,
                help="Method for selecting which examples to include"
            )

            st.checkbox(
                "Use negative examples",
                value=False,
                help="Include examples of incorrect outputs with explanations"
            )

            st.checkbox(
                "Cross-validation",
                value=False,
                help="Test different example sets to find the most effective ones"
            )

            st.slider(
                "Example Weight",
                min_value=1,
                max_value=5,
                value=3,
                help="How much emphasis to place on following the examples (relative to instructions)"
            )

        # Example of how this workflow would be used
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of Few-Shot Learning workflow
def few_shot_learning_workflow(input_text, examples):
    # Format the examples
    formatted_examples = ""
    for idx, example in enumerate(examples):
        formatted_examples += f\"\"\"
        Example {idx+1}:
        Input: {example['input']}
        Output: {example['output']}
        \"\"\"

    # Build the few-shot prompt
    prompt = f\"\"\"
    I'll show you some examples of the task, then ask you to complete a new instance.

    {formatted_examples}

    Now, please perform the same task:
    Input: {input_text}
    Output: 
    \"\"\"

    # Call the LLM with few-shot prompt
    response = llm_call(prompt)

    return response
            """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Tasks where the pattern or format is easier to demonstrate than explain
            * Applications requiring specific output formats or styles
            * Scenarios where detailed instructions would be complex or lengthy
            * When consistency with existing examples is important

            **Real-World Examples:**

            * Generating content in a specific style or voice
            * Creating structured data like JSON or XML outputs
            * Summarization with specific length and style requirements
            * Translation with particular tone or terminology preferences
            """)

            # Academic citation
            st.info("""
            *"Few-shot learning uses examples to guide the model's understanding. This workflow
            provides implicit guidance on style, tone, and depth, helping the model understand
            nuanced requirements without explicit instructions. It's most effective when examples
            closely match the desired output format and quality."*

            — Anthropic Engineering
            """)