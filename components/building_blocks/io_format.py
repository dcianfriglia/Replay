import streamlit as st
from utils.ui_helpers import section_with_info


def render_input_format_section():
    """Render the Input Data Format section"""
    with st.container(border=True):
        section_with_info(
            "Input Data Format",
            "Describe how input data is structured"
        )

        input_format = st.selectbox(
            "Format",
            ["Plain Text", "JSON", "CSV", "XML", "Custom Format"],
            index=["Plain Text", "JSON", "CSV", "XML", "Custom Format"].index(st.session_state.input_format),
            key="input_format_select",
            on_change=lambda: setattr(st.session_state, "input_format", st.session_state.input_format_select)
        )

        st.text_area(
            "Describe the structure of input data or provide a sample",
            value=st.session_state.input_description,
            height=100,
            key="input_description_area",
            on_change=lambda: setattr(st.session_state, "input_description", st.session_state.input_description_area)
        )


def render_output_section():
    """Render the Output Requirements section"""
    with st.container(border=True):
        section_with_info(
            "Output Requirements",
            "Specify format, length, tone, and style for the output"
        )

        col_a, col_b = st.columns(2)
        with col_a:
            output_format = st.selectbox(
                "Format",
                ["Plain Text", "JSON", "Markdown", "HTML", "Custom Format"],
                index=["Plain Text", "JSON", "Markdown", "HTML", "Custom Format"].index(st.session_state.output_format),
                key="output_format_select",
                on_change=lambda: setattr(st.session_state, "output_format", st.session_state.output_format_select)
            )

        with col_b:
            output_tone = st.selectbox(
                "Tone",
                ["Professional", "Conversational", "Technical", "Educational", "Creative"],
                index=["Professional", "Conversational", "Technical", "Educational", "Creative"].index(
                    st.session_state.output_tone),
                key="output_tone_select",
                on_change=lambda: setattr(st.session_state, "output_tone", st.session_state.output_tone_select)
            )

        st.text_area(
            "Describe any other output requirements like length, structure, etc",
            value=st.session_state.output_requirements,
            height=100,
            key="output_requirements_area",
            on_change=lambda: setattr(st.session_state, "output_requirements",
                                      st.session_state.output_requirements_area)
        )