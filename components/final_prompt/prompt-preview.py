import streamlit as st
from utils.ui_helpers import subsection_header
from models.prompt_generator import generate_prompt


def render_prompt_preview():
    """Render the Prompt Preview section"""
    with st.container(border=True):
        subsection_header("Generated Prompt")
        
        # Get the prompt based on current session state
        prompt_text = generate_prompt()
        
        # Option to view or edit raw prompt
        edit_mode = st.checkbox("Edit Raw Prompt", value=st.session_state.get("edit_raw", False),
                               key="edit_raw_toggle")
        st.session_state.edit_raw = edit_mode
        
        if edit_mode:
            # Editable prompt with full height
            edited_prompt = st.text_area(
                "Edit Prompt",
                value=prompt_text,
                height=400,
                key="edited_prompt"
            )
            
            # Allow saving changes
            if st.button("Apply Changes"):
                # In a real implementation, we would need to parse this back to components
                # or keep the edited version separate
                st.session_state.custom_prompt = edited_prompt
                st.success("Changes applied to prompt.")
        else:
            # Read-only prompt preview
            with st.container(border=True, height=400):
                st.code(prompt_text, language="markdown")
            
            # Add token count and other statistics
            prompt_tokens = len(prompt_text.split())
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Est. Tokens", f"{prompt_tokens}")
            
            with col2:
                sections_count = sum(1 for section, included in st.session_state.prompt_structure.items() if included)
                st.metric("Active Sections", f"{sections_count}")
            
            with col3:
                workflows_count = len(st.session_state.get("selected_workflows", []))
                st.metric("Active Workflows", f"{workflows_count}")
            
        # Add export option
        with st.expander("Export Options", expanded=False):
            export_format = st.selectbox(
                "Export Format",
                ["Plain Text", "Markdown", "JSON"],
                index=1
            )
            
            st.download_button(
                "Download Prompt",
                data=prompt_text,
                file_name=f"prompt_template.{'md' if export_format == 'Markdown' else 'txt' if export_format == 'Plain Text' else 'json'}",
                mime="text/plain"
            )