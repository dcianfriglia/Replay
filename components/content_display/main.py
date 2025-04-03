import streamlit as st
import time
from utils.ui_helpers import section_header
from models.prompt_generator import generate_prompt, simulate_content_generation, calculate_quality_metrics
from models.content_generator import ContentGenerator, generate_content
from .metrics import render_quality_metrics
from .feedback import render_feedback_section


def render_content_display():
    """Render the Content Display section for generated content"""

    st.markdown("---")
    section_header("Generated Content")

    # Check if content is available or needs to be generated
    if "result_content" not in st.session_state or st.session_state.get("regenerate", False):
        with st.spinner("Generating content..."):
            # Reset regenerate flag if set
            if st.session_state.get("regenerate", False):
                st.session_state.regenerate = False

            # Get the current prompt
            prompt = generate_prompt()

            # Check if we should use API or simulation
            use_api = st.session_state.get("use_api", False)

            if use_api and "api_key" in st.session_state and st.session_state.api_key:
                # Use LLM API
                try:
                    generator = ContentGenerator(api_key=st.session_state.api_key)

                    # Get model parameters
                    model = st.session_state.get("model_selection", "claude-3-5-sonnet")
                    temperature = st.session_state.get("temperature", 0.7)
                    max_tokens = st.session_state.get("max_tokens", 1000)

                    # Track generation time
                    start_time = time.time()

                    # Make API call
                    result = generator.generate(
                        prompt,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )

                    # Calculate generation time
                    generation_time = time.time() - start_time

                    # Store results
                    st.session_state.result_content = result["content"]
                    st.session_state.generation_metadata = {
                        "model": model,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "generation_time": generation_time,
                        "prompt_tokens": result.get("metadata", {}).get("prompt_tokens", 0),
                        "completion_tokens": result.get("metadata", {}).get("completion_tokens", 0),
                        "total_tokens": result.get("metadata", {}).get("total_tokens", 0)
                    }
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
                    # Fall back to simulation
                    st.session_state.result_content = simulate_content_generation()
            else:
                # Simulate content generation
                st.session_state.result_content = simulate_content_generation()

                # Add simulated metadata
                st.session_state.generation_metadata = {
                    "model": "simulation",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                    "generation_time": 1.2,
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(st.session_state.result_content.split()),
                    "total_tokens": len(prompt.split()) + len(st.session_state.result_content.split()),
                    "simulated": True
                }

            # Calculate quality metrics
            st.session_state.quality_metrics = calculate_quality_metrics(st.session_state.result_content)

    # Display generation info
    if "generation_metadata" in st.session_state:
        with st.expander("Generation Details", expanded=False):
            metadata = st.session_state.generation_metadata

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Generation Time", f"{metadata.get('generation_time', 0):.2f}s")

            with col2:
                st.metric("Model", metadata.get("model", "unknown"))

            with col3:
                st.metric("Prompt Tokens", metadata.get("prompt_tokens", 0))

            with col4:
                st.metric("Output Tokens", metadata.get("completion_tokens", 0))

            # Show full prompt option
            if st.checkbox("Show full prompt"):
                st.code(generate_prompt(), language="markdown")

    # Display regenerate option
    col1, col2, col3 = st.columns([5, 2, 2])

    with col1:
        st.markdown("This content was generated based on your prompt configuration.")

    with col2:
        # API settings
        use_api = st.toggle("Use LLM API", value=st.session_state.get("use_api", False), key="use_api_toggle")
        st.session_state.use_api = use_api

    with col3:
        if st.button("Regenerate", type="secondary", use_container_width=True):
            # Set flag to regenerate content
            st.session_state.regenerate = True
            st.rerun()

    # If using API, show API settings
    if use_api:
        with st.expander("API Settings", expanded=not bool(st.session_state.get("api_key"))):
            col_a, col_b = st.columns(2)

            with col_a:
                api_key = st.text_input(
                    "API Key",
                    type="password",
                    value=st.session_state.get("api_key", ""),
                    key="api_key_input",
                    help="Your Anthropic API key"
                )
                st.session_state.api_key = api_key

                model = st.selectbox(
                    "Model",
                    ["claude-3-5-sonnet", "claude-3-5-haiku", "claude-3-opus"],
                    index=0,
                    key="model_selection"
                )
                st.session_state.model_selection = model

            with col_b:
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=st.session_state.get("temperature", 0.7),
                    step=0.1,
                    key="temperature_slider"
                )
                st.session_state.temperature = temperature

                max_tokens = st.slider(
                    "Max Tokens",
                    min_value=100,
                    max_value=4000,
                    value=st.session_state.get("max_tokens", 1000),
                    step=100,
                    key="max_tokens_slider"
                )
                st.session_state.max_tokens = max_tokens

    # Display the generated content in a markdown box
    with st.container(border=True, height=400):
        # Add edit option
        if st.session_state.get("edit_content", False):
            edited_content = st.text_area(
                "Edit Content",
                value=st.session_state.result_content,
                height=350,
                key="content_editor"
            )

            col_edit, col_cancel = st.columns(2)

            with col_edit:
                if st.button("Save Edits", use_container_width=True):
                    st.session_state.result_content = edited_content
                    st.session_state.edit_content = False
                    st.rerun()

            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.edit_content = False
                    st.rerun()
        else:
            st.markdown(st.session_state.result_content)

    # Action buttons for the content
    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.download_button(
            "Download Content",
            data=st.session_state.result_content,
            file_name="generated_content.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col_b:
        # Clipboard functionality requires JS interop, showing user message instead
        if st.button("Copy to Clipboard", use_container_width=True):
            st.success("Content copied to clipboard! (In a real app, this would use JavaScript)")

    with col_c:
        if st.button("Edit Content", use_container_width=True):
            st.session_state.edit_content = True
            st.rerun()

    with col_d:
        refine_options = {"Improve": "Enhance overall quality",
                          "Simplify": "Make more concise and clear",
                          "Elaborate": "Add more details and examples"}

        refine_action = st.selectbox(
            "Refine Action",
            list(refine_options.keys()),
            format_func=lambda x: f"{x}: {refine_options[x]}",
            key="refine_action"
        )

        if st.button("Refine Content", type="primary", use_container_width=True):
            with st.spinner(f"{refine_action}ing content..."):
                # Simulate refinement (in a real app, this would call the API again)
                time.sleep(1.5)

                if refine_action == "Improve":
                    st.session_state.result_content = st.session_state.result_content.replace(
                        "implementing Agile", "implementing Agile methodologies effectively"
                    )
                elif refine_action == "Simplify":
                    st.session_state.result_content = st.session_state.result_content.replace(
                        "revolutionized software development", "improved how teams build software"
                    )
                elif refine_action == "Elaborate":
                    st.session_state.result_content = st.session_state.result_content.replace(
                        "... (content continues)",
                        "\n\n### Additional Resources\n\n* **Scrum Guide**: The official guide to Scrum framework\n* **Kanban Guide**: Detailed implementation of Kanban boards\n* **SAFe Framework**: For scaling Agile in larger organizations\n\n### Case Studies\n\nCompanies that have successfully implemented Agile methodologies have reported:\n\n* 25-30% increase in productivity\n* 50% reduction in time-to-market\n* Significant improvement in customer satisfaction\n\nThese improvements stem from better communication, faster feedback cycles, and more adaptable planning approaches."
                    )

                st.success(f"Content {refine_action.lower()}d successfully!")
                st.rerun()

    # Display quality metrics
    render_quality_metrics(st.session_state.result_content)

    # Display feedback section
    render_feedback_section()