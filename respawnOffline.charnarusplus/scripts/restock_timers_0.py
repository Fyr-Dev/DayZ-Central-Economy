import xml.etree.ElementTree as ET


def update_restock_times(types_file):
    tree = ET.parse(types_file)
    root = tree.getroot()

    changed_items = []

    for type_elem in root.findall("type"):
        restock_elem = type_elem.find("restock")
        if restock_elem is not None:
            restock_elem.text = "0"
            item_name = type_elem.get("name")
            if item_name:
                changed_items.append(item_name)

    # Write the updated XML back to file
    tree.write(types_file, encoding="UTF-8", xml_declaration=True)
    print(f"Updated {types_file} with restock times set to 0.")

    # Print the list of changed items
    print("List of changed items:")
    for item_name in changed_items:
        print(f" - {item_name}")


# Example usage:
types_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"
update_restock_times(types_file)
