# LLM Prompt Engineering Framework

A comprehensive Streamlit application for creating, testing, and optimizing prompts for Large Language Models (LLMs).

## Features

- **Building Blocks:** Define core prompt components including context, task definitions, input/output formats, examples, and evaluation criteria
- **Workflow Configuration:** Configure different prompt engineering techniques including Chain-of-Thought, Few-Shot Learning, and Retrieval-Augmented Generation
- **Agent-Based Design:** Define different "agents" for content creation, editing, fact-checking, and audience adaptation
- **Prompt Management:** Save, load, and share prompt templates
- **Content Generation:** Test prompts with LLM integration and evaluate results

## Project Structure

```
prompt_engineering_framework/
├── app.py                    # Main application entry point
├── styles/
│   └── main.css              # CSS styles for the application
├── utils/
│   ├── __init__.py
│   ├── state_management.py   # Session state initialization and management
│   └── template_manager.py   # Functions for saving and loading templates
├── components/
│   ├── __init__.py
│   ├── building_blocks.py    # Building Blocks tab implementation
│   ├── workflows.py          # Workflows tab implementation
│   ├── agents.py             # Agents tab implementation
│   ├── final_prompt.py       # Final Prompt tab implementation
│   └── content_display.py    # Generated content display component
└── models/
    ├── __init__.py
    └── prompt_generator.py   # Logic for generating prompts
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prompt-engineering-framework.git
cd prompt-engineering-framework
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

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

By default, the application includes a simulation of content generation. To connect to real LLM APIs:

1. Add your API keys to a `.env` file (see `.env.example`)
2. Modify the `generate_content` function in `models/prompt_generator.py` to call your preferred LLM API
3. Handle the API response and update the UI accordingly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.