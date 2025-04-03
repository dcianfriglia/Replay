import streamlit as st
from utils.ui_helpers import section_with_info, subsection_header


def render_rag_section():
    """Render the Retrieval-Augmented Generation (RAG) workflow configuration section"""

    st.markdown("### Retrieval-Augmented Generation (RAG) Workflow")

    st.markdown("""
    Retrieval-Augmented Generation (RAG) enhances LLM responses with external knowledge
    by retrieving relevant information from specified sources. This approach grounds
    responses in specific knowledge sources and improves accuracy and factuality.
    """)

    # Diagram
    st.image("https://via.placeholder.com/800x200?text=RAG+Workflow+Diagram",
             caption="Retrieval-Augmented Generation workflow showing retrieval and integration of external information",
             use_column_width=True)

    # Enable/disable toggle using a callback pattern
    if "rag_enabled" not in st.session_state:
        st.session_state.rag_enabled = False

    def on_toggle_change():
        # Callback updates the main session state variable from the widget-specific one
        st.session_state.rag_enabled = st.session_state.rag_component_toggle

    # Use the toggle with a unique key that doesn't conflict with session state variable
    rag_enabled = st.toggle(
        "Enable Retrieval-Augmented Generation",
        value=st.session_state.rag_enabled,
        help="When enabled, responses will be augmented with retrieved external knowledge",
        key="rag_component_toggle",  # Unique key different from session state variable
        on_change=on_toggle_change
    )

    if rag_enabled:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Knowledge sources configuration
            st.markdown("#### Knowledge Sources")

            # Initialize knowledge sources if not present
            if "rag_knowledge_sources" not in st.session_state:
                st.session_state.rag_knowledge_sources = [
                    {"type": "Internal Documentation", "description": "Company documentation and policies",
                     "enabled": True},
                    {"type": "Industry Standards", "description": "Standards and best practices in the industry",
                     "enabled": True},
                    {"type": "Academic Research", "description": "Recent academic papers and research findings",
                     "enabled": False}
                ]

            # Display and manage knowledge sources
            for i, source in enumerate(st.session_state.rag_knowledge_sources):
                with st.container(border=True):
                    cols = st.columns([1, 2, 1])

                    with cols[0]:
                        source_types = ["Internal Documentation", "Industry Standards", "Academic Research",
                                        "Case Studies", "Custom Knowledge Base", "External API", "Vector Database"]
                        current_index = source_types.index(source["type"]) if source["type"] in source_types else 0
                        source["type"] = st.selectbox(f"Source {i + 1} Type", source_types,
                                                      index=current_index, key=f"source_type_{i}")

                    with cols[1]:
                        source["description"] = st.text_input("Description", value=source["description"],
                                                              key=f"source_desc_{i}")

                    with cols[2]:
                        source["enabled"] = st.checkbox("Enabled", value=source["enabled"], key=f"source_enabled_{i}")

                        if i > 0 and st.button("Remove", key=f"rag_remove_source_{i}"):
                            st.session_state.rag_knowledge_sources.pop(i)
                            st.rerun()

            # Add source button
            if st.button("+ Add Knowledge Source", key="rag_add_source_btn"):
                st.session_state.rag_knowledge_sources.append({
                    "type": "Custom Knowledge Base",
                    "description": "Description of this knowledge source",
                    "enabled": True
                })
                st.rerun()

            # Retrieval instructions
            st.markdown("#### Retrieval Instructions")
            retrieval_instructions = st.text_area(
                "Explain how the model should retrieve and incorporate external knowledge",
                value="Retrieve relevant information from the specified knowledge sources based on the query. Synthesize the retrieved information with your own knowledge to provide a comprehensive response.",
                height=100,
                key="retrieval_instructions"
            )

        with col2:
            # Retrieval configuration
            st.markdown("#### Retrieval Configuration")

            st.slider(
                "Number of Chunks to Retrieve",
                min_value=1,
                max_value=10,
                value=3,
                help="Maximum number of text chunks to retrieve per query"
            )

            st.slider(
                "Chunk Size (tokens)",
                min_value=256,
                max_value=2048,
                value=512,
                step=128,
                help="Size of each retrieved chunk in tokens"
            )

            st.slider(
                "Relevance Threshold",
                min_value=0.5,
                max_value=0.95,
                value=0.75,
                help="Minimum relevance score for retrieved chunks"
            )

            # Integration settings
            st.markdown("#### Integration Settings")

            st.radio(
                "Integration Method",
                ["In-Context Retrieval", "Query-Based Retrieval", "Multi-Query Retrieval", "Hybrid Approach"],
                index=0,
                help="Method for retrieving and integrating information"
            )

            st.checkbox(
                "Citation for retrieved info",
                value=True,
                help="Include source citations for retrieved information"
            )

            st.checkbox(
                "Dynamic retrieval",
                value=True,
                help="Allow model to dynamically generate retrieval queries during generation"
            )

            st.checkbox(
                "Re-ranking of retrieved chunks",
                value=False,
                help="Apply re-ranking to improve relevance of retrieved information"
            )

        # Example of how this workflow would be used
        with st.expander("Example Implementation", expanded=False):
            st.code("""
# Example Python implementation of RAG workflow
def rag_workflow(input_text, knowledge_sources, num_chunks=3, relevance_threshold=0.75):
    # Step 1: Generate retrieval queries based on input
    query_generation_prompt = f\"\"\"
    Generate specific search queries to retrieve information related to:

    {input_text}

    Return 1-3 search queries that would help answer this question.
    \"\"\"

    query_response = llm_call(query_generation_prompt)
    search_queries = parse_queries(query_response)

    # Step 2: Retrieve relevant information
    retrieved_chunks = []
    for query in search_queries:
        for source in [s for s in knowledge_sources if s["enabled"]]:
            # Perform vector search in the knowledge source
            source_chunks = vector_search(
                query=query,
                source=source["type"],
                num_results=num_chunks,
                threshold=relevance_threshold
            )

            if source_chunks:
                retrieved_chunks.extend([
                    {
                        "content": chunk["text"],
                        "source": source["type"],
                        "relevance": chunk["score"]
                    }
                    for chunk in source_chunks
                ])

    # Deduplicate and sort by relevance
    unique_chunks = deduplicate_chunks(retrieved_chunks)
    top_chunks = sorted(unique_chunks, key=lambda x: x["relevance"], reverse=True)[:num_chunks]

    # Step 3: Generate augmented response with retrieved information
    augmented_prompt = f\"\"\"
    Based on the following information and your knowledge, answer the question:

    Question: {input_text}

    Retrieved Information:
    {format_retrieved_chunks(top_chunks)}

    Provide a comprehensive answer that incorporates the retrieved information.
    Include citations to the source when using retrieved information.
    \"\"\"

    augmented_response = llm_call(augmented_prompt)

    return {
        "response": augmented_response,
        "retrieved_chunks": top_chunks,
        "queries_used": search_queries
    }
            """, language="python")

        # File upload for knowledge sources
        st.markdown("#### Upload Knowledge Source Files")

        uploaded_files = st.file_uploader(
            "Upload documents to use as knowledge sources",
            accept_multiple_files=True,
            type=["pdf", "txt", "docx", "csv", "json", "md"]
        )

        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} files to use as knowledge sources!")

            with st.expander("Processing Settings", expanded=False):
                st.checkbox("Chunk documents automatically", value=True)
                st.checkbox("Extract metadata from documents", value=True)
                st.selectbox(
                    "Document Embedding Model",
                    ["Default Embedding", "OpenAI Embeddings", "Custom Embedding Model"]
                )

        # Best practices
        with st.expander("When To Use This Workflow", expanded=False):
            st.markdown("""
            **Ideal Use Cases:**

            * Tasks requiring access to specific knowledge not in the model's training
            * Applications where factual accuracy and citation are critical
            * Domains with frequently changing information or specialized knowledge
            * Systems where grounding responses in specific sources is important

            **Real-World Examples:**

            * Customer support systems accessing product documentation and knowledge bases
            * Research assistants retrieving and synthesizing information from multiple sources
            * Technical documentation generators that ground responses in official specifications
            * Legal or compliance applications requiring citation to specific regulations
            """)

            # Citation from the Anthropic article
            st.info("""
            *"RAG enhances responses with external knowledge, reduces hallucinations by grounding 
            responses in provided sources, and can incorporate domain-specific information or recent content. 
            It's particularly valuable for specialized topics or when factual accuracy is critical."*

            — Anthropic Engineering
            """)