import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_parallelization_section():
    """Render the Parallelization workflow configuration section"""

    st.markdown("### Parallelization Workflow")

    st.markdown("""
    Parallelization allows multiple LLM instances to work simultaneously on different aspects 
    of a task, with their outputs aggregated programmatically. This workflow has two key variations:

    1. **Sectioning**: Breaking a task into independent subtasks that can be run in parallel
    2. **Voting**: Running the same task multiple times to get diverse outputs
    """)

    # Diagram
    st.image("https://via.placeholder.com/800x200?text=Parallelization+Workflow+Diagram",
             caption="Parallelization workflow showing multiple parallel LLM calls with aggregation",
             use_column_width=True)

    # Enable/disable toggle
    parallel_enabled = st.toggle("Enable Parallelization",
                                 value=st.session_state.get("parallelization_enabled", False),
                                 help="When enabled, tasks will be broken down or repeated for parallel processing")
    st.session_state.parallelization_enabled = parallel_enabled

    if parallel_enabled:
        # Parallelization type selector
        parallel_type = st.radio(
            "Parallelization Type",
            ["Sectioning (Different Subtasks)", "Voting (Same Task, Multiple Runs)"],
            horizontal=True,
            help="Choose how to parallelize your task"
        )

        # Store the selection
        st.session_state.parallelization_type = parallel_type

        # Different UI based on parallelization type
        if parallel_type == "Sectioning (Different Subtasks)":
            render_sectioning_configuration()
        else:  # Voting
            render_voting_configuration()

        # Common aggregation settings
        st.markdown("#### Aggregation Configuration")

        aggregation_method = st.selectbox(
            "Aggregation Method",
            ["Programmatic Merge", "LLM Synthesis", "Hierarchical Aggregation", "Rule-based"],
            index=1,
            help="How to combine the results from parallel operations"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Maximum Parallel Calls",
                min_value=2,
                max_value=10,
                value=3,
                help="Maximum number of parallel LLM calls to make"
            )

        with col2:
            st.checkbox(
                "Handle failures gracefully",
                value=True,
                help="Continue processing if some parallel calls fail"
            )

        # Example of how this workflow would be used
        with st.expander("Example Implementation", expanded=False):
            if parallel_type == "Sectioning (Different Subtasks)":
                st.code("""
# Example Python implementation of Sectioning Parallelization
async def sectioning_parallel_workflow(input_text, sections):
    # Create tasks for each section
    tasks = []
    for section in sections:
        prompt = f\"\"\"
        Process the following for section: {section['name']}

        Instructions: {section['instructions']}

        Input: {input_text}
        \"\"\"

        # Add task to list
        tasks.append(async_llm_call(prompt))

    # Run all tasks in parallel and wait for results
    section_results = await asyncio.gather(*tasks)

    # Aggregate results
    aggregation_prompt = f\"\"\"
    Combine the following section outputs into a cohesive response:

    {format_section_results(section_results, sections)}
    \"\"\"

    final_result = llm_call(aggregation_prompt)

    return final_result
                """, language="python")
            else:  # Voting
                st.code("""
# Example Python implementation of Voting Parallelization
async def voting_parallel_workflow(input_text, num_votes=3):
    # Create multiple identical tasks
    tasks = []
    for i in range(num_votes):
        prompt = f\"\"\"
        Evaluate the following input and provide your assessment:

        Input: {input_text}

        Respond with 'YES' or 'NO' with a brief explanation.
        \"\"\"

        # Add task to list
        tasks.append(async_llm_call(prompt))

    # Run all tasks in parallel and wait for results
    vote_results = await asyncio.gather(*tasks)

    # Count votes
    yes_votes = sum(1 for result in vote_results if 'YES' in result.upper())

    # Determine outcome
    decision = yes_votes > (num_votes / 2)

    return {
        'decision': decision,
        'yes_votes': yes_votes,
        'total_votes': num_votes,
        'vote_details': vote_results
    }
                """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Tasks that can be naturally divided into independent components
            * Scenarios requiring consensus or voting from multiple perspectives
            * Applications where parallel processing can reduce latency
            * Complex tasks with multiple considerations that benefit from focused attention

            **Real-World Examples:**

            * Content moderation with multiple LLMs evaluating different aspects or voting
            * Document analysis where different sections are processed in parallel
            * Code review where different LLMs check for different types of issues
            * Creativity tasks where multiple perspectives are aggregated
            """)

            # Citation from the Anthropic article
            st.info("""
            *"Parallelization is effective when the divided subtasks can be parallelized for speed, 
            or when multiple perspectives or attempts are needed for higher confidence results. 
            For complex tasks with multiple considerations, LLMs generally perform better when each 
            consideration is handled by a separate LLM call."*

            — Anthropic Engineering
            """)


def render_sectioning_configuration():
    """Render configuration options for sectioning parallelization"""

    st.markdown("#### Sectioning Configuration")

    # Initialize section list if not present
    if "parallelization_sections" not in st.session_state:
        st.session_state.parallelization_sections = [
            {"name": "Content Analysis", "instructions": "Analyze the factual content and accuracy",
             "model": "Claude 3.5 Sonnet"},
            {"name": "Style Evaluation", "instructions": "Evaluate the writing style and tone",
             "model": "Claude 3.5 Haiku"},
            {"name": "Structure Review", "instructions": "Review the organizational structure",
             "model": "Claude 3.5 Sonnet"}
        ]

    # Display and manage sections
    for i, section in enumerate(st.session_state.parallelization_sections):
        with st.container(border=True):
            cols = st.columns([1, 2, 1])

            with cols[0]:
                section["name"] = st.text_input(f"Section {i + 1} Name", value=section["name"], key=f"section_name_{i}")

            with cols[1]:
                section["instructions"] = st.text_area("Instructions", value=section["instructions"],
                                                       key=f"section_instr_{i}", height=80)

            with cols[2]:
                section["model"] = st.selectbox("Model", ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                                                key=f"section_model_{i}", index=0)

                if i > 0 and st.button("Remove", key=f"remove_section_{i}"):
                    st.session_state.parallelization_sections.pop(i)
                    st.rerun()

    # Add section button
    if st.button("+ Add Section"):
        st.session_state.parallelization_sections.append({
            "name": f"New Section {len(st.session_state.parallelization_sections) + 1}",
            "instructions": "Instructions for this section",
            "model": "Claude 3.5 Sonnet"
        })
        st.rerun()


def render_voting_configuration():
    """Render configuration options for voting parallelization"""

    st.markdown("#### Voting Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.number_input(
            "Number of Votes",
            min_value=3,
            max_value=9,
            value=5,
            step=2,  # Odd numbers preferred for voting
            help="Number of independent LLM calls for voting"
        )

        st.slider(
            "Confidence Threshold",
            min_value=50,
            max_value=100,
            value=60,
            format="%d%%",
            help="Percentage of votes required for a positive decision"
        )

    with col2:
        st.selectbox(
            "Voting Strategy",
            ["Majority Vote", "Weighted Vote", "Unanimous Consent", "Threshold-based"],
            index=0,
            help="Strategy for determining the final outcome"
        )

        st.checkbox(
            "Include vote explanations",
            value=True,
            help="Include explanations from each voter in the final result"
        )

        st.checkbox(
            "Use diverse prompting",
            value=True,
            help="Use slightly different prompts for each voter to increase diversity of perspectives"
        )