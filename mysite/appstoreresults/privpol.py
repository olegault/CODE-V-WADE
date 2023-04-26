import sqlite3
import openai
import os
from google_play_scraper import app
import numpy as np
import requests

def scrape_policy(url):
    package = url.split('id=')[1].split('&')[0]
    print(package)

    result = app(
        package,
        lang='en', # defaults to 'en'
        country='us' # defaults to 'us'
    )



    policy_link = result['privacyPolicy']



    

def analyze_policy(policy_url):


    
    # Set up your OpenAI API credentials
    openai.api_key = os.environ["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"]
 
    prompt2=""" 
    I am going to list a series of questions. I want you to answer them 
    about the privacy policy linked as the end of this sentence. The link is
    to the webpage that has the privacy policy.
    I am going to list a series of questions. I want you to answer 
    them about the privacy policy linked as the end of this prompt.
    There are 8 questions. Each of the questions are binary--the answer
    is either YES or NO. For each question, you will be given the question
    itself and the "default answer". You must cite a specific part of the
    privacy policy when you given you answer and specify the line number.
    If the policy does not mention anything pertinent to the question being
    asked, then return the default answer. The questions are:

    1.) Does the policy at NOT all mention that it will never share information
    with law enforcement? Default answer is YES.
    2.) Does the policy at NOT all mention that it will never share information
    with advertisers? Default answer is YES.
    3.) Does the policy at NOT all mention that it will never share personal
    health information? Default answer is YES.
    4.) Does the policy at NOT all mention that it will never share personal
    health information? Default answer is YES.
    5.) Does the policy at NOT all mention that it will never collect or share 
    information on the medications a user takes? Default answer is YES.
    6.) Does the policy at NOT all mention that it will never collect or share
    reproductive information about a user? Default answer is YES.
    7.) Does the policy at NOT all mention that it will never collect or share
    the period calendar of a user? Default answer is YES.
    8.) Does the policy explicitly allow for a user to delete their data? 
    Default answer is NO.
    9.) Does the policy explicitly allow for a user to control
    which parts of their data are shared and which are not? 
    Default answer is NO.
    10.) Does the policy explicitly allow for a user to control who
    their data is shared with. Default answer is NO.

    If the answer to a question is YES then VALUE is 1. If the
    answer is NO then VALUE is 0.

    The output should be a comma separated list of numbers
    (either 1 or 0) where the nth index in the list is the
    numerical encoding of the answer to the nth question. 
    There should be no other output. The comma-separated list
    of 9 binary values is the only output.
    The link is below:

    """
  
    # Define your input prompt
    input_prompt = prompt2+policy_url

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
    engine="davinci-3-5",
    prompt=input_prompt,
    max_tokens=2048,
    n=1,
    stop=None,
    temperature=0.0
    )

    # Extract the generated text from the API response
    output = response.choices[0].text.strip()
    my_list = output.split(",")



 
    metrics = {"collectPII": 0,
            "shareLawEnforcement":0,
            "shareAdvertisers":0,
            "shareHealthCare":0,
            "collectHealthInfo": 0,
            "collectMedicationInfo" : 0,
            "collectReproductiveInfo": 0,
            "collectPeriodCalendarInfo": 0,
            "requestDeletion": 0,
            "controlData": 0,
            "controlSharing": 0}

    metrics['collectPII'] = my_list[0]
    metrics['shareLawEnforcement'] = my_list[1]
    metrics['shareAdvertisers'] = my_list[2]
    metrics['shareHealthCare'] = my_list[3]
    metrics['collectHealthInfo'] = my_list[4]
    metrics['collectMedicationInfo'] = my_list[5]
    metrics['collectPeriodCalendarInfo'] = my_list[6]
    metrics['requestDeletion'] = my_list[7]
    metrics['controlData'] = my_list[8]
    metrics['controlSharing'] = my_list[9]

    #ret arr
    # print(r.json())
    return metrics

if __name__ == '__main__':

    try:
        sqliteConnection = sqlite3.connect('db-final.db')
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")


        cursor.execute("SELECT privacyPolicy FROM 'App Matrix'")
        output = cursor.fetchall()
        res = np.array(output)
        for n in res:
            arr = {}
            arr = analyze_policy(n)
            keys = arr.keys()
            values = list(arr.values())
            print(values)                  
            cursor.execute('''UPDATE 'App Matrix' SET 'collectPII'=?, 'collectHealthInfo'=?, 'collectMedicationInfo'=?, 'collectReproductiveInfo'=?, 'collectPeriodCalendarInfo'=?, 'requestDeletion'=?, 'controlData'=?, 'controlSharing'=? WHERE privacyPolicy = ?''', (*values, n[0]))
            sqliteConnection.commit()
        cursor.close()

    #cannot connect:
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



