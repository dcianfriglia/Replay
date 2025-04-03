import sys
import os
import pytest
from pathlib import Path

# Add the root directory to path to ensure imports work correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import key modules needed for testing
from utils.state_management import initialize_session_state
from models.prompt_generator import generate_prompt


@pytest.fixture
def mock_session_state():
    """
    Create a mock session state for testing
    
    This fixture provides a dictionary-like object that simulates Streamlit's session_state
    """
    class MockSessionState(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__dict__ = self
    
    mock_state = MockSessionState()
    yield mock_state


@pytest.fixture
def default_session_state():
    """
    Create a session state initialized with default values
    """
    # In a real implementation, streamlit.session_state would be mocked
    # For testing purposes, we return a simple dictionary with the default values
    state = {}
    
    # Add key session state values
    state["context"] = "You are an AI assistant with expertise in content creation."
    state["task"] = "Create a comprehensive guide on implementing Agile methodology."
    state["input_format"] = "Plain Text"
    state["input_description"] = "The user will provide information about their team size."
    state["output_format"] = "Markdown"
    state["output_tone"] = "Professional"
    state["output_requirements"] = "Length: Comprehensive but concise"
    state["examples"] = [{"input": "Example input", "output": "Example output"}]
    state["constraints"] = "Focus on practical implementation"
    state["evaluation_criteria"] = "Content should be factually accurate"
    state["selected_workflows"] = ["Chain-of-Thought", "Few-Shot Learning"]
    state["chain_of_thought_steps"] = ["Analyze requirements", "Research key concepts"]
    state["thinking_steps_enabled"] = True
    state["few_shot_enabled"] = True
    state["selected_agents"] = ["Content Creator", "Editor/Refiner"]
    state["content_creator_enabled"] = True
    state["editor_enabled"] = True
    state["prompt_structure"] = {
        "Context & Background": True,
        "Task Definition": True,
        "Input Data Format": True,
        "Output Requirements": True,
        "Examples (Few-Shot Learning)": True,
        "Chain-of-Thought Instructions": True,
    }
    
    yield state


@pytest.fixture
def sample_prompt():
    """
    Provide a sample prompt for testing
    """
    return """# Context & Background
You are an AI assistant with expertise in content creation.

# Task Definition
Create a comprehensive guide on implementing Agile methodology.

# Input Data Format
The user will provide information about their team size.

# Output Requirements
Format: Markdown
Tone: Professional
Length: Comprehensive but concise

# Examples
Input: Example input
Output: Example output

# Chain-of-Thought Instructions
1. Analyze requirements
2. Research key concepts
"""