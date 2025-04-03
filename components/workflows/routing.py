import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_routing_section():
    """Render the Routing workflow configuration section"""

    st.markdown("### Routing Workflow")

    st.markdown("""
    Routing classifies an input and directs it to a specialized followup task. 
    This workflow allows for separation of concerns and building more specialized prompts, 
    optimizing for different input types.
    """)

    # Diagram
    st.image("https://via.placeholder.com/800x200?text=Routing+Workflow+Diagram",
             caption="Routing workflow showing classification and specialized handlers",
             use_column_width=True)

    # Enable/disable toggle
    routing_enabled = st.toggle("Enable Routing",
                                value=st.session_state.get("routing_enabled", False),
                                help="When enabled, inputs will be classified and routed to specialized handlers")
    st.session_state.routing_enabled = routing_enabled

    if routing_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Route configuration
            st.markdown("#### Route Configuration")

            # Initialize route list if not present
            if "routing_routes" not in st.session_state:
                st.session_state.routing_routes = [
                    {"name": "General Questions",
                     "description": "Common inquiries that don't require specialized knowledge", "enabled": True},
                    {"name": "Technical Support", "description": "Technical issues requiring specific domain expertise",
                     "enabled": True},
                    {"name": "Creative Requests", "description": "Requests for creative content or ideation",
                     "enabled": True}
                ]

            # Display and manage routes
            for i, route in enumerate(st.session_state.routing_routes):
                with st.container(border=True):
                    cols = st.columns([3, 1])
                    with cols[0]:
                        # Route information
                        route["name"] = st.text_input(f"Route {i + 1} Name", value=route["name"], key=f"route_name_{i}")
                        route["description"] = st.text_area(f"Description", value=route["description"],
                                                            key=f"route_desc_{i}", height=80)
                    with cols[1]:
                        # Route status and actions
                        route["enabled"] = st.checkbox("Enabled", value=route["enabled"], key=f"route_enabled_{i}")

                        # Models can be different for different routes
                        st.selectbox("Model", ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                                     key=f"route_model_{i}")

                        if i > 0 and st.button("Remove", key=f"remove_route_{i}"):
                            st.session_state.routing_routes.pop(i)
                            st.rerun()

            # Add route button
            if st.button("+ Add Route"):
                st.session_state.routing_routes.append({
                    "name": f"New Route {len(st.session_state.routing_routes) + 1}",
                    "description": "Description of this route",
                    "enabled": True
                })
                st.rerun()

        with col2:
            # Router configuration
            st.markdown("#### Router Configuration")

            st.selectbox(
                "Router Type",
                ["LLM Classifier", "Rule-based", "Hybrid", "External ML Model"],
                index=0,
                help="Method used to classify and route inputs"
            )

            st.selectbox(
                "Router Model",
                ["Claude 3.5 Haiku", "Custom Classifier", "Embedding-based"],
                index=0,
                help="Model used for input classification"
            )

            st.slider(
                "Classification Confidence Threshold",
                min_value=0.5,
                max_value=0.95,
                value=0.75,
                step=0.05,
                help="Minimum confidence required for classification"
            )

            st.checkbox(
                "Enable fallback route",
                value=True,
                help="Route to a default handler when classification confidence is below threshold"
            )

            st.checkbox(
                "Save routing decisions",
                value=True,
                help="Store routing decisions for later analysis and improvement"
            )

        # Example of how this workflow would be used
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of Routing workflow
def routing_workflow(input_query):
    # Step 1: Classify the input
    classification_prompt = f\"\"\"
    Classify the following query into one of these categories:
    - General Questions
    - Technical Support
    - Creative Requests

    Query: {input_query}

    Category:
    \"\"\"

    # Get the classification
    category = llm_call(classification_prompt).strip()

    # Step 2: Route to specialized handler
    if category == "General Questions":
        return handle_general_question(input_query)
    elif category == "Technical Support":
        return handle_technical_support(input_query)
    elif category == "Creative Requests":
        return handle_creative_request(input_query)
    else:
        # Fallback route
        return handle_default(input_query)
            """, language="python")

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Complex tasks with distinct categories that are better handled separately
            * Scenarios where input types require specialized prompting or different models
            * Systems handling a wide variety of user requests
            * Applications aiming to optimize cost by routing simpler queries to smaller models

            **Real-World Examples:**

            * Customer service systems routing different types of queries (general questions, refunds, technical support)
            * Content generation systems that handle different content types with specialized templates
            * Question answering systems that route factual vs. creative questions differently
            * Cost optimization by routing simple queries to smaller, faster models
            """)

            # Citation from the Anthropic article
            st.info("""
            *"Routing works well for complex tasks where there are distinct categories that are better handled separately, 
            and where classification can be handled accurately, either by an LLM or a more traditional classification 
            model/algorithm."*

            — Anthropic Engineering
            """)