import os
import argparse

def delete_files(file_paths, verbose=False):
    for file_path in file_paths:
        try:
            os.remove(file_path)
            if verbose:
                print(f"Deleted: {file_path}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except PermissionError:
            print(f"Permission denied: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {str(e)}")

def scan_directory(directory, files_to_find, verbose=False):
    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in files_to_find:
                full_path = os.path.abspath(os.path.join(root, file))
                found_files.append(full_path)
                if verbose:
                    print(f"Detected: {full_path}")
    return found_files

def load_malware_list(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Malware list file '{file_path}' not found.")
        return []

def main():
    parser = argparse.ArgumentParser(description="Scan and delete malware files.")
    parser.add_argument('directory', type=str, help='Directory to scan.')
    parser.add_argument('malware_file', type=str, help='File containing list of malware file names.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output.')
    
    args = parser.parse_args()
    
    # Load malware list
    files_to_find = load_malware_list(args.malware_file)

    if files_to_find:
        found_files = scan_directory(args.directory, files_to_find, args.verbose)
        if found_files:
            print("\nFound the following malware files:")
            for file in found_files:
                print(file)
                
            choice = input("\nDo you want to delete these files? (y/n): ").strip().lower()
            if choice == 'y':
                delete_files(found_files, args.verbose)
            else:
                print("No files deleted.")
        else:
            print("No viruses found.")
    else:
        print("No malware files specified.")

if __name__ == "__main__":
    main()
