import streamlit as st
from utils.ui_helpers import section_header, subsection_header


def render_critic_agent():
    """Render the Critic/Evaluator Agent configuration section"""

    st.markdown("### Critic/Evaluator Agent")

    st.markdown("""
    The Critic/Evaluator Agent assesses content against predefined criteria.
    This agent provides detailed feedback and evaluates quality across multiple dimensions.
    """)

    # Enable/disable toggle
    critic_enabled = st.toggle("Enable Critic/Evaluator Agent",
                              value=st.session_state.critic_enabled,
                              help="When enabled, this agent will evaluate content quality against criteria")
    st.session_state.critic_enabled = critic_enabled

    if critic_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Evaluation criteria
            subsection_header("Evaluation Criteria")

            # Initialize evaluation criteria if not present
            if "critic_evaluation_criteria" not in st.session_state:
                st.session_state.critic_evaluation_criteria = [
                    {"name": "Accuracy", "description": "Factual correctness and absence of errors", "weight": 5},
                    {"name": "Clarity", "description": "Clear and understandable explanations", "weight": 4},
                    {"name": "Completeness", "description": "Comprehensive coverage of the topic", "weight": 3},
                    {"name": "Relevance", "description": "Direct relevance to the query or task", "weight": 4}
                ]

            # Display and manage evaluation criteria
            for i, criterion in enumerate(st.session_state.critic_evaluation_criteria):
                with st.container(border=True):
                    cols = st.columns([2, 2, 1, 1])

                    with cols[0]:
                        criterion["name"] = st.text_input(f"Criterion {i + 1}", value=criterion["name"],
                                                          key=f"critic_name_{i}")

                    with cols[1]:
                        criterion["description"] = st.text_input("Description", value=criterion["description"],
                                                                 key=f"critic_desc_{i}")

                    with cols[2]:
                        criterion["weight"] = st.slider("Weight", min_value=1, max_value=5, value=criterion["weight"],
                                                        key=f"critic_weight_{i}")

                    with cols[3]:
                        if i > 0 and st.button("Remove", key=f"critic_remove_{i}"):
                            st.session_state.critic_evaluation_criteria.pop(i)
                            st.rerun()

            # Add criterion button
            if st.button("+ Add Criterion"):
                st.session_state.critic_evaluation_criteria.append({
                    "name": f"New Criterion",
                    "description": "Description of this criterion",
                    "weight": 3
                })
                st.rerun()

            # Evaluation method
            subsection_header("Evaluation Method")

            eval_method = st.radio(
                "Select evaluation method",
                ["Qualitative assessment", "Rubric-based scoring", "Comparative analysis"],
                index=1,
                key="critic_eval_method"
            )

            if eval_method == "Rubric-based scoring":
                st.slider(
                    "Minimum acceptable score (%)",
                    min_value=50,
                    max_value=90,
                    value=75,
                    key="critic_min_score"
                )

            # Instructions for Critic
            subsection_header("Instructions for Critic")

            st.text_area(
                "Provide specific instructions for this agent",
                value="Evaluate the content against each criterion, providing detailed feedback for improvement. Be specific about strengths and weaknesses. Suggest concrete ways to improve lower-scoring areas. Maintain a constructive tone throughout the evaluation.",
                height=150,
                key="critic_instructions"
            )

        with col2:
            # Model selection
            subsection_header("Model Configuration")

            st.selectbox(
                "Model",
                ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                index=0,
                key="critic_model"
            )

            # Advanced settings
            subsection_header("Advanced Settings")

            st.checkbox(
                "Provide overall score",
                value=True,
                key="critic_overall_score",
                help="Calculate and provide an overall score based on weighted criteria"
            )

            st.checkbox(
                "Score each criterion",
                value=True,
                key="critic_criterion_scores",
                help="Provide individual scores for each evaluation criterion"
            )

            st.checkbox(
                "Include improvement suggestions",
                value=True,
                key="critic_improvements",
                help="Provide specific suggestions for improvement in each area"
            )

            st.checkbox(
                "Compare to benchmarks",
                value=False,
                key="critic_benchmarks",
                help="Compare content to benchmark examples or standards"
            )

            st.checkbox(
                "Highlight exemplary elements",
                value=True,
                key="critic_highlight_good",
                help="Specifically identify particularly strong elements"
            )

            # Feedback detail level
            st.select_slider(
                "Feedback Detail Level",
                options=["Brief", "Moderate", "Detailed", "Comprehensive"],
                value="Detailed",
                key="critic_detail_level"
            )

        # Critic output example
        with st.expander("Evaluation Example", expanded=False):
            st.markdown("""
            #### Example: Evaluation of Article on Renewable Energy

            **Overall Evaluation: 82/100**

            *This content demonstrates strong technical accuracy and good organization, but could improve in providing actionable insights and maintaining audience-appropriate language.*

            **Criterion-by-Criterion Assessment:**

            **1. Accuracy (26/30)**
            - Factual information about solar and wind energy is correct and well-sourced
            - Recent statistics are accurate and from reputable sources
            - Minor issue: The statement about battery storage costs needs updating with 2023 figures
            - Suggestion: Update battery storage cost data and include recent innovations in storage technology

            **2. Clarity (22/25)**
            - Explanations of technical concepts are generally clear
            - Good use of examples to illustrate complex ideas
            - Room for improvement: Some technical terms are used without explanation
            - Suggestion: Add brief definitions for specialized terms like "grid parity" and "capacity factor"

            **3. Completeness (19/25)**
            - Covers major renewable energy types comprehensively
            - Good discussion of advantages and limitations
            - Missing: Limited discussion of geothermal and tidal energy
            - Suggestion: Add a brief section on emerging renewable technologies or explain scope limitation

            **4. Relevance (15/20)**
            - Content generally addresses the stated purpose well
            - Economic analysis is particularly relevant to the target audience
            - Weakness: Policy section could be more targeted to the audience's needs
            - Suggestion: Include more actionable insights for the specific industry stakeholders

            **Key Strengths:**
            - Excellent use of data visualization to communicate trends
            - Strong comparative analysis of different renewable technologies
            - Well-structured progression of topics

            **Priority Improvements:**
            1. Update battery storage cost information
            2. Define technical terms for broader audience accessibility
            3. Expand coverage of emerging technologies
            4. Add more specific, actionable recommendations
            """)