import streamlit as st
from utils.ui_helpers import subsection_header
from models.prompt_generator import calculate_quality_metrics


def render_quality_metrics(content):
    """Render quality metrics for the generated content"""

    with st.container(border=True):
        subsection_header("Quality Metrics")

        st.markdown("""
        Quality metrics evaluate different aspects of the generated content.
        These metrics are calculated based on the evaluation criteria you specified.
        """)

        # Get metrics for the content
        if "quality_metrics" not in st.session_state:
            # Calculate metrics if not already present
            st.session_state.quality_metrics = calculate_quality_metrics(content)

        metrics = st.session_state.quality_metrics

        # Create metrics visualization
        cols = st.columns(len(metrics))

        for i, (metric_name, value) in enumerate(metrics.items()):
            with cols[i]:
                # Add color coding based on score
                if value >= 90:
                    color = "green"
                elif value >= 75:
                    color = "blue"
                elif value >= 60:
                    color = "orange"
                else:
                    color = "red"

                # Display metric as progress bar
                st.markdown(f"**{metric_name}**")
                st.progress(value / 100)
                st.markdown(f"<p style='text-align:center; color:{color};'><b>{value}%</b></p>",
                            unsafe_allow_html=True)

        # Add overall quality score
        overall_score = sum(metrics.values()) / len(metrics)

        st.markdown("---")
        st.markdown(f"### Overall Quality: {overall_score:.1f}%")

        # Quality improvement suggestions
        with st.expander("Quality Improvement Suggestions", expanded=False):
            lowest_metric = min(metrics.items(), key=lambda x: x[1])

            st.markdown(f"""
            #### Suggested Improvements

            The content could be improved by focusing on **{lowest_metric[0]}**:

            - Review the content for {lowest_metric[0].lower()} issues
            - Consider refining the prompt to emphasize {lowest_metric[0].lower()}
            - Add explicit instructions related to {lowest_metric[0].lower()} in your prompt

            You can use the "Refine Content" button to make targeted improvements.
            """)