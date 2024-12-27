import xml.etree.ElementTree as ET


def update_item_counts(types_file):
    tree = ET.parse(types_file)
    root = tree.getroot()

    changed_items = []

    for type_elem in root.findall("type"):
        item_changed = False

        # Find the flags element
        flags_elem = type_elem.find("flags")
        if flags_elem is not None:
            # Update count_in_cargo attribute
            if flags_elem.get("count_in_cargo") == "1":
                flags_elem.set("count_in_cargo", "0")
                item_changed = True

            # Update count_in_hoarder attribute
            if flags_elem.get("count_in_hoarder") == "1":
                flags_elem.set("count_in_hoarder", "0")
                item_changed = True

            # Update count_in_player attribute
            if flags_elem.get("count_in_player") == "1":
                flags_elem.set("count_in_player", "0")
                item_changed = True

        if item_changed:
            item_name = type_elem.get("name")
            if item_name:
                changed_items.append(item_name)

    # Write the updated XML back to file
    tree.write(types_file, encoding="UTF-8", xml_declaration=True)
    print(
        f"Updated {types_file} with count_in_cargo, count_in_hoarder, and count_in_player set to 0."
    )

    # Print the list of changed items
    print("List of changed items:")
    for item_name in changed_items:
        print(f" - {item_name}")


# Example usage:
types_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"
update_item_counts(types_file)
