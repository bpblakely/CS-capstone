import re
import pandas as pd
import os
import glob
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import difflib
#import spacy
from io import StringIO

#spacy.load('en_core_web_sm')

default_path = os.getcwd()
lookup_table = pd.read_csv(default_path+r'/CVs/lookup_table.csv')

departments = ['africana studies', 'asian studies', 'biological sciences', 'biology', 'chemistry', 'computer science',
               'english', 'fire administration',
               'forensic science', 'history', 'international studies', 'mathematics and statistics',
               'philosophy', 'physics and astronomy', 'political science', 'psychology', 'soclology',
               'theatre and film', 'world languages & cultures', 'american culture studies', 'ethnic studies',
               'popular culture',
               "women's, gender, & sexuality studies"]

departments_varients = ['mathematics & statistics', 'mathematics', 'statistics', 'physics & astronomy', 'physics',
                        'astronomy',
                        'theatre & film', 'theatre', 'film', 'world languages and cultures',
                        "women's, gender, and sexuality studies"]

# mapping used to unify department names
varient_mapping = {'mathematics & statistics': 'mathematics and statistics',
                   'mathematics': 'mathematics and statistics',
                   'statistics': 'mathematics and statistics', 'physics & astronomy': 'physics and astronomy',
                   'physics': 'physics and astronomy',
                   'astronomy': 'physics and astronomy', 'theatre & film': 'theatre and film',
                   'theatre': 'theatre and film', 'film': 'theatre and film',
                   'world languages & cultures': 'world languages and cultures',
                   "women's, gender, and sexuality studies":
                       "women's, gender, & sexuality studies"}
delimiters = [',', ';']  # list of delimiters being checked in research interests


def remove_special(string):
    return re.sub('[^A-Za-z]+', ' ', string)


def remove_special_delimiters(string):
    chars_to_keep = ''.join(delimiters)
    expression = '[^A-Za-z' + chars_to_keep + ']+'
    return re.sub(expression, ' ', string)


def pdf_to_text(pdfname):
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    with open(pdfname, 'rb') as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
        f.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()
    return text


def clean_text(text):
    nlp = en_core_web_sm.load()
    doc = nlp(text)
    spacy_dataframe = pd.DataFrame()
    for token in doc:
        if token.lemma_ == "-PRON-":
            lemma = token.text
        else:
            lemma = token.lemma_
        row = {
            "Word": token.text,
            "Lemma": lemma,
            "PoS": token.pos_,
            "Stop Word": token.is_stop
        }
        spacy_dataframe = spacy_dataframe.append(row, ignore_index=True)
    corpus_clean = " ".join(spacy_dataframe["Lemma"][spacy_dataframe["Stop Word"] == False].values)
    corpus_clean = re.sub("[\(\[].*?[\)\]]", ' ', corpus_clean)  # this sub removes all words between [] and ()
    corpus_clean = re.sub(r'[^A-Za-z0-9]+', ' ', corpus_clean)
    return corpus_clean.lower().rstrip().lstrip()


def get_interests(raw_text, scrub_text=False):
    raw_interests = ''
    try:
        raw_interests = re.findall('(?<=research interests)(.*?)(?=research projects and grants)', raw_text.lower(), flags=re.S)[0]
    except:
        try:
            raw_interests = re.findall('(?<=research interests)(.*?)(?=research projects & grants)', raw_text.lower(), flags=re.S)[0]
        except:
            try:
                raw_interests = re.findall('(?<=research interests)(.*?)(?=publication)', raw_text.lower(), flags=re.S)[0]
            except:
                print("CV doesn't follow rubric, input data manually")
                return ''
    interests = []

    if len(raw_interests.split('\n')) > 20:
        n = len(raw_interests.split('\n'))
        print(f"CV doesn't follow rubric, input data manually | Too many research interests: {n}")
        return ''

    for s in raw_interests.split('\n')[:-1]:
        s = remove_special(s).strip()
        if not s == '':  # can be reduced by 'if s' but that is confusing notation
            interests.append(s)
    if scrub_text:
        keywords = []
        for i in range(len(interests)):
            keywords.append(clean_text(interests[i]))
        return keywords
    return interests


# Work in progress
def get_interests_complex(raw_text, scrub_text=False):
    raw_interests = ''
    try:
        raw_interests = \
        re.findall('(?<=research interests)(.*?)(?=research projects and grants)', raw_text.lower(), flags=re.S)[0]
    except:
        try:
            raw_interests = \
            re.findall('(?<=research interests)(.*?)(?=research projects & grants)', raw_text.lower(), flags=re.S)[0]
        except:
            print('CV does not follow the rubric. Cant process.')
            return ''
    interests = []
    delimiter_frequency = {}
    for s in raw_interests.split('\n')[:-1]:
        # check for delimiters
        s = remove_special_delimiters(s).strip()  # remove weird expressions except the delimiters we care about
        for delimiter in delimiters:
            delimiter_frequency[delimiter] = s.count(delimiter)

        if max(delimiter_frequency.values()) > 1:  # make sure it happens more than once
            delimiter = max(delimiter_frequency, key=delimiter_frequency.get)
            for interest in s.split(delimiter):
                interest = remove_special(interest).strip()
                if not interest == '':  # can be reduced by 'if s' but that is confusing notation
                    interests.append(interest)
        else:
            s = remove_special(s).strip()
            if not s == '':  # can be reduced by 'if s' but that is confusing notation
                interests.append(s)
    # if scrub_text:
    #     keywords = []
    #     for i in range(len(interests)):
    #         keywords.append(clean_text(interests[i]))
    #     return keywords
    return interests


def get_department(raw_text):
    # get text from academic positions to research interests
    refined_text = re.findall('(?<=academic positions)(.*?)(?<=research interests)', raw_text.lower(), flags=re.S)[0]
    # consider the first match of 'professor of _______ ____,' (professor of anything until a comma), replace uneeded words, strip, and title
    try:
        # the department search might not work, so we need to put it in a try statement
        department = re.search('professor+\s+of\s+.*,', refined_text).group(0)  # \s so we can check multiple spaces
        department = department.replace('professor', '').replace('of', '').replace(',',
                                                                                   '').strip()  # there might be 2 spaces between 'computer  science'
        department = re.sub(' +', ' ', department)  # remove extra spaces if present
        if department in departments:
            return department.title()
        elif department in departments_varients:
            return varient_mapping[department].title()  # unify the department names
    except:
        "continue/do nothing"  # want to loop through if the if statements aren't true, not only when department search breaks, so do nothing and continue

    # if we can't find a department with this logic, then we loop, return the most frequently mentioned department

    frequency = {}
    for d in departments:
        frequency[d] = refined_text.count(d)

    frequency_varients = {}  # lets also check if the varients are more frequent than the standard names
    for dv in departments_varients:
        frequency_varients[dv] = refined_text.count(dv)

    if max(frequency.values()) == 0 and max(frequency_varients.values()) == 0:
        return 'NULL'  # no matches in the code, tough luck

    # determine if standard_dept_names occur more often than their varients
    if max(frequency.values()) >= max(frequency_varients.values()):
        # we know we have a normal department name so just get the max value in frequency and return its title()
        return max(frequency, key=frequency.get).title()
    else:
        return varient_mapping[
            max(frequency_varients, key=frequency_varients.get)].title()  # return the unified department name

def pdf_processor(file):
    df = pd.DataFrame([])
    raw_text = pdf_to_text(file)
    # probably a bad assumption (without any text cleaning)
    name = raw_text.split('\n')[0].strip().lower()
    name = re.sub(' +', ' ', name)  # remove extra spaces
    name = name.replace('curriculum vitae',
                        '').strip()  # if curriculum vitae is in the first line with their name, just remove it
    name = name.split(',')[0].strip()
    matched_name = difflib.get_close_matches(name, lookup_table['name_ref'].to_list(), n=1)

    if len(matched_name) == 0:
        email = 'placeholder_email@bgsu.edu'
    else:
        email = lookup_table.loc[lookup_table.name_ref == matched_name[0]].email.iloc[0]

    department = get_department(raw_text).lower()
    interests = get_interests(raw_text, False)  # list of interests
    if interests == '': return df, False
    li = []
    for i in range(len(interests)):
        li.append([name,department,email,interests[i]])
    df = df.append(li)
    df.rename(columns={0:'name',1:'department',2:'email',3:'interest'},inplace=True)
    return df, True

