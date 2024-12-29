import xml.etree.ElementTree as ET


def fix_mapgroupproto(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    changed_buildings = []
    for group in root.findall("group"):
        bld_name = group.get("name", "")
        old_lootmax = group.get("lootmax", "0")

        # Sum up all <point> tags in all <container> children
        total_points = 0
        for container in group.findall("container"):
            total_points += len(container.findall("point"))

        # Update lootmax if different
        if str(total_points) != old_lootmax:
            group.set("lootmax", str(total_points))
            changed_buildings.append((bld_name, old_lootmax, str(total_points)))

    # Write out the updated file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    # Print out the buildings changed
    print("Buildings with updated lootmax:")
    for bld_name, old_val, new_val in changed_buildings:
        print(f"  {bld_name}: {old_val} -> {new_val}")


if __name__ == "__main__":
    fix_mapgroupproto(
        "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml",
        "C:/Users/lewis/Documents/GitHub/DayZ-Central-Economy/respawnOffline.charnarusplus/mapgroupproto.xml",
    )
