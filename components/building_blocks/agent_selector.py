import streamlit as st
from utils.ui_helpers import section_with_info, agent_card


def render_agent_selector():
    """Render the Agent Selector section"""
    with st.container(border=True):
        section_with_info(
            "Agent Configuration",
            "Set up agents for different aspects of content creation"
        )

        st.markdown("Select the agents you want to use in your prompt engineering framework:")

        # First row
        col1, col2 = st.columns(2)
        
        with col1:
            # Content Creator agent
            content_creator_enabled = agent_card(
                "Content Creator",
                "Primary agent responsible for generating content",
                "content_creator_enabled"
            )
            
            if content_creator_enabled:
                with st.container(border=False):
                    st.selectbox(
                        "Content Creator Focus",
                        ["Balanced (Default)", "Creative Focus", "Factual Focus", "Educational Focus"],
                        index=0,
                        key="content_creator_focus"
                    )
        
        with col2:
            # Fact Checker agent
            fact_checker_enabled = agent_card(
                "Fact Checker",
                "Verifies factual accuracy of generated content",
                "fact_checker_enabled"
            )
            
            if fact_checker_enabled:
                with st.container(border=False):
                    st.selectbox(
                        "Fact Checking Level",
                        ["Basic", "Comprehensive", "Academic", "Domain-Specific"],
                        index=1,
                        key="fact_checking_level"
                    )
        
        # Second row
        col3, col4 = st.columns(2)
        
        with col3:
            # Editor/Refiner agent
            editor_enabled = agent_card(
                "Editor/Refiner",
                "Improves style, clarity, and coherence",
                "editor_enabled"
            )
            
            if editor_enabled:
                with st.container(border=False):
                    st.selectbox(
                        "Editing Focus",
                        ["Grammar & Style", "Simplification", "Elaboration", "Flow & Structure"],
                        index=0,
                        key="editing_focus"
                    )
        
        with col4:
            # Critic/Evaluator agent
            critic_enabled = agent_card(
                "Critic/Evaluator",
                "Assesses content against predefined criteria",
                "critic_enabled"
            )
            
            if critic_enabled:
                with st.container(border=False):
                    st.selectbox(
                        "Evaluation Approach",
                        ["Qualitative", "Quantitative", "Comparative", "Custom"],
                        index=0,
                        key="evaluation_approach"
                    )
        
        # Last row
        col5, col6 = st.columns(2)
        
        with col5:
            # Audience Adapter agent
            audience_adapter_enabled = agent_card(
                "Audience Adapter",
                "Tailors content for specific audiences",
                "audience_adapter_enabled"
            )
            
            if audience_adapter_enabled:
                with st.container(border=False):
                    st.selectbox(
                        "Target Audience",
                        ["General", "Technical", "Business", "Academic", "Beginner", "Custom"],
                        index=0,
                        key="target_audience"
                    )
        
        # Update selected agents in session state
        selected_agents = []
        if content_creator_enabled:
            selected_agents.append("Content Creator")
        if fact_checker_enabled:
            selected_agents.append("Fact Checker")
        if editor_enabled:
            selected_agents.append("Editor/Refiner")
        if critic_enabled:
            selected_agents.append("Critic/Evaluator")
        if audience_adapter_enabled:
            selected_agents.append("Audience Adapter")
        
        st.session_state.selected_agents = selected_agents

        # Display hint if no agents selected
        if not selected_agents:
            st.warning("Select at least one agent to be included in your workflow.")