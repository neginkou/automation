from pathlib import Path

import os
import shutil

def create_folder(folder_name):
    """Create a folder with the specified name."""
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Folder '{folder_name}' created.")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists.")

def move_user_documents(user_folder, temp_folder):
    """Move documents from a deleted user's folder to a temporary folder."""
    user_folder_path = Path(user_folder)
    temp_folder_path = Path(temp_folder)

    if not temp_folder_path.exists():
        create_folder(temp_folder_path)
    
    if user_folder_path.exists():
        for file in user_folder_path.iterdir():
            shutil.move(file, temp_folder_path / file.name)
        print(f"Documents from '{user_folder}' have been moved to '{temp_folder}'.")
    else:
        print(f"User folder '{user_folder}' does not exist.")

def sort_documents(folder_path):
    """Sort documents into 'logs' and 'mail' folders based on their file type."""
    folder_path = Path(folder_path)
    logs_path = folder_path / 'logs'
    mail_path = folder_path / 'mail'

    for path in (logs_path, mail_path):
        path.mkdir(parents=True, exist_ok=True)

    for file in folder_path.iterdir():
        if file.suffix == '.log.txt':
            shutil.move(file, logs_path / file.name)
        elif file.suffix == '.mail':
            shutil.move(file, mail_path / file.name)

def parse_log_files(logs_folder):
    """Parse log files for errors and warnings and write them to separate files."""
    logs_folder_path = Path(logs_folder)
    errors_path = logs_folder_path / 'errors.log'
    warnings_path = logs_folder_path / 'warnings.log'

    with errors_path.open('w') as errors_file, warnings_path.open('w') as warnings_file:
        for log_file in logs_folder_path.iterdir():
            if log_file.suffix == '.log.txt':
                with log_file.open() as lf:
                    for line in lf:
                        if 'ERROR' in line:
                            errors_file.write(line)
                        elif 'WARNING' in line:
                            warnings_file.write(line)

def count_file_types(directory):
    """Count the number of specific file types in a directory."""
    file_types = {'.txt': 0, '.mail': 0, '.log.txt': 0}
    
    directory_path = Path(directory)
    for file in directory_path.iterdir():
        if file.suffix in file_types:
            file_types[file.suffix] += 1
    
    for file_type, count in file_types.items():
        print(f"{file_type} files: {count}")

def menu():
    """Display a menu for the user to choose an automation task."""
    while True:
        print("\nAutomation Tasks:")
        print("1. Create a new folder")
        print("2. Move a deleted user's documents to a temporary folder")
        print("3. Sort documents into appropriate folders")
        print("4. Parse log files for errors and warnings")
        print("5. Count the number of specific file types in a directory")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            folder_name = input("Enter the name of the new folder: ")
            create_folder(folder_name)
        elif choice == '2':
            user_folder = input("Enter the user's folder to move documents from: ")
            temp_folder = input("Enter the temporary folder name: ")
            move_user_documents(user_folder, temp_folder)
        elif choice == '3':
            folder_path = input("Enter the path of the folder to sort documents in: ")
            sort_documents(folder_path)
        elif choice == '4':
            logs_folder = input("Enter the logs folder path to parse: ")
            parse_log_files(logs_folder)
        elif choice == '5':
            directory = input("Enter the directory to count file types in: ")
            count_file_types(directory)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    menu()
