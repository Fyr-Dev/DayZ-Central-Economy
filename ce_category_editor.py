"""
DayZ Central Economy Category Editor

This script allows you to set all nominal and min values to zero for items
in a specific category (section) in the types.xml file.

Usage:
    python ce_category_editor.py

The script will prompt you for:
1. The types.xml file path (or use default)
2. The category name (e.g., "ATTACHMENTS", "FIREARMS", etc.)
3. Confirmation before saving changes
"""

import os
import re
import sys


def get_categories(xml_file):
    """Extract all category headers from the file"""
    with open(xml_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!--####################\s+(.*?)\s+####################-->"
    matches = re.findall(pattern, content)

    return matches


def process_xml_file(xml_file, target_category):
    """Process the XML file and set nominal and min values to 0 for the specified category"""
    with open(xml_file, "r", encoding="utf-8") as f:
        content = f.read()

    category_pattern = (
        f"<!--####################\\s+{target_category}\\s+####################-->"
    )
    category_match = re.search(category_pattern, content)

    if not category_match:
        print(f"Category '{target_category}' not found in the file.")
        return None

    start_pos = category_match.start()

    next_category_pattern = r"<!--####################\s+.*?\s+####################-->"
    next_matches = list(re.finditer(next_category_pattern, content[start_pos + 1 :]))

    if next_matches:
        end_pos = start_pos + 1 + next_matches[0].start()
    else:
        end_pos = len(content)

    section_to_modify = content[start_pos:end_pos]

    modified_section = re.sub(
        r"(<nominal>)(\d+)(</nominal>)", r"\g<1>0\g<3>", section_to_modify
    )
    modified_section = re.sub(r"(<min>)(\d+)(</min>)", r"\g<1>0\g<3>", modified_section)

    modified_content = content[:start_pos] + modified_section + content[end_pos:]

    original_nominals = re.findall(r"<nominal>\d+</nominal>", section_to_modify)
    re.findall(r"<nominal>\d+</nominal>", modified_section)

    # Check if any changes were made
    if section_to_modify == modified_section:
        print(
            f"No changes were needed for category '{target_category}'. All items may already be set to 0."
        )
        return None

    return modified_content, len(original_nominals)


def save_file(xml_file, content):
    """Save the modified content to the file"""
    backup_file = f"{xml_file}.backup"
    if not os.path.exists(backup_file):
        with open(xml_file, "r", encoding="utf-8") as f_in:
            with open(backup_file, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
        print(f"Created backup at: {backup_file}")

    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"File saved successfully: {xml_file}")


def main():
    """Main function to run the script"""
    print("DayZ Central Economy Category Editor")
    print("===================================")

    default_path = os.path.join("dayzOffline.charnarusplus", "db", "types", "types.xml")
    backup_path = os.path.join(
        "dayzOffline.charnarusplus", "db", "backup.types", "organized_types.xml"
    )

    if os.path.exists(default_path):
        suggested_path = default_path
    elif os.path.exists(backup_path):
        suggested_path = backup_path
    else:
        suggested_path = ""

    xml_file = input(
        f"Enter the path to the types.xml file [{suggested_path}]: "
    ).strip()
    if not xml_file:
        xml_file = suggested_path

    if not os.path.exists(xml_file):
        print(f"Error: File '{xml_file}' not found.")
        sys.exit(1)

    categories = get_categories(xml_file)
    if not categories:
        print("No categories found in the file.")
        sys.exit(1)

    print("\nAvailable categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")

    choice = input("\nEnter the number or name of the category to modify: ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(categories):
            target_category = categories[idx]
        else:
            print("Invalid selection. Please enter a valid number or category name.")
            sys.exit(1)
    except ValueError:
        target_category = choice.upper()
        if target_category not in categories:
            print(f"Warning: '{target_category}' not found in the list of categories.")
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != "y":
                sys.exit(0)

    result = process_xml_file(xml_file, target_category)
    if result is None:
        sys.exit(0)

    modified_content, item_count = result

    print(f"\nFound {item_count} items in the '{target_category}' category.")
    confirm = (
        input("Do you want to set all nominal and min values to 0? (y/n): ")
        .strip()
        .lower()
    )
    if confirm != "y":
        print("Operation cancelled.")
        sys.exit(0)

    save_file(xml_file, modified_content)
    print(f"Successfully set {item_count} items in '{target_category}' to 0.")


if __name__ == "__main__":
    main()
