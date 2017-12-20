"""
This example prints a table that shows which profile in the texture profile is hitting which atlas.


Profile Name            | Glob Path                                        | Atlas Path
____________________________________________________________________________________________________________________________
RGBA_RGBA_2048          | /assets/atlases/effects.atlas                     | /assets/atlases/effects.atlas
RGBA_RGBA_1024          | /assets/atlases/particles.atlas                   | /assets/atlases/particles.atlas

"""

import os
import glob
import deftree


def atlas_texture_profile(project_folder, texture_profile):
    # String placements
    max_profile_string_length = 24
    max_glob_length = 50
    profile_name = "Profile Name"
    atlas_p = "| Atlas Path"
    glob_p = "| Glob Path"
    dist = (max_profile_string_length + max_glob_length + 50) * "_"

    atlas_files = list()
    for root, folders, files in os.walk(project_folder):
        [atlas_files.append(os.path.join(root, x)) for x in files if ".atlas" in x]

    tree = deftree.DefTree()
    root = tree.parse(texture_profile)
    output_string = "{}{}{}  {} {}\n{}\n".format(profile_name, (max_profile_string_length - len(profile_name)) * " ", glob_p, (max_glob_length - len(profile_name)) * " ", atlas_p, dist)

    for index, setting in enumerate(root.iter_find_elements("path_settings")):
        path = setting.get_attribute("path").value.replace('"', "")
        profile = setting.get_attribute("profile").value.replace('"', "")
        glob_hits = glob.glob(os.path.join(project_folder, path[1:]))
        for atlas in glob_hits:
            atlas_name = atlas.replace(project_folder, "")
            if atlas_name in output_string:
                continue
            output_string += "{}{}| {}{}| {}\n".format(profile, (max_profile_string_length - len(profile)) * " ", path, (max_glob_length - len(path)) * " ", atlas_name)
            if atlas in atlas_files:
                atlas_files.remove(atlas)

    for atlas in atlas_files:
        atlas_name = atlas.replace(project_folder, "")
        output_string += "{}{}| {}\n".format("", (max_profile_string_length + max_glob_length) * " ", atlas_name)

    print(output_string)
