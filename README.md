# Drugs referencing application

## Purpose of this application

This application intends to retrieve all the journals and articles' references to a list of drugs
Drugs, articles and journals are listed in local files

## Directory structure

* data
  * clinical_trials: Contains trials files
  * drugs: Contains drugs files
  * pubmed
    * csv: Contains medical publication files with CSV format
    * json: Contains medical publication files with JSON format
* drug_referencing
  * lib
    * common_functions.py: Module with general reusable functions
  * drugs.py: Module to manage drugs
  * main.py: Main module to construct the JSON file linking drugs, articles and journals
  * pubmeds.py: Module to manage medical publications
  * trials.py: Module to manage clinical trials

## Requirements

* Python 3

## Expected result

After running the script, several JSON files will be generated:

* drugs_list.json: JSON representing the list of drugs found
* pubmeds_list.json: JSON representing the list of medical publications found
* trials_list.json: JSON representing the list of clinalc trials found
* drugs_references.json: JSON displaying links between drugs, articles and journal
  drugs_references.json can be graphically represented by the following graph:
![Drugs referencing](./drugs_referencing.png)
