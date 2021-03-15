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

    jobs=browser.find_elements_by_class_name("job-card-container")

    jobs_links=[]
    for i in jobs:
        jobs_links.append(i.find_elements_by_tag_name('a')[0].get_attribute('href'))
    return jobs_links


def scrape_job(job_link):
    """
    """
    browser.get(job_link)
    more_button=browser.find_element_by_class_name("artdeco-card__action")
    more_button.click()
    time.sleep(3)
    content=browser.find_elements_by_class_name('jobs-box__html-content')[0].text
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
    print(summarized_sentences)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    print(summary)
    return summary
# max_freq = Counter(keyword).most_common(1)[0][1]
# for word in freq_word.keys():  
#         freq_word[word] = (freq_word[word]/max_freq)
# freq_word.most_common(10)    

def match_resume_and_job(job_description, resume):
    text_list = [job_description, resume]
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    from sklearn.metrics.pairwise import cosine_similarity
    # get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2) # round to two decimal
    print("Your resume matches about "+ str(matchPercentage)+ "% of the job description.")
    print(keywords(text, ratio=0.25)) 
    # gives you the keywords of the job description

jobs='https://www.linkedin.com/jobs/search/?f_L=France&geoId=105015875&keywords=Data%20scientist&location=France' 
userN="fotzotalom@gmail.com"
pswd="7662;Y@nn"   

def matching_pipeline(job_link,user,pwd,resume_path):
    links=get_jobs_links(job_link,user,pwd)
    job_content=scrape_job(links[0])
    # keywords=get_keywords_from_job(job_content)
    # freq_words=get_n_common_words(keywords,5)
    # sent_strength=get_sent_strength(freq_words)
    # summary=summurize_sent(sent_strength)
    resume_content = docx2txt.process("CV_Brice_FOTZO.docx")
    match_resume_and_job(job_content,resume_content)
    

if __name__=="__main__":
    matching_pipeline(job_link=jobs,user=userN,pwd=pswd,resume_path="CV_Brice_FOTZO.docx")