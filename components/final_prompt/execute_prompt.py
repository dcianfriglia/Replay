import streamlit as st
import time
from utils.ui_helpers import subsection_header
from models.content_generator import ContentGenerator, generate_content


def render_execution_controls():
    """Render controls for executing the prompt with different models and parameters"""

    subsection_header("Execute Prompt")

    st.markdown("""
    Test your prompt with different models and parameters. Results will be displayed in the Content section
    and saved for comparison.
    """)

    # Model selection and parameters
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # Provider selection
        provider_options = ["OpenAI", "Anthropic", "Custom"]
        selected_provider = st.selectbox(
            "Provider",
            provider_options,
            index=0,
            key="execution_provider"
        )

        # Model selection based on provider
        if selected_provider == "OpenAI":
            model_options = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        elif selected_provider == "Anthropic":
            model_options = ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
        else:
            model_options = ["Custom Model 1", "Custom Model 2"]

        selected_model = st.selectbox(
            "Model",
            model_options,
            key="execution_model"
        )

    with col2:
        # Basic parameters
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            key="execution_temperature",
            help="Higher values make output more creative/random"
        )

        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=1000,
            step=100,
            key="execution_max_tokens",
            help="Maximum length of generated response"
        )

    with col3:
        # API key input
        use_api = st.checkbox("Use API", value=False, key="execution_use_api")

        if use_api:
            api_key = st.text_input(
                "API Key",
                type="password",
                key="execution_api_key"
            )

        # Advanced parameters toggle
        show_advanced = st.checkbox("Advanced Parameters", value=False, key="show_advanced_params")

    # Advanced parameters section
    if show_advanced:
        advanced_cols = st.columns(3)

        with advanced_cols[0]:
            top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=1.0,
                step=0.05,
                key="execution_top_p",
                help="Controls diversity via nucleus sampling"
            )

        with advanced_cols[1]:
            frequency_penalty = st.slider(
                "Frequency Penalty",
                min_value=0.0,
                max_value=2.0,
                value=0.0,
                step=0.1,
                key="execution_frequency_penalty",
                help="Reduces repetition of token sequences"
            )

        with advanced_cols[2]:
            presence_penalty = st.slider(
                "Presence Penalty",
                min_value=0.0,
                max_value=2.0,
                value=0.0,
                step=0.1,
                key="execution_presence_penalty",
                help="Reduces repetition of topics"
            )

    # Execution button row
    button_cols = st.columns([2, 1, 1])

    with button_cols[0]:
        execute_button = st.button(
            "Execute Prompt",
            type="primary",
            use_container_width=True,
            key="execute_prompt_btn"
        )

    with button_cols[1]:
        save_version_button = st.button(
            "Save Version",
            use_container_width=True,
            key="save_prompt_version_btn"
        )

    with button_cols[2]:
        compare_button = st.button(
            "Compare Versions",
            use_container_width=True,
            key="compare_versions_btn"
        )

    # Initialize execution history if needed
    if "execution_history" not in st.session_state:
        st.session_state.execution_history = []

    # Handle execution
    if execute_button:
        # Get current prompts
        system_prompt = st.session_state.get("final_system_prompt", "")
        user_prompt = st.session_state.get("final_user_prompt", "")

        # If these are empty, try raw prompts
        if not system_prompt:
            system_prompt = st.session_state.get("raw_system_prompt", "")
        if not user_prompt:
            user_prompt = st.session_state.get("raw_user_prompt", "")

        # Show execution in progress
        with st.spinner("Generating content..."):
            # Create execution parameters dict
            params = {
                "provider": selected_provider,
                "model": selected_model,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # Add advanced params if shown
            if show_advanced:
                params.update({
                    "top_p": top_p,
                    "frequency_penalty": frequency_penalty,
                    "presence_penalty": presence_penalty
                })

            # Create unique execution ID
            import uuid
            execution_id = str(uuid.uuid4())[:8]

            # Prepare API Call
            if use_api and api_key:
                # Use real API
                generator = ContentGenerator(api_key=api_key)

                try:
                    start_time = time.time()
                    result = generator.generate(
                        prompt=user_prompt,
                        system_prompt=system_prompt,
                        model=selected_model,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    generation_time = time.time() - start_time

                    content = result["content"]
                    metadata = result.get("metadata", {})
                    metadata["generation_time"] = generation_time

                except Exception as e:
                    content = f"Error: {str(e)}"
                    metadata = {"error": True}
            else:
                # Use simulation
                start_time = time.time()
                # Pause for realistic effect
                time.sleep(1.5)
                content = f"""**Generated content using {selected_model}**

Based on your prompt, here is a comprehensive guide on implementing Agile methodology in software development teams:

## Implementing Agile in Software Development

Agile methodologies provide flexibility and efficiency for development teams by emphasizing:
- Iterative development cycles
- Continuous feedback
- Team collaboration
- Customer involvement

### Key Frameworks

1. **Scrum**
   - Sprint planning and reviews
   - Daily standups
   - Defined roles (Product Owner, Scrum Master, Development Team)

2. **Kanban**
   - Visualized workflow
   - Limited work in progress
   - Continuous delivery

### Implementation Steps

Start with these practical steps:
1. Train your team on Agile principles
2. Select an appropriate framework
3. Begin with a pilot project
4. Establish regular ceremonies
5. Iterate and improve based on retrospectives

### Common Challenges

- Resistance to change
- Maintaining consistent velocity
- Balancing technical debt with new features

This guide provides a foundation for successful Agile implementation, tailored to your team's specific needs and context.
"""
                generation_time = time.time() - start_time
                metadata = {
                    "model": selected_model,
                    "provider": selected_provider,
                    "prompt_tokens": len(system_prompt.split()) + len(user_prompt.split()),
                    "completion_tokens": len(content.split()),
                    "total_tokens": len(system_prompt.split()) + len(user_prompt.split()) + len(content.split()),
                    "generation_time": generation_time,
                    "simulated": True
                }

            # Store execution in history
            execution_record = {
                "id": execution_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "result": content,
                "params": params,
                "metadata": metadata
            }

            st.session_state.execution_history.append(execution_record)

            # Set generated flag for content display
            st.session_state.generated = True
            st.session_state.result_content = content
            st.session_state.generation_metadata = metadata

            # Show success message
            st.success(f"Prompt executed successfully with {selected_model}")

    # Save version button handler
    if save_version_button:
        import json

        # Get current prompts
        system_prompt = st.session_state.get("final_system_prompt", "")
        user_prompt = st.session_state.get("final_user_prompt", "")

        # If these are empty, try raw prompts
        if not system_prompt:
            system_prompt = st.session_state.get("raw_system_prompt", "")
        if not user_prompt:
            user_prompt = st.session_state.get("raw_user_prompt", "")

        # Generate version ID and name
        import uuid
        version_id = str(uuid.uuid4())[:8]
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        version_name = st.text_input("Version name (optional):", key="version_name_input")
        if not version_name:
            version_name = f"Version_{timestamp}"

        # Create version data
        version_data = {
            "id": version_id,
            "name": version_name,
            "timestamp": timestamp,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "provider": selected_provider,
            "model": selected_model,
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        }

        # Save version
        if "saved_versions" not in st.session_state:
            st.session_state.saved_versions = []

        st.session_state.saved_versions.append(version_data)

        # Offer download
        version_json = json.dumps(version_data, indent=2)
        st.download_button(
            label="Download Version",
            data=version_json,
            file_name=f"prompt_version_{version_id}.json",
            mime="application/json",
            key="download_version_btn"
        )

        st.success(f"Version '{version_name}' saved successfully!")

    # Compare versions button handler
    if compare_button:
        if "saved_versions" in st.session_state and len(st.session_state.saved_versions) > 1:
            st.session_state.show_version_comparison = True
        else:
            st.warning("You need at least 2 saved versions to compare. Please save more versions first.")

    # Show version comparison if requested
    if st.session_state.get("show_version_comparison", False) and "saved_versions" in st.session_state:
        with st.expander("Version Comparison", expanded=True):
            st.markdown("### Compare Saved Prompt Versions")

            # Select versions to compare
            versions = st.session_state.saved_versions
            version_options = [f"{v['name']} ({v['timestamp']})" for v in versions]

            col_v1, col_v2 = st.columns(2)

            with col_v1:
                v1_index = st.selectbox(
                    "Select first version",
                    range(len(version_options)),
                    format_func=lambda i: version_options[i],
                    key="compare_v1_select"
                )

            with col_v2:
                v2_index = st.selectbox(
                    "Select second version",
                    range(len(version_options)),
                    format_func=lambda i: version_options[i],
                    index=min(1, len(version_options) - 1),
                    key="compare_v2_select"
                )

            if st.button("Show Comparison", key="show_comparison_btn"):
                # Get the selected versions
                v1 = versions[v1_index]
                v2 = versions[v2_index]

                # Display side-by-side comparison
                col_left, col_right = st.columns(2)

                with col_left:
                    st.markdown(f"### {v1['name']}")
                    st.markdown(f"*Model: {v1['model']}*")

                    with st.expander("System Prompt", expanded=True):
                        st.code(v1['system_prompt'], language="markdown")

                    with st.expander("User Prompt", expanded=True):
                        st.code(v1['user_prompt'], language="markdown")

                    st.markdown("**Parameters:**")
                    for param, value in v1['parameters'].items():
                        st.markdown(f"- {param}: {value}")

                with col_right:
                    st.markdown(f"### {v2['name']}")
                    st.markdown(f"*Model: {v2['model']}*")

                    with st.expander("System Prompt", expanded=True):
                        st.code(v2['system_prompt'], language="markdown")

                    with st.expander("User Prompt", expanded=True):
                        st.code(v2['user_prompt'], language="markdown")

                    st.markdown("**Parameters:**")
                    for param, value in v2['parameters'].items():
                        st.markdown(f"- {param}: {value}")

                # Diff view option
                if st.checkbox("Show diff view", key="show_diff_view"):
                    from difflib import HtmlDiff

                    st.markdown("### System Prompt Differences")
                    diff_html = HtmlDiff().make_file(
                        v1['system_prompt'].splitlines(),
                        v2['system_prompt'].splitlines(),
                        f"{v1['name']} (System)",
                        f"{v2['name']} (System)"
                    )
                    st.components.v1.html(diff_html, height=400, scrolling=True)

                    st.markdown("### User Prompt Differences")
                    diff_html = HtmlDiff().make_file(
                        v1['user_prompt'].splitlines(),
                        v2['user_prompt'].splitlines(),
                        f"{v1['name']} (User)",
                        f"{v2['name']} (User)"
                    )
                    st.components.v1.html(diff_html, height=400, scrolling=True)

    # Display execution history
    if st.session_state.execution_history:
        with st.expander("Execution History", expanded=False):
            st.markdown("### Recent Executions")

            # Create a table of executions
            import pandas as pd

            history_data = []
            for exec_record in st.session_state.execution_history:
                history_data.append({
                    "ID": exec_record["id"],
                    "Timestamp": exec_record["timestamp"],
                    "Model": exec_record["params"]["model"],
                    "Provider": exec_record["params"]["provider"],
                    "Temperature": exec_record["params"]["temperature"],
                    "Generation Time": f"{exec_record['metadata'].get('generation_time', 0):.2f}s",
                    "Total Tokens": exec_record["metadata"].get("total_tokens", "N/A")
                })

            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df, use_container_width=True)

            # Option to clear history
            if st.button("Clear History", key="clear_history_btn"):
                st.session_state.execution_history = []
                st.rerun()