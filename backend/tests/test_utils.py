import unittest
from app.utils import extract_variables, validate_prompt_content, search_prompts
from pydantic import BaseModel
from typing import Optional, List

class TestExtractVariables(unittest.TestCase):
    def test_extract_variables(self):
        # Test with multiple variables
        content = 'Hello, {{name}}! Your account {{account_number}} is active.'
        expected = ['name', 'account_number']
        result = extract_variables(content)
        self.assertEqual(result, expected)

        # Test with no variables
        content = 'Hello, World!'
        expected = []
        result = extract_variables(content)
        self.assertEqual(result, expected)

        # Test with variables with digits
        content = '{{var1}} and {{var2}}'
        expected = ['var1', 'var2']
        result = extract_variables(content)
        self.assertEqual(result, expected)

        # Test with complex content
        content = '{{name}}, your balance is {{balance}}. Date: {{date}}'
        expected = ['name', 'balance', 'date']
        result = extract_variables(content)
        self.assertEqual(result, expected)


class TestValidatePromptContent(unittest.TestCase):
    def test_validate_prompt_content(self):
        # Test with empty content
        self.assertFalse(validate_prompt_content(""))
        
        # Test with content that is only whitespace
        self.assertFalse(validate_prompt_content("   "))
        
        # Test with content less than 10 characters
        self.assertFalse(validate_prompt_content("short"))
        
        # Test with valid content
        self.assertTrue(validate_prompt_content("This is valid content."))

        # Test with content exactly 10 characters long
        self.assertTrue(validate_prompt_content("1234567890"))


# Assuming the Prompt class is something like this based on the error message
class Prompt(BaseModel):
    title: str
    description: Optional[str] = None
    content: str  # Adding the required content field

class TestSearchPrompts(unittest.TestCase):
    def setUp(self):
        self.prompts = [
            Prompt(title="Hello World", description="A classic programming example.", content="Sample content for Hello World"),
            Prompt(title="Goodbye World", description="An example of saying farewell.", content="Sample content for Goodbye World"),
            Prompt(title="Python Programming", description="Learn to code in Python.", content="Sample content for Python Programming"),
            Prompt(title="Data Science", description="Analyze data with Python.", content="Sample content for Data Science"),
        ]
    
    def test_search_in_empty_list(self):
        result = search_prompts([], "Python")
        self.assertEqual(result, [])

    def test_search_with_empty_query(self):
        result = search_prompts(self.prompts, "")
        self.assertEqual(result, self.prompts)
    
    def test_search_matching_title(self):
        result = search_prompts(self.prompts, "hello")
        self.assertEqual(result, [self.prompts[0]])
        
    def test_search_matching_description(self):
        result = search_prompts(self.prompts, "analyze")
        self.assertEqual(result, [self.prompts[3]])
    
    def test_search_no_matches(self):
        result = search_prompts(self.prompts, "java")
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()