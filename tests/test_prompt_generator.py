import pytest
import re
from models.prompt_generator import generate_prompt


class TestPromptGenerator:
    """Tests for the prompt generator functionality"""
    
    def test_prompt_includes_sections(self, monkeypatch, default_session_state):
        """Test that the prompt includes the expected sections based on settings"""
        # Patch session_state access in the generate_prompt function
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Verify that all enabled sections are present
        for section, included in default_session_state["prompt_structure"].items():
            if included:
                # Convert section name to something we can find in the output
                section_text = section.replace("&", "").strip()
                assert section_text in prompt, f"Section '{section_text}' should be in the prompt"
    
    def test_chain_of_thought_formatting(self, monkeypatch, default_session_state):
        """Test that the chain of thought steps are properly formatted"""
        # Enable Chain-of-Thought
        default_session_state["thinking_steps_enabled"] = True
        default_session_state["prompt_structure"]["Chain-of-Thought Instructions"] = True
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Verify that steps are numbered correctly
        for i, step in enumerate(default_session_state["chain_of_thought_steps"]):
            expected_step = f"{i + 1}. {step}"
            assert expected_step in prompt, f"Step '{expected_step}' should be in the prompt"
    
    def test_few_shot_examples(self, monkeypatch, default_session_state):
        """Test that few-shot examples are included properly"""
        # Enable Few-Shot Learning
        default_session_state["few_shot_enabled"] = True
        default_session_state["prompt_structure"]["Examples (Few-Shot Learning)"] = True
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Verify that examples are included
        for example in default_session_state["examples"]:
            assert f"Input: {example['input']}" in prompt, "Example input should be in the prompt"
            assert f"Output: {example['output']}" in prompt, "Example output should be in the prompt"
    
    def test_disabled_sections_excluded(self, monkeypatch, default_session_state):
        """Test that disabled sections are excluded from the prompt"""
        # Disable a section
        default_session_state["prompt_structure"]["Self-Review Requirements"] = False
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Verify section is not included
        assert "Self-Review Requirements" not in prompt, "Disabled section should not be in the prompt"
    
    def test_markdown_formatting(self, monkeypatch, default_session_state):
        """Test that the generated prompt uses proper markdown formatting"""
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Verify markdown headers are used
        header_pattern = r'^# [A-Za-z &]+'
        assert re.search(header_pattern, prompt, re.MULTILINE), "Prompt should contain markdown headers"
        
        # Verify subheaders if needed
        subheader_pattern = r'^## [A-Za-z &]+'
        assert re.search(subheader_pattern, prompt, re.MULTILINE), "Prompt should contain markdown subheaders"


class TestPromptContent:
    """Tests for the content of generated prompts"""
    
    def test_context_content(self, monkeypatch, default_session_state):
        """Test that the context section contains the expected content"""
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Look for the context content
        assert default_session_state["context"] in prompt, "Context content should be in the prompt"
    
    def test_task_content(self, monkeypatch, default_session_state):
        """Test that the task section contains the expected content"""
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Look for the task content
        assert default_session_state["task"] in prompt, "Task content should be in the prompt"
    
    def test_output_requirements(self, monkeypatch, default_session_state):
        """Test that output requirements are properly included"""
        monkeypatch.setattr('streamlit.session_state', default_session_state)
        
        prompt = generate_prompt()
        
        # Check for format and tone
        assert f"Format: {default_session_state['output_format']}" in prompt, "Output format should be specified"
        assert f"Tone: {default_session_state['output_tone']}" in prompt, "Output tone should be specified"