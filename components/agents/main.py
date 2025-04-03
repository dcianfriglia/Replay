import streamlit as st
from utils.ui_helpers import section_header
from .content_creator import render_content_creator_agent
from .editor import render_editor_agent
from .fact_checker import render_fact_checker_agent
from .critic import render_critic_agent
from .audience_adapter import render_audience_adapter_agent


def render_agents_tab():
    """Render the Agents tab content"""

    section_header("Agent Configuration")

    st.markdown("""
    Agents are specialized LLMs configured for specific roles in the content generation process.
    Configure the agents you want to use in your prompt engineering framework.
    """)

    agent_tabs = st.tabs([
        "Content Creator",
        "Editor/Refiner",
        "Fact Checker",
        "Critic/Evaluator",
        "Audience Adapter"
    ])

    # Content Creator Agent
    with agent_tabs[0]:
        render_content_creator_agent()

    # Editor/Refiner Agent
    with agent_tabs[1]:
        render_editor_agent()

    # Fact Checker Agent
    with agent_tabs[2]:
        render_fact_checker_agent()

    # Critic/Evaluator Agent
    with agent_tabs[3]:
        render_critic_agent()

    # Audience Adapter Agent
    with agent_tabs[4]:
        render_audience_adapter_agent()

    # Display active agents summary
    st.markdown("---")
    render_active_agents_summary()


def render_active_agents_summary():
    """Render a summary of currently active agents"""

    st.markdown("### Active Agents")

    active_agents = []
    if st.session_state.content_creator_enabled:
        active_agents.append("Content Creator")
    if st.session_state.editor_enabled:
        active_agents.append("Editor/Refiner")
    if st.session_state.fact_checker_enabled:
        active_agents.append("Fact Checker")
    if st.session_state.critic_enabled:
        active_agents.append("Critic/Evaluator")
    if st.session_state.audience_adapter_enabled:
        active_agents.append("Audience Adapter")

    if active_agents:
        cols = st.columns(len(active_agents))
        for i, agent in enumerate(active_agents):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; border-radius: 5px; background-color: #d4edda; color: #155724;">
                    <h4>{agent}</h4>
                    <p>Active</p>
                </div>
                """, unsafe_allow_html=True)

        # Agent interaction explanation
        st.markdown("""
        #### Agent Interaction Flow

        The agents above will work together in the following sequence:
        1. Content Creator generates the initial content
        2. Fact Checker verifies factual accuracy (if enabled)
        3. Editor/Refiner improves style and clarity (if enabled)
        4. Critic/Evaluator assesses against criteria (if enabled)
        5. Audience Adapter tailors for specific audience (if enabled)
        """)
    else:
        st.warning("No agents are currently active. Enable at least one agent to use agent-based processing.")