# GitHub Copilot Instructions

Welcome to the project! This guide is designed to help AI agents and developers efficiently navigate the codebase and workflow, ensuring consistent and high-quality contributions.

## Project Overview

This project is an AI Prompt Engineering Platform built using FastAPI. It allows users to manage AI prompts and collections, providing a robust backend service for AI developers.

## Contribution Guidelines

- **Coding Standards**: Follow PEP 8 for Python code. Use meaningful variable names and include type hints where applicable.
- **Docstrings**: Use Google-style docstrings for function and class documentation to ensure clarity and consistency across the codebase.
- **Testing**: Write unit tests for all new features and bug fixes. Tests should be placed in the `tests/` directory.

## AI Agent Guidance

### Understanding Context
- Focus on understanding the architectural decisions and the modular setup of the project. Recognize the separation of backend API logic and future frontend integration.

### Custom Instructions
- When adding new endpoints or features, ensure they are fully documented in `API_REFERENCE.md`.
- For any front-end related decisions, consider the placeholder nature of the current setup and plan for scalable UI interactions in a future tech stack (e.g., React or Vue.js).

### Error Handling
- Implement comprehensive error handling for all endpoints. Use HTTP status codes appropriately and provide clear error messages in JSON format.

### Collaboration
- Use pull requests for all code changes with detailed descriptions of the changes made, linked to relevant issues when possible.
- Encourage code reviews from peers to maintain code quality and share knowledge.

## Automation and CI/CD

- The project uses a CI/CD pipeline for testing and deployment. Ensure that all tests pass before merging code into the main branch.

## Security Best Practices

- Regularly update dependencies to protect against vulnerabilities.
- Review and follow best practices for secure coding, particularly when handling user input and API requests/responses.

## Seeking Assistance

If you have questions or need further guidance, feel free to reach out to the project maintainers or open an issue for discussion. We're here to support a collaborative and innovative development environment.