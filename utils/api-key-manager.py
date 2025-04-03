"""
API Key Manager for the LLM Prompt Engineering Framework.
This module provides functions for managing API keys securely.
"""

import os
import json
import datetime
import getpass
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv, set_key

# Load environment variables
load_dotenv()


def get_api_key(provider="anthropic", from_env=True, from_session=True):
    """
    Get API key for a specific provider
    
    Args:
        provider (str): The API provider (e.g., "anthropic", "openai")
        from_env (bool): Whether to check environment variables
        from_session (bool): Whether to check session state
    
    Returns:
        str: The API key or None if not found
    """
    # Map provider to environment variable name
    env_var_map = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
    }
    
    # Try to get from session state first if enabled
    if from_session and provider.upper() + "_API_KEY" in st.session_state:
        return st.session_state[provider.upper() + "_API_KEY"]
    
    # Try to get from environment variable if enabled
    if from_env and provider in env_var_map:
        env_var = env_var_map[provider]
        api_key = os.getenv(env_var)
        if api_key:
            return api_key
    
    # Try to get from secure storage as last resort
    return get_api_key_from_storage(provider)


def save_api_key(provider, api_key, save_to_env=True, save_to_session=True):
    """
    Save API key for a provider
    
    Args:
        provider (str): The API provider (e.g., "anthropic", "openai")
        api_key (str): The API key to save
        save_to_env (bool): Whether to save to .env file
        save_to_session (bool): Whether to save to session state
    
    Returns:
        bool: True if saved successfully
    """
    # Map provider to environment variable name
    env_var_map = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
    }
    
    # Save to session state if enabled
    if save_to_session:
        st.session_state[provider.upper() + "_API_KEY"] = api_key
    
    # Save to environment file if enabled
    success = True
    if save_to_env and provider in env_var_map:
        env_var = env_var_map[provider]
        try:
            # Check if .env file exists
            env_path = Path(".env")
            if not env_path.exists():
                # Create .env file if it doesn't exist
                with open(env_path, "w") as f:
                    f.write(f"{env_var}={api_key}\n")
            else:
                # Update existing .env file
                set_key(env_path, env_var, api_key)
            
            # Also set the current environment variable
            os.environ[env_var] = api_key
        except Exception as e:
            print(f"Error saving API key to .env file: {e}")
            success = False
    
    # Save to secure storage as backup
    secure_success = save_api_key_to_storage(provider, api_key)
    
    return success and secure_success


def get_api_key_from_storage(provider):
    """
    Get API key from secure storage
    
    Args:
        provider (str): The API provider
    
    Returns:
        str: The API key or None if not found
    """
    # Define the storage location
    storage_dir = Path.home() / ".prompt_engineering_framework"
    storage_file = storage_dir / "api_keys.json"
    
    # Check if storage exists
    if not storage_file.exists():
        return None
    
    try:
        # Read from storage
        with open(storage_file, "r") as f:
            data = json.load(f)
        
        # Get the API key for the provider
        if provider in data:
            return data[provider]["key"]
    except Exception as e:
        print(f"Error reading API key from storage: {e}")
    
    return None


def save_api_key_to_storage(provider, api_key):
    """
    Save API key to secure storage
    
    Args:
        provider (str): The API provider
        api_key (str): The API key to save
    
    Returns:
        bool: True if saved successfully
    """
    # Define the storage location
    storage_dir = Path.home() / ".prompt_engineering_framework"
    storage_file = storage_dir / "api_keys.json"
    
    # Create directory if it doesn't exist
    storage_dir.mkdir(exist_ok=True)
    
    try:
        # Read existing data if available
        data = {}
        if storage_file.exists():
            with open(storage_file, "r") as f:
                data = json.load(f)
        
        # Update the data
        data[provider] = {
            "key": api_key,
            "saved_at": datetime.datetime.now().isoformat()
        }
        
        # Write back to storage
        with open(storage_file, "w") as f:
            json.dump(data, f, indent=2)
        
        # Set secure permissions on file (Unix-like systems)
        try:
            import stat
            storage_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except Exception:
            pass
        
        return True
    except Exception as e:
        print(f"Error saving API key to storage: {e}")
        return False


def prompt_for_api_keys(providers=None):
    """
    Interactive CLI prompt for API keys
    
    Args:
        providers (list): List of providers to prompt for (defaults to all supported)
    
    Returns:
        dict: Dictionary of provider -> API key pairs
    """
    if providers is None:
        providers = ["anthropic", "openai"]
    
    api_keys = {}
    print("Please enter your API keys:")
    
    for provider in providers:
        # Check if we already have the key
        existing_key = get_api_key(provider)
        if existing_key:
            print(f"{provider.capitalize()} API key: {'*' * 8}{existing_key[-4:]}")
            use_existing = input(f"Use existing {provider.capitalize()} API key? (Y/n): ")
            if use_existing.lower() != "n":
                api_keys[provider] = existing_key
                continue
        
        # Prompt for new key
        key = getpass.getpass(f"{provider.capitalize()} API key: ")
        if key:
            api_keys[provider] = key
            save_api_key(provider, key)
    
    return api_keys


def render_api_key_manager():
    """Render a Streamlit UI for API key management"""
    st.markdown("## API Key Management")
    
    providers = [
        ("anthropic", "Anthropic (Claude)"),
        ("openai", "OpenAI (GPT)"),
    ]
    
    for provider_id, provider_name in providers:
        st.markdown(f"### {provider_name}")
        
        # Check if key exists
        existing_key = get_api_key(provider_id)
        
        if existing_key:
            # Show masked key
            st.success(f"API key configured: {'*' * 10}{existing_key[-4:]}")
            
            # Update key option
            if st.button(f"Update {provider_name} Key", key=f"update_{provider_id}"):
                st.session_state[f"show_{provider_id}_input"] = True
        else:
            # No key present
            st.warning(f"No API key configured for {provider_name}")
            st.session_state[f"show_{provider_id}_input"] = True
        
        # Show input if requested
        if st.session_state.get(f"show_{provider_id}_input", False):
            new_key = st.text_input(
                f"{provider_name} API Key",
                type="password",
                key=f"{provider_id}_api_key_input"
            )
            
            save_options = st.radio(
                "Save options:",
                ["Session only", "Session + .env file"],
                horizontal=True,
                key=f"{provider_id}_save_options"
            )
            
            if st.button("Save", key=f"save_{provider_id}"):
                if new_key:
                    save_to_env = save_options == "Session + .env file"
                    if save_api_key(provider_id, new_key, save_to_env=save_to_env):
                        st.success(f"{provider_name} API key saved successfully!")
                        st.session_state[f"show_{provider_id}_input"] = False
                        st.rerun()
                    else:
                        st.error(f"Failed to save {provider_name} API key.")
                else:
                    st.error("API key cannot be empty.")
            
            if st.button("Cancel", key=f"cancel_{provider_id}"):
                st.session_state[f"show_{provider_id}_input"] = False
                st.rerun()
    
    # Add option to clear all keys
    st.markdown("### Advanced Options")
    if st.button("Clear All API Keys"):
        # Clear from session state
        for provider_id, _ in providers:
            if provider_id.upper() + "_API_KEY" in st.session_state:
                del st.session_state[provider_id.upper() + "_API_KEY"]
        st.success("All API keys cleared from session.")


if __name__ == "__main__":
    # Command-line interface for testing
    print("API Key Manager CLI")
    prompt_for_api_keys()
