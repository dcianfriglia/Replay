import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_content_intent_section():
    """Render the Content Intent & Guidelines section"""
    with st.container(border=True):
        section_with_info(
            "Content Intent & Guidelines",
            "Define the purpose and guidelines for content generation"
        )

        # Content Intent
        subsection_header("Content Intent")

        # Initialize intent in session state if not present
        if "content_intent" not in st.session_state:
            st.session_state.content_intent = "Inform"

        intent_options = [
            "Inform", "Explain", "Persuade", "Entertain",
            "Instruct", "Inspire", "Compare", "Summarize"
        ]

        selected_intent = st.selectbox(
            "What is the intent of the content?",
            intent_options,
            index=intent_options.index(st.session_state.content_intent),
            key="content_intent_select",
            on_change=lambda: setattr(st.session_state, "content_intent", st.session_state.content_intent_select)
        )

        # Mission Statement
        subsection_header("Content Mission Statement")

        # Initialize mission statement if not present
        if "mission_statement" not in st.session_state:
            mission_template = f"This content aims to {selected_intent.lower()} the audience about [topic] by providing [specific value]. It will help readers to [desired outcome]."
            st.session_state.mission_statement = mission_template

        mission_statement = st.text_area(
            "Define the purpose and goals of the content",
            value=st.session_state.mission_statement,
            height=100,
            key="mission_statement_input",
            on_change=lambda: setattr(st.session_state, "mission_statement", st.session_state.mission_statement_input)
        )

        # Voice & Tone
        subsection_header("Voice & Tone")

        # Initialize voice choice if not present
        if "voice_choice" not in st.session_state:
            st.session_state.voice_choice = "Professional"

        voice_options = [
            "Professional", "Conversational", "Academic", "Technical",
            "Enthusiastic", "Empathetic", "Authoritative", "Casual"
        ]

        selected_voice = st.selectbox(
            "Select the voice for your content",
            voice_options,
            index=voice_options.index(st.session_state.voice_choice),
            key="voice_choice_select",
            on_change=lambda: setattr(st.session_state, "voice_choice", st.session_state.voice_choice_select)
        )

        # Content Rules
        subsection_header("Content Rules & Restrictions")

        # Initialize rules list if not present
        if "content_rules" not in st.session_state:
            st.session_state.content_rules = []

        # Display existing rules
        if st.session_state.content_rules:
            st.markdown("Current rules for what should NOT be included:")
            for i, rule in enumerate(st.session_state.content_rules):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(f"- {rule}")
                with col2:
                    if st.button("×", key=f"remove_rule_{i}"):
                        st.session_state.content_rules.pop(i)
                        st.rerun()

        # Add new rule
        new_rule = st.text_input(
            "Add a rule for what should not be included",
            key="new_rule_input"
        )

        if st.button("+ Add Rule", key="add_rule_btn"):
            if new_rule and new_rule not in st.session_state.content_rules:
                st.session_state.content_rules.append(new_rule)
                st.rerun()


def render_content_setup_section():
    """Render the Content Setup section"""
    with st.container(border=True):
        section_with_info(
            "Content Setup",
            "Define what content is being generated and its business context"
        )

        # Content Description
        subsection_header("Content Description")

        # Initialize content description if not present
        if "content_description" not in st.session_state:
            st.session_state.content_description = ""

        content_description = st.text_area(
            "Provide a short description of the content to be generated",
            value=st.session_state.content_description,
            height=100,
            key="content_description_input",
            help="Example: Product description for an e-commerce website",
            on_change=lambda: setattr(st.session_state, "content_description",
                                      st.session_state.content_description_input)
        )

        # Business Context
        subsection_header("Business Context")

        col1, col2 = st.columns(2)

        with col1:
            # Initialize business name if not present
            if "business_name" not in st.session_state:
                st.session_state.business_name = ""

            business_name = st.text_input(
                "What are we calling this content?",
                value=st.session_state.business_name,
                key="business_name_input",
                help="Example: Product Spotlight",
                on_change=lambda: setattr(st.session_state, "business_name", st.session_state.business_name_input)
            )

            # Initialize business where if not present
            if "business_where" not in st.session_state:
                st.session_state.business_where = ""

            business_where = st.text_input(
                "Where and when does it display?",
                value=st.session_state.business_where,
                key="business_where_input",
                help="Example: On the product page, below the main image",
                on_change=lambda: setattr(st.session_state, "business_where", st.session_state.business_where_input)
            )

        with col2:
            # Initialize business who if not present
            if "business_who" not in st.session_state:
                st.session_state.business_who = ""

            business_who = st.text_input(
                "Who sees it?",
                value=st.session_state.business_who,
                key="business_who_input",
                help="Example: All website visitors",
                on_change=lambda: setattr(st.session_state, "business_who", st.session_state.business_who_input)
            )

            # Initialize business look if not present
            if "business_look" not in st.session_state:
                st.session_state.business_look = ""

            business_look = st.text_input(
                "What does it look like?",
                value=st.session_state.business_look,
                key="business_look_input",
                help="Example: 3-5 short paragraphs with bullet points",
                on_change=lambda: setattr(st.session_state, "business_look", st.session_state.business_look_input)
            )

        # Initialize business why if not present
        if "business_why" not in st.session_state:
            st.session_state.business_why = ""

        business_why = st.text_area(
            "Why does it exist?",
            value=st.session_state.business_why,
            height=80,
            key="business_why_input",
            help="Example: To highlight key features and benefits of the product",
            on_change=lambda: setattr(st.session_state, "business_why", st.session_state.business_why_input)
        )


def render_design_requirements_section():
    """Render the Design Requirements section"""
    with st.container(border=True):
        section_with_info(
            "Design Requirements",
            "Define structural components and formatting requirements"
        )

        # Content Components
        subsection_header("Content Components")

        # Initialize components list if not present
        if "components" not in st.session_state:
            st.session_state.components = []

        # Component selector
        component_types = [
            "Headline", "Subheadline", "Introduction", "Body Text",
            "Bullet Points", "Call to Action", "Conclusion", "Disclaimer"
        ]

        selected_component = st.selectbox(
            "Select a component type",
            component_types,
            key="component_type_select"
        )

        component_description = st.text_area(
            "Provide a short description for this component",
            height=80,
            key="component_description_input"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            component_min_chars = st.number_input(
                "Minimum characters",
                min_value=0,
                value=0,
                key="component_min_chars_input"
            )

        with col2:
            component_max_chars = st.number_input(
                "Maximum characters",
                min_value=0,
                value=0,
                key="component_max_chars_input"
            )

        with col3:
            component_sentences = st.number_input(
                "Number of sentences",
                min_value=0,
                value=0,
                key="component_sentences_input"
            )

        # Add component button
        if st.button("Add Component", key="add_component_btn"):
            component = {
                "type": selected_component,
                "description": component_description,
                "min_chars": component_min_chars,
                "max_chars": component_max_chars,
                "sentences": component_sentences
            }
            st.session_state.components.append(component)
            st.rerun()

        # Display existing components
        if st.session_state.components:
            st.markdown("**Added Components:**")
            for i, component in enumerate(st.session_state.components):
                with st.container(border=True):
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"**{component['type']}**")
                        st.markdown(f"Description: {component['description']}")
                        st.markdown(
                            f"Characters: {component['min_chars']}-{component['max_chars']} | Sentences: {component['sentences']}")
                    with col2:
                        if st.button("Remove", key=f"remove_component_{i}"):
                            st.session_state.components.pop(i)
                            st.rerun()

        # Language and Localization
        subsection_header("Language & Localization")

        # Initialize language choice if not present
        if "language_choice" not in st.session_state:
            st.session_state.language_choice = "English (US)"

        language_options = [
            "English (US)", "English (UK)", "English (AUS)",
            "Spanish", "French", "German", "Japanese", "Custom"
        ]

        selected_language = st.selectbox(
            "Select target language and locale",
            language_options,
            index=language_options.index(st.session_state.language_choice),
            key="language_choice_select",
            on_change=lambda: setattr(st.session_state, "language_choice", st.session_state.language_choice_select)
        )

        if selected_language == "Custom":
            custom_language = st.text_input(
                "Specify custom language and locale",
                key="custom_language_input"
            )

        # Initialize globalization items if not present
        if "globalization_items" not in st.session_state:
            st.session_state.globalization_items = []

        # Globalization aspects
        globalization_item = st.text_input(
            "Add specific globalization aspects to focus on",
            key="globalization_item_input",
            help="Example: 'Ensure use of local currency symbols', 'Adapt examples for local market'"
        )

        if st.button("+ Add Globalization Aspect", key="add_global_aspect_btn"):
            if globalization_item and globalization_item not in st.session_state.globalization_items:
                st.session_state.globalization_items.append(globalization_item)
                st.rerun()

        # Display existing globalization items
        if st.session_state.globalization_items:
            st.markdown("**Globalization Aspects:**")
            for i, item in enumerate(st.session_state.globalization_items):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(f"- {item}")
                with col2:
                    if st.button("×", key=f"remove_global_{i}"):
                        st.session_state.globalization_items.pop(i)
                        st.rerun()


def render_enhanced_building_blocks():
    """Render the enhanced building blocks sections"""

    # Update the initialize_session_state function in utils/state_management.py to include new state variables:
    # - content_intent, mission_statement, voice_choice, content_rules
    # - content_description, business_name, business_where, business_who, business_look, business_why
    # - components, language_choice, globalization_items

    col1, col2 = st.columns(2)

    with col1:
        render_content_intent_section()
        render_design_requirements_section()

    with col2:
        render_content_setup_section()

    # Update prompt structure in session state to include new sections
    if "prompt_structure" in st.session_state:
        if "Content Intent & Guidelines" not in st.session_state.prompt_structure:
            st.session_state.prompt_structure["Content Intent & Guidelines"] = True
        if "Content Setup" not in st.session_state.prompt_structure:
            st.session_state.prompt_structure["Content Setup"] = True
        if "Design Requirements" not in st.session_state.prompt_structure:
            st.session_state.prompt_structure["Design Requirements"] = True