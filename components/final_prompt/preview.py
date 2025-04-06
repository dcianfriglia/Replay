import streamlit as st
from utils.ui_helpers import subsection_header
from models.prompt_generator import generate_prompt, generate_system_prompt, generate_user_prompt


def render_prompt_preview():
    """Render the Prompt Preview section with support for both combined and role-based formats"""
    with st.container(border=True):
        subsection_header("Generated Prompt")

        # Add toggle for preview format
        preview_format = st.radio(
            "Preview Format",
            ["Combined Prompt", "Role-Based (System/User)"],
            horizontal=True,
            key="structure_preview_format"
        )

        # Generate prompts based on current session state
        if preview_format == "Combined Prompt":
            # Get the prompt based on current session state using original format
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
                if st.button("Apply Changes", key="apply_changes_btn"):
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
                    sections_count = sum(
                        1 for section, included in st.session_state.prompt_structure.items() if included)
                    st.metric("Active Sections", f"{sections_count}")

                with col3:
                    workflows_count = len(st.session_state.get("selected_workflows", []))
                    st.metric("Active Workflows", f"{workflows_count}")
        else:
            # Get system and user prompts for role-based format
            system_prompt = generate_system_prompt()
            user_prompt = generate_user_prompt()

            # Create tabs for system and user prompts
            prompt_role_tabs = st.tabs(["System Prompt", "User Prompt"])

            with prompt_role_tabs[0]:
                # System prompt edit mode
                system_edit_mode = st.checkbox("Edit System Prompt",
                                               value=st.session_state.get("edit_system_raw", False),
                                               key="edit_system_raw_toggle")
                st.session_state.edit_system_raw = system_edit_mode

                if system_edit_mode:
                    edited_system_prompt = st.text_area(
                        "Edit System Prompt",
                        value=system_prompt,
                        height=300,
                        key="edited_system_prompt"
                    )

                    if st.button("Apply System Changes", key="apply_system_changes_btn"):
                        st.session_state.custom_system_prompt = edited_system_prompt
                        st.success("Changes applied to system prompt.")
                else:
                    with st.container(border=True, height=300):
                        st.code(system_prompt, language="markdown")

                    # System prompt statistics
                    system_tokens = len(system_prompt.split())
                    st.metric("System Prompt Tokens", f"{system_tokens}")

            with prompt_role_tabs[1]:
                # User prompt edit mode
                user_edit_mode = st.checkbox("Edit User Prompt", value=st.session_state.get("edit_user_raw", False),
                                             key="edit_user_raw_toggle")
                st.session_state.edit_user_raw = user_edit_mode

                if user_edit_mode:
                    edited_user_prompt = st.text_area(
                        "Edit User Prompt",
                        value=user_prompt,
                        height=300,
                        key="edited_user_prompt"
                    )

                    if st.button("Apply User Changes", key="apply_user_changes_btn"):
                        st.session_state.custom_user_prompt = edited_user_prompt
                        st.success("Changes applied to user prompt.")
                else:
                    with st.container(border=True, height=300):
                        st.code(user_prompt, language="markdown")

                    # User prompt statistics
                    user_tokens = len(user_prompt.split())
                    st.metric("User Prompt Tokens", f"{user_tokens}")

            # Total token count for both prompts
            total_tokens = len(system_prompt.split()) + len(user_prompt.split())
            st.metric("Total Tokens", f"{total_tokens}")

            # Store prompts in session state for execution
            st.session_state.final_system_prompt = system_prompt
            st.session_state.final_user_prompt = user_prompt

        # Add export option
        with st.expander("Export Options", expanded=False):
            export_format = st.selectbox(
                "Export Format",
                ["Plain Text", "Markdown", "JSON"],
                index=1,
                key="export_format_select"
            )

            if preview_format == "Combined Prompt":
                # Single download button for combined prompt
                st.download_button(
                    "Download Prompt",
                    data=prompt_text,
                    file_name=f"prompt_template.{'md' if export_format == 'Markdown' else 'txt' if export_format == 'Plain Text' else 'json'}",
                    mime="text/plain",
                    key="download_combined_btn"
                )
            else:
                # Separate download buttons for system and user prompts
                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        "Download System Prompt",
                        data=system_prompt,
                        file_name=f"system_prompt.{'md' if export_format == 'Markdown' else 'txt' if export_format == 'Plain Text' else 'json'}",
                        mime="text/plain",
                        key="download_system_btn"
                    )

                with col2:
                    st.download_button(
                        "Download User Prompt",
                        data=user_prompt,
                        file_name=f"user_prompt.{'md' if export_format == 'Markdown' else 'txt' if export_format == 'Plain Text' else 'json'}",
                        mime="text/plain",
                        key="download_user_btn"
                    )

                # Option to download both in a single JSON file
                import json

                if export_format == "JSON":
                    combined_data = json.dumps({
                        "system": system_prompt,
                        "user": user_prompt
                    }, indent=2)

                    st.download_button(
                        "Download Combined JSON",
                        data=combined_data,
                        file_name="prompt_template.json",
                        mime="application/json",
                        key="download_combined_json_btn"
                    )