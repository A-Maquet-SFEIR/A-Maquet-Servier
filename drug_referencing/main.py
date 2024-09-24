"""
Main module :
Construct JSON structured graph showing references

Retrieve journals referencing most drugs
"""

import argparse
import statistics
import drugs
import pubmeds
import trials
import library.common_funtions as com_fun

parser = argparse.ArgumentParser()
parser.add_argument('--journal-ref',
                    action='store_true',
                    dest='journal_ref',
                    help='Flag to retrieve journals \
referencing the most drugs')
args = parser.parse_args()


def get_drug_references(
    drugs_list, pubmed_list, trials_list
):  # noqa # pylint: disable=too-many-locals, too-many-statements
    """
    Construct a JSON file to display references between
    drugs, articles and journal

    Inputs:
    - drugs_list (list) : list of drugs
    - pubmed_list (list) : list of medical publications
    - trials_list (list) : list of clinical trials

    Output:
    - references_list_json (str) : JSON dumps of references
    """
    references_dict = {}  # A dictionary of a reference for a given drug
    references_dict_list = []  # List of all references' dictionary

    com_fun.write_logs(
        "Constructing structured JSON",
        "INFO")
    for drug in drugs_list:
        # Set the drug caracteristics
        references_dict["drug_atccode"] = drug["atccode"]
        references_dict["drug_name"] = drug["drug"]

        references_pubmed_dict = (
            {}
        )  # noqa # A dictionary of a pubmed reference for a given drug
        references_pubmed_dict_list = []  # List all pubmed references
        references_trials_dict = (
            {}
        )  # noqa # A dictionary of a trial reference for a given drug
        references_trials_dict_list = []  # List all trial references

        trials_unique_list = []  # List to deduplicate trial references

        pubmed_unique_list = []  # List to deduplicate pubmed references

        # Loop over all pubmed
        for pubmed in pubmed_list:
            journal_pubmed_dict = {}  # A dictionary for the given pubmed
            journal_pubmed_dict_list = []  # List of all pubmed
            journal_pubmed_unique_list = []  # Deduplicate pubmed

            # If the drug is referenced in the pubmed article's title
            if drug["drug"].lower() in pubmed["title"].lower():
                cln_title = com_fun.rm_invalid_unicode(pubmed["title"])
                references_pubmed_dict = {"title": cln_title}

                # Loop over pubmed to find if a pubmed is referenced
                # in several journals
                for pubmed_mult_mentions in pubmed_list:
                    if pubmed["title"] == pubmed_mult_mentions["title"]:
                        cln_journal = com_fun.rm_invalid_unicode(
                            pubmed_mult_mentions["journal"]
                        )
                        fmt_date = com_fun.format_date(
                            pubmed_mult_mentions["date"])
                        journal_pubmed_dict = {
                            "journal": cln_journal,
                            "date": fmt_date
                        }
                        journal_pubmed_dict_list.append(
                            journal_pubmed_dict.copy())
                        journal_pubmed_unique_list = list(
                            {
                                journ_dedupl["journal"]: journ_dedupl
                                for journ_dedupl in journal_pubmed_dict_list  # noqa # pylint: disable=line-too-long
                            }.values()
                        )

                references_pubmed_dict["journal_references"] = (
                    journal_pubmed_unique_list  # noqa # pylint: disable=line-too-long
                )

                references_pubmed_dict_list.append(
                    references_pubmed_dict.copy()
                )  # noqa # pylint: disable=line-too-long
                pubmed_unique_list = list(
                    {
                        pubmed_dedupl["title"]: pubmed_dedupl
                        for pubmed_dedupl in references_pubmed_dict_list  # noqa # pylint: disable=line-too-long
                    }.values()
                )

        # If there's at least 1 pubmed mention
        if len(references_pubmed_dict_list) > 0:
            references_dict["article_references"] = {
                "pubmed": pubmed_unique_list
            }
        # Otherwise, initialize article_references key
        else:
            references_dict["article_references"] = {}

        # Loop over all trials
        for trial in trials_list:
            journal_trials_dict = {}  # A dictionary for the given trial
            journal_trials_dict_list = []  # List of all pubmed
            journal_trials_unique_list = []  # Deduplicate pubmed
            # If the drug is referenced in the trial article's title
            if drug["drug"].lower() in trial["scientific_title"].lower():
                cln_title = com_fun.rm_invalid_unicode(
                    trial["scientific_title"])
                references_trials_dict = {"title": cln_title}

                for trial_mult_mentions in trials_list:
                    if (
                        trial["scientific_title"]
                        == trial_mult_mentions["scientific_title"]
                    ):  # noqa # pylint: disable=line-too-long
                        cln_journal = com_fun.rm_invalid_unicode(
                            trial_mult_mentions["journal"]
                        )
                        fmt_date = com_fun.format_date(
                            trial_mult_mentions["date"])
                        journal_trials_dict = {
                            "journal": cln_journal,
                            "date": fmt_date
                        }
                        journal_trials_dict_list.append(
                            journal_trials_dict.copy())
                        journal_trials_unique_list = list(
                            {
                                journ_dedupl["journal"]: journ_dedupl
                                for journ_dedupl in journal_trials_dict_list  # noqa # pylint: disable=line-too-long
                            }.values()
                        )

                references_trials_dict["journal_references"] = (
                    journal_trials_unique_list  # noqa # pylint: disable=line-too-long
                )

                references_trials_dict_list.append(
                    references_trials_dict.copy())
                trials_unique_list = list(
                    {
                        trial_dedupl["title"]: trial_dedupl
                        for trial_dedupl in references_trials_dict_list  # noqa # pylint: disable=line-too-long
                    }.values()
                )

        if len(references_trials_dict_list) > 0:
            references_dict["article_references"][
                "trials"
            ] = trials_unique_list  # noqa # pylint: disable=line-too-long

        references_dict_list.append(references_dict.copy())

    com_fun.write_logs(
        f"Structured JSON {references_dict_list}",
        "INFO")

    com_fun.export_to_json(references_dict_list, "./drugs_references.json")

    return references_dict_list


def extract_journal_most_drugs(references_list):
    """
    Find the journals mentioning the most drugs

    Inputs:
    - references_list (str) : List of the drugs and their references
    """
    all_drug_journal_list = []
    # Loop over all drugs
    for drug in references_list:
        drug_journal_list = []
        # Loop over pubmed to find attached journals
        if 'pubmed' in drug['article_references']:
            for pubmed in drug['article_references']['pubmed']:
                for pubmed_journal in pubmed['journal_references']:
                    drug_journal_list.append(pubmed_journal['journal'])
        # Loop over trials to find attached journals
        if 'trials' in drug['article_references']:
            for trial in drug['article_references']['trials']:
                for trial_journal in trial['journal_references']:
                    drug_journal_list.append(trial_journal['journal'])

        # Merge all lists of unique journals per drug
        all_drug_journal_list.extend(list(set(drug_journal_list)))

    # Retrieve the most common ones
    journal_ref_most_drugs = statistics.multimode(all_drug_journal_list)
    com_fun.write_logs(
        f"Journals referencing the most drugs are {journal_ref_most_drugs}",
        "INFO")


if __name__ == "__main__":
    drugs_list_refined = drugs.get_drugs()
    pubmed_list_refined = pubmeds.get_pubmed()
    trials_list_refined = trials.get_clinical_trials()
    drug_list_references = get_drug_references(
        drugs_list_refined, pubmed_list_refined, trials_list_refined
    )

    if args.journal_ref:
        extract_journal_most_drugs(drug_list_references)
