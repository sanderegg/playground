# Example usage:
# sleep_and_print(5)
import time
import argparse
import os
import getpass

def sleep_and_print(seconds):
    for i in range(seconds):
        remaining = seconds - i - 1
        print(f"Step {i + 1}: Sleeping for 1 second... {remaining} seconds remaining.")
        time.sleep(1)
    print(f"Slept for {seconds} seconds in total.")


def print_working_directory_file_rights_and_user_info():
    cwd = os.getcwd()
    print(f"Current Working Directory: {cwd}")

    username = getpass.getuser()
    user_id = os.getuid()
    print(f"Current User: {username} (UID: {user_id})")

    files = os.listdir(cwd)
    if not files:
        print("No files found in the current working directory.")
    else:
        print("File Access Rights:")
        for file in files:
            if os.path.isfile(file):
                rights = ""
                rights += "r" if os.access(file, os.R_OK) else "-"
                rights += "w" if os.access(file, os.W_OK) else "-"
                rights += "x" if os.access(file, os.X_OK) else "-"
                print(f"{file}: {rights}")

def main():
    parser = argparse.ArgumentParser(description="Sleep for a given number of seconds and print each second passed with remaining time.")
    parser.add_argument("seconds", type=int, help="Number of seconds to sleep")
    args = parser.parse_args()

    print_working_directory_file_rights_and_user_info()
    sleep_and_print(args.seconds)

if __name__ == "__main__":
    main()

