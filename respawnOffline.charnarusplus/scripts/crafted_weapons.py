import xml.etree.ElementTree as ET


def set_crafted_for_weapons(xml_input, xml_output):
    tree = ET.parse(xml_input)
    root = tree.getroot()

    changed_weapons = []

    for type_elem in root.findall("type"):
        category_elem = type_elem.find("category")
        flags_elem = type_elem.find("flags")

        # Check if it has a category = "weapons"
        if category_elem is not None and category_elem.get("name") == "weapons":
            if flags_elem is not None:
                # Set crafted to 0
                flags_elem.set("crafted", "0")
                # Store the weapon name in our list
                item_name = type_elem.get("name")
                if item_name:
                    changed_weapons.append(item_name)

    # Write modified XML back to file
    tree.write(xml_output, encoding="UTF-8", xml_declaration=True)

    # Print the list of changed weapons
    print("Weapons changed to crafted=0:")
    for weapon in changed_weapons:
        print(f" - {weapon}")


set_crafted_for_weapons(
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml",
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml",
)
