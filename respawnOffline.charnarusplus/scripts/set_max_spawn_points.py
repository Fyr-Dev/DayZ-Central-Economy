import xml.etree.ElementTree as ET


def set_max_spawn_points(mapgroupproto_file, output_file):
    # Parse mapgroupproto.xml
    tree_proto = ET.parse(mapgroupproto_file)
    root_proto = tree_proto.getroot()

    # Iterate through each group and container to set lootmax to the number of points
    for group in root_proto.findall("group"):
        for container in group.findall("container"):
            points = container.findall("point")
            lootmax = len(points)
            container.set("lootmax", str(lootmax))

    # Write the updated XML back to file
    tree_proto.write(output_file, encoding="UTF-8", xml_declaration=True)
    print(f"Updated {output_file} with maximum spawn points for each container.")


# Example usage:
set_max_spawn_points(
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml",
    "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml",
)
