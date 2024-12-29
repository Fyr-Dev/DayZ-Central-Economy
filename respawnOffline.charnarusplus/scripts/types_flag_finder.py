import xml.etree.ElementTree as ET


def gather_all_flags(types_file):
    tree = ET.parse(types_file)
    root = tree.getroot()
    flags = set()

    for type_elem in root.findall("type"):
        flags_elem = type_elem.find("flags")
        if flags_elem is not None:
            for flag_name in flags_elem.attrib:
                flags.add(flag_name)

    return sorted(flags)


def extract_items_with_flag(types_file, flag_name, flag_value):
    tree = ET.parse(types_file)
    root = tree.getroot()
    items = []

    for type_elem in root.findall("type"):
        item_name = type_elem.get("name")
        flags_elem = type_elem.find("flags")
        if flags_elem is not None:
            flag = flags_elem.get(flag_name)
            if flag == flag_value:
                items.append(item_name)

    return items


def update_flag_value(types_file, flag_name, item_names):
    tree = ET.parse(types_file)
    root = tree.getroot()
    updated_items = []

    for type_elem in root.findall("type"):
        item_name = type_elem.get("name")
        if item_name in item_names:
            flags_elem = type_elem.find("flags")
            if flags_elem is not None:
                current_value = flags_elem.get(flag_name)
                new_value = "0" if current_value == "1" else "1"
                flags_elem.set(flag_name, new_value)
                updated_items.append(item_name)

    # Write the updated XML back to file
    tree.write(types_file, encoding="UTF-8", xml_declaration=True)
    return updated_items


def main():
    types_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"

    all_flags = gather_all_flags(types_file)
    print("Available flags:")
    for flag in all_flags:
        print(f" - {flag}")

    flag_name = input("Enter the flag name to search for: ")
    flag_value = input("Enter the flag value to search for (e.g., 1): ")

    items = extract_items_with_flag(types_file, flag_name, flag_value)

    print(f"Items with {flag_name} set to {flag_value}:")
    for index, item in enumerate(items):
        print(f"{index + 1}. {item}")

    selected_indices = input(
        "Enter the numbers of items to change the flag value (comma-separated): "
    ).split(",")
    selected_items = [items[int(index.strip()) - 1] for index in selected_indices]

    updated_items = update_flag_value(types_file, flag_name, selected_items)

    print(f"Updated items with {flag_name} set to the opposite value:")
    for item in updated_items:
        print(f" - {item}")


if __name__ == "__main__":
    main()
