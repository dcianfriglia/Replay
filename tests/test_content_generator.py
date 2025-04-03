import pytest
import responses
import json
from models.content_generator import ContentGenerator, generate_content


class TestContentGenerator:
    """Tests for the ContentGenerator class"""
    
    def test_init_with_api_key(self):
        """Test initialization with a provided API key"""
        api_key = "test_api_key_123"
        generator = ContentGenerator(api_key=api_key)
        
        assert generator.api_key == api_key
    
    def test_init_without_api_key(self, monkeypatch):
        """Test initialization without an API key (should try environment variable)"""
        # Mock the environment variable
        monkeypatch.setenv("LLM_API_KEY", "env_api_key_456")
        
        generator = ContentGenerator()
        assert generator.api_key == "env_api_key_456"
    
    def test_simulation_mode(self):
        """Test that simulation mode works when no API key is available"""
        # Create generator with no API key
        generator = ContentGenerator(api_key=None)
        
        # Ensure environment variable is not used
        import os
        if "LLM_API_KEY" in os.environ:
            del os.environ["LLM_API_KEY"]
        
        prompt = "Test prompt for simulation"
        result = generator.generate(prompt)
        
        # Verify simulation worked
        assert result["success"] is True
        assert "Simulated Response" in result["content"]
        assert "simulated" in result["metadata"]
        assert result["metadata"]["simulated"] is True
    
    @responses.activate
    def test_successful_api_call(self):
        """Test a successful API call to the LLM provider"""
        # Mock the API response
        responses.add(
            responses.POST,
            "https://api.anthropic.com/v1/messages",
            json={
                "content": [{"text": "This is a test response from the mocked API."}],
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 20,
                    "total_tokens": 30
                }
            },
            status=200
        )
        
        # Create generator with test API key
        generator = ContentGenerator(api_key="test_api_key")
        
        # Test API call
        prompt = "Test prompt for API"
        result = generator.generate(prompt)
        
        # Verify success
        assert result["success"] is True
        assert "This is a test response from the mocked API." in result["content"]
        assert result["metadata"]["total_tokens"] == 30
    
    @responses.activate
    def test_failed_api_call(self):
        """Test handling of a failed API call"""
        # Mock a failed API response
        responses.add(
            responses.POST,
            "https://api.anthropic.com/v1/messages",
            json={"error": "Invalid API key"},
            status=401
        )
        
        # Create generator with invalid API key
        generator = ContentGenerator(api_key="invalid_key")
        
        # Test API call
        prompt = "Test prompt for failed API call"
        result = generator.generate(prompt)
        
        # Verify failure handling
        assert result["success"] is False
        assert "error" in result
        assert "API Request Failed" in result["content"]
    
    def test_batch_generate(self):
        """Test generating content for multiple prompts"""
        # Create generator without API key (simulation mode)
        generator = ContentGenerator(api_key=None)
        
        # Test batch generation
        prompts = [
            "Test prompt 1",
            "Test prompt 2",
            "Test prompt 3"
        ]
        
        results = generator.batch_generate(prompts)
        
        # Verify results
        assert len(results) == 3
        for result in results:
            assert result["success"] is True
            assert "Simulated Response" in result["content"]


class TestContentGeneratorHelpers:
    """Tests for helper functions in the content_generator module"""
    
    def test_generate_content_helper(self):
        """Test the generate_content helper function"""
        # The generate_content function should return just the content string
        prompt = "Test prompt for helper function"
        content = generate_content(prompt)
        
        # Verify it returns a string and contains simulated response
        assert isinstance(content, str)
        assert "Simulated Response" in content