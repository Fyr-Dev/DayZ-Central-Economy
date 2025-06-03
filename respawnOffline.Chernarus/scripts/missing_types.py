import os
import xml.etree.ElementTree as ET


def find_all_types_files(root_dir):
    types_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "types.xml":
                types_files.append(os.path.join(dirpath, filename))
    return types_files


def extract_types_from_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    types = set()
    for type_elem in root.findall("type"):
        type_name = type_elem.get("name")
        if type_name:
            types.add(type_name)
    return types


def create_empty_types_file(file_path):
    root = ET.Element("types")
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding="UTF-8", xml_declaration=True)


def add_missing_types(source_files, target_file):
    # Check if the target file exists, if not, create it
    if not os.path.exists(target_file):
        create_empty_types_file(target_file)

    # Extract types from the target file
    target_tree = ET.parse(target_file)
    target_root = target_tree.getroot()
    target_types = extract_types_from_file(target_file)

    # Extract types from all source files
    all_source_types = set()
    for source_file in source_files:
        if source_file != target_file:
            source_types = extract_types_from_file(source_file)
            all_source_types.update(source_types)

    # Find missing types
    missing_types = all_source_types - target_types

    # Add missing types to the target file
    added_types = []
    for source_file in source_files:
        if source_file != target_file:
            source_tree = ET.parse(source_file)
            source_root = source_tree.getroot()
            for type_elem in source_root.findall("type"):
                type_name = type_elem.get("name")
                if type_name in missing_types and type_name not in target_types:
                    target_root.append(type_elem)
                    target_types.add(type_name)
                    added_types.append(type_name)

    # Write the updated target file
    target_tree.write(target_file, encoding="UTF-8", xml_declaration=True)
    print(f"Added {len(added_types)} missing types to {target_file}")

    # Print the list of added types
    print("List of added types:")
    for type_name in added_types:
        print(f" - {type_name}")


# Example usage:
root_directory = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy"
target_directory = (
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.Chernarus/db"
)

all_types_files = find_all_types_files(root_directory)
target_types_file = os.path.join(target_directory, "types.xml")

add_missing_types(all_types_files, target_types_file)
