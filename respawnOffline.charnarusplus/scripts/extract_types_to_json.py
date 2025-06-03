import xml.etree.ElementTree as ET
import json

# Load and parse XML
tree = ET.parse(
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/types.xml"
)
root = tree.getroot()

# Extract type names and prepare JSON structure
output = []
for type_elem in root.findall("type"):
    name = type_elem.attrib.get("name")
    if name:
        output.append({"type_name": name, "human_name": ""})

# Write to JSON file
with open(
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/db/type_names_human.json",
    "w",
) as f:
    json.dump(output, f, indent=2)

print("JSON file with type names and editable human_name fields created.")
