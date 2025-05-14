import subprocess
import re
import os


def normalize_package_name(name):
    """
    Normalize package name according to PEP 503 (lowercase, replace runs of '-', '_', '.' with '-').
    """
    return re.sub(r"[-_.]+", "-", name).lower()


def get_installed_packages():
    """
    Get a dictionary of installed packages and their versions using 'pip freeze'.
    Returns an empty dictionary if 'pip freeze' fails or 'pip' is not found.
    """
    installed_packages = {}
    try:
        process = subprocess.run(
            ['pip', 'freeze'], capture_output=True, text=True, check=True)
        for line in process.stdout.strip().split('\n'):
            if '==' in line:
                name, version = line.split('==', 1)
                installed_packages[normalize_package_name(name)] = version
    except subprocess.CalledProcessError as e:
        print(f"Error running 'pip freeze': {e.stderr}")
    except FileNotFoundError:
        print("Error: 'pip' command not found. Ensure pip is installed and in your PATH.")
    return installed_packages


def update_requirements_file(requirements_path="requirements.txt"):
    """
    Update the versions in the requirements.txt file to match currently installed versions.
    """
    print(f"Updating '{requirements_path}'...")
    installed_packages = get_installed_packages()

    if not installed_packages:
        print("No installed packages found. Aborting.")
        return

    if not os.path.exists(requirements_path):
        print(f"Error: '{requirements_path}' not found.")
        return

    updated_lines = []
    package_name_regex = re.compile(r"^\s*([a-zA-Z0-9_.-]+)")

    try:
        with open(requirements_path, 'r') as f_req:
            for line_number, original_line in enumerate(f_req, 1):
                stripped_line = original_line.strip()

                # Preserve comments, blank lines, and editable installs
                if not stripped_line or stripped_line.startswith(('#', '-e')):
                    updated_lines.append(original_line)
                    continue

                match = package_name_regex.match(stripped_line)
                if match:
                    package_name_in_req_file = match.group(1)
                    normalized_req_name = normalize_package_name(
                        package_name_in_req_file)

                    if normalized_req_name in installed_packages:
                        current_version = installed_packages[normalized_req_name]
                        new_line_content = f"{package_name_in_req_file}=={current_version}"
                        updated_lines.append(new_line_content + '\n')
                    else:
                        updated_lines.append(original_line)
                else:
                    updated_lines.append(original_line)
    except Exception as e:
        print(f"Error processing '{requirements_path}': {e}")
        return

    try:
        with open(requirements_path, 'w') as f_req:
            f_req.writelines(updated_lines)
        print(f"Successfully updated '{requirements_path}'.")
    except IOError as e:
        print(f"Error writing to '{requirements_path}': {e}")


if __name__ == "__main__":
    update_requirements_file()
