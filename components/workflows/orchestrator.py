import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_orchestrator_section():
    """Render the Orchestrator-Workers workflow configuration section"""

    st.markdown("### Orchestrator-Workers Workflow")

    st.markdown("""
    In the Orchestrator-Workers workflow, a central LLM dynamically breaks down tasks, 
    delegates them to worker LLMs, and synthesizes their results. This pattern provides
    flexibility for complex tasks where subtasks can't be predefined.
    """)

    # Diagram
    st.image("https://via.placeholder.com/800x200?text=Orchestrator-Workers+Workflow+Diagram",
             caption="Orchestrator-Workers workflow showing dynamic task delegation",
             use_column_width=True)

    # Enable/disable toggle
    orchestrator_enabled = st.toggle("Enable Orchestrator-Workers",
                                     value=st.session_state.get("orchestrator_enabled", False),
                                     help="When enabled, tasks will be dynamically broken down and delegated")
    st.session_state.orchestrator_enabled = orchestrator_enabled

    if orchestrator_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Orchestrator configuration
            st.markdown("#### Orchestrator Configuration")

            st.selectbox(
                "Orchestrator Model",
                ["Claude 3.5 Sonnet", "Claude 3 Opus", "Custom Orchestrator"],
                index=1,
                help="Model used for task orchestration (should be highly capable)"
            )

            st.text_area(
                "Orchestrator Instructions",
                value="Analyze the input, break it down into subtasks, delegate to appropriate workers, and synthesize results.",
                height=100,
                help="Instructions for the orchestrator on how to break down and delegate tasks"
            )

            # Worker configuration
            st.markdown("#### Worker Configuration")

            # Initialize worker list if not present
            if "orchestrator_workers" not in st.session_state:
                st.session_state.orchestrator_workers = [
                    {"name": "Research Worker", "skills": "Information gathering, data analysis",
                     "model": "Claude 3.5 Sonnet"},
                    {"name": "Content Writer", "skills": "Content creation, formatting, style",
                     "model": "Claude 3.5 Sonnet"},
                    {"name": "Technical Expert", "skills": "Technical analysis, code generation",
                     "model": "Claude 3.5 Sonnet"}
                ]

            # Display and manage workers
            for i, worker in enumerate(st.session_state.orchestrator_workers):
                with st.container(border=True):
                    cols = st.columns([1, 2, 1])

                    with cols[0]:
                        worker["name"] = st.text_input(f"Worker {i + 1} Name", value=worker["name"],
                                                       key=f"worker_name_{i}")

                    with cols[1]:
                        worker["skills"] = st.text_area("Skills/Specialization", value=worker["skills"],
                                                        key=f"worker_skills_{i}", height=80)

                    with cols[2]:
                        worker["model"] = st.selectbox("Model",
                                                       ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                                                       key=f"worker_model_{i}", index=0)

                        if i > 0 and st.button("Remove", key=f"remove_worker_{i}"):
                            st.session_state.orchestrator_workers.pop(i)
                            st.rerun()

            # Add worker button
            if st.button("+ Add Worker"):
                st.session_state.orchestrator_workers.append({
                    "name": f"New Worker {len(st.session_state.orchestrator_workers) + 1}",
                    "skills": "Describe worker skills and specialization",
                    "model": "Claude 3.5 Sonnet"
                })
                st.rerun()

        with col2:
            # Synthesis configuration
            st.markdown("#### Synthesis Configuration")

            st.selectbox(
                "Synthesis Method",
                ["Orchestrator Synthesis", "Dedicated Synthesizer", "Hierarchical Synthesis"],
                index=0,
                help="How to synthesize worker outputs"
            )

            st.checkbox(
                "Allow worker collaboration",
                value=True,
                help="Allow workers to communicate with each other"
            )

            st.checkbox(
                "Dynamic worker allocation",
                value=True,
                help="Allow orchestrator to dynamically determine required workers"
            )

            st.number_input(
                "Maximum Workers Per Task",
                min_value=2,
                max_value=10,
                value=5,
                help="Maximum number of workers that can be assigned"
            )

            st.markdown("#### Process Controls")

            st.slider(
                "Max Orchestration Depth",
                min_value=1,
                max_value=5,
                value=2,
                help="Maximum depth of nested orchestration"
            )

            st.checkbox(
                "Intermediate Review",
                value=True,
                help="Allow human review of subtasks before synthesis"
            )

            st.checkbox(
                "Task Caching",
                value=True,
                help="Cache subtask results for reuse"
            )

        # Example of how this workflow would be used
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of Orchestrator-Workers workflow
async def orchestrator_workers_workflow(input_text, available_workers):
    # Step 1: Orchestrator breaks down the task
    orchestration_prompt = f\"\"\"
    Analyze the following task and break it down into subtasks.
    Assign each subtask to the most appropriate worker based on their skills.

    Task: {input_text}

    Available workers and their skills:
    {format_workers(available_workers)}

    Return a JSON with subtasks and worker assignments.
    \"\"\"

    # Get the orchestration plan
    orchestration_result = llm_call(orchestration_prompt)
    subtasks = parse_orchestration_result(orchestration_result)

    # Step 2: Execute worker tasks in parallel
    worker_tasks = []
    for subtask in subtasks:
        worker = get_worker(subtask["worker_id"], available_workers)

        worker_prompt = f\"\"\"
        You are the {worker['name']} with skills in {worker['skills']}.

        Task: {subtask['task_description']}

        Provide your result based on your specialization.
        \"\"\"

        # Add task to list
        worker_tasks.append({
            "task_id": subtask["task_id"],
            "future": async_llm_call(worker_prompt, model=worker["model"])
        })

    # Execute all worker tasks
    worker_results = {}
    for task in worker_tasks:
        worker_results[task["task_id"]] = await task["future"]

    # Step 3: Synthesize results
    synthesis_prompt = f\"\"\"
    Synthesize the following worker results into a cohesive final result:

    Original task: {input_text}

    Worker results:
    {format_worker_results(worker_results, subtasks)}
    \"\"\"

    final_result = llm_call(synthesis_prompt)

    return final_result
            """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Complex tasks where you can't predict the subtasks needed
            * Projects requiring diverse specialized knowledge
            * Tasks where subtasks need to be determined dynamically
            * Situations where flexibility in execution is important

            **Real-World Examples:**

            * Coding projects that involve changes to multiple files based on requirements
            * Research tasks gathering information from multiple sources
            * Complex content creation requiring specialized knowledge in different areas
            * Project planning with dynamic allocation of resources
            """)

            # Citation from the Anthropic article
            st.info("""
            *"This workflow is well-suited for complex tasks where you can't predict the subtasks needed. 
            The key difference from parallelization is its flexibility—subtasks aren't pre-defined, but 
            determined by the orchestrator based on the specific input."*

            — Anthropic Engineering
            """)