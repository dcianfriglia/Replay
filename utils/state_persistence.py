import streamlit as st
import json
import os
from datetime import datetime
import uuid


def save_state_to_local_storage(name=None):
    """
    Save the current session state to local storage

    Args:
        name (str, optional): Name to save the state under. If not provided, uses timestamp.

    Returns:
        str: The filename used for saving
    """
    # Create storage directory if it doesn't exist
    os.makedirs("stored_states", exist_ok=True)

    # Generate filename
    if not name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"state_{timestamp}"

    # Make sure the filename is valid
    filename = f"stored_states/{name.replace(' ', '_')}.json"

    # Prepare data to save
    # Exclude any callable objects or things that can't be serialized
    save_data = {}
    for key, value in st.session_state.items():
        try:
            # Test JSON serialization
            json.dumps(value)
            save_data[key] = value
        except (TypeError, OverflowError):
            # Skip values that can't be serialized
            save_data[key] = str(value) if value is not None else None

    # Add metadata
    save_data["__metadata__"] = {
        "saved_at": datetime.now().isoformat(),
        "id": str(uuid.uuid4())
    }

    # Save to file
    with open(filename, "w") as f:
        json.dump(save_data, f, indent=2)

    return filename


def load_state_from_local_storage(filename=None):
    """
    Load session state from local storage

    Args:
        filename (str): Path to the state file to load.
        If None, shows a selection interface.

    Returns:
        bool: True if loading was successful, False otherwise
    """
    # If no filename provided, show selection interface
    if not filename:
        return show_state_selector()

    try:
        with open(filename, "r") as f:
            loaded_data = json.load(f)

        # Remove metadata before loading into session state
        if "__metadata__" in loaded_data:
            del loaded_data["__metadata__"]

        # Update session state with loaded data
        for key, value in loaded_data.items():
            st.session_state[key] = value

        return True

    except Exception as e:
        st.error(f"Error loading state: {str(e)}")
        return False


def show_state_selector():
    """
    Show a selector for choosing saved states to load

    Returns:
        bool: True if a state was loaded, False otherwise
    """
    # Check if storage directory exists
    if not os.path.exists("stored_states"):
        st.warning("No saved states found.")
        return False

    # Get list of saved states
    state_files = [f for f in os.listdir("stored_states") if f.endswith(".json")]

    if not state_files:
        st.warning("No saved states found.")
        return False

    # Sort by modification time (newest first)
    state_files.sort(key=lambda x: os.path.getmtime(os.path.join("stored_states", x)), reverse=True)

    # Prepare options with timestamps
    options = []
    for filename in state_files:
        try:
            with open(os.path.join("stored_states", filename), "r") as f:
                data = json.load(f)
                metadata = data.get("__metadata__", {})
                saved_at = metadata.get("saved_at", "Unknown")

                # Format datetime
                if saved_at != "Unknown":
                    try:
                        dt = datetime.fromisoformat(saved_at)
                        saved_at = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass

                # Show filename and save time
                display_name = f"{filename.replace('.json', '')} ({saved_at})"
                options.append((filename, display_name))
        except:
            # If error reading file, just show filename
            options.append((filename, filename))

    # Create selection dropdown
    selected_option = st.selectbox(
        "Select saved state to load:",
        options=[opt[1] for opt in options],
        key="state_selector"
    )

    # Find matching filename
    selected_filename = None
    for filename, display_name in options:
        if display_name == selected_option:
            selected_filename = filename
            break

    if selected_filename and st.button("Load Selected State"):
        return load_state_from_local_storage(os.path.join("stored_states", selected_filename))

    return False


def list_saved_states():
    """
    List all saved states

    Returns:
        list: List of dictionaries with state info
    """
    if not os.path.exists("stored_states"):
        return []

    state_files = [f for f in os.listdir("stored_states") if f.endswith(".json")]

    states = []
    for filename in state_files:
        try:
            filepath = os.path.join("stored_states", filename)
            modified_time = os.path.getmtime(filepath)

            with open(filepath, "r") as f:
                data = json.load(f)
                metadata = data.get("__metadata__", {})

            states.append({
                "filename": filename,
                "path": filepath,
                "saved_at": metadata.get("saved_at", datetime.fromtimestamp(modified_time).isoformat()),
                "id": metadata.get("id", "unknown"),
                "display_name": filename.replace(".json", "").replace("_", " ")
            })
        except:
            # If error reading file, add basic info
            states.append({
                "filename": filename,
                "path": os.path.join("stored_states", filename),
                "display_name": filename
            })

    # Sort by saved time (newest first)
    states.sort(key=lambda x: x.get("saved_at", ""), reverse=True)

    return states


def delete_saved_state(filename):
    """
    Delete a saved state

    Args:
        filename (str): Filename or path to the state file to delete

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Ensure we're using the correct path
        if not filename.startswith("stored_states/"):
            filepath = os.path.join("stored_states", filename)
        else:
            filepath = filename

        # Check if file exists
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Error deleting state: {str(e)}")
        return False