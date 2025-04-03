import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_evaluator_optimizer_section():
    """Render the Evaluator-Optimizer workflow configuration section"""

    st.markdown("### Evaluator-Optimizer Workflow")

    st.markdown("""
    In the Evaluator-Optimizer workflow, one LLM call generates a response while another 
    provides evaluation and feedback in a loop. This creates an iterative improvement cycle 
    that continues until meeting quality criteria or reaching iteration limits.
    """)

    # Diagram
    st.image("https://via.placeholder.com/800x200?text=Evaluator-Optimizer+Workflow+Diagram",
             caption="Evaluator-Optimizer workflow showing the feedback loop between generator and evaluator",
             use_column_width=True)

    # Enable/disable toggle
    evaluator_optimizer_enabled = st.toggle("Enable Evaluator-Optimizer",
                                            value=st.session_state.get("evaluator_optimizer_enabled", False),
                                            help="When enabled, content will be evaluated and improved iteratively")
    st.session_state.evaluator_optimizer_enabled = evaluator_optimizer_enabled

    if evaluator_optimizer_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Generator configuration
            st.markdown("#### Generator Configuration")

            st.selectbox(
                "Generator Model",
                ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                index=0,
                help="Model used for content generation"
            )

            st.text_area(
                "Generator Instructions",
                value="Generate a comprehensive and well-structured response to the input query.",
                height=100,
                help="Instructions for the generator on how to create content"
            )

            # Evaluator configuration
            st.markdown("#### Evaluator Configuration")

            st.selectbox(
                "Evaluator Model",
                ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                index=0,
                help="Model used for content evaluation (can be same or different from generator)"
            )

            # Initialize evaluation criteria if not present
            if "evaluator_criteria" not in st.session_state:
                st.session_state.evaluator_criteria = [
                    {"name": "Accuracy", "description": "Factual correctness and absence of errors", "weight": 5},
                    {"name": "Clarity", "description": "Clear and understandable explanations", "weight": 4},
                    {"name": "Completeness", "description": "Comprehensive coverage of the topic", "weight": 3},
                    {"name": "Relevance", "description": "Direct relevance to the query or task", "weight": 4}
                ]

            st.markdown("#### Evaluation Criteria")

            # Display and manage evaluation criteria
            for i, criterion in enumerate(st.session_state.evaluator_criteria):
                with st.container(border=True):
                    cols = st.columns([2, 2, 1, 1])

                    with cols[0]:
                        criterion["name"] = st.text_input(f"Criterion {i + 1}", value=criterion["name"],
                                                          key=f"criterion_name_{i}")

                    with cols[1]:
                        criterion["description"] = st.text_input("Description", value=criterion["description"],
                                                                 key=f"criterion_desc_{i}")

                    with cols[2]:
                        criterion["weight"] = st.slider("Weight", min_value=1, max_value=5, value=criterion["weight"],
                                                        key=f"criterion_weight_{i}")

                    with cols[3]:
                        if i > 0 and st.button("Remove", key=f"remove_criterion_{i}"):
                            st.session_state.evaluator_criteria.pop(i)
                            st.rerun()

            # Add criterion button
            if st.button("+ Add Criterion"):
                st.session_state.evaluator_criteria.append({
                    "name": f"New Criterion",
                    "description": "Description of this criterion",
                    "weight": 3
                })
                st.rerun()

        with col2:
            # Loop configuration
            st.markdown("#### Loop Configuration")

            st.number_input(
                "Maximum Iterations",
                min_value=1,
                max_value=10,
                value=3,
                help="Maximum number of improvement iterations"
            )

            st.slider(
                "Quality Threshold",
                min_value=0.5,
                max_value=0.95,
                value=0.8,
                format="%.2f",
                help="Minimum quality score to accept final output"
            )

            st.checkbox(
                "Enable early stopping",
                value=True,
                help="Stop iterations when quality threshold is reached"
            )

            st.checkbox(
                "Preserve feedback history",
                value=True,
                help="Include all feedback history in each iteration"
            )

            st.markdown("#### Process Controls")

            st.radio(
                "Feedback Granularity",
                ["Detailed (per criterion)", "Summary only", "Hybrid"],
                index=0,
                help="Level of detail in feedback provided to generator"
            )

            st.checkbox(
                "Allow evaluator to edit",
                value=False,
                help="Allow evaluator to directly edit content rather than just provide feedback"
            )

            st.checkbox(
                "Show iteration progress",
                value=True,
                help="Display intermediate results during iterations"
            )

        # Example of how this workflow would be used
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of Evaluator-Optimizer workflow
def evaluator_optimizer_workflow(input_text, criteria, max_iterations=3, quality_threshold=0.8):
    # Initial generation
    generator_prompt = f\"\"\"
    Generate a comprehensive response to the following:
    {input_text}
    \"\"\"

    current_content = llm_call(generator_prompt)
    feedback_history = []

    # Iterative improvement loop
    for iteration in range(max_iterations):
        # Evaluate current content
        evaluator_prompt = f\"\"\"
        Evaluate the following content based on these criteria:
        {format_criteria(criteria)}

        Content to evaluate:
        {current_content}

        Provide a detailed assessment for each criterion and suggestions for improvement.
        Also assign a score from 0.0 to 1.0 for each criterion, and calculate an overall score.
        \"\"\"

        evaluation_result = llm_call(evaluator_prompt)
        parsed_evaluation = parse_evaluation(evaluation_result)
        feedback_history.append(parsed_evaluation)

        # Check if quality threshold is met
        if parsed_evaluation["overall_score"] >= quality_threshold:
            print(f"Quality threshold met after {iteration+1} iterations")
            break

        # Generate improved content
        optimization_prompt = f\"\"\"
        Please improve the following content based on the provided feedback:

        Original Content:
        {current_content}

        Feedback:
        {parsed_evaluation["feedback"]}

        Provide an improved version that addresses all the feedback points.
        \"\"\"

        current_content = llm_call(optimization_prompt)

    return {
        "final_content": current_content,
        "iterations": iteration + 1,
        "feedback_history": feedback_history,
        "final_score": parsed_evaluation["overall_score"]
    }
            """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Content that requires high quality based on clear evaluation criteria
            * Tasks where improvement through feedback provides measurable value
            * Projects where quality is more important than latency
            * Content types that human writers would typically revise multiple times

            **Real-World Examples:**

            * Literary translation with nuances the translator might miss initially
            * Technical writing that requires multiple improvement passes
            * Creative content that benefits from structured critique and revision
            * Complex search tasks requiring multiple rounds of searching and analysis
            """)

            # Citation from the Anthropic article
            st.info("""
            *"This workflow is particularly effective when we have clear evaluation criteria, and when 
            iterative refinement provides measurable value. The two signs of good fit are, first, that 
            LLM responses can be demonstrably improved when a human articulates their feedback; and second, 
            that the LLM can provide such feedback."*

            — Anthropic Engineering
            """)