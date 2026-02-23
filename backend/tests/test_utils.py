"""Tests for utility functions"""

import pytest
from app.models import Prompt
from app.utils import validate_prompt_content, extract_variables


class TestValidatePromptContent:
    """Tests for validate_prompt_content function."""
    
    def test_valid_content(self):
        assert validate_prompt_content("This is valid content") is True
    
    def test_empty_content(self):
        assert validate_prompt_content("") is False
    
    def test_whitespace_only(self):
        assert validate_prompt_content("   ") is False
    
    def test_too_short(self):
        assert validate_prompt_content("short") is False


class TestExtractVariables:
    """Tests for extract_variables function."""
    
    def test_extract_single_variable(self):
        content = "Hello {{name}}"
        assert extract_variables(content) == ["name"]
    
    def test_extract_multiple_variables(self):
        content = "{{greeting}} {{name}}, your code: {{code}}"
        assert extract_variables(content) == ["greeting", "name", "code"]
    
    def test_no_variables(self):
        content = "No variables here"
        assert extract_variables(content) == []
