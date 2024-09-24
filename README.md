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
  * library
    * common_functions.py: Module with general reusable functions
  * drugs.py: Module to manage drugs
  * main.py: Main module to construct the JSON file linking drugs, articles and journals
  * pubmeds.py: Module to manage medical publications
  * trials.py: Module to manage clinical trials

## Requirements

* Python 3
* Packages:
  * All needed packages are built-in Python packages

## Usage

To Run this application, follow these steps:

1. Position yourself within the application folder
2. Create a Python virtual environment:
   1. python3 -m venv venv
   2. source venv/bin/activate
   3. python3 -m pip install -r requirements.txt
3. Execute the application:
   1. python3 drug_referencing/main.py [--journal-ref]

You can access to the helper with the following command:
python3 drug_referencing/main.py --help

**Flags:**

* --journal-ref: Adding this flag while running the application will also execute the function intended to retrieve which journals mention the most drugs

## Expected result

After running the script, several JSON files will be generated:

* drugs_list.json: JSON representing the list of drugs found
* pubmeds_list.json: JSON representing the list of medical publications found
* trials_list.json: JSON representing the list of clinalc trials found
* drugs_references.json: JSON displaying links between drugs, articles and journal
  drugs_references.json can be graphically represented by the following graph:
  ![Drugs referencing](./drugs_referencing.png)
