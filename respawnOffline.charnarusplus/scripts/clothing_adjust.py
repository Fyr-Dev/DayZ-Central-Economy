import xml.etree.ElementTree as ET


def adjust_civilian_clothing(xml_file, reduction_percent):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(xml_file, parser=parser)
    root = tree.getroot()

    modified_items = []
    military_tags = ["military", "police", "hunting"]

    for type_elem in root.findall("type"):
        # Check if it's clothing
        category = type_elem.find("category")
        if category is not None and category.get("name") == "clothes":
            name = type_elem.get("name")
            nominal = type_elem.find("nominal")
            min_elem = type_elem.find("min")
            usages = type_elem.findall("usage")

            # Check if any usage is a military-related tag
            has_military_tag = any(
                usage.get("name", "").lower() in military_tags for usage in usages
            )

            if nominal is not None and int(nominal.text) > 20 and not has_military_tag:
                old_nominal = int(nominal.text)
                old_min = int(min_elem.text) if min_elem is not None else 0

                # Calculate new values
                new_nominal = max(1, int(old_nominal * (1 - reduction_percent / 100)))
                new_min = max(1, int(old_min * (1 - reduction_percent / 100)))

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

    # Ask for reduction percentage
    while True:
        try:
            reduction_percent = float(input("Enter reduction percentage (1-99): "))
            if 1 <= reduction_percent <= 99:
                break
            else:
                print("Please enter a number between 1 and 99")
        except ValueError:
            print("Please enter a valid number")

    modified = adjust_civilian_clothing(xml_file, reduction_percent)

    print(f"\nModified civilian clothing spawns (reduced by {reduction_percent}%):")
    for item in modified:
        print(f"- {item['name']}:")
        print(f"  Nominal: {item['old_nominal']} → {item['new_nominal']}")
        print(f"  Min: {item['old_min']} → {item['new_min']}")
