import xml.etree.ElementTree as ET


def update_vehicle_chances(xml_file):
    # Parse XML while preserving comments
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(xml_file, parser=parser)
    root = tree.getroot()

    in_vehicle_section = False
    modified_vehicles = []

    # Iterate through elements
    for elem in root.iter():
        if elem.tag == ET.Comment:
            comment_text = elem.text.strip()
            if comment_text == "VEHICLES":
                in_vehicle_section = True
                continue
            elif comment_text == "END OF VEHICLES":
                in_vehicle_section = False
                continue

        # Update chances in vehicle section
        if in_vehicle_section and elem.tag == "type":
            vehicle_name = elem.get("name")
            print(f"Processing: {vehicle_name}")

            for attachments in elem.findall("attachments"):
                attachments.set("chance", "1.00")
                for item in attachments.findall("item"):
                    old_chance = item.get("chance")
                    if old_chance != "1.00":
                        item.set("chance", "1.00")
                        modified_vehicles.append(f"{vehicle_name} - {item.get('name')}")

    # Save changes preserving format
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    return modified_vehicles


if __name__ == "__main__":
    xml_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/cfgspawnabletypes.xml"
    modified = update_vehicle_chances(xml_file)

    print("\nModified vehicles and attachments:")
    for item in modified:
        print(f"- {item}")
