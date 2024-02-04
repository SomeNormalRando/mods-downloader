import os
import json
# HTTP library
import requests

import logging
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S", level=logging.INFO)


# if True, no client-side only mods will be downloaded
NO_CLIENT_SIDE = False

MODS_LIST_FILE_PATH = "mods_list.json"
MODS_OUTPUT_DIRECTORY = "OUTPUT_MODS"


def get_modrinth_download_URL(slug, version_id):
    response = requests.get(f"https://api.modrinth.com/v2/project/{slug}/version/{version_id}")

    response_JSON = response.json()

    return response_JSON["files"][0]["url"]

def download_fromURL_toFile(URL, file_path):
    response = requests.get(URL, stream=True)
    with open(file_path, "wb") as output_file:
        for chunk in response.iter_content(chunk_size=128):
            output_file.write(chunk)


def download_from_mods_list(mods_list, output_directory_path):
    for [mod_name, version_number, client_side_only] in mods_list:
        if NO_CLIENT_SIDE is True and client_side_only is True:
            logging.info("(skipped mod, NO_CLIENT_SIDE is True)")
            continue
        
        URL = get_modrinth_download_URL(mod_name, version_number)
        
        logging.info(f"downloading {mod_name}, version {version_number}")

        filename = URL.split("/")[-1]
        download_fromURL_toFile(URL, f"{output_directory_path}/{filename}")


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

    # PERFORMANCE MODS
    perf_mods_list = mods_list["mods"]["performance"]

    print("\n")
    logging.info(f"fetching download URLS of {len(perf_mods_list)} performance mods...\n")

    download_from_mods_list(perf_mods_list, MODS_OUTPUT_DIRECTORY)

    # UTILITY MODS
    utility_mods_list = mods_list["mods"]["utility"]

    print("\n")
    logging.info(f"fetching download URLS of {len(utility_mods_list)} utility mods...\n")

    download_from_mods_list(utility_mods_list, MODS_OUTPUT_DIRECTORY)

    # CONTENT MODS
    content_mods_list = mods_list["mods"]["content"]

    print("\n")
    logging.info(f"fetching download URLS of {len(content_mods_list)} content mods...\n")

    download_from_mods_list(content_mods_list, MODS_OUTPUT_DIRECTORY)

    # DEPENDENCY MODS
    dependencies_mods_list = mods_list["mods"]["dependencies"]

    print("\n")
    logging.info(f"fetching download URLS of {len(content_mods_list)} dependency mods...\n")

    download_from_mods_list(dependencies_mods_list, MODS_OUTPUT_DIRECTORY)
