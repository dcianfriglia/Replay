import streamlit as st


def generate_prompt():
    """
    Generate a formatted prompt based on the selected components in session state

    Returns:
        str: The formatted prompt text
    """
    prompt = ""

    # Context & Background
    if st.session_state.prompt_structure["Context & Background"] and st.session_state.context:
        prompt += "# Context & Background\n"
        prompt += st.session_state.context + "\n\n"

    # Task Definition
    if st.session_state.prompt_structure["Task Definition"] and st.session_state.task:
        prompt += "# Task Definition\n"
        prompt += st.session_state.task + "\n\n"

    # Content Intent & Guidelines (new section)
    if st.session_state.prompt_structure.get("Content Intent & Guidelines", False):
        prompt += "# Content Intent & Guidelines\n"
        prompt += f"**Intent:** {st.session_state.content_intent}\n\n"
        prompt += f"**Mission Statement:** {st.session_state.mission_statement}\n\n"
        prompt += f"**Voice & Tone:** {st.session_state.voice_choice}\n\n"

        if hasattr(st.session_state, "content_rules") and st.session_state.content_rules:
            prompt += "**Content Rules (Do NOT include):**\n"
            for rule in st.session_state.content_rules:
                prompt += f"- {rule}\n"
            prompt += "\n"

    # Content Setup (new section)
    if st.session_state.prompt_structure.get("Content Setup", False):
        prompt += "# Content Setup\n"
        prompt += f"**Content Description:** {st.session_state.content_description}\n\n"
        prompt += "**Business Context:**\n"
        prompt += f"- Name: {st.session_state.business_name}\n"
        prompt += f"- Display Location: {st.session_state.business_where}\n"
        prompt += f"- Target Audience: {st.session_state.business_who}\n"
        prompt += f"- Content Format: {st.session_state.business_look}\n"
        prompt += f"- Purpose: {st.session_state.business_why}\n\n"

    # Design Requirements (new section)
    if st.session_state.prompt_structure.get("Design Requirements", False):
        prompt += "# Design Requirements\n"

        if hasattr(st.session_state, "components") and st.session_state.components:
            prompt += "**Content Components:**\n"
            for component in st.session_state.components:
                prompt += f"- {component['type']}: {component['description']}\n"
                prompt += f"  Length: {component['min_chars']}-{component['max_chars']} chars, ~{component['sentences']} sentences\n"
            prompt += "\n"

        prompt += f"**Language & Locale:** {st.session_state.language_choice}\n\n"

        if hasattr(st.session_state, "globalization_items") and st.session_state.globalization_items:
            prompt += "**Globalization Considerations:**\n"
            for item in st.session_state.globalization_items:
                prompt += f"- {item}\n"
            prompt += "\n"

    # Data Sources & Examples (new section)
    if st.session_state.prompt_structure.get("Data Sources & Examples", False):
        prompt += "# Data Sources & Examples\n"

        # Add file mappings if available
        if hasattr(st.session_state, "file_mappings") and st.session_state.file_mappings:
            prompt += "**Data Fields:**\n"
            for mapping in st.session_state.file_mappings:
                prompt += f"- {mapping['placeholder']}: Corresponds to {mapping['field']} in the provided data\n"
            prompt += "\n"

        # Add GraphQL mappings if available
        if hasattr(st.session_state, "graphql_mappings") and st.session_state.graphql_mappings:
            prompt += "**GraphQL Data Fields:**\n"
            for mapping in st.session_state.graphql_mappings:
                prompt += f"- {mapping['placeholder']}: Corresponds to {mapping['field']} in the GraphQL data\n"
            prompt += "\n"

        # Add manual examples if available
        if hasattr(st.session_state, "manual_examples") and st.session_state.manual_examples:
            prompt += "**Examples for Reference:**\n"
            for i, example in enumerate(st.session_state.manual_examples):
                prompt += f"Example {i + 1} ({example['comment']}):\n```\n{example['text']}\n```\n\n"

    # Input Data Format
    if st.session_state.prompt_structure["Input Data Format"] and st.session_state.input_description:
        prompt += "# Input Data Format\n"
        prompt += f"Format: {st.session_state.input_format}\n"
        prompt += st.session_state.input_description + "\n\n"

    # Output Requirements
    if st.session_state.prompt_structure["Output Requirements"]:
        prompt += "# Output Requirements\n"
        prompt += f"Format: {st.session_state.output_format}\n"
        prompt += f"Tone: {st.session_state.output_tone}\n"
        if st.session_state.output_requirements:
            prompt += st.session_state.output_requirements + "\n\n"
        else:
            prompt += "\n"

    # Examples (Few-Shot Learning)
    if st.session_state.prompt_structure["Examples (Few-Shot Learning)"] and st.session_state.few_shot_enabled:
        prompt += "# Examples & Constraints\n"
        for i, example in enumerate(st.session_state.examples):
            if example["input"] or example["output"]:
                prompt += f"[Example {i + 1}]\n"
                prompt += f"Input: {example['input']}\n"
                prompt += f"Output: {example['output']}\n\n"

        # Constraints
        if st.session_state.constraints:
            prompt += "## Constraints\n"
            prompt += st.session_state.constraints + "\n\n"

    # Chain-of-Thought Instructions
    if st.session_state.prompt_structure["Chain-of-Thought Instructions"] and st.session_state.thinking_steps_enabled:
        prompt += "## Chain-of-Thought Instructions\n"
        for i, step in enumerate(st.session_state.chain_of_thought_steps):
            prompt += f"{i + 1}. {step}\n"
        prompt += "\n"

    # Self-Review Requirements
    if st.session_state.prompt_structure["Self-Review Requirements"] and st.session_state.self_consistency_enabled:
        prompt += "## Self-Review Requirements\n"
        prompt += "After generating content, review it to ensure:\n"
        prompt += "- All claims are factually accurate\n"
        prompt += "- Content is well-organized and flows logically\n"
        prompt += "- Advice is practical and actionable\n"
        prompt += "- Language is clear and professional\n"
        prompt += "- Content follows specified output requirements\n\n"

    # Fact Checking Instructions
    if st.session_state.prompt_structure["Fact Checking Instructions"] and st.session_state.fact_checker_enabled:
        prompt += "## Fact Checking Instructions\n"
        prompt += "Verify all factual claims and ensure accuracy of:\n"
        prompt += "- Statistics and numerical data\n"
        prompt += "- Historical information\n"
        prompt += "- Technical specifications\n"
        prompt += "- Citations and references\n\n"

    return prompt


def generate_content_with_data_injection(prompt):
    """
    Replace placeholders in the prompt with actual data values

    Args:
        prompt (str): The prompt template with placeholders

    Returns:
        str: The prompt with placeholders replaced by actual data
    """
    processed_prompt = prompt

    # Process file mappings if available
    if hasattr(st.session_state,
               "file_mappings") and st.session_state.file_mappings and st.session_state.uploaded_file_data is not None:
        data = st.session_state.uploaded_file_data

        for mapping in st.session_state.file_mappings:
            field = mapping["field"]
            placeholder = mapping["placeholder"]

            if isinstance(data, dict) and field in data:
                # JSON dictionary
                processed_prompt = processed_prompt.replace(f"{{{{{placeholder}}}}}", str(data[field]))

            elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and field in data[0]:
                # JSON list of dictionaries (use first item)
                processed_prompt = processed_prompt.replace(f"{{{{{placeholder}}}}}", str(data[0][field]))

            elif hasattr(data, "columns") and field in data.columns:
                # DataFrame
                processed_prompt = processed_prompt.replace(f"{{{{{placeholder}}}}}", str(data[field].iloc[0]))

    # Process GraphQL mappings if available
    if hasattr(st.session_state,
               "graphql_mappings") and st.session_state.graphql_mappings and st.session_state.graphql_results is not None:
        data = st.session_state.graphql_results

        for mapping in st.session_state.graphql_mappings:
            field_path = mapping["field"].split(".")
            placeholder = mapping["placeholder"]

            # Navigate through the nested data structure
            current_data = data
            try:
                for part in field_path:
                    if part and current_data is not None:
                        if isinstance(current_data, dict) and part in current_data:
                            current_data = current_data[part]
                        elif isinstance(current_data, list) and len(current_data) > 0:
                            current_data = current_data[0]  # Take first item from list
                            if isinstance(current_data, dict) and part in current_data:
                                current_data = current_data[part]
                            else:
                                current_data = None
                                break
                        else:
                            current_data = None
                            break

                if current_data is not None:
                    processed_prompt = processed_prompt.replace(f"{{{{{placeholder}}}}}", str(current_data))
            except:
                pass  # Skip if field path is invalid

    return processed_prompt


def simulate_content_generation():
    """
    Simulate generating content from a prompt (to be replaced with actual LLM API calls)

    Returns:
        str: The generated content
    """
    # This is a placeholder for actual LLM API integration
    return """## Implementing Agile in Software Development

Agile methodologies have revolutionized software development by emphasizing iterative progress, team collaboration, and customer feedback. This guide will help you understand and implement Agile practices in your organization.

### Understanding Agile Foundations

At its core, Agile is built on four key values from the Agile Manifesto:
1. Individuals and interactions over processes and tools
2. Working software over comprehensive documentation
3. Customer collaboration over contract negotiation
4. Responding to change over following a plan

### Key Agile Methodologies

#### Scrum
Scrum is the most widely used Agile framework, featuring:
- Sprint planning, daily standups, sprint reviews, and retrospectives
- Defined roles: Product Owner, Scrum Master, Development Team
- Artifacts: Product Backlog, Sprint Backlog, Increment

#### Kanban
Kanban focuses on visualizing workflow and limiting work in progress:
- Visual board with columns representing stages of work
- Work items move across the board as they progress
- Focus on limiting WIP to identify bottlenecks

### Implementing Agile in Your Team

1. **Start with a pilot project**
   Choose a small, non-critical project to test Agile practices.

2. **Build your Agile team**
   Focus on cross-functional skills and collaborative mindset.

3. **Establish ceremonies**
   Implement daily standups, sprint planning, reviews, and retrospectives.

4. **Create and manage your backlog**
   Prioritize features based on business value and customer needs.

5. **Measure and improve**
   Use velocity, lead time, and other metrics to track progress.

### Overcoming Common Challenges

- **Resistance to change**: Provide training and emphasize benefits
- **Scope creep**: Maintain a disciplined backlog management process
- **Distributed teams**: Leverage collaboration tools and establish clear communication channels

### Measuring Success

Track these metrics to evaluate your Agile implementation:
- Team velocity and predictability
- Product quality (defect rates)
- Time to market
- Customer satisfaction
- Team morale and engagement

By following these guidelines, your team can successfully adopt Agile methodologies and realize the benefits of increased flexibility, faster delivery, and higher quality software.
"""


def calculate_quality_metrics(content):
    """
    Calculate quality metrics for the generated content

    Args:
        content (str): The generated content

    Returns:
        dict: Dictionary containing quality metrics
    """
    # This is a placeholder for actual content quality evaluation
    return {
        "Relevance": 92,
        "Accuracy": 88,
        "Completeness": 85,
        "Clarity": 90,
        "Actionability": 94
    }