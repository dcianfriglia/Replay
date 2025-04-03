"""
End-to-End Test for LLM Prompt Engineering Framework

This test script verifies the core functionality of the prompt engineering framework
by testing the prompt generation, template management, and content generation flow.
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import required modules
from utils.state_management import initialize_session_state
from models.prompt_generator import generate_prompt
from models.content_generator import ContentGenerator, generate_content
from utils.template_manager import save_template, load_template


class MockSessionState(dict):
    """Mock for Streamlit's session_state"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def setup_test_environment():
    """Set up test environment and mock session state"""
    print("Setting up test environment...")

    # Create test directories
    os.makedirs(project_root / "templates", exist_ok=True)
    os.makedirs(project_root / "stored_states", exist_ok=True)

    # Create mock session state
    mock_state = MockSessionState()

    # Initialize with test values
    mock_state.context = "You are an AI assistant with expertise in technical documentation."
    mock_state.task = "Create a comprehensive API documentation guide."
    mock_state.input_format = "JSON"
    mock_state.input_description = "The user will provide endpoint specifications in JSON format."
    mock_state.output_format = "Markdown"
    mock_state.output_tone = "Technical"
    mock_state.output_requirements = "Include code examples and parameter descriptions."
    mock_state.examples = [
        {
            "input": "Example endpoint specification",
            "output": "Example API documentation"
        }
    ]
    mock_state.constraints = "Focus on readability and completeness."
    mock_state.evaluation_criteria = "Documentation should be accurate and well-structured."

    # Set up workflow configurations
    mock_state.thinking_steps_enabled = True
    mock_state.few_shot_enabled = True
    mock_state.chain_of_thought_steps = [
        "Analyze API endpoint structure",
        "Identify required and optional parameters",
        "Create parameter documentation",
        "Add request and response examples",
        "Include error handling information"
    ]

    # Set up prompt structure
    mock_state.prompt_structure = {
        "Context & Background": True,
        "Task Definition": True,
        "Input Data Format": True,
        "Output Requirements": True,
        "Examples (Few-Shot Learning)": True,
        "Chain-of-Thought Instructions": True,
        "Self-Review Requirements": True,
        "Fact Checking Instructions": False
    }

    return mock_state


def test_prompt_generation(mock_state):
    """Test prompt generation functionality"""
    print("\nTesting prompt generation...")

    # Override the global session_state with our mock
    import streamlit as st
    st.session_state = mock_state

    # Generate prompt
    prompt = generate_prompt()

    # Verify prompt contains expected sections
    expected_sections = [
        "Context & Background",
        "Task Definition",
        "Input Data Format",
        "Output Requirements"
    ]

    all_found = True
    for section in expected_sections:
        if section not in prompt:
            print(f"ERROR: Expected section '{section}' not found in prompt")
            all_found = False

    if all_found:
        print("✓ All expected sections found in generated prompt")

    # Verify chain of thought steps are included
    step_count = 0
    for step in mock_state.chain_of_thought_steps:
        if step in prompt:
            step_count += 1

    if step_count == len(mock_state.chain_of_thought_steps):
        print(f"✓ All {step_count} thinking steps included in prompt")
    else:
        print(f"ERROR: Only {step_count}/{len(mock_state.chain_of_thought_steps)} thinking steps found in prompt")

    return prompt


def test_template_management(mock_state, prompt):
    """Test template saving and loading"""
    print("\nTesting template management...")

    template_name = "test_template"
    template_path = project_root / "templates" / f"{template_name.replace(' ', '_')}.json"

    # Clean up any existing test template
    if os.path.exists(template_path):
        os.remove(template_path)

    # Create template data from mock state
    template_data = {
        "context": mock_state.context,
        "task": mock_state.task,
        "input_format": mock_state.input_format,
        "input_description": mock_state.input_description,
        "output_format": mock_state.output_format,
        "output_tone": mock_state.output_tone,
        "output_requirements": mock_state.output_requirements,
        "examples": mock_state.examples,
        "constraints": mock_state.constraints,
        "evaluation_criteria": mock_state.evaluation_criteria,
        "chain_of_thought_steps": mock_state.chain_of_thought_steps,
        "prompt_structure": mock_state.prompt_structure
    }

    # Save template
    saved_path = save_template(template_data, template_name)

    if os.path.exists(saved_path):
        print(f"✓ Template saved to {saved_path}")
    else:
        print(f"ERROR: Failed to save template to {saved_path}")
        return False

    # Modify mock state to verify loading works
    mock_state.context = "MODIFIED CONTEXT"
    mock_state.task = "MODIFIED TASK"

    # Load template
    loaded_data = load_template(saved_path)

    if loaded_data["context"] == template_data["context"] and loaded_data["task"] == template_data["task"]:
        print("✓ Template loaded correctly")
    else:
        print("ERROR: Loaded template data doesn't match saved data")
        return False

    # Clean up
    os.remove(saved_path)
    return True


def test_content_generation(prompt):
    """Test content generation from prompt"""
    print("\nTesting content generation (simulation mode)...")

    # Create content generator without API key (simulation mode)
    generator = ContentGenerator(api_key=None)

    # Generate content
    result = generator.generate(prompt)

    if result["success"] and len(result["content"]) > 100:
        print(f"✓ Content generated successfully ({len(result['content'])} chars)")
        print("✓ Sample of generated content:")
        print(f"  {result['content'][:200]}...")
    else:
        print("ERROR: Content generation failed or produced too little content")
        return False

    return True


def run_tests():
    """Run all tests"""
    print("====== LLM PROMPT ENGINEERING FRAMEWORK TEST SUITE ======")

    # Set up test environment
    mock_state = setup_test_environment()

    # Run tests
    prompt = test_prompt_generation(mock_state)
    template_result = test_template_management(mock_state, prompt)
    content_result = test_content_generation(prompt)

    # Print summary
    print("\n====== TEST SUMMARY ======")
    if prompt and template_result and content_result:
        print("✓ All tests passed successfully!")
    else:
        print("❌ Some tests failed. See details above.")


if __name__ == "__main__":
    run_tests()