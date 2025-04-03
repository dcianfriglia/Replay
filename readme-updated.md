# LLM Prompt Engineering Framework

A comprehensive application for creating, testing, and optimizing prompts for Large Language Models (LLMs). This framework provides a visual interface for constructing advanced prompts using best practices like Chain-of-Thought, Few-Shot Learning, and Retrieval-Augmented Generation.

![Prompt Engineering Framework](https://via.placeholder.com/800x400?text=Prompt+Engineering+Framework)

## Features

- **Building Blocks:** Define core prompt components including context, task definitions, input/output formats, examples, and evaluation criteria
- **Workflow Configuration:** Configure different prompt engineering techniques including Chain-of-Thought, Few-Shot Learning, and Retrieval-Augmented Generation
- **Agent-Based Design:** Define different "agents" for content creation, editing, fact-checking, and audience adaptation
- **Prompt Management:** Save, load, and share prompt templates
- **Content Generation:** Test prompts with LLM integration and evaluate results
- **State Persistence:** Save and load your complete application state
- **API Integration:** Connect to Anthropic's Claude models (expandable to other providers)

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prompt-engineering-framework.git
cd prompt-engineering-framework
```

2. Create an environment file:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your API keys

4. Start with Docker Compose:
```bash
docker-compose up -d
```

5. Open your browser and navigate to `http://localhost:8501`

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prompt-engineering-framework.git
cd prompt-engineering-framework
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Create an environment file:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your API keys

6. Run the application:
```bash
streamlit run app.py
```

7. Open your browser and navigate to `http://localhost:8501`

## Development Mode

For development purposes, you can run the application in development mode:

```bash
streamlit run dev_app.py
```

This provides additional debugging tools and information to help during development.

## Usage Guide

### Building Blocks Tab

In this tab, define the foundational elements of your prompt:

1. **Context & Background:** Provide domain knowledge and relevant context for the LLM
2. **Task Definition:** Clearly define what you want the LLM to accomplish
3. **Input/Output Format:** Specify how data will be structured
4. **Examples & Constraints:** Add few-shot examples and define limitations
5. **Evaluation Criteria:** Set metrics to assess output quality

### Workflows Tab

Configure different prompt engineering techniques:

1. **Chain-of-Thought:** Break complex tasks into logical steps for better reasoning
2. **Iterative Refinement:** Gradually improve output through multiple generations
3. **Few-Shot Learning:** Use examples to guide the model's understanding
4. **Retrieval-Augmented Generation:** Enhance responses with external knowledge
5. **Self-Consistency Checking:** Validate outputs against multiple reasoning paths
6. **Routing:** Direct inputs to specialized handlers based on type
7. **Parallelization:** Process multiple aspects of a task simultaneously
8. **Orchestrator-Workers:** Dynamically break down and delegate complex tasks
9. **Evaluator-Optimizer:** Evaluate and iteratively improve content quality

### Agents Tab

Define specialized "agents" for different aspects of content creation:

1. **Content Creator:** Primary agent responsible for generating content
2. **Editor/Refiner:** Improves style, clarity, and coherence
3. **Fact Checker:** Verifies factual accuracy of generated content
4. **Critic/Evaluator:** Assesses content against predefined criteria
5. **Audience Adapter:** Tailors content for specific audiences

### Final Prompt Tab

1. **Prompt Structure:** Customize which sections to include in the final prompt
2. **Generated Prompt:** Preview the assembled prompt
3. **Actions:** Download the prompt, edit it directly, or generate content

## LLM Integration

The application supports direct integration with Anthropic's Claude models. To use this feature:

1. Obtain an API key from [Anthropic](https://www.anthropic.com/)
2. Add your API key to the `.env` file or enter it in the application UI
3. Toggle "Use LLM API" when generating content

## Session & Template Management

### Saving and Loading Sessions

You can save your entire application state and load it later:

1. Use the "Save State" button in the header or sidebar
2. Name your session for easy reference
3. Use "Load State" to restore a previous session

### Templates

Templates allow you to save and reuse specific prompt configurations:

1. Configure your prompt components
2. Select "+ Save Current as Template" from the Templates dropdown
3. Load previously saved templates from the same dropdown

## Project Structure

```
prompt_engineering_framework/
├── app.py                    # Main application entry point
├── dev_app.py                # Development version with debugging tools
├── styles/
│   └── main.css              # CSS styles for the application
├── utils/
│   ├── state_management.py   # Session state initialization
│   ├── state_persistence.py  # Save/load functionality
│   ├── template_manager.py   # Template management
│   └── ui_helpers.py         # UI helper functions
├── components/
│   ├── building_blocks/      # Building Blocks tab components
│   ├── workflows/            # Workflow configuration components
│   ├── agents/               # Agent configuration components
│   ├── final_prompt/         # Final prompt tab components
│   └── content_display/      # Content display components
├── models/
│   ├── prompt_generator.py   # Logic for generating prompts
│   └── content_generator.py  # Logic for generating content (LLM API)
└── tests/                    # Unit and integration tests
```

## Testing

Refer to the [Testing Guide](README_TESTING.md) for information on running and writing tests.

## Contributing

Contributions are welcome! Please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Inspired by research on prompt engineering techniques from [Anthropic](https://www.anthropic.com/), [OpenAI](https://openai.com/), and other AI labs
- Built with [Streamlit](https://streamlit.io/)