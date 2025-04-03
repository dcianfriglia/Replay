import streamlit as st


def initialize_session_state():
    """Initialize all session state variables with default values"""

    # Context & Background
    if 'context' not in st.session_state:
        st.session_state.context = "You are an AI assistant with expertise in content creation. You have access to information about modern software development practices and project management methodologies."

    # Task Definition
    if 'task' not in st.session_state:
        st.session_state.task = "Create a comprehensive guide on implementing Agile methodology in software development teams."

    # Input Format
    if 'input_format' not in st.session_state:
        st.session_state.input_format = "Plain Text"
    if 'input_description' not in st.session_state:
        st.session_state.input_description = "The user will provide information about their team size, current processes, and specific challenges."

    # Output Requirements
    if 'output_format' not in st.session_state:
        st.session_state.output_format = "Markdown"
    if 'output_tone' not in st.session_state:
        st.session_state.output_tone = "Professional"
    if 'output_requirements' not in st.session_state:
        st.session_state.output_requirements = "Length: Comprehensive but concise, focusing on actionable insights\nInclude: Headers, bullet points, and examples where appropriate"

    # Examples & Constraints
    if 'examples' not in st.session_state:
        st.session_state.examples = [
            {
                "input": "What are the key principles of Agile development?",
                "output": "Agile development is based on four key values and twelve principles outlined in the Agile Manifesto. The four values are:\n\n1. Individuals and interactions over processes and tools\n2. Working software over comprehensive documentation\n3. Customer collaboration over contract negotiation\n4. Responding to change over following a plan\n\nThese values are supported by principles such as delivering working software frequently, welcoming changing requirements, and maintaining technical excellence."
            }
        ]
    if 'constraints' not in st.session_state:
        st.session_state.constraints = "Focus on practical implementation rather than theoretical background.\nProvide specific examples for different team sizes and contexts."

    # Evaluation Criteria
    if 'evaluation_criteria' not in st.session_state:
        st.session_state.evaluation_criteria = "Content should be factually accurate, well-structured, practical, and actionable.\nExamples should be relevant to real-world scenarios."

    # Workflows
    if 'selected_workflows' not in st.session_state:
        st.session_state.selected_workflows = ["Chain-of-Thought", "Few-Shot Learning"]

    # Chain of Thought
    if 'chain_of_thought_steps' not in st.session_state:
        st.session_state.chain_of_thought_steps = [
            "Analyze requirements and current team situation",
            "Research key Agile concepts relevant to the specific case",
            "Outline content structure with clear sections",
            "Draft content sections with practical examples",
            "Review for consistency and completeness"
        ]
    if 'thinking_steps_enabled' not in st.session_state:
        st.session_state.thinking_steps_enabled = True

    # Iterative Refinement
    if 'iterative_refinement_enabled' not in st.session_state:
        st.session_state.iterative_refinement_enabled = False

    # Few-shot learning
    if 'few_shot_enabled' not in st.session_state:
        st.session_state.few_shot_enabled = True

    # RAG
    if 'rag_enabled' not in st.session_state:
        st.session_state.rag_enabled = False

    # Self-consistency
    if 'self_consistency_enabled' not in st.session_state:
        st.session_state.self_consistency_enabled = False

    # Agents
    if 'selected_agents' not in st.session_state:
        st.session_state.selected_agents = ["Content Creator", "Editor/Refiner"]

    # Content Creator
    if 'content_creator_enabled' not in st.session_state:
        st.session_state.content_creator_enabled = True

    # Fact Checker
    if 'fact_checker_enabled' not in st.session_state:
        st.session_state.fact_checker_enabled = False

    # Editor
    if 'editor_enabled' not in st.session_state:
        st.session_state.editor_enabled = True

    # Critic
    if 'critic_enabled' not in st.session_state:
        st.session_state.critic_enabled = False

    # Audience Adapter
    if 'audience_adapter_enabled' not in st.session_state:
        st.session_state.audience_adapter_enabled = False

    # Prompt structure
    if 'prompt_structure' not in st.session_state:
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

        # UI state
        if 'generated' not in st.session_state:
            st.session_state.generated = False
        if 'edit_raw' not in st.session_state:
            st.session_state.edit_raw = False
        if 'regenerate' not in st.session_state:
            st.session_state.regenerate = False
        if 'show_save_dialog' not in st.session_state:
            st.session_state.show_save_dialog = False
        if 'show_load_dialog' not in st.session_state:
            st.session_state.show_load_dialog = False

        # State persistence
        if 'feedback_data' not in st.session_state:
            st.session_state.feedback_data = None
        if 'content_satisfaction' not in st.session_state:
            st.session_state.content_satisfaction = 0
        if 'feedback_submitted' not in st.session_state:
            st.session_state.feedback_submitted = False

        # Advanced workflow settings
        if 'iterative_iterations' not in st.session_state:
            st.session_state.iterative_iterations = 3
        if 'iterative_focus' not in st.session_state:
            st.session_state.iterative_focus = ["Clarity", "Accuracy", "Coherence"]
        if 'iterative_instructions' not in st.session_state:
            st.session_state.iterative_instructions = "Improve the clarity and conciseness of the content. Ensure all concepts are explained clearly and information flows logically."
        if 'critic_evaluation_criteria' not in st.session_state:
            st.session_state.critic_evaluation_criteria = [
                {"name": "Accuracy", "description": "Factual correctness and absence of errors", "weight": 5},
                {"name": "Clarity", "description": "Clear and understandable explanations", "weight": 4},
                {"name": "Completeness", "description": "Comprehensive coverage of the topic", "weight": 3},
                {"name": "Relevance", "description": "Direct relevance to the query or task", "weight": 4}
            ]