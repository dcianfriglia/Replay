import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_iterative_refinement_section():
    """Render the Iterative Refinement workflow configuration section"""

    st.markdown("### Iterative Refinement Workflow")

    st.markdown("""
    Iterative Refinement gradually improves content through multiple generations.
    This workflow involves generating initial content, evaluating it against criteria,
    and refining it over multiple iterations to reach higher quality.
    """)

    # Render workflow diagram
    from .workflow_diagrams.iterative import render_iterative_diagram
    render_iterative_diagram()

    # Enable/disable toggle using a callback pattern
    if "iterative_refinement_enabled" not in st.session_state:
        st.session_state.iterative_refinement_enabled = False

    def on_toggle_change():
        # Callback updates the main session state variable from the widget-specific one
        st.session_state.iterative_refinement_enabled = st.session_state.iterative_component_toggle

    # Use the toggle with a unique key that doesn't conflict with session state variable
    iterative_refinement_enabled = st.toggle(
        "Enable Iterative Refinement",
        value=st.session_state.iterative_refinement_enabled,
        help="When enabled, content will be iteratively improved",
        key="iterative_component_toggle",  # Unique key different from session state variable
        on_change=on_toggle_change
    )

    # Use the toggle with a key that matches the session state variable
    iterative_refinement_enabled = st.toggle(
        "Enable Iterative Refinement",
        value=st.session_state.iterative_refinement_enabled,
        help="When enabled, content will be iteratively improved",
        key="iterative_refinement_enabled",
        on_change=on_toggle_change
    )

    if iterative_refinement_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Refinement configuration
            st.markdown("#### Refinement Configuration")

            # Initialize iterative settings if not present
            if "iterative_iterations" not in st.session_state:
                st.session_state.iterative_iterations = 3

            if "iterative_focus" not in st.session_state:
                st.session_state.iterative_focus = ["Clarity", "Accuracy", "Coherence"]

            # Iterations configuration
            st.number_input(
                "Number of iterations",
                min_value=2,
                max_value=5,
                value=st.session_state.iterative_iterations,
                key="iterations_input",
                help="How many refinement iterations to perform",
                on_change=lambda: setattr(st.session_state, "iterative_iterations", st.session_state.iterations_input)
            )

            # Refinement focus areas
            st.markdown("#### Refinement Focus")

            col_a, col_b = st.columns(2)

            with col_a:
                focus_clarity = st.checkbox("Clarity", value="Clarity" in st.session_state.iterative_focus,
                                            key="iterative_focus_clarity")
                focus_accuracy = st.checkbox("Accuracy", value="Accuracy" in st.session_state.iterative_focus,
                                             key="iterative_focus_accuracy")
                focus_coherence = st.checkbox("Coherence", value="Coherence" in st.session_state.iterative_focus,
                                              key="iterative_focus_coherence")

            with col_b:
                focus_conciseness = st.checkbox("Conciseness", value="Conciseness" in st.session_state.iterative_focus,
                                                key="iterative_focus_conciseness")
                focus_completeness = st.checkbox("Completeness",
                                                 value="Completeness" in st.session_state.iterative_focus,
                                                 key="iterative_focus_completeness")
                focus_style = st.checkbox("Style", value="Style" in st.session_state.iterative_focus,
                                         key="iterative_focus_style")

            # Update focus areas in session state
            st.session_state.iterative_focus = [
                area for area, enabled in [
                    ("Clarity", focus_clarity),
                    ("Accuracy", focus_accuracy),
                    ("Coherence", focus_coherence),
                    ("Conciseness", focus_conciseness),
                    ("Completeness", focus_completeness),
                    ("Style", focus_style)
                ] if enabled
            ]

            # Custom instructions
            st.markdown("#### Custom Refinement Instructions")

            st.text_area(
                "Provide specific instructions for refinement process",
                value=st.session_state.get("iterative_instructions",
                                           "Improve the clarity and conciseness of the content. Ensure all concepts are explained clearly and information flows logically. Fix any grammatical or style issues."),
                height=100,
                key="iterative_instructions_input",
                on_change=lambda: setattr(st.session_state, "iterative_instructions",
                                          st.session_state.iterative_instructions_input)
            )

        with col2:
            # Advanced settings
            st.markdown("#### Advanced Settings")

            st.radio(
                "Refinement Approach",
                ["Self-refinement", "Separate reviewer", "Multiple reviewers"],
                index=0,
                help="Who performs the evaluation and refinement",
                key="refinement_approach"
            )

            # Quality threshold
            st.slider(
                "Quality Threshold",
                min_value=0.5,
                max_value=0.95,
                value=0.8,
                step=0.05,
                format="%.2f",
                help="Minimum quality score to accept output",
                key="quality_threshold"
            )

            # Early stopping
            st.checkbox(
                "Enable early stopping",
                value=True,
                help="Stop iterations when quality threshold is reached",
                key="early_stopping"
            )

            # Feedback history
            st.radio(
                "Feedback History",
                ["Include all feedback", "Include last iteration only", "No previous feedback"],
                index=0,
                help="How much feedback history to include in each iteration",
                key="feedback_history"
            )

            # Show process
            st.checkbox(
                "Show iteration process",
                value=True,
                help="Show intermediate results during iterations",
                key="show_iterations"
            )

        # Example implementation
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of Iterative Refinement workflow
def iterative_refinement_workflow(input_query, focus_areas, max_iterations=3, quality_threshold=0.8):
    # Generate initial content
    initial_prompt = f\"\"\"
    Generate content addressing the following:

    {input_query}

    Provide a comprehensive response.
    \"\"\"

    current_content = llm_call(initial_prompt)

    # Initialize iteration tracking
    iterations = 1
    current_quality = 0.0
    refinement_history = []

    # Refinement loop
    while iterations < max_iterations and current_quality < quality_threshold:
        # Evaluate current content
        evaluation_prompt = f\"\"\"
        Evaluate the following content on these dimensions:
        {', '.join(focus_areas)}

        Content to evaluate:
        {current_content}

        For each dimension, provide specific feedback for improvement.
        Also assign an overall quality score from 0.0 to 1.0.
        \"\"\"

        evaluation = llm_call(evaluation_prompt)

        # Extract quality score and feedback (in a real implementation, parse this properly)
        current_quality = extract_quality_score(evaluation)
        feedback = extract_feedback(evaluation)

        refinement_history.append({
            "iteration": iterations,
            "content": current_content,
            "evaluation": evaluation,
            "quality": current_quality,
            "feedback": feedback
        })

        # Check if quality threshold is reached
        if current_quality >= quality_threshold:
            print(f"Quality threshold reached after {iterations} iterations")
            break

        # Refine content
        refinement_prompt = f\"\"\"
        Improve the following content based on this feedback:

        Content:
        {current_content}

        Feedback:
        {feedback}

        Focus especially on improving: {', '.join(focus_areas)}

        Provide a refined version that addresses all feedback points.
        \"\"\"

        current_content = llm_call(refinement_prompt)
        iterations += 1

    return {
        "final_content": current_content,
        "iterations": iterations,
        "final_quality": current_quality,
        "refinement_history": refinement_history
    }
            """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Content creation requiring high quality
            * Complex writing tasks with multiple quality dimensions
            * Tasks where initial outputs need significant improvement
            * Projects where quality is more important than speed
            * Cases where specific improvements need to be targeted

            **Real-World Examples:**

            * Professional writing like articles, reports, and essays
            * Technical documentation requiring precision and clarity
            * Marketing copy that needs to be polished and engaging
            * Complex explanations of difficult concepts
            * Critical communications that need careful crafting
            """)

            # Citation from research
            st.info("""
            *"Iterative refinement has been shown to significantly improve content quality, with 
            studies demonstrating that even one additional refinement iteration can improve quality 
            scores by 15-30%. This improvement is even more pronounced in complex or specialized domains."*

            — Research on LLM Output Optimization Techniques
            """)