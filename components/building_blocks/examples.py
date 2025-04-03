import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_examples_section():
    """Render the Examples & Constraints section"""
    with st.container(border=True):
        section_with_info(
            "Examples & Constraints",
            "Provide examples and limitations"
        )

        # Few-shot examples
        subsection_header("Examples (Few-shot learning)")

        for i, example in enumerate(st.session_state.examples):
            with st.expander(f"Example {i + 1}", expanded=i == 0):
                ex_input = st.text_area("Input", value=example["input"], key=f"example_input_{i}")
                ex_output = st.text_area("Output", value=example["output"], key=f"example_output_{i}")

                # Update session state when values change
                st.session_state.examples[i]["input"] = ex_input
                st.session_state.examples[i]["output"] = ex_output

        col_add, col_remove = st.columns([1, 1])
        with col_add:
            if st.button("Add Example"):
                st.session_state.examples.append({"input": "", "output": ""})
                st.rerun()

        with col_remove:
            if len(st.session_state.examples) > 1:
                if st.button("Remove Last Example"):
                    st.session_state.examples.pop()
                    st.rerun()

        # Constraints
        subsection_header("Constraints")
        st.text_area(
            "Define any limitations or boundaries for content generation",
            value=st.session_state.constraints,
            height=100,
            key="constraints_area",
            on_change=lambda: setattr(st.session_state, "constraints", st.session_state.constraints_area)
        )