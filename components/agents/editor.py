import streamlit as st
from utils.ui_helpers import section_header, subsection_header


def render_editor_agent():
    """Render the Editor/Refiner Agent configuration section"""

    st.markdown("### Editor/Refiner Agent")

    st.markdown("""
    The Editor/Refiner Agent improves the style, clarity, and coherence of content.
    This agent takes content from the Creator and enhances readability and presentation.
    """)

    # Initialize the state if it doesn't exist
    if "editor_enabled" not in st.session_state:
        st.session_state.editor_enabled = True

    # Enable/disable toggle with callback
    def on_toggle_change():
        # Callback updates the main session state variable
        st.session_state.editor_enabled = st.session_state.editor_component_toggle

    # Use a unique key for the widget
    editor_enabled = st.toggle(
        "Enable Editor/Refiner Agent",
        value=st.session_state.editor_enabled,
        help="When enabled, this agent will refine and improve content",
        key="editor_component_toggle",  # Unique key different from session state variable
        on_change=on_toggle_change
    )

    if editor_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Editing focus
            subsection_header("Editing Focus")

            editing_focus = st.multiselect(
                "Select focus areas",
                ["Grammar & syntax", "Clarity & readability", "Flow & coherence",
                 "Tone consistency", "Simplification", "Elaboration"],
                default=["Grammar & syntax", "Clarity & readability", "Flow & coherence"],
                key="editor_component_focus_areas"  # Changed to unique key
            )

            # Style guide
            subsection_header("Style Guide")

            style_guide = st.selectbox(
                "Select style guide",
                ["None (General editing)", "Professional/Business", "Academic",
                 "Technical", "Creative", "Journalistic", "Custom..."],
                index=1,
                key="editor_component_style"  # Made key more specific
            )

            if style_guide == "Custom...":
                st.text_area(
                    "Define custom style guide",
                    value="",
                    height=100,
                    key="editor_custom_style"
                )

            # Instructions for Editor
            subsection_header("Instructions for Editor")

            st.text_area(
                "Provide specific instructions for this agent",
                value="Ensure content uses consistent terminology throughout. Prefer active voice and direct statements. Aim for concise paragraphs with clear topic sentences. Maintain logical flow between sections.",
                height=150,
                key="editor_instructions"
            )

        with col2:
            # Model selection
            subsection_header("Model Configuration")

            st.selectbox(
                "Model",
                ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                index=0,
                key="editor_component_model"  # Changed to unique key
            )

            st.slider(
                "Edit Intensity",
                min_value=1,
                max_value=5,
                value=3,
                help="Higher values lead to more substantial edits, lower values for lighter editing"
            )

            # Advanced settings
            subsection_header("Advanced Settings")

            st.checkbox(
                "Track changes",
                value=True,
                key="editor_track_changes",
                help="Highlight changes made to the original content"
            )

            st.checkbox(
                "Explain edits",
                value=True,
                key="editor_explain_edits",
                help="Provide explanations for significant edits"
            )

            st.checkbox(
                "Respect original structure",
                value=True,
                key="editor_respect_structure",
                help="Maintain the original content's structure while improving it"
            )

            st.checkbox(
                "Fix factual errors",
                value=False,
                key="editor_fix_facts",
                help="Allow editor to correct factual errors (requires Fact Checker capabilities)"
            )

        # Editor before/after examples
        with st.expander("Before/After Examples", expanded=False):
            st.markdown("""
            #### Example 1: Improving Clarity

            **Before:**
            ```
            The implementation of the system requires several steps which need to be followed in order to ensure proper functionality of all components as specified by the documentation that was provided by the vendor and must be adhered to strictly.
            ```

            **After:**
            ```
            Implementing the system requires following several steps in sequence. Adhere strictly to the vendor's documentation to ensure all components function properly.
            ```

            #### Example 2: Enhancing Flow

            **Before:**
            ```
            Machine learning models process data. The data must be clean. Pre-processing is important. Feature selection matters too. Then you train the model.
            ```

            **After:**
            ```
            Machine learning models process data that must be clean and properly pre-processed. After selecting relevant features, you can then train the model effectively.
            ```

            #### Example 3: Improving Tone Consistency

            **Before:**
            ```
            Our research indicates significant market potential. The numbers are really good. We anticipate substantial ROI within the first fiscal quarter.
            ```

            **After:**
            ```
            Our research indicates significant market potential. The financial projections are promising. We anticipate substantial ROI within the first fiscal quarter.
            ```
            """)