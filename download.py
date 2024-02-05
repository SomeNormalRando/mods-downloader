import os
import pathlib
import json
# HTTP library
import requests

import logging
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S", level=logging.INFO)

from typing import List, Tuple, Set


# if True, no client-side only mods will be downloaded
NO_CLIENT_SIDE = False

MODS_LIST_FILE_PATH = "mods_list.json"
MODS_OUTPUT_DIRECTORY = "OUTPUT_MODS"


def download_fromURL_toFile(URL: str, file_path: str):
    response = requests.get(URL, stream=True)
    with open(file_path, "wb") as output_file:
        for chunk in response.iter_content(chunk_size=128):
            output_file.write(chunk)

def modrinth_getVersionFromIdOrNumber(mod_name, mod_version_number):
    api_response = requests.get(f"https://api.modrinth.com/v2/project/{mod_name}/version/{mod_version_number}")
    return api_response.json()

def modrinth_getProjectVersions(mod_ID):
    api_response = requests.get(f"https://api.modrinth.com/v2/project/{mod_ID}/version?loaders=[\"fabric\"]&game_versions=[\"1.20.1\"]")
    return api_response.json()

def download_from_mods_list(
        mods_list: List[Tuple[str, str, bool]],
        downloaded_mods_IDs: Set[str],
        dependency_IDs_unfiltered: Set[str]
):
    for [mod_name, mod_version_number, mod_client_side_only] in mods_list:
        if NO_CLIENT_SIDE is True and mod_client_side_only is True:
            logging.info("(skipped mod, NO_CLIENT_SIDE is True)")
            continue

        res = modrinth_getVersionFromIdOrNumber(mod_name, mod_version_number)

        download_URL = res["files"][0]["url"]
        filename = res["files"][0]["filename"]
        logging.info(f"downloading {mod_name}, version {mod_version_number} ({filename})")
        download_fromURL_toFile(download_URL, f"{MODS_OUTPUT_DIRECTORY}/{filename}")

        mod_project_id = res["project_id"]
        downloaded_mods_IDs.add(mod_project_id)

        for dependency in res["dependencies"]:
            if (dependency["dependency_type"] == "required"):
                dependency_IDs_unfiltered.add(dependency["project_id"])

    return (downloaded_mods_IDs, dependency_IDs_unfiltered)


print(f"\nThis script will download the mods listed in `{MODS_LIST_FILE_PATH}` into the directory (folder) of `{MODS_OUTPUT_DIRECTORY}`.\n\nThe mods will be downloaded from Modrinth (to be more specific: the URLs of the mods will be fetched from the Modrinth API, then the mods' JAR files will be downloaded from those URLs).\n\nThis, of course, requires a stable Internet connection throughout the process.")

i = input("\nDo you wish to proceed? [y]: ")

if i.lower() not in ["y", "yes"]:
    print("This script will terminate now.")
    raise SystemExit

print("\n")


with open(MODS_LIST_FILE_PATH) as mods_list_file:
    # load the contents of mods_list.json as a Python dictionary
    mods_list = json.load(mods_list_file)
    logging.info(f"loaded contents of `{MODS_LIST_FILE_PATH}`\n")

    # check if the path in OUTPUT_DIRECTORY exists and create it if it doesn't
    if not os.path.exists(MODS_OUTPUT_DIRECTORY):
        logging.info(f"NOTE: output directory `{MODS_OUTPUT_DIRECTORY}` does not exist, creating it now")
        os.makedirs(MODS_OUTPUT_DIRECTORY)

    if NO_CLIENT_SIDE is True:
        logging.info("NOTE: `NO_CLIENT_SIDE` is set to True, client-side only mods will not be downloaded")

    downloaded_mods_IDs = set()
    dependency_IDs_unfiltered = set()

    # ~ PERFORMANCE MODS
    perf_mods_list = mods_list["mods"]["performance"]

    print("\n")
    logging.info(f"fetching download URLs of {len(perf_mods_list)} performance mods...\n")

    (downloaded_mods_IDs, dependency_IDs_unfiltered) = download_from_mods_list(
        perf_mods_list, downloaded_mods_IDs, dependency_IDs_unfiltered
    )

    # ~ UTILITY MODS
    utility_mods_list = mods_list["mods"]["utility"]

    print("\n")
    logging.info(f"fetching download URLs of {len(utility_mods_list)} utility mods...\n")

    (downloaded_mods_IDs, dependency_IDs_unfiltered) = download_from_mods_list(
        utility_mods_list, downloaded_mods_IDs, dependency_IDs_unfiltered
    )

    # ~ CONTENT MODS
    content_mods_list = mods_list["mods"]["content"]

    print("\n")
    logging.info(f"fetching download URLs of {len(content_mods_list)} content mods...\n")

    (downloaded_mods_IDs, dependency_IDs_unfiltered) = download_from_mods_list(
        content_mods_list, downloaded_mods_IDs, dependency_IDs_unfiltered
    )

    # ~ DEPENDENCY MODS
    # remove dependencies that are in the mods list JSON file (they've already been downloaded)
    dependency_IDs_filtered = dependency_IDs_unfiltered - downloaded_mods_IDs

    print("\n")
    logging.info(f"fetching download URLs of dependency mods...\n")

    for dependency_mod_ID in dependency_IDs_filtered:
        res = modrinth_getProjectVersions(dependency_mod_ID)

        download_URL = res[0]["files"][0]["url"]
        filename = res[0]["files"][0]["filename"]
        logging.info(f"downloading {filename}")
        download_fromURL_toFile(download_URL, f"{MODS_OUTPUT_DIRECTORY}/{filename}")

        # dependencies of this dependency (if any)
        d_dependencies = res[0]["dependencies"]
        for d in d_dependencies:
            project_id = d["project_id"]
            if d["dependency_type"] == "required" and project_id not in downloaded_mods_IDs and project_id not in dependency_IDs_filtered:
                r = modrinth_getProjectVersions(project_id)

                download_URL = r[0]["files"][0]["url"]
                filename = r[0]["files"][0]["filename"]
                logging.info(f"downloading {filename}")
                download_fromURL_toFile(download_URL, f"{MODS_OUTPUT_DIRECTORY}/{filename}")

print("\n")
print(f"done!\n\nall your mods should now be in {pathlib.Path(__file__).parent.resolve()}\\{MODS_OUTPUT_DIRECTORY}")

print("\n")
input("(press enter to close)\n")