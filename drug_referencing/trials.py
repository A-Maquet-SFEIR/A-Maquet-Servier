"""
Module to retrieve and manage trials
"""
import library.common_funtions as com_fun


def get_clinical_trials():
    """
    Find all clinical trials listed in CSV local files

    Output:
    - trials_unique_list (list) : list of medical publications
    """
    trials_dir = com_fun.get_data_folder("clinical_trials")
    all_trials_list = []  # List of all trials
    for file in com_fun.get_files(trials_dir, ".csv"):
        com_fun.write_logs(f"Trial file {file}", "INFO")
        all_trials_list.extend(com_fun.extract_csv(file))

    for e in all_trials_list.copy():
        # If there's not title nor journal for the line, remove it
        if not (e["scientific_title"] or e["journal"]):
            all_trials_list.remove(e)

    # Deduplication
    trials_unique_list = [
        dict(t) for t in {tuple(d.items()) for d in all_trials_list}
    ]

    com_fun.write_logs(
        f"List of all clinical trials found : {trials_unique_list}",
        "INFO")

    com_fun.export_to_json(trials_unique_list, "./trials_list.json")

    return trials_unique_list
