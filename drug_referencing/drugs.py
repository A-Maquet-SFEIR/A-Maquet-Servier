"""
Module to retrieve and manage drugs
"""
import library.common_funtions as com_fun


def get_drugs():
    """
    Find all drugs listed in CSV local files

    Output:
    - drugs_unique_list (list) : list of drugs
    """
    drugs_dir = com_fun.get_data_folder("drugs")
    all_drugs_list = []  # List of all drugs
    for file in com_fun.get_files(drugs_dir, ".csv"):
        com_fun.write_logs(f"Drugs file {file}", "INFO")
        all_drugs_list.extend(com_fun.extract_csv(file))

    # Deduplicate drug list
    drugs_unique_list = list(
        {drug["atccode"]: drug for drug in all_drugs_list}.values()
    )

    com_fun.write_logs(
        f"List of all drugs found : {drugs_unique_list}",
        "INFO")

    com_fun.export_to_json(drugs_unique_list, "./drugs_list.json")

    return drugs_unique_list
