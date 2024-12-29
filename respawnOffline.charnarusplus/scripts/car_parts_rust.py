import xml.etree.ElementTree as ET


def find_rust_parts(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rust_parts = []

    for type_elem in root.findall("type"):
        name = type_elem.get("name", "")
        if "Rust" in name and any(
            car_part in name
            for car_part in [
                "Door",
                "Hood",
                "Trunk",
                "Wheel",
                "Battery",
                "Radiator",
                "SparkPlug",
                "Headlight",
            ]
        ):
            rust_parts.append(name)

    return sorted(rust_parts)


if __name__ == "__main__":
    xml_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"
    rust_parts = find_rust_parts(xml_file)

    print("\nFound rusted car parts:")
    for part in rust_parts:
        print(f"- {part}")
