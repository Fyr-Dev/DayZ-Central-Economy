import xml.etree.ElementTree as ET


def update_vehicle_attachment_chances(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    in_vehicle_section = False

    for elem in root.iter():
        if elem.tag is ET.Comment and elem.text.strip() == "VEHICLES":
            in_vehicle_section = True
            continue
        if elem.tag is ET.Comment and elem.text.strip() == "END OF VEHICLES":
            in_vehicle_section = False
            continue

        if in_vehicle_section and elem.tag == "attachments":
            for item in elem.findall("item"):
                item.set("chance", "1.00")

    tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    input_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/cfgspawnabletypes.xml"
    output_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/cfgspawnabletypes.xml"
    update_vehicle_attachment_chances(input_file, output_file)

    print(f"Updated vehicle attachment chances in {output_file}")
