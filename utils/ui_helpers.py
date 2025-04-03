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
    # Initialize the key in session state if it doesn't exist
    if key not in st.session_state:
        # Check if there's a corresponding main state variable to use for initialization
        # Extract the base variable name (removing "_selector", "_component_toggle", etc.)
        base_key = key.split("_")[0]
        main_key = f"{base_key}_enabled"

        if main_key in st.session_state:
            st.session_state[key] = st.session_state[main_key]
        else:
            st.session_state[key] = default

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{label}**")
        if help_text:
            st.markdown(f"<small>{help_text}</small>", unsafe_allow_html=True)
    with col2:
        value = st.checkbox("", value=st.session_state[key],
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
    # For agents, determine the corresponding main state variable
    agent_type = enabled_key.replace("_selector", "").replace("_component_toggle", "")
    main_key = f"{agent_type}_enabled"

    # Initialize the widget key in session state if it doesn't exist
    if enabled_key not in st.session_state and main_key in st.session_state:
        st.session_state[enabled_key] = st.session_state[main_key]

    with st.container(border=True):
        is_enabled = toggle_switch(title, enabled_key,
                                   default=False,
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
    # Initialize the key in session state if it doesn't exist yet
    if selected_key not in st.session_state:
        # Check if there's a related main state variable we should use for initialization
        if "thinking_steps_enabled" in st.session_state and "cot" in selected_key:
            st.session_state[selected_key] = st.session_state.thinking_steps_enabled
        elif "iterative_refinement_enabled" in st.session_state and "iterative" in selected_key:
            st.session_state[selected_key] = st.session_state.iterative_refinement_enabled
        elif "few_shot_enabled" in st.session_state and "few_shot" in selected_key:
            st.session_state[selected_key] = st.session_state.few_shot_enabled
        elif "rag_enabled" in st.session_state and "rag" in selected_key:
            st.session_state[selected_key] = st.session_state.rag_enabled
        elif "self_consistency_enabled" in st.session_state and "consistency" in selected_key:
            st.session_state[selected_key] = st.session_state.self_consistency_enabled
        elif "routing_enabled" in st.session_state and "routing" in selected_key:
            st.session_state[selected_key] = st.session_state.routing_enabled
        else:
            st.session_state[selected_key] = False

    is_selected = st.checkbox(title,
                              value=st.session_state[selected_key],
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