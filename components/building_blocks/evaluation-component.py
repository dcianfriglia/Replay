import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_evaluation_section():
    """Render the Evaluation Criteria section"""
    with st.container(border=True):
        section_with_info(
            "Evaluation Criteria",
            "Define metrics to assess output quality"
        )

        st.text_area(
            "Specify metrics and standards to evaluate the quality of generated content",
            value=st.session_state.evaluation_criteria,
            height=150,
            key="evaluation_criteria_area",
            on_change=lambda: setattr(st.session_state, "evaluation_criteria", st.session_state.evaluation_criteria_area)
        )

        # Advanced evaluation settings
        with st.expander("Advanced Evaluation Settings", expanded=False):
            subsection_header("Quality Metrics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                use_relevance = st.checkbox("Relevance", value=True, key="eval_relevance")
                use_accuracy = st.checkbox("Accuracy", value=True, key="eval_accuracy")
                use_completeness = st.checkbox("Completeness", value=True, key="eval_completeness")
            
            with col2:
                use_clarity = st.checkbox("Clarity", value=True, key="eval_clarity")
                use_actionability = st.checkbox("Actionability", value=True, key="eval_actionability")
                use_creativity = st.checkbox("Creativity", value=False, key="eval_creativity")
            
            # Store the selected metrics in session state
            st.session_state.selected_metrics = {
                "relevance": use_relevance,
                "accuracy": use_accuracy, 
                "completeness": use_completeness,
                "clarity": use_clarity,
                "actionability": use_actionability,
                "creativity": use_creativity
            }
            
            subsection_header("Evaluation Method")
            
            eval_method = st.radio(
                "Select evaluation method",
                ["Qualitative Assessment", "Rubric-Based Scoring", "Comparative Evaluation"],
                index=1,
                key="eval_method"
            )
            
            if eval_method == "Rubric-Based Scoring":
                st.slider(
                    "Score Threshold for Acceptance",
                    min_value=50,
                    max_value=100,
                    value=75,
                    format="%d%%",
                    key="eval_threshold"
                )