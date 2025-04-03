import os
import json


def save_template(template_data, template_name):
    """
    Save prompt template to a JSON file

    Args:
        template_data (dict): Dictionary containing all template data
        template_name (str): Name of the template

    Returns:
        str: Path to the saved template file
    """
    os.makedirs("templates", exist_ok=True)
    file_path = f"templates/{template_name.replace(' ', '_')}.json"

    with open(file_path, 'w') as f:
        json.dump(template_data, f, indent=2)

    return file_path


def load_template(file_path):
    """
    Load prompt template from a JSON file

    Args:
        file_path (str): Path to the template file

    Returns:
        dict: Dictionary containing all template data
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def list_templates():
    """
    List all available templates in the templates directory

    Returns:
        list: List of template names (without extension)
    """
    if not os.path.exists("templates"):
        return []

    templates = []

    for filename in os.listdir("templates"):
        if filename.endswith(".json"):
            template_name = filename.replace(".json", "").replace("_", " ")
            templates.append(template_name)

    return templates


def delete_template(template_name):
    """
    Delete a template

    Args:
        template_name (str): Name of the template to delete

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    file_path = f"templates/{template_name.replace(' ', '_')}.json"

    if os.path.exists(file_path):
        os.remove(file_path)
        return True

    return False