import streamlit as st
from utils.ui_helpers import subsection_header


def render_prompt_structure():
    """Render the Prompt Structure section with role-based awareness"""
    with st.container(border=True):
        subsection_header("Prompt Structure")

        st.markdown("""
        Rearrange or toggle prompt sections to customize your final prompt.
        Select which sections go into the System prompt vs. User prompt.
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

        # Initialize system vs user roles for sections if not present
        if "section_roles" not in st.session_state:
            st.session_state.section_roles = {
                "Context & Background": "System",
                "Task Definition": "User",
                "Input Data Format": "User",
                "Output Requirements": "User",
                "Examples (Few-Shot Learning)": "User",
                "Chain-of-Thought Instructions": "User",
                "Self-Review Requirements": "System",
                "Fact Checking Instructions": "User"
            }

        # Get the current order of sections
        if "prompt_section_order" not in st.session_state:
            st.session_state.prompt_section_order = list(st.session_state.prompt_structure.keys())

        # Grouping option - show system and user sections separately or chronologically
        display_mode = st.radio(
            "Display Mode",
            ["Chronological Order", "Grouped by Role"],
            horizontal=True,
            key="structure_display_mode"
        )

        if display_mode == "Grouped by Role":
            # Display sections grouped by system and user roles
            st.markdown("### System Prompt Sections")

            system_sections = [s for s in st.session_state.prompt_section_order
                               if st.session_state.section_roles.get(s, "System") == "System"]

            for i, section in enumerate(system_sections):
                with st.container(border=True):
                    cols = st.columns([5, 1, 1, 1])

                    with cols[0]:
                        # Toggle section inclusion
                        is_included = st.checkbox(
                            section,
                            value=st.session_state.prompt_structure.get(section, True),
                            key=f"section_toggle_system_{i}"
                        )
                        st.session_state.prompt_structure[section] = is_included

                    with cols[1]:
                        # Move section up within its group
                        if i > 0:
                            if st.button("↑", key=f"move_up_system_{i}"):
                                # Get the original indices in the full order
                                curr_idx = st.session_state.prompt_section_order.index(section)
                                prev_idx = st.session_state.prompt_section_order.index(system_sections[i - 1])

                                # Swap in the full order list
                                temp = st.session_state.prompt_section_order[curr_idx]
                                st.session_state.prompt_section_order[curr_idx] = st.session_state.prompt_section_order[
                                    prev_idx]
                                st.session_state.prompt_section_order[prev_idx] = temp
                                st.rerun()

                    with cols[2]:
                        # Move section down within its group
                        if i < len(system_sections) - 1:
                            if st.button("↓", key=f"move_down_system_{i}"):
                                # Get the original indices in the full order
                                curr_idx = st.session_state.prompt_section_order.index(section)
                                next_idx = st.session_state.prompt_section_order.index(system_sections[i + 1])

                                # Swap in the full order list
                                temp = st.session_state.prompt_section_order[curr_idx]
                                st.session_state.prompt_section_order[curr_idx] = st.session_state.prompt_section_order[
                                    next_idx]
                                st.session_state.prompt_section_order[next_idx] = temp
                                st.rerun()

                    with cols[3]:
                        # Change role to User
                        if st.button("→ User", key=f"to_user_{i}"):
                            st.session_state.section_roles[section] = "User"
                            st.rerun()

            st.markdown("### User Prompt Sections")

            user_sections = [s for s in st.session_state.prompt_section_order
                             if st.session_state.section_roles.get(s, "User") == "User"]

            for i, section in enumerate(user_sections):
                with st.container(border=True):
                    cols = st.columns([5, 1, 1, 1])

                    with cols[0]:
                        # Toggle section inclusion
                        is_included = st.checkbox(
                            section,
                            value=st.session_state.prompt_structure.get(section, True),
                            key=f"section_toggle_user_{i}"
                        )
                        st.session_state.prompt_structure[section] = is_included

                    with cols[1]:
                        # Move section up within its group
                        if i > 0:
                            if st.button("↑", key=f"move_up_user_{i}"):
                                # Get the original indices in the full order
                                curr_idx = st.session_state.prompt_section_order.index(section)
                                prev_idx = st.session_state.prompt_section_order.index(user_sections[i - 1])

                                # Swap in the full order list
                                temp = st.session_state.prompt_section_order[curr_idx]
                                st.session_state.prompt_section_order[curr_idx] = st.session_state.prompt_section_order[
                                    prev_idx]
                                st.session_state.prompt_section_order[prev_idx] = temp
                                st.rerun()

                    with cols[2]:
                        # Move section down within its group
                        if i < len(user_sections) - 1:
                            if st.button("↓", key=f"move_down_user_{i}"):
                                # Get the original indices in the full order
                                curr_idx = st.session_state.prompt_section_order.index(section)
                                next_idx = st.session_state.prompt_section_order.index(user_sections[i + 1])

                                # Swap in the full order list
                                temp = st.session_state.prompt_section_order[curr_idx]
                                st.session_state.prompt_section_order[curr_idx] = st.session_state.prompt_section_order[
                                    next_idx]
                                st.session_state.prompt_section_order[next_idx] = temp
                                st.rerun()

                    with cols[3]:
                        # Change role to System
                        if st.button("→ Sys", key=f"to_system_{i}"):
                            st.session_state.section_roles[section] = "System"
                            st.rerun()

        else:
            # Display sections in chronological order
            for i, section in enumerate(st.session_state.prompt_section_order):
                with st.container(border=True):
                    cols = st.columns([4, 2, 1, 1, 1])

                    with cols[0]:
                        # Toggle section inclusion
                        is_included = st.checkbox(
                            section,
                            value=st.session_state.prompt_structure.get(section, True),
                            key=f"section_toggle_{i}"
                        )
                        st.session_state.prompt_structure[section] = is_included

                    with cols[1]:
                        # Role selector (System or User)
                        current_role = st.session_state.section_roles.get(section, "System")
                        new_role = st.selectbox(
                            "Role",
                            ["System", "User"],
                            index=0 if current_role == "System" else 1,
                            key=f"role_select_{i}",
                            label_visibility="collapsed"
                        )
                        st.session_state.section_roles[section] = new_role

                    with cols[2]:
                        # Move section up
                        if i > 0:
                            if st.button("↑", key=f"move_up_{i}"):
                                # Swap with previous section
                                temp = st.session_state.prompt_section_order[i]
                                st.session_state.prompt_section_order[i] = st.session_state.prompt_section_order[i - 1]
                                st.session_state.prompt_section_order[i - 1] = temp
                                st.rerun()

                    with cols[3]:
                        # Move section down
                        if i < len(st.session_state.prompt_section_order) - 1:
                            if st.button("↓", key=f"move_down_{i}"):
                                # Swap with next section
                                temp = st.session_state.prompt_section_order[i]
                                st.session_state.prompt_section_order[i] = st.session_state.prompt_section_order[i + 1]
                                st.session_state.prompt_section_order[i + 1] = temp
                                st.rerun()

                    with cols[4]:
                        # Delete section
                        if len(st.session_state.prompt_section_order) > 1:
                            if st.button("×", key=f"delete_{i}"):
                                # Remove this section
                                section_name = st.session_state.prompt_section_order.pop(i)
                                # Also remove from prompt structure and roles if present
                                if section_name in st.session_state.prompt_structure:
                                    del st.session_state.prompt_structure[section_name]
                                if section_name in st.session_state.section_roles:
                                    del st.session_state.section_roles[section_name]
                                st.rerun()

        # Allow adding custom sections
        with st.expander("Add Custom Section", expanded=False):
            custom_section = st.text_input("Custom Section Name", key="custom_section_name")
            custom_role = st.selectbox("Section Role", ["System", "User"], key="custom_section_role")

            if st.button("Add Section") and custom_section:
                if custom_section not in st.session_state.prompt_structure:
                    st.session_state.prompt_structure[custom_section] = True
                    st.session_state.prompt_section_order.append(custom_section)
                    st.session_state.section_roles[custom_section] = custom_role
                    st.rerun()