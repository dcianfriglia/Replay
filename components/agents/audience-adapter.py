import streamlit as st
from utils.ui_helpers import section_header, subsection_header


def render_audience_adapter_agent():
    """Render the Audience Adapter Agent configuration section"""

    st.markdown("### Audience Adapter Agent")

    st.markdown("""
    The Audience Adapter Agent tailors content for specific audiences.
    This agent adjusts terminology, examples, and complexity to suit the target audience.
    """)

    # Enable/disable toggle
    audience_adapter_enabled = st.toggle("Enable Audience Adapter Agent",
                                        value=st.session_state.audience_adapter_enabled,
                                        help="When enabled, this agent will tailor content for specific audiences")
    st.session_state.audience_adapter_enabled = audience_adapter_enabled

    if audience_adapter_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Target audience
            subsection_header("Target Audience")

            audience_type = st.selectbox(
                "Primary audience type",
                ["General audience", "Technical professionals", "Business stakeholders", 
                 "Beginners/Novices", "Academic audience", "Custom audience"],
                index=0,
                key="audience_type"
            )

            if audience_type == "Custom audience":
                st.text_area(
                    "Describe custom audience",
                    value="",
                    height=100,
                    key="custom_audience_description"
                )
            else:
                # Show audience characteristics based on selection
                if audience_type == "Technical professionals":
                    st.multiselect(
                        "Technical domains",
                        ["Software development", "Engineering", "Healthcare",
                         "Finance", "Legal", "Education", "Science"],
                        default=["Software development"],
                        key="technical_domains"
                    )
                elif audience_type == "Business stakeholders":
                    st.multiselect(
                        "Business roles",
                        ["Executives", "Managers", "Analysts",
                         "Marketing", "Sales", "HR", "Operations"],
                        default=["Executives", "Managers"],
                        key="business_roles"
                    )
                elif audience_type == "Academic audience":
                    st.multiselect(
                        "Academic level",
                        ["Undergraduate", "Graduate", "PhD/Researchers",
                         "Faculty", "K-12 Educators"],
                        default=["Undergraduate"],
                        key="academic_level"
                    )

            # Audience characteristics
            subsection_header("Audience Characteristics")

            col_a, col_b = st.columns(2)
            
            with col_a:
                st.slider(
                    "Technical Knowledge",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Minimal, 5 = Expert",
                    key="audience_technical_knowledge"
                )
                
                st.slider(
                    "Attention Span",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Very short, 5 = Extended focus",
                    key="audience_attention_span"
                )
            
            with col_b:
                st.slider(
                    "Domain Familiarity",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Newcomer, 5 = Subject expert",
                    key="audience_domain_familiarity"
                )
                
                st.slider(
                    "Reading Level",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Basic, 5 = Academic/specialized",
                    key="audience_reading_level"
                )

            # Adaptation focus
            subsection_header("Adaptation Focus")

            adaptation_areas = st.multiselect(
                "Select areas to adapt",
                ["Terminology", "Examples/analogies", "Level of detail",
                 "Complexity", "Cultural context", "Visual elements"],
                default=["Terminology", "Examples/analogies", "Level of detail"],
                key="adaptation_areas"
            )

            # Instructions for Adapter
            subsection_header("Instructions for Adapter")

            st.text_area(
                "Provide specific instructions for this agent",
                value="Adapt content to suit the target audience by adjusting terminology, examples, and level of detail. Make complex concepts accessible without oversimplifying. Use relevant examples that resonate with the audience's context and experience. Maintain the core message while tailoring the presentation.",
                height=150,
                key="audience_adapter_instructions"
            )

        with col2:
            # Model selection
            subsection_header("Model Configuration")

            st.selectbox(
                "Model",
                ["Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude 3 Opus"],
                index=0,
                key="audience_adapter_model"
            )

            # Advanced settings
            subsection_header("Advanced Settings")

            st.checkbox(
                "Preserve core content",
                value=True,
                key="preserve_core_content",
                help="Ensure core information remains intact during adaptation"
            )

            st.checkbox(
                "Adapt content structure",
                value=True,
                key="adapt_structure",
                help="Reorganize content structure based on audience needs"
            )

            st.checkbox(
                "Adjust tone/style",
                value=True,
                key="adjust_tone",
                help="Modify tone and style to suit audience preferences"
            )

            st.checkbox(
                "Include audience-specific resources",
                value=False,
                key="audience_resources",
                help="Add references to resources relevant to the specific audience"
            )

            # Communication style
            subsection_header("Communication Style")
            
            st.select_slider(
                "Formality",
                options=["Casual", "Conversational", "Neutral", "Professional", "Academic"],
                value="Neutral",
                key="audience_formality"
            )
            
            st.select_slider(
                "Complexity",
                options=["Elementary", "Basic", "Moderate", "Advanced", "Technical"],
                value="Moderate",
                key="audience_complexity"
            )

        # Adaptation example
        with st.expander("Adaptation Examples", expanded=False):
            st.markdown("""
            #### Examples of Content Adaptation for Different Audiences

            **Original Content (Technical):**
            ```
            The system implements a distributed microservices architecture using containerized deployments orchestrated via Kubernetes. Service communication follows the CQRS pattern with event sourcing for state management, achieving eventual consistency across bounded contexts.
            ```

            **Adapted for Business Stakeholders:**
            ```
            The system uses a modern, flexible design that breaks functionality into small, independent services. This approach allows for easier updates, better reliability, and faster scaling when user demand increases. The design ensures all parts of the system stay synchronized, even during high-volume operations.
            ```

            **Adapted for Beginners:**
            ```
            The system is built using an approach called "microservices," which means we've divided it into smaller, more manageable parts that work together. Think of it like a restaurant where instead of one person doing everything, you have specialized roles—chefs, servers, and hosts—working together to create a smooth experience. This makes our system easier to maintain and expand as needed.
            ```

            **Adapted for General Audience:**
            ```
            The system uses a modern design where functionality is split into smaller, independent components. These components can be updated separately, making the system more reliable and easier to improve over time. This design ensures that all parts work together smoothly, even when many people are using the system at once.
            ```

            **Adapted for Academic Audience:**
            ```
            The implementation employs a distributed architecture leveraging containerized microservices orchestrated via Kubernetes. The system's communication paradigm adheres to Command Query Responsibility Segregation principles, while state management utilizes event sourcing methodologies. This approach facilitates eventual consistency across distinct bounded contexts, enabling robust scalability and fault tolerance.
            ```
            """)
            
            st.info("The Audience Adapter Agent adjusts terminology, examples, and complexity while preserving the core information. It considers the audience's technical knowledge, domain familiarity, and context to make content more accessible and relevant.")