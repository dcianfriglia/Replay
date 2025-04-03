import streamlit as st
from utils.ui_helpers import subsection_header


def render_feedback_section():
    """Render a feedback collection section for the generated content"""

    with st.container(border=True):
        subsection_header("Feedback")

        st.markdown("""
        Provide feedback on the generated content to improve future generations.
        Your feedback helps optimize prompt settings and configurations.
        """)

        # Initialize values in session state if they don't exist
        if "content_satisfaction" not in st.session_state:
            st.session_state.content_satisfaction = 4

        if "feedback_submitted" not in st.session_state:
            st.session_state.feedback_submitted = False

        # Define callback functions
        def on_satisfaction_change():
            # This gets called when satisfaction slider changes
            pass

        def on_feedback_submit():
            """Callback for feedback submission - with updated checkbox handling"""
            st.session_state.feedback_submitted = True

            # Update session state from the widget values
            st.session_state.feedback_accuracy = st.session_state.feedback_cont_accuracy
            st.session_state.feedback_relevance = st.session_state.feedback_cont_relevance
            st.session_state.feedback_organization = st.session_state.feedback_cont_organization
            st.session_state.feedback_style = st.session_state.feedback_cont_style
            st.session_state.feedback_depth = st.session_state.feedback_cont_depth
            st.session_state.feedback_creativity = st.session_state.feedback_cont_creativity

            # Collect all feedback data
            feedback_data = {
                "satisfaction": st.session_state.content_satisfaction,
                "areas": {
                    "accuracy": st.session_state.feedback_accuracy,
                    "relevance": st.session_state.feedback_relevance,
                    "organization": st.session_state.feedback_organization,
                    "style": st.session_state.feedback_style,
                    "depth": st.session_state.feedback_depth,
                    "creativity": st.session_state.feedback_creativity
                },
                "comments": st.session_state.feedback_comments
            }

            st.session_state.feedback_data = feedback_data

        # Satisfaction rating
        satisfaction = st.slider(
            "Overall Satisfaction",
            min_value=1,
            max_value=5,
            value=st.session_state.content_satisfaction,
            help="Rate your satisfaction with the generated content",
            key="content_satisfaction",
            on_change=on_satisfaction_change
        )

        # Display different prompts based on satisfaction level
        if satisfaction >= 4:
            st.success("Great! What aspects of the content worked well?")
        elif satisfaction >= 2:
            st.info("Thanks for your feedback. How could the content be improved?")
        else:
            st.warning("We're sorry the content didn't meet your expectations. Please tell us what went wrong.")

        # Specific feedback areas
        st.markdown("#### Specific Feedback Areas")

        # Initialize checkbox values in session state if needed
        for key in ["feedback_accuracy", "feedback_relevance", "feedback_organization",
                    "feedback_style", "feedback_depth", "feedback_creativity"]:
            if key not in st.session_state:
                st.session_state[key] = False

        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("Content accuracy", value=st.session_state.feedback_accuracy, key="feedback_cont_accuracy")
            st.checkbox("Relevance to prompt", value=st.session_state.feedback_relevance, key="feedback_cont_relevance")
            st.checkbox("Organization/structure", value=st.session_state.feedback_organization,
                        key="feedback_cont_organization")

        with col2:
            st.checkbox("Writing style/tone", value=st.session_state.feedback_style, key="feedback_cont_style")
            st.checkbox("Depth/comprehensiveness", value=st.session_state.feedback_depth, key="feedback_cont_depth")
            st.checkbox("Creativity/originality", value=st.session_state.feedback_creativity,
                        key="feedback_cont_creativity")

        # Initialize comments in session state if needed
        if "feedback_comments" not in st.session_state:
            st.session_state.feedback_comments = ""

        # Free-form feedback
        st.text_area(
            "Additional Comments",
            value=st.session_state.feedback_comments,
            placeholder="Please provide any additional feedback about the generated content...",
            height=100,
            key="feedback_comments"
        )

        # Submit button
        if st.button("Submit Feedback", on_click=on_feedback_submit):
            # Show success message (this will execute after the callback)
            if st.session_state.feedback_submitted:
                st.success("Thank you for your feedback! It will help improve future generations.")

        # Show saved feedback if available
        if st.session_state.get("feedback_data") and st.session_state.feedback_submitted:
            with st.expander("View Submitted Feedback", expanded=False):
                # Display satisfaction
                st.write(f"**Overall satisfaction:** {st.session_state.feedback_data['satisfaction']}/5")

                # Display areas
                st.write("**Feedback areas:**")
                areas = [area for area, selected in st.session_state.feedback_data["areas"].items() if selected]
                if areas:
                    st.write(", ".join(areas))
                else:
                    st.write("No specific areas selected")

                # Display comments
                if st.session_state.feedback_data["comments"]:
                    st.write("**Comments:**")
                    st.write(st.session_state.feedback_data["comments"])