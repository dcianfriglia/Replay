import streamlit as st


def section_header(title):
    """
    Render a section header with consistent styling

    Args:
        title (str): The title of the section
    """
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def subsection_header(title):
    """
    Render a subsection header with consistent styling

    Args:
        title (str): The title of the subsection
    """
    st.markdown(f"#### {title}")


def info_tooltip(text):
    """
    Create an information tooltip with the given text

    Args:
        text (str): The tooltip text

    Returns:
        str: HTML for the tooltip
    """
    return f"""
    <span class="tooltip">
        ℹ️
        <span class="tooltiptext">{text}</span>
    </span>
    """


def section_with_info(title, info_text):
    """
    Render a section header with an information tooltip

    Args:
        title (str): The title of the section
        info_text (str): The tooltip text
    """
    st.markdown(
        f'<div class="section-header">{title} {info_tooltip(info_text)}</div>',
        unsafe_allow_html=True
    )


def card_container(content_func):
    """
    Wrapper to render content inside a card container

    Args:
        content_func: Function to call inside the container
    """
    with st.container(border=True):
        content_func()


def toggle_switch(label, key, default=False, help_text=None):
    """
    Create a toggle switch with label to the left

    Args:
        label (str): Label for the toggle
        key (str): Session state key
        default (bool): Default value
        help_text (str): Optional help text

    Returns:
        bool: The current value of the toggle
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{label}**")
        if help_text:
            st.markdown(f"<small>{help_text}</small>", unsafe_allow_html=True)
    with col2:
        value = st.checkbox("", value=default if key not in st.session_state else st.session_state[key],
                            key=key, help=help_text)

    return value


def agent_card(title, description, enabled_key):
    """
    Render a card for an agent with a toggle switch

    Args:
        title (str): Agent title
        description (str): Agent description
        enabled_key (str): Session state key for enabled state

    Returns:
        bool: Whether the agent is enabled
    """
    with st.container(border=True):
        is_enabled = toggle_switch(title, enabled_key,
                                   default=False if enabled_key not in st.session_state else st.session_state[
                                       enabled_key],
                                   help_text=description)

        return is_enabled


def workflow_option(title, description, selected_key):
    """
    Render a workflow option with a toggle and description

    Args:
        title (str): Workflow title
        description (str): Workflow description
        selected_key (str): Session state key for selected state

    Returns:
        bool: Whether the workflow is selected
    """
    is_selected = st.checkbox(title,
                              value=False if selected_key not in st.session_state else st.session_state[selected_key],
                              key=selected_key)

    if is_selected:
        with st.expander(f"About {title}", expanded=False):
            st.markdown(description)

    return is_selected


def step_input(index, value, on_delete=None):
    """
    Render an input for a step with delete button

    Args:
        index (int): Step index
        value (str): Current step value
        on_delete (function): Function to call on delete

    Returns:
        str: Updated step value
    """
    col1, col2 = st.columns([10, 1])

    with col1:
        new_value = st.text_input(f"Step {index + 1}", value=value, key=f"step_{index}")

    with col2:
        if index > 0 and on_delete and st.button("×", key=f"delete_step_{index}"):
            on_delete(index)
            # No need to return here as rerun will happen

    return new_value