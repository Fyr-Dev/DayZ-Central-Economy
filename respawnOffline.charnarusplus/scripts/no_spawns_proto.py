import xml.etree.ElementTree as ET


def find_buildings_without_spawn_points(mapgroupproto_file):
    tree = ET.parse(mapgroupproto_file)
    root = tree.getroot()

    buildings_without_spawn_points = []

    for group in root.findall("group"):
        bld_name = group.get("name", "")
        total_points = 0

        for container in group.findall("container"):
            total_points += len(container.findall("point"))

        if total_points == 0:
            buildings_without_spawn_points.append(bld_name)

    return buildings_without_spawn_points


if __name__ == "__main__":
    mapgroupproto_file = "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml"
    buildings_without_spawn_points = find_buildings_without_spawn_points(
        mapgroupproto_file
    )

    print("Buildings without spawn points:")
    for bld_name in buildings_without_spawn_points:
        print(f"  {bld_name}")
