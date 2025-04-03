import streamlit as st
from utils.ui_helpers import section_header, subsection_header


def render_fact_checker_agent():
    """Render the Fact Checker Agent configuration section"""

    st.markdown("### Fact Checker Agent")

    st.markdown("""
    The Fact Checker Agent verifies the factual accuracy of generated content.
    This agent identifies potential errors, makes corrections, and ensures information reliability.
    """)

    # Initialize the state if it doesn't exist
    if "fact_checker_enabled" not in st.session_state:
        st.session_state.fact_checker_enabled = False

    # Enable/disable toggle with callback
    def on_toggle_change():
        # Callback updates the main session state variable
        st.session_state.fact_checker_enabled = st.session_state.fact_checker_component_toggle

    # Use a unique key for the widget
    fact_checker_enabled = st.toggle(
        "Enable Fact Checker Agent",
        value=st.session_state.fact_checker_enabled,
        help="When enabled, this agent will verify factual accuracy of content",
        key="fact_checker_component_toggle",  # Unique key different from session state variable
        on_change=on_toggle_change
    )

    if fact_checker_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Verification approach
            subsection_header("Verification Approach")

            verification = st.selectbox(
                "Select verification approach",
                ["Basic fact checking", "Comprehensive verification", "Domain-specific expertise", "Custom approach"],
                index=1,
                key="verification_approach"
            )

            if verification == "Domain-specific expertise":
                st.selectbox(
                    "Domain",
                    ["General knowledge", "Science & Technology", "Business & Finance",
                     "Health & Medicine", "History & Politics", "Arts & Culture"],
                    index=0,
                    key="verification_domain"
                )

            if verification == "Custom approach":
                st.text_area(
                    "Define custom verification approach",
                    value="",
                    height=100,
                    key="custom_verification_approach"
                )

            # Verification sources
            subsection_header("Verification Sources")

            sources = st.multiselect(
                "Select verification sources",
                ["Internal knowledge", "Industry standards", "Academic sources",
                 "Current events database", "Custom references", "RAG knowledge base"],
                default=["Internal knowledge", "Industry standards"],
                key="verification_sources"
            )

            if "Custom references" in sources:
                st.text_area(
                    "Specify custom references",
                    value="",
                    height=100,
                    key="custom_references"
                )

            # Instructions for Fact Checker
            subsection_header("Instructions for Fact Checker")

            st.text_area(
                "Provide specific instructions for this agent",
                value="Verify all factual claims against reliable sources. Flag any statements that cannot be confidently verified. Check numerical data for accuracy. Ensure dates, names, and specific assertions are correct. Provide suggestions for corrections when inaccuracies are found.",
                height=150,
                key="fact_checker_instructions"
            )

        with col2:
            # Model selection
            subsection_header("Model Configuration")

            st.selectbox(
                "Model",
                ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                index=0,
                key="fact_checker_component_model"  # Changed to unique key
            )

            st.slider(
                "Verification Thoroughness",
                min_value=1,
                max_value=5,
                value=4,
                help="Higher values increase verification thoroughness but may increase processing time"
            )

            # Advanced settings
            subsection_header("Advanced Settings")

            st.checkbox(
                "Cite sources",
                value=True,
                key="fact_checker_cite_sources",
                help="Include citations for verified information"
            )

            st.checkbox(
                "Flag uncertainty",
                value=True,
                key="fact_checker_flag_uncertainty",
                help="Explicitly mark claims that cannot be verified with high confidence"
            )

            st.checkbox(
                "Auto-correct errors",
                value=False,
                key="fact_checker_auto_correct",
                help="Automatically correct factual errors (when confidence is high)"
            )

            st.checkbox(
                "Check for omissions",
                value=True,
                key="fact_checker_check_omissions",
                help="Identify important information that may be missing"
            )

            # Confidence threshold
            st.slider(
                "Confidence Threshold",
                min_value=0.5,
                max_value=0.95,
                value=0.75,
                step=0.05,
                key="fact_checker_confidence",
                help="Minimum confidence level required to consider a fact verified"
            )

        # Fact checking example
        with st.expander("Fact Checking Example", expanded=False):
            st.markdown("""
            #### Example: Fact Checking a Historical Passage

            **Original Text:**
            ```
            Thomas Edison invented the light bulb in 1880. His invention revolutionized modern society and was his first major innovation. Edison worked entirely alone on this project in his New Jersey laboratory, refusing any assistance.
            ```

            **Fact Checker Analysis:**
            ```
            FACT CHECK RESULTS:

            1. ❌ "Thomas Edison invented the light bulb in 1880."
               - CORRECTION: Edison patented an improved design in 1879 (not 1880), but he did not invent the first light bulb. Earlier inventors including Joseph Swan had working designs.
               - CONFIDENCE: High (Multiple reliable historical sources confirm this)

            2. ✅ "His invention revolutionized modern society."
               - VERIFIED: This statement is generally accepted.
               - CONFIDENCE: High

            3. ❌ "...was his first major innovation."
               - CORRECTION: Edison had several major innovations before the light bulb, including the phonograph (1877) and numerous telegraph improvements.
               - CONFIDENCE: High (Well-documented timeline of Edison's inventions)

            4. ❌ "Edison worked entirely alone on this project..."
               - CORRECTION: Edison had a team of assistants and researchers who contributed significantly to the light bulb's development.
               - CONFIDENCE: High (Well-documented in historical records)

            SUGGESTED REVISION:
            "Thomas Edison patented an improved light bulb design in 1879. While earlier inventors had created working light bulbs, Edison's practical and commercially viable version revolutionized modern society. This came after several other major innovations, including the phonograph. Edison worked with a team of skilled assistants at his Menlo Park laboratory in New Jersey."
            ```
            """)