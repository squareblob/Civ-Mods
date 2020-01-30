import re
import urllib.request
import pprint
import json
from shutil import copyfile
import requests
from pathlib import Path

with open('mods.json') as f:
    mods = json.load(f)

input = "install minihud voxelmap bettersprinting worldedit noteblockdisplays mousewheelie optifine"
setversion = "1.14"
setmodloader = "fabric"

repo = "https://raw.githubusercontent.com/squareblob/Civ-Mods/1.14/configs/"

downloaded = []
required = []
command = input.split(" ")[0]
configonly = False
jaronly = False

if command == "list":
    output = ""
    for i in range(0, len(mods['mods'])):
        output += str(mods['mods'][i]['name']) + " "
    print(output)


elif command == "install":
    if minecraft_location == "":
        print("error : set minecraft location")
        exit()

    packages = input.split(" ")[1:]
    o = 0
    while o < len(packages):
        package = packages[o]
        o += 1
        group = "civdefault"
        if package.startswith("--"):
            if package == "--config-only":
                configonly = True
            elif package == "--jar-only":
                jaronly = True
        elif package.startswith("-"):
            group = package.replace("-", "")
        else:
            package_found = False
            for i in range(0, len(mods['mods'])):
                if package.casefold() == mods['mods'][i]['name'].casefold():
                    package_found = True
                    global_config = mods['mods'][i]['config']
                    tests = {"modloader_found": False, "version_found": False}
                    for j in range(0, len(mods['mods'][i]['versions'])):
                        jar_url = mods['mods'][i]['versions'][j]['jar_url']

                        requirements = mods['mods'][i]['versions'][j]["require"]
                        check_version = re.match("\d+\.\d+",requirements['minecraft']).group(0) == setversion
                        check_modloader = requirements['modloader'] == setmodloader
                        if requirements['modloader'] is None or requirements['modloader'] == "" or requirements['modloader'] == "*":
                            check_modloader = True

                        tests["modloader_found"] = tests["modloader_found"] or check_modloader
                        tests["version_found"] = tests["version_found"] or check_version

                        if check_version and check_modloader:
                            try:
                                if not configonly:
                                    jar_request = urllib.request.urlopen(jar_url)
                                    location = minecraft_location + "/mods"

                                    if 'type' in mods['mods'][i].keys():
                                        if mods['mods'][i]['type'] == "resourcepack":
                                            location = minecraft_location + "/resourcepacks"

                                    Path(location).mkdir(parents=True, exist_ok=True)

                                    with open(location + "/" + str(jar_url.rsplit('/', 1)[-1]), 'wb') as f:
                                        f.write(jar_request.read())
                                    print("downloaded " + str(jar_url.rsplit('/', 1)[-1]))
                                    downloaded.append(package)

                                    if 'dependencies' in requirements:
                                        print("    required dependencies: " + " ".join(requirements['dependencies']))
                                        for dependency in requirements['dependencies']:
                                            if dependency not in packages:
                                                packages.append(dependency)
                                            if dependency not in required:
                                                required.append(dependency)

                                if not jaronly:
                                    for file in global_config.keys():
                                        url = str(repo) + str(package) + "/" + str(group) + "/" + str(file)
                                        r = requests.get(url)

                                        with open(str(file), 'w') as f:
                                            f.write(r.text)

                                        inner_location = "".join(global_config[file].rsplit('/', 1)[:-1])
                                        location = minecraft_location + inner_location
                                        Path(location).mkdir(parents=True, exist_ok=True)
                                        copyfile(str(file), minecraft_location + global_config[file])
                                        print("config : downloaded " + str(file))
                            except Exception as e:
                                print("failed to download \'" + package + "\': file url did not resolve")
                    if not(tests["modloader_found"] and tests["version_found"]):
                        error_msg = ""
                        error_msg += "failed to download \'" + package + "\'"
                        if not tests["version_found"]:
                            error_msg += "(No version (game version=[" + str(setversion) + "]) found)"
                        if not tests["modloader_found"]:
                            error_msg += " (No version (modloader version=[" + str(setmodloader) + "]) found)"
                        print(error_msg)
            if not package_found:
                print("package \'" +package + "\' could not be found")
    for p in required:
        if p not in downloaded:
            print("error : dependency "+ p + " could not be found")