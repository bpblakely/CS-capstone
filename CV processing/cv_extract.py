import glob
import os
import datetime
import re
import en_core_web_sm
# import random
# import requests
# import json
import pandas as pd
# from spellchecker import SpellChecker
from spacy.lang.pt.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

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

def get_pos(text):
    sentences = text.split('.')
    nlp = en_core_web_sm.load()
    df = pd.DataFrame() # store parts of speech by sentence in summary
    verbs = []
    nouns = []
    adverbs = []
    adjectives = []
    for i in range(len(sentences)):
        # picking an arbitrary number to filter how long a sentnce should be. If its less than 5 characters, odds are it isnt a sentence
        if len(sentences[i])<=5: 
            continue
        doc = nlp(sentences[i])
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
            spacy_dataframe = spacy_dataframe.append(row, ignore_index = True)
        verbs.append([spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "VERB"].values,spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "VERB"].index])
        nouns.append([spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "NOUN"].values,spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "NOUN"].index])
        adverbs.append([spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "ADV"].values,spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "ADV"].index])
        adjectives.append([spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "ADJ"].values,spacy_dataframe["Lemma"][spacy_dataframe["PoS"] == "ADJ"].index])
    df['verbs'] = verbs
    df['nouns'] = nouns
    df['adverbs'] = adverbs
    df['adj'] = adjectives
    
    return df

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
        spacy_dataframe = spacy_dataframe.append(row, ignore_index = True)
    corpus_clean = " ".join(spacy_dataframe["Lemma"][spacy_dataframe["Stop Word"] == False].values)
    corpus_clean = re.sub("[\(\[].*?[\)\]]", ' ', corpus_clean) # this sub removes all words between [] and ()
    corpus_clean = re.sub(r'[^A-Za-z0-9]+', ' ', corpus_clean)   
    return corpus_clean.lower().rstrip().lstrip()

# sections to extract: (Name? first row?)
    # VIII.  Research Interests
    # IX.  Publications 
# p = re.compile(r'Research Interests([\S\s]*)Research Projects and Grants', re.MULTILINE)
# re.findall(p,raw_text)

cv_file = r'G:\Python File Saves\Capstone Project\cv_data\JongKwanLee-CV-09062020.pdf'
raw_text=pdf_to_text(cv_file)

raw_interests = re.findall('(?<=Research Interests)(.*?)(?=Research Projects and Grants)', raw_text, flags=re.S)[0]
interests = []
for s in raw_interests.split('\n')[:-1]:
    s= s.lstrip().rstrip()
    if s == '':
        continue
    else:
        interests.append(s)

t = re.search(r'Publications(.*?)Service', raw_text, re.DOTALL).group()
publications = re.findall(r'“(.*?)”', t, re.DOTALL)

keywords = []
for i in range(len(interests)):
    keywords.append(clean_text(interests[i]))
key = []
for k in keywords:
    key+= k.split()
    
pub_keys = []
for i in range(len(publications)):
    pub_keys.append(clean_text(publications[i]))
    
pub = [p.lower().replace('\n','').lstrip().rstrip() for p in publications]
pub1 = []
for p in pub:
    pub1 += p.split()
#%%

# IMPOSING REQUIREMENT: A USER MUST HAVE QUOTES AROUND THEIR PUBLICATION NAME TO GET DETECTED BY OUR SOFTWARE

roy_cv = r'G:\Python File Saves\Capstone Project\cv_data\roy_cv.pdf'
raw_text2=pdf_to_text(roy_cv)

raw_interests2 = re.findall('(?<=Research Interests)(.*?)(?=Research Projects and Grants)', raw_text2, flags=re.S)[0]
interests2 = []
for s in raw_interests2.split('\n')[:-1]:
    s= s.lstrip().rstrip()
    if s == '':
        continue
    else:
        interests2.append(s)

  
t2 = re.search(r'Publications(.*?)Service', raw_text2, re.DOTALL).group()
publications2 = re.findall(r'“(.*?)”', t2, re.DOTALL)

keywords2 = []
for i in range(len(interests2)):
    keywords2.append(clean_text(interests2[i]))

key2 = []
for k in keywords2:
    key2+= k.split()

pub_keys2 = []
for i in range(len(publications2)):
    pub_keys2.append(clean_text(publications2[i]))
    
pub2 = [p.lower().replace('\n','').lstrip().rstrip() for p in publications2]
pub22 = []
for p in pub2:
    pub22 += p.split()
#%% Pretend database: name, research interests, publications
row = [['JONG KWAN “JAKE” LEE',key,pub1],
 ['SANKARDAS ROY',key2,pub22]]
df = pd.DataFrame(row,columns=['name','interests','publications'])
#%% pretend query

query= clean_text("machine learning")
query2 = clean_text("computer vision")
query3= clean_text("learn")

df.interests.apply(lambda x: all(q in x for q in query.split()))
df.interests.apply(lambda x: all(q in x for q in query2.split()))
df.interests.apply(lambda x: all(q in x for q in query3.split()))

df.publications.apply(lambda x: all(q in x for q in query.split()))
df.publications.apply(lambda x: all(q in x for q in query2.split()))
df.publications.apply(lambda x: all(q in x for q in query3.split()))


key = []
for k in keywords:
    key+= k.split()