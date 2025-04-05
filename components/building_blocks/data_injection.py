import streamlit as st
import pandas as pd
import json
import io
from utils.ui_helpers import section_with_info, subsection_header


def render_data_injection_section():
    """Render the Data Injection section for file uploads and GraphQL connections"""
    with st.container(border=True):
        section_with_info(
            "Data Sources & Examples",
            "Import data from files or GraphQL for use in prompts"
        )

        # Data source selection
        subsection_header("Data Sources")

        # Initialize data source type if not present
        if "data_source_type" not in st.session_state:
            st.session_state.data_source_type = "File"

        data_source_type = st.radio(
            "Choose data source type",
            ["File", "GraphQL", "Manual Examples"],
            horizontal=True,
            key="data_source_type_radio",
            on_change=lambda: setattr(st.session_state, "data_source_type", st.session_state.data_source_type_radio)
        )

        # File upload section
        if data_source_type == "File":
            render_file_upload_section()

        # GraphQL connection section
        elif data_source_type == "GraphQL":
            render_graphql_section()

        # Manual examples section
        else:
            render_manual_examples_section()


def render_file_upload_section():
    """Handle file upload functionality"""
    # Supported file types
    supported_file_types = ["csv", "xlsx", "json", "txt"]

    # Initialize file mappings if not present
    if "file_mappings" not in st.session_state:
        st.session_state.file_mappings = []

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a data file (CSV, Excel, JSON, or text)",
        type=supported_file_types
    )

    if uploaded_file is not None:
        # Process the uploaded file
        file_data = read_uploaded_file(uploaded_file)

        if file_data is not None:
            # Store file data in session state
            st.session_state.uploaded_file_data = file_data

            # Preview the data
            st.subheader("Data Preview")

            if isinstance(file_data, pd.DataFrame):
                # Show DataFrame preview
                st.dataframe(file_data.head(5))
                fields = file_data.columns.tolist()

            elif isinstance(file_data, dict) or isinstance(file_data, list):
                # Show JSON preview
                if isinstance(file_data, list) and len(file_data) > 0:
                    st.json(file_data[0])
                else:
                    st.json(file_data)

                # Extract fields from JSON
                fields = extract_keys_from_json(file_data)

            else:
                # Show text preview
                st.text_area("Content Preview",
                             value=str(file_data)[:1000] + ("..." if len(str(file_data)) > 1000 else ""), height=200,
                             disabled=True)
                st.info("Text files can be used directly in prompts without field mapping.")
                fields = ["full_text"]

            # Create field mappings
            st.subheader("Map Data Fields to Prompt Placeholders")

            # Only show field mapping for structured data
            if fields and fields != ["full_text"]:
                col1, col2 = st.columns(2)

                with col1:
                    selected_field = st.selectbox(
                        "Select data field",
                        fields,
                        key="file_field_select"
                    )

                with col2:
                    placeholder_name = st.text_input(
                        "Enter placeholder name",
                        key="placeholder_name_input",
                        help="This will be used as {{placeholder_name}} in your prompts"
                    )

                if st.button("Add Field Mapping", key="add_mapping_btn"):
                    if selected_field and placeholder_name:
                        # Add mapping to session state
                        new_mapping = {
                            "field": selected_field,
                            "placeholder": placeholder_name
                        }

                        # Check if mapping already exists
                        if not any(m["field"] == selected_field and m["placeholder"] == placeholder_name for m in
                                   st.session_state.file_mappings):
                            st.session_state.file_mappings.append(new_mapping)
                            st.rerun()

            # Display current mappings
            if st.session_state.file_mappings:
                st.subheader("Field Mappings")

                # Create DataFrame for display
                mappings_df = pd.DataFrame(st.session_state.file_mappings)
                st.dataframe(mappings_df)

                # Button to clear mappings
                if st.button("Clear All Mappings", key="clear_mappings_btn"):
                    st.session_state.file_mappings = []
                    st.rerun()

            # Prompt usage example
            with st.expander("How to Use Data in Prompts", expanded=False):
                st.markdown("""
                ### Using Data in Prompts

                Refer to mapped fields in your prompts using double curly braces:

                ```
                Please analyze the following information:

                Customer: {{customer_name}}
                Product: {{product_name}}
                Feedback: {{feedback_text}}

                Generate a response addressing their concerns.
                ```

                When generating content, these placeholders will be replaced with actual data values.
                """)


def render_graphql_section():
    """Handle GraphQL connection functionality"""
    # Initialize GraphQL state variables if not present
    if "graphql_endpoint" not in st.session_state:
        st.session_state.graphql_endpoint = ""

    if "graphql_query" not in st.session_state:
        st.session_state.graphql_query = """query {
  example {
    id
    name
    description
  }
}"""

    if "graphql_headers" not in st.session_state:
        st.session_state.graphql_headers = {}

    if "graphql_results" not in st.session_state:
        st.session_state.graphql_results = None

    if "graphql_mappings" not in st.session_state:
        st.session_state.graphql_mappings = []

    # GraphQL endpoint
    st.text_input(
        "GraphQL Endpoint URL",
        value=st.session_state.graphql_endpoint,
        key="graphql_endpoint_input",
        on_change=lambda: setattr(st.session_state, "graphql_endpoint", st.session_state.graphql_endpoint_input)
    )

    # GraphQL headers
    with st.expander("Headers", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            header_key = st.text_input("Header Name", key="header_key_input")

        with col2:
            header_value = st.text_input("Header Value", key="header_value_input",
                                         type="password" if header_key.lower() in ["authorization", "x-api-key",
                                                                                   "apikey", "api-key",
                                                                                   "token"] else "default")

        if st.button("Add Header", key="add_header_btn"):
            if header_key:
                st.session_state.graphql_headers[header_key] = header_value
                st.rerun()

        # Display current headers
        if st.session_state.graphql_headers:
            st.markdown("**Current Headers:**")
            for key, value in st.session_state.graphql_headers.items():
                masked_value = value[:2] + "*" * (len(value) - 4) + value[-2:] if key.lower() in ["authorization",
                                                                                                  "x-api-key", "apikey",
                                                                                                  "api-key",
                                                                                                  "token"] and len(
                    value) > 4 else value
                st.markdown(f"- **{key}**: {masked_value}")

            # Button to clear headers
            if st.button("Clear All Headers", key="clear_headers_btn"):
                st.session_state.graphql_headers = {}
                st.rerun()

    # GraphQL query
    st.text_area(
        "GraphQL Query",
        value=st.session_state.graphql_query,
        height=200,
        key="graphql_query_input",
        on_change=lambda: setattr(st.session_state, "graphql_query", st.session_state.graphql_query_input)
    )

    # Execute query button
    if st.button("Execute Query", key="execute_query_btn"):
        if st.session_state.graphql_endpoint:
            with st.spinner("Executing query..."):
                # Mock execution for demonstration
                # In a real implementation, this would make an API request
                st.session_state.graphql_results = {
                    "data": {
                        "example": [
                            {"id": "1", "name": "Example 1", "description": "First example item"},
                            {"id": "2", "name": "Example 2", "description": "Second example item"},
                            {"id": "3", "name": "Example 3", "description": "Third example item"}
                        ]
                    }
                }
                st.success("Query executed successfully!")
        else:
            st.error("Please enter a GraphQL endpoint URL")

    # Display query results
    if st.session_state.graphql_results:
        st.subheader("Query Results")

        # Pretty-print the results
        st.json(st.session_state.graphql_results)

        # Extract fields for mapping
        fields = extract_graphql_fields(st.session_state.graphql_results)

        if fields:
            # Create field mappings
            st.subheader("Map GraphQL Fields to Prompt Placeholders")

            col1, col2 = st.columns(2)

            with col1:
                selected_field = st.selectbox(
                    "Select field",
                    fields,
                    key="graphql_field_select"
                )

            with col2:
                placeholder_name = st.text_input(
                    "Enter placeholder name",
                    key="graphql_placeholder_input",
                    help="This will be used as {{placeholder_name}} in your prompts"
                )

            if st.button("Add Field Mapping", key="add_graphql_mapping_btn"):
                if selected_field and placeholder_name:
                    # Add mapping to session state
                    new_mapping = {
                        "field": selected_field,
                        "placeholder": placeholder_name
                    }

                    # Check if mapping already exists
                    if not any(m["field"] == selected_field and m["placeholder"] == placeholder_name for m in
                               st.session_state.graphql_mappings):
                        st.session_state.graphql_mappings.append(new_mapping)
                        st.rerun()

            # Display current mappings
            if st.session_state.graphql_mappings:
                st.subheader("Field Mappings")

                # Create DataFrame for display
                mappings_df = pd.DataFrame(st.session_state.graphql_mappings)
                st.dataframe(mappings_df)

                # Button to clear mappings
                if st.button("Clear All Mappings", key="clear_graphql_mappings_btn"):
                    st.session_state.graphql_mappings = []
                    st.rerun()


def render_manual_examples_section():
    """Handle manual example entry functionality"""
    # Initialize examples list if not present
    if "manual_examples" not in st.session_state:
        st.session_state.manual_examples = []

    # Maximum number of examples
    max_examples = 10

    st.markdown(f"Add up to {max_examples} examples to guide the model's understanding (Few-Shot Learning).")

    # Example input fields
    st.subheader("Add New Example")

    example_text = st.text_area(
        "Example content",
        key="example_content_input",
        height=150,
        help="Enter an example of the kind of content you want the model to generate"
    )

    example_comment = st.text_input(
        "Example description",
        key="example_comment_input",
        help="Briefly describe what this example demonstrates"
    )

    # Add example button
    if st.button("+ Add Example", key="add_example_btn"):
        if example_text and len(st.session_state.manual_examples) < max_examples:
            new_example = {
                "text": example_text,
                "comment": example_comment
            }
            st.session_state.manual_examples.append(new_example)
            st.rerun()
        elif not example_text:
            st.warning("Please enter example content.")
        else:
            st.warning(f"Maximum number of examples ({max_examples}) reached.")

    # Display current examples
    if st.session_state.manual_examples:
        st.subheader("Added Examples")

        for i, example in enumerate(st.session_state.manual_examples):
            with st.expander(
                    f"Example {i + 1}: {example['comment'][:30]}{'...' if len(example['comment']) > 30 else ''}",
                    expanded=False):
                st.text_area(
                    "Content",
                    value=example["text"],
                    height=100,
                    key=f"example_text_{i}",
                    disabled=True
                )
                st.markdown(f"**Description:** {example['comment']}")

                # Remove example button
                if st.button("Remove Example", key=f"remove_example_{i}"):
                    st.session_state.manual_examples.pop(i)
                    st.rerun()

        # Clear all examples button
        if st.button("Clear All Examples", key="clear_examples_btn"):
            st.session_state.manual_examples = []
            st.rerun()

        st.caption(f"Added {len(st.session_state.manual_examples)}/{max_examples} examples")


# Utility functions

def read_uploaded_file(uploaded_file):
    """
    Read the uploaded file and return its contents in an appropriate format

    Args:
        uploaded_file: The uploaded file object from st.file_uploader

    Returns:
        The file contents as a DataFrame, dict, list, or string depending on file type
    """
    # Get file extension
    file_extension = uploaded_file.name.split(".")[-1].lower()

    try:
        # Process based on file type
        if file_extension == "csv":
            return pd.read_csv(uploaded_file)

        elif file_extension == "xlsx":
            return pd.read_excel(uploaded_file)

        elif file_extension == "json":
            return json.load(uploaded_file)

        elif file_extension == "txt":
            # Read text file
            return uploaded_file.getvalue().decode("utf-8")

        else:
            st.error(f"Unsupported file type: {file_extension}")
            return None
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None


def extract_keys_from_json(json_data):
    """
    Extract fields/keys from JSON data

    Args:
        json_data: JSON data as dict or list

    Returns:
        List of field names
    """
    if isinstance(json_data, dict):
        return list(json_data.keys())

    elif isinstance(json_data, list) and len(json_data) > 0:
        if isinstance(json_data[0], dict):
            return list(json_data[0].keys())

    return []


def extract_graphql_fields(graphql_results):
    """
    Extract fields from GraphQL query results

    Args:
        graphql_results: The GraphQL query results

    Returns:
        List of field paths in dot notation
    """
    fields = []

    def extract_fields_recursive(data, prefix=""):
        if isinstance(data, dict):
            for key, value in data.items():
                if key not in ["__typename"]:
                    new_prefix = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, (dict, list)):
                        extract_fields_recursive(value, new_prefix)
                    else:
                        fields.append(new_prefix)

        elif isinstance(data, list) and len(data) > 0:
            extract_fields_recursive(data[0], prefix)

    if graphql_results and "data" in graphql_results:
        extract_fields_recursive(graphql_results["data"])

    return fields