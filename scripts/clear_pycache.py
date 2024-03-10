import os


def delete_pycache_contents(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Check if current directory is a __pycache__ directory
        if "__pycache__" in dirpath:
            print(f"Clearing {dirpath}")
            for filename in filenames:
                try:
                    # Construct the full path and remove each file
                    file_path = os.path.join(dirpath, filename)
                    os.remove(file_path)
                    print(f"Removed {file_path}")
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")
            # Optionally, you can remove the __pycache__ directory itself
            # by uncommenting the next line
            # shutil.rmtree(dirpath)


if __name__ == "__main__":
    project_root = ".."  # Assumes this script is run from the project root
    delete_pycache_contents(project_root)
    print("Cleanup completed.")
