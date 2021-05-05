Directory for all code that deals with the raw CV file and the small example CVs being used.

The output from these functions will be the data which is stored in the database.

# extract_research_interests.py

The extract_research_interests.py file is the script used to read PDF files in a directory, extract research interests data, persons name, and their department, then store all extracted data in one csv

**required libraries**

Spacy and en_core_web_sm
* pip install -U pip setuptools wheel
* pip install -U spacy
* python -m spacy download en_core_web_sm

Pandas
* pip install pandas

PDFMiner
* pip install pdfminer


# Department Extraction Process

In order to extract department info correctly we must consider where we want to look at in a CV and how to attribute a department name.

The following steps are how department names are attributed.

0. Get directory of official department names from BGSU's website
1. Check if the first (most recent) entry of 'academic positions' has the following string: "professor of (....)," (....) is dept. name
    * If this string is present and the (....) is a valid department, then we are done
2. Otherwise, we check the frequency of all department names from the headers 'academic positions' to 'research interests'
3. The department name with the highest frequency gets selected as the department

Note: Different variations of department names are considered and gets corrected in the database
