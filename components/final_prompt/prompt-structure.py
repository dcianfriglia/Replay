import streamlit as st
from utils.ui_helpers import subsection_header


def render_prompt_structure():
    """Render the Prompt Structure section"""
    with st.container(border=True):
        subsection_header("Prompt Structure")
        
        st.markdown("""
        Rearrange or toggle prompt sections to customize your final prompt.
        Drag sections to change their order or click to include/exclude them.
        """)
        
        # Initialize prompt structure if not in session state
        if "prompt_structure" not in st.session_state:
            st.session_state.prompt_structure = {
                "Context & Background": True,
                "Task Definition": True,
                "Input Data Format": True,
                "Output Requirements": True,
                "Examples (Few-Shot Learning)": True,
                "Chain-of-Thought Instructions": True,
                "Self-Review Requirements": True,
                "Fact Checking Instructions": False
            }
        
        # In Streamlit, we can't do drag-and-drop natively, so we'll use a simpler approach
        # We'll let users reorder using up/down buttons and toggle with checkboxes
        
        # Get the current order of sections
        if "prompt_section_order" not in st.session_state:
            st.session_state.prompt_section_order = list(st.session_state.prompt_structure.keys())
        
        # Display each section with toggle and reorder buttons
        for i, section in enumerate(st.session_state.prompt_section_order):
            with st.container(border=True):
                cols = st.columns([5, 1, 1, 1])
                
                with cols[0]:
                    # Toggle section inclusion
                    is_included = st.checkbox(
                        section,
                        value=st.session_state.prompt_structure.get(section, True),
                        key=f"section_toggle_{i}"
                    )
                    st.session_state.prompt_structure[section] = is_included
                
                with cols[1]:
                    # Move section up
                    if i > 0:
                        if st.button("↑", key=f"move_up_{i}"):
                            # Swap with previous section
                            temp = st.session_state.prompt_section_order[i]
                            st.session_state.prompt_section_order[i] = st.session_state.prompt_section_order[i-1]
                            st.session_state.prompt_section_order[i-1] = temp
                            st.rerun()
                
                with cols[2]:
                    # Move section down
                    if i < len(st.session_state.prompt_section_order) - 1:
                        if st.button("↓", key=f"move_down_{i}"):
                            # Swap with next section
                            temp = st.session_state.prompt_section_order[i]
                            st.session_state.prompt_section_order[i] = st.session_state.prompt_section_order[i+1]
                            st.session_state.prompt_section_order[i+1] = temp
                            st.rerun()
                
                with cols[3]:
                    # Visual indicator of inclusion status
                    if is_included:
                        st.markdown("<span style='color:green;'>✓</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color:red;'>✗</span>", unsafe_allow_html=True)
        
        # Allow adding custom sections
        with st.expander("Add Custom Section", expanded=False):
            custom_section = st.text_input("Custom Section Name", key="custom_section_name")
            if st.button("Add Section") and custom_section:
                if custom_section not in st.session_state.prompt_structure:
                    st.session_state.prompt_structure[custom_section] = True
                    st.session_state.prompt_section_order.append(custom_section)
                    st.rerun()