import streamlit as st
from utils.ui_helpers import section_header, subsection_header


def render_content_creator_agent():
    """Render the Content Creator Agent configuration section"""

    st.markdown("### Content Creator Agent")

    st.markdown("""
    The Content Creator is the primary agent responsible for generating content.
    This agent focuses on producing well-structured, informative content based on the input prompt.
    """)

    # Enable/disable toggle
    creator_enabled = st.toggle("Enable Content Creator Agent",
                                value=st.session_state.content_creator_enabled,
                                help="When enabled, this agent will generate the initial content")
    st.session_state.content_creator_enabled = creator_enabled

    if creator_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Agent personality
            subsection_header("Agent Personality")

            personality = st.selectbox(
                "Select personality",
                ["Neutral & Objective", "Informative & Educational", "Creative & Engaging",
                 "Concise & Direct", "Custom..."],
                index=1,
                key="creator_personality",
                help="The overall tone and style of the content creator"
            )

            if personality == "Custom...":
                st.text_area(
                    "Define custom personality",
                    value="",
                    height=100,
                    key="creator_custom_personality"
                )

            # Knowledge emphasis
            subsection_header("Knowledge Emphasis")

            st.markdown("Balance between factual accuracy and creative expression:")

            col_a, col_b, col_c = st.columns([1, 10, 1])
            with col_a:
                st.write("Factual")
            with col_b:
                emphasis = st.slider(
                    "Emphasis",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key="knowledge_emphasis",
                    label_visibility="collapsed"
                )
            with col_c:
                st.write("Creative")

            # Instructions for Creator
            subsection_header("Instructions for Creator")

            st.text_area(
                "Provide specific instructions for this agent",
                value="Focus on creating well-structured content that balances theoretical knowledge with practical examples. Use clear headings and subheadings to organize information logically.",
                height=150,
                key="creator_instructions"
            )

        with col2:
            # Model selection
            subsection_header("Model Configuration")

            st.selectbox(
                "Model",
                ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                index=0,
                key="creator_model"
            )

            st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                key="creator_temperature",
                help="Higher values make output more creative, lower values more deterministic"
            )

            st.number_input(
                "Max Output Length (tokens)",
                min_value=100,
                max_value=4000,
                value=1000,
                step=100,
                key="creator_max_tokens"
            )

            # Advanced settings
            subsection_header("Advanced Settings")

            st.checkbox(
                "Enable self-review",
                value=True,
                key="creator_self_review",
                help="Agent will review and refine its own output before submission"
            )

            st.checkbox(
                "Access to external knowledge",
                value=True,
                key="creator_external_knowledge",
                help="Allow agent to access external knowledge sources"
            )

            st.checkbox(
                "Include reasoning steps",
                value=True,
                key="creator_reasoning_steps",
                help="Include explicit reasoning steps in the generation process"
            )

        # Examples of creator output
        with st.expander("Content Creator Examples", expanded=False):
            st.markdown("""
            #### Example 1: Technical Explanation

            **Prompt:** Explain how neural networks work

            **Output:**
            ```
            # Understanding Neural Networks

            Neural networks are computational systems inspired by the human brain. They consist of interconnected nodes (neurons) that process and transmit information.

            ## Key Components

            1. **Input Layer**: Receives initial data
            2. **Hidden Layers**: Process information through weighted connections
            3. **Output Layer**: Produces the final result

            Neural networks learn by adjusting connection weights through a process called backpropagation, minimizing the difference between actual and expected outputs.
            ```

            #### Example 2: Creative Content

            **Prompt:** Write a short story about time travel

            **Output:**
            ```
            # The Moment Between

            Eliza stepped into the chamber, her heart racing. The chronometric display counted down: 3...2...1...

            Suddenly, she was standing in her childhood home. The smell of her mother's cooking filled the air—a recipe lost to time and memory. She had exactly ten minutes before the temporal field collapsed.

            What would you say to your younger self, if you had the chance? Eliza had rehearsed this moment for years, but now, watching her 10-year-old self reading by the window, words failed her.

            Sometimes the most profound changes come not from what we say, but from what we realize in silence.
            ```
            """)