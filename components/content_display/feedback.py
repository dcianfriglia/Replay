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
        
        # Satisfaction rating
        satisfaction = st.slider(
            "Overall Satisfaction",
            min_value=1,
            max_value=5,
            value=4,
            help="Rate your satisfaction with the generated content"
        )
        
        # Store the rating in session state
        st.session_state.content_satisfaction = satisfaction
        
        # Display different prompts based on satisfaction level
        if satisfaction >= 4:
            st.success("Great! What aspects of the content worked well?")
        elif satisfaction >= 2:
            st.info("Thanks for your feedback. How could the content be improved?")
        else:
            st.warning("We're sorry the content didn't meet your expectations. Please tell us what went wrong.")
        
        # Specific feedback areas
        st.markdown("#### Specific Feedback Areas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Content accuracy", value=True, key="feedback_accuracy")
            st.checkbox("Relevance to prompt", value=True, key="feedback_relevance")
            st.checkbox("Organization/structure", value=True, key="feedback_organization")
        
        with col2:
            st.checkbox("Writing style/tone", value=False, key="feedback_style")
            st.checkbox("Depth/comprehensiveness", value=True, key="feedback_depth")
            st.checkbox("Creativity/originality", value=False, key="feedback_creativity")
        
        # Free-form feedback
        st.text_area(
            "Additional Comments",
            placeholder="Please provide any additional feedback about the generated content...",
            height=100,
            key="feedback_comments"
        )
        
        # Submit button
        if st.button("Submit Feedback"):
            # In a real implementation, this would store feedback data
            # and potentially use it to improve future generations
            
            # Store feedback in session state
            st.session_state.feedback_submitted = True
            
            # Collect all feedback data
            feedback_data = {
                "satisfaction": satisfaction,
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
            
            # Show success message