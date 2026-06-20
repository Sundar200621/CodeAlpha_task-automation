import os
import shutil
import re
import requests


def move_jpg_files():
    source = input("Enter source folder path: ").strip()
    destination = input("Enter destination folder path: ").strip()

    if not os.path.isdir(source):
        print("Source folder does not exist.\n")
        return

    if not os.path.exists(destination):
        os.makedirs(destination)

    moved_count = 0
    for filename in os.listdir(source):
        if filename.lower().endswith(".jpg"):
            src_path = os.path.join(source, filename)
            dest_path = os.path.join(destination, filename)
            shutil.move(src_path, dest_path)
            moved_count += 1
            print(f"Moved: {filename}")

    print(f"\nDone! {moved_count} .jpg file(s) moved to '{destination}'.\n")


def extract_emails():
    input_file = input("Enter path to .txt file to read from: ").strip()
    output_file = input("Enter path to .txt file to save emails to: ").strip()

    if not os.path.isfile(input_file):
        print("Input file does not exist.\n")
        return

    with open(input_file, "r") as f:
        content = f.read()

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, content)
    unique_emails = sorted(set(emails))

    with open(output_file, "w") as f:
        for email in unique_emails:
            f.write(email + "\n")

    print(f"\nDone! {len(unique_emails)} unique email(s) saved to '{output_file}'.\n")


def scrape_title():
    url = input("Enter webpage URL: ").strip()
    output_file = input("Enter filename to save the title to (e.g., title.txt): ").strip()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}\n")
        return

    match = re.search(r"<title>(.*?)</title>", response.text, re.IGNORECASE | re.DOTALL)
    title = match.group(1).strip() if match else "No title found"

    with open(output_file, "w") as f:
        f.write(title)

    print(f"\nPage title: {title}")
    print(f"Saved to '{output_file}'.\n")


def main():
    print("Task Automation Menu")
    print("1. Move all .jpg files from one folder to another")
    print("2. Extract email addresses from a .txt file")
    print("3. Scrape the title of a webpage")

    choice = input("\nChoose an option (1/2/3): ").strip()

    if choice == "1":
        move_jpg_files()
    elif choice == "2":
        extract_emails()
    elif choice == "3":
        scrape_title()
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
