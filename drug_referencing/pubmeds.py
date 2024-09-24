"""
Module to retrieve and manage medical publications
"""
import json
import lib.common_funtions as com_fun


def get_pubmed():
    """
    Find all medical publications listed in CSV/JSON local files

    Output:
    - pubmed_unique_list (list) : list of medical publications
    """
    pubmed_dir = com_fun.get_data_folder("pubmed")
    all_pubmed_list = []  # List of all pubmed
    for file in com_fun.get_files(pubmed_dir, ".csv"):
        com_fun.write_logs(f"Medical publications file {file}", "INFO")
        all_pubmed_list.extend(com_fun.extract_csv(file))

    for file in com_fun.get_files(pubmed_dir, ".json"):
        com_fun.write_logs(f"Medical publications file {file}", "INFO")
        with open(file) as pubmeds_file:  # noqa # pylint: disable=unspecified-encoding
            raw_json_data = pubmeds_file.read().replace(
                "\n", ""
            )  # noqa # Read the json data
            # Remove the trailing comma
            clean_json_data = "}]".join(raw_json_data.rsplit("},]", 1))
            pubmed_json_dict = json.loads(clean_json_data)  # Load JSON data
            all_pubmed_list.extend(pubmed_json_dict)

    for e in all_pubmed_list.copy():
        # If there's not title nor journal for the line, remove it
        if not (e["title"] or e["journal"]):
            all_pubmed_list.remove(e)

    # Deduplication
    pubmed_unique_list = [
        dict(t) for t in {tuple(d.items()) for d in all_pubmed_list}
    ]

    com_fun.write_logs(
        f"List of all medical publications found : {pubmed_unique_list}",
        "INFO")

    com_fun.export_to_json(pubmed_unique_list, "./pubmeds_list.json")

    return pubmed_unique_list
