import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_self_consistency_section():
    """Render the Self-Consistency workflow configuration section"""

    st.markdown("### Self-Consistency Checking Workflow")

    st.markdown("""
    Self-Consistency Checking validates outputs against multiple reasoning paths. 
    This workflow helps identify and correct inconsistencies before delivering the 
    final output, creating more reliable and coherent content.
    """)

    # Diagram
    st.image("https://via.placeholder.com/800x200?text=Self-Consistency+Workflow+Diagram",
             caption="Self-Consistency workflow showing validation across multiple reasoning paths",
             use_column_width=True)

    # Enable/disable toggle using a callback pattern
    if "self_consistency_enabled" not in st.session_state:
        st.session_state.self_consistency_enabled = False

    def on_toggle_change():
        # Callback updates the main session state variable from the widget-specific one
        st.session_state.self_consistency_enabled = st.session_state.consistency_component_toggle

    # Use the toggle with a unique key that doesn't conflict with session state variable
    self_consistency_enabled = st.toggle(
        "Enable Self-Consistency Checking",
        value=st.session_state.self_consistency_enabled,
        help="When enabled, outputs will be verified for consistency using multiple approaches",
        key="consistency_component_toggle",  # Unique key different from session state variable
        on_change=on_toggle_change
    )

    if self_consistency_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Consistency checks configuration
            st.markdown("#### Consistency Checks")

            # Core consistency checks
            st.markdown("Select aspects to check for consistency:")

            check_cols = st.columns(2)
            with check_cols[0]:
                factual_check = st.checkbox("Factual consistency", value=True, key="consistency_factual_check")
                logical_check = st.checkbox("Logical coherence", value=True, key="consistency_logical_check")
                contextual_check = st.checkbox("Contextual relevance", value=False, key="consistency_contextual_check")

            with check_cols[1]:
                contradictions_check = st.checkbox("Internal contradictions", value=True,
                                                   key="consistency_contradictions_check")
                style_check = st.checkbox("Style uniformity", value=False, key="consistency_style_check")
                completeness_check = st.checkbox("Completeness", value=True, key="consistency_completeness_check")

            # Validation method
            st.markdown("#### Validation Method")

            validation_method = st.selectbox(
                "Validation Method",
                ["Self-review only", "Multiple reasoning paths", "External knowledge verification"],
                index=1,
                help="Choose how to validate consistency and correctness"
            )

            # Custom consistency checking instructions
            st.text_area(
                "Custom consistency checking instructions",
                value="Verify that all statements are factually accurate, logically coherent, and free from internal contradictions. Ensure all claims are supported by evidence or reasoning.",
                height=100,
                key="consistency_instructions"
            )

        with col2:
            # Advanced settings
            st.markdown("#### Advanced Settings")

            # For multiple reasoning paths
            if validation_method == "Multiple reasoning paths":
                st.number_input(
                    "Number of Reasoning Paths",
                    min_value=2,
                    max_value=5,
                    value=3,
                    help="Number of different reasoning approaches to generate"
                )

                st.slider(
                    "Consistency Threshold",
                    min_value=50,
                    max_value=100,
                    value=70,
                    format="%d%%",
                    help="Percentage agreement required across reasoning paths"
                )

            # For external knowledge verification
            elif validation_method == "External knowledge verification":
                st.checkbox(
                    "Use RAG for verification",
                    value=True,
                    help="Use retrieval to verify factual claims against external sources"
                )

                st.checkbox(
                    "Include confidence scores",
                    value=True,
                    help="Include confidence level for each verified claim"
                )

            # Common settings
            st.markdown("#### Response Options")

            st.radio(
                "On Inconsistency",
                ["Flag inconsistencies", "Auto-correct inconsistencies", "Regenerate response", "Request human review"],
                index=1,
                help="Action to take when inconsistencies are detected"
            )

            st.checkbox(
                "Explain reasoning",
                value=True,
                help="Include explanation of consistency checking process"
            )

            st.checkbox(
                "Highlight uncertainties",
                value=True,
                help="Explicitly note areas of uncertainty or ambiguity"
            )

        # Example of how this workflow would be used
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of Self-Consistency Checking workflow
def self_consistency_workflow(input_text, num_paths=3, consistency_threshold=0.7):
    # Step 1: Generate multiple reasoning paths
    reasoning_paths = []

    for i in range(num_paths):
        reasoning_prompt = f\"\"\"
        Consider the following question and provide your reasoning path {i+1}.
        Think carefully about reaching a correct answer.

        Question: {input_text}

        Reasoning Path {i+1}:
        \"\"\"

        reasoning_result = llm_call(reasoning_prompt)
        reasoning_paths.append(reasoning_result)

    # Step 2: Extract conclusions from each reasoning path
    conclusions = []
    for path in reasoning_paths:
        conclusion_prompt = f\"\"\"
        Based on the following reasoning, what is the final conclusion?

        Reasoning: {path}

        Conclusion:
        \"\"\"

        conclusion = llm_call(conclusion_prompt)
        conclusions.append(conclusion)

    # Step 3: Check consistency across conclusions
    consistency_check_prompt = f\"\"\"
    Evaluate the consistency of the following conclusions for the question:

    Question: {input_text}

    Conclusions:
    {format_conclusions(conclusions)}

    Are these conclusions consistent? Provide a consistency score from 0.0 to 1.0.
    Explain any inconsistencies detected.
    \"\"\"

    consistency_result = llm_call(consistency_check_prompt)
    parsed_consistency = parse_consistency_result(consistency_result)

    # Step 4: Generate final response based on consistency check
    if parsed_consistency["score"] >= consistency_threshold:
        # Conclusions are consistent, synthesize final answer
        final_prompt = f\"\"\"
        Based on the following consistent reasoning paths, provide a final answer:

        Question: {input_text}

        Reasoning Paths:
        {format_reasoning_paths(reasoning_paths)}

        Provide a comprehensive and well-supported answer.
        \"\"\"

        final_answer = llm_call(final_prompt)
    else:
        # Inconsistencies detected, generate a nuanced response
        final_prompt = f\"\"\"
        The following reasoning paths have some inconsistencies:

        Question: {input_text}

        Reasoning Paths:
        {format_reasoning_paths(reasoning_paths)}

        Inconsistencies:
        {parsed_consistency["explanation"]}

        Provide a nuanced answer that acknowledges these uncertainties.
        \"\"\"

        final_answer = llm_call(final_prompt)

    return {
        "answer": final_answer,
        "reasoning_paths": reasoning_paths,
        "consistency_score": parsed_consistency["score"],
        "inconsistencies": parsed_consistency.get("explanation", "")
    }
            """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Tasks where accuracy and reliability are critical
            * Scenarios involving complex reasoning or multi-step problem solving
            * Applications where identifying uncertainties is important
            * Content where internal consistency is essential

            **Real-World Examples:**

            * Complex reasoning tasks with multiple stakeholders or considerations
            * Safety-critical applications where detecting inconsistencies is important
            * Content moderation systems that need to evaluate content across multiple dimensions
            * Mathematical or logical problem solving requiring verification
            """)

            # Citation from the article
            st.info("""
            *"Self-Consistency Checking validates outputs against multiple reasoning paths to identify 
            and correct inconsistencies before delivering the final output, creating more reliable and 
            coherent content. This creates a validation layer that improves the dependability of LLM responses."*
            """)