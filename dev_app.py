"""
Development version of the app for testing purposes.
This script includes useful utilities for debugging and development.
"""

import streamlit as st
import os
import sys
import json
import time
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from utils.state_management import initialize_session_state
from models.prompt_generator import generate_prompt
from models.content_generator import ContentGenerator


def display_dev_tools():
    """Display developer tools in the sidebar"""
    st.sidebar.markdown("## Developer Tools")
    
    # Session state inspector
    with st.sidebar.expander("Session State Inspector", expanded=False):
        st.json({k: str(v) if callable(v) else v for k, v in st.session_state.items()})
    
    # Prompt generation tester
    with st.sidebar.expander("Quick Prompt Generator", expanded=False):
        if st.button("Generate Prompt"):
            prompt = generate_prompt()
            st.code(prompt)
    
    # Content generation tester
    with st.sidebar.expander("LLM API Tester", expanded=False):
        api_key = st.text_input("API Key (leave empty for simulation)", 
                                value=os.environ.get("LLM_API_KEY", ""), type="password")
        
        test_prompt = st.text_area("Test Prompt", value="Write a short paragraph about prompt engineering.")
        
        if st.button("Test API"):
            with st.spinner("Generating content..."):
                generator = ContentGenerator(api_key=api_key if api_key else None)
                start_time = time.time()
                result = generator.generate(test_prompt)
                end_time = time.time()
                
                st.write(f"Time taken: {end_time - start_time:.2f}s")
                st.json({"metadata": result["metadata"]})
                st.markdown("### Generated Content")
                st.markdown(result["content"])
    
    # Template viewer
    with st.sidebar.expander("Template Explorer", expanded=False):
        # Show templates directory content
        if os.path.exists("templates"):
            templates = [f.replace(".json", "") for f in os.listdir("templates") if f.endswith(".json")]
            
            if templates:
                selected_template = st.selectbox("Select Template", templates)
                
                if selected_template:
                    try:
                        with open(f"templates/{selected_template}.json", "r") as f:
                            template_data = json.load(f)
                        
                        st.json(template_data)
                    except Exception as e:
                        st.error(f"Error loading template: {str(e)}")
            else:
                st.info("No templates found in the templates directory.")
        else:
            st.info("Templates directory doesn't exist yet.")


def main():
    """Main function for the development app"""
    st.set_page_config(
        page_title="LLM Prompt Engineering Framework (Dev)",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Display dev version indicator
    st.markdown(
        """
        <div style="background-color:#FFC107; padding:10px; border-radius:5px; margin-bottom:10px">
            <h1 style="color:#212121; margin:0">🧪 DEVELOPMENT MODE 🧪</h1>
            <p style="color:#212121; margin:0">This is the development version of the LLM Prompt Engineering Framework.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Load and run the main app
    from app import main as app_main
    app_main()
    
    # Add developer tools
    display_dev_tools()


if __name__ == "__main__":
    main()