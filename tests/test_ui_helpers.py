import pytest
from unittest.mock import MagicMock, patch
from utils.ui_helpers import section_header, subsection_header, info_tooltip, section_with_info


@pytest.mark.ui
class TestUIHelpers:
    """Tests for UI helper functions"""
    
    @patch('streamlit.markdown')
    def test_section_header(self, mock_markdown):
        """Test the section_header function"""
        section_header("Test Section")
        
        # Verify that streamlit.markdown was called with the correct HTML
        mock_markdown.assert_called_once()
        call_args = mock_markdown.call_args[0][0]
        assert '<div class="section-header">Test Section</div>' in call_args
        assert mock_markdown.call_args[1]['unsafe_allow_html'] is True
    
    @patch('streamlit.markdown')
    def test_subsection_header(self, mock_markdown):
        """Test the subsection_header function"""
        subsection_header("Test Subsection")
        
        # Verify that streamlit.markdown was called with the correct markdown
        mock_markdown.assert_called_once_with("#### Test Subsection")
    
    def test_info_tooltip(self):
        """Test the info_tooltip function"""
        tooltip = info_tooltip("Test tooltip text")
        
        # Verify tooltip HTML formatting
        assert '<span class="tooltip">' in tooltip
        assert 'ℹ️' in tooltip
        assert '<span class="tooltiptext">Test tooltip text</span>' in tooltip
    
    @patch('streamlit.markdown')
    def test_section_with_info(self, mock_markdown):
        """Test the section_with_info function"""
        section_with_info("Test Section", "Test info text")
        
        # Verify that streamlit.markdown was called with the correct HTML
        mock_markdown.assert_called_once()
        call_args = mock_markdown.call_args[0][0]
        assert '<div class="section-header">Test Section' in call_args
        assert 'Test info text' in call_args
        assert mock_markdown.call_args[1]['unsafe_allow_html'] is True


@pytest.mark.ui
class TestUIComponentHelpers:
    """Tests for more complex UI component helper functions"""
    
    @patch('streamlit.container')
    def test_card_container(self, mock_container):
        """Test the card_container function"""
        # Import here to avoid issues with early imports
        from utils.ui_helpers import card_container
        
        # Create a mock content function
        mock_content_func = MagicMock()
        
        # Mock the context manager behavior of container
        mock_context = MagicMock()
        mock_container.return_value.__enter__.return_value = mock_context
        
        # Call card_container
        card_container(mock_content_func)
        
        # Verify container was created and content function was called
        mock_container.assert_called_once()
        mock_content_func.assert_called_once()
    
    @patch('streamlit.columns')
    @patch('streamlit.markdown')
    @patch('streamlit.checkbox')
    def test_toggle_switch(self, mock_checkbox, mock_markdown, mock_columns):
        """Test the toggle_switch function"""
        # Import here to avoid issues with early imports
        from utils.ui_helpers import toggle_switch
        
        # Mock columns and their behavior
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        # Mock checkbox behavior
        mock_checkbox.return_value = True
        
        # Call toggle_switch
        result = toggle_switch("Test Toggle", "test_key", default=False, help_text="Test help")
        
        # Verify results
        assert result is True  # The value of the checkbox
        mock_columns.assert_called_once()
        mock_checkbox.assert_called_once_with("", value=False, key="test_key", help="Test help")
        
        # Check that markdown was called in the first column
        mock_col1.__enter__.return_value.markdown.assert_called()
    
    @patch('streamlit.container')
    @patch('streamlit.toggle_switch')  # Mocking our own toggle_switch function
    def test_agent_card(self, mock_toggle_switch, mock_container):
        """Test the agent_card function"""
        # Import here to avoid issues with early imports
        from utils.ui_helpers import agent_card
        
        # Mock toggle_switch to return True
        mock_toggle_switch.return_value = True
        
        # Mock container context
        mock_context = MagicMock()
        mock_container.return_value.__enter__.return_value = mock_context
        
        # Call agent_card
        with patch('utils.ui_helpers.toggle_switch', mock_toggle_switch):  # Patch at import location
            result = agent_card("Test Agent", "Test description", "test_agent_key")
        
        # Verify results
        assert result is True  # The value returned by toggle_switch
        mock_container.assert_called_once()
        mock_toggle_switch.assert_called_once_with("Test Agent", "test_agent_key", 
                                                  default=False, help_text="Test description")