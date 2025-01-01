import xml.etree.ElementTree as ET


def adjust_civilian_clothing(xml_file, reduction_percent):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(xml_file, parser=parser)
    root = tree.getroot()

    modified_items = []
    military_tags = ["military", "police", "hunting"]

    for type_elem in root.findall("type"):
        usage = type_elem.find("usage")
        if usage is not None and usage.text is not None:
            name = type_elem.get("name")
            nominal = type_elem.find("nominal")
            min_elem = type_elem.find("min")

            if nominal is not None and int(nominal.text) > 20:
                usage_text = usage.text.lower()

                if not any(tag in usage_text for tag in military_tags):
                    old_nominal = int(nominal.text)
                    old_min = int(min_elem.text) if min_elem is not None else 0

                    # Calculate new values
                    new_nominal = int(old_nominal * (1 - reduction_percent / 100))
                    new_min = int(old_min * (1 - reduction_percent / 100))

                    # Ensure minimums of 1
                    new_nominal = max(1, new_nominal)
                    new_min = max(1, new_min)

                    # Update values
                    nominal.text = str(new_nominal)
                    if min_elem is not None:
                        min_elem.text = str(new_min)

                    modified_items.append(
                        {
                            "name": name,
                            "old_nominal": old_nominal,
                            "new_nominal": new_nominal,
                            "old_min": old_min,
                            "new_min": new_min,
                        }
                    )

    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    return modified_items


if __name__ == "__main__":
    xml_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"
    reduction_percent = 50  # Reduce by 50%

    modified = adjust_civilian_clothing(xml_file, reduction_percent)

    print("\nModified civilian clothing spawns:")
    for item in modified:
        print(f"- {item['name']}:")
        print(f"  Nominal: {item['old_nominal']} → {item['new_nominal']}")
        print(f"  Min: {item['old_min']} → {item['new_min']}")
