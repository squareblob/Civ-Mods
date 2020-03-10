import argparse
import re
import urllib.request
import pprint
import json
import requests
from pathlib import Path
from os import path as ospath
import sys
import pickle


def run(setminecraftloc, setversion, setmodloader, input):
    repo = "https://raw.githubusercontent.com/squareblob/Civ-Mods/1.14/configs/"

    with open('mods.json') as f:
        mods = json.load(f)

    downloaded = []
    required = []

    configonly = False
    jaronly = False
    overwrite = False

    command = input.split(" ")[0]

    # Create an issue to add a config (or clone the repo)
    config_choices = []

    if command == "list":
        output = ""
        for i in range(0, len(mods['mods'])):
            output += str(mods['mods'][i]['name']) + " "
        print(output)

    elif command == "install":
        if setminecraftloc == "":
            print("error : set minecraft location")
            exit()

        packages = input.split(" ")[1:]
        packages = list(set(packages))

        o = 0
        while o < len(packages):
            package = packages[o]
            o += 1
            if package.startswith("--"):
                if package == "--config-only":
                    configonly = True
                elif package == "--jar-only":
                    jaronly = True
                elif package == "--overwrite":
                    overwrite = True
            elif package.startswith("-"):
                config_choices.append(package.replace("-", ""))  # = package.replace("-", "")
            else:
                config_choices_for_package = ["civdefault"]
                if config_choices:
                    config_choices_for_package = config_choices.copy()
                config_choices = []

                package_found = False
                for i in range(0, len(mods['mods'])):
                    if package.casefold() == mods['mods'][i]['name'].casefold():
                        package_found = True
                        global_config = mods['mods'][i]['config']
                        tests = {"modloader_found": False, "version_found": False}
                        for j in range(0, len(mods['mods'][i]['versions'])):
                            jar_url = mods['mods'][i]['versions'][j]['jar_url']

                            requirements = mods['mods'][i]['versions'][j]["require"]
                            check_version = re.match("\d+\.\d+", requirements['minecraft']).group(0) == setversion
                            check_modloader = requirements['modloader'] == setmodloader
                            if requirements['modloader'] is None or requirements['modloader'] == "" or requirements[
                                'modloader'] == "*":
                                check_modloader = True

                            tests["modloader_found"] = tests["modloader_found"] or check_modloader
                            tests["version_found"] = tests["version_found"] or check_version

                            if check_version and check_modloader:
                                try:
                                    if not configonly:
                                        jar_request = urllib.request.urlopen(jar_url)
                                        location = setminecraftloc + "/mods"

                                        if 'type' in mods['mods'][i].keys():
                                            if mods['mods'][i]['type'] == "resourcepack":
                                                location = setminecraftloc + "/resourcepacks"

                                        Path(location).mkdir(parents=True, exist_ok=True)

                                        path_exists = ospath.exists(location + "/" + str(jar_url.rsplit('/', 1)[-1]))
                                        if (path_exists and overwrite) or not path_exists:
                                            with open(location + "/" + str(jar_url.rsplit('/', 1)[-1]), 'wb') as f:
                                                f.write(jar_request.read())

                                            print("downloaded " + str(jar_url.rsplit('/', 1)[-1]))
                                            downloaded.append(package)

                                        if 'dependencies' in requirements:
                                            print(
                                                "    required dependencies: " + " ".join(requirements['dependencies']))
                                            for dependency in requirements['dependencies']:
                                                if dependency not in packages:
                                                    packages.append(dependency)
                                                if dependency not in required:
                                                    required.append(dependency)

                                    if not jaronly:
                                        for config_choice in config_choices_for_package:
                                            for file in global_config.keys():
                                                url = str(repo) + str(package) + "/" + str(config_choice) + "/" + str(
                                                    file)
                                                r = requests.get(url)
                                                if r.status_code == 404:
                                                    print(
                                                        "failed to find " + str(file) + " config with choice \'" + str(
                                                            config_choice) + "\'")
                                                else:
                                                    inner_location = "".join(global_config[file].rsplit('/', 1)[:-1])
                                                    location = setminecraftloc + inner_location
                                                    Path(location).mkdir(parents=True, exist_ok=True)

                                                    path_exists = ospath.exists(
                                                        setminecraftloc + global_config[file])
                                                    if (path_exists and overwrite) or not path_exists:
                                                        with open(setminecraftloc + global_config[file], 'w') as f:
                                                            f.write(r.text)

                                                        # copyfile(str(file), minecraft_location + global_config[file])
                                                        print("config : downloaded " + str(file))
                                except Exception as e:
                                    # print(e)
                                    print("failed to download \'" + package + "\': file url did not resolve")
                        if not (tests["modloader_found"] and tests["version_found"]):
                            error_msg = ""
                            error_msg += "failed to download \'" + package + "\'"
                            if not tests["version_found"]:
                                error_msg += "(No version (game version=[" + str(setversion) + "]) found)"
                            if not tests["modloader_found"]:
                                error_msg += " (No version (modloader version=[" + str(setmodloader) + "]) found)"
                            print(error_msg)
                if not package_found:
                    print("package \'" + package + "\' could not be found")
        for p in required:
            if p not in downloaded:
                print("error : dependency " + p + " could not be found")


def main():
    #this is terrible
    config = {
        "minecraftloc": None,
        "version": None,
        "modloader": None
    }

    try:
        with open('config.pickle', 'rb') as handle:
            config = pickle.load(handle)
    except:
        pass

    input = None

    for i in range(0, len(sys.argv[1:])):
        if i + 1 < len(sys.argv[1:]):
            if sys.argv[1:][i] == "--setminecraftloc":
                config["minecraftloc"] = " ".join(sys.argv[2 + i:])
            elif sys.argv[1:][i] == "--setversion":
                config["version"] = sys.argv[1:][i+1]
            elif sys.argv[1:][i] == "--setmodloader":
                config["modloader"] = sys.argv[1:][i+1]
            elif sys.argv[1:][i] == "install":
                input = " ".join(sys.argv[1 + i:])

    with open('config.pickle', 'wb') as handle:
        pickle.dump(config, handle, protocol=pickle.HIGHEST_PROTOCOL)

    for x in config.keys():
        print(x + ": " + str(config[x]))

    if config["minecraftloc"] is None or config["version"] is None or config["modloader"] is None:
        print("Error : You must have used \"--setminecraftloc\" and \"--setversion\" and \"--setmodloader\"")
    else:
        if input is not None:
            run(config["minecraftloc"], config["version"], config["modloader"], input)


if __name__ == "__main__":
    main()