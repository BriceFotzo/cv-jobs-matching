from time import sleep
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common import keys
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import en_core_web_sm
import fr_core_news_sm
# Import summarize from gensim
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords# Import the library
# to convert MSword doc to txt for processing.
import docx2txt
nlp_job = fr_core_news_sm.load()
nlp_resume=fr_core_news_sm.load()
from dotenv import load_dotenv,dotenv_values
from getpass import getpass

load_dotenv()

config = dotenv_values(".env")



def get_jobs_links(job_query,user,pwd):
    """[summary]

    Args:
        job_query ([type]): [description]
    """
    browser=webdriver.Chrome("chromedriver.exe")
    browser.get("https://www.linkedin.com")

    username=browser.find_element_by_id("session_key")
    username.send_keys(user)
    password=browser.find_element_by_id("session_password")
    password.send_keys(pwd)

    login_button=browser.find_element_by_class_name("sign-in-form__submit-button")
    login_button.click()

    browser.get(job_query)
    sleep(3)
    jobs=browser.find_elements_by_class_name("job-card-container")
    
    
    
    jobs_links=[]
    jobs_head=[]
    for i in jobs:
        jobs_links.append(i.find_elements_by_tag_name('a')[0].get_attribute('href'))
        jobs_head.append(i.find_element_by_class_name("artdeco-entity-lockup__content").text)
    return browser,jobs_links,jobs_head


def scrape_job(browser,job_link):
    """
    """
    browser.get(job_link)
    sleep(3)
    more_button=browser.find_element_by_class_name("artdeco-card__action")
    more_button.click()
    sleep(3)
    content=browser.find_elements_by_class_name('jobs-box__html-content')[0].text
    # print(content)
    return content

def get_keywords_from_job(job_description):
    """[summary]

    Args:
        job_description ([type]): [description]
    """
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in job_description:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)
    return keyword
            
def get_n_common_words(keywords,n):
    freq_word = Counter(keywords)
    print(freq_word.most_common(n))    
    return freq_word   

def get_sent_strength(freq_word):
    sent_strength={}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]
    print(sent_strength)
    return sent_strength
def summurize_sent(sent_strength,ratio=3):
    summarized_sentences = nlargest(ratio, sent_strength, key=sent_strength.get)
    # print(summarized_sentences)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    # print(summary)
    return summary


def match_resume_and_job(job_description, resume,head,i):
    text_list = [job_description, resume]
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    from sklearn.metrics.pairwise import cosine_similarity
    # get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2) # round to two decimal
    print("Job {} - Score {} %".format(i,str(matchPercentage)))
    print("Infos",head)
    # print("Your resume matches about "+ str(matchPercentage)+ "% of the job description.")
    print("----------------------------------------------------------------------------")
    # print(keywords(job_description, ratio=0.25)) 
    # gives you the keywords of the job description
from urllib.parse import quote
 

def matching_pipeline(job_link,user,pwd,resume_path):
    resume_content = docx2txt.process("CV_Brice_FOTZO.docx")
    browser,links,heads=get_jobs_links(job_link,user,pwd)
    sleep(3)
    cpt=1
    for head,job in zip(heads,links):
        job_content=scrape_job(browser,job)
        match_resume_and_job(job_content,resume_content,head,cpt)
        cpt=cpt+1

if __name__=="__main__":
    userN=input("Email/Nom d'utilisateur : ")
    pswd=getpass("Mot de passe : ")
    job_query_online = input("Enter Job description : ")
    keyword_job=quote(job_query_online)
    jobs="https://www.linkedin.com/jobs/search/?keywords="+keyword_job+"&location=France"
    matching_pipeline(job_link=jobs,user=userN,pwd=pswd,resume_path="CV_Brice_FOTZO.docx")
