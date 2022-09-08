import json
import re


import sql_statements
import traceback
from database import Database
from lxml import etree
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup


def add_to_cleaned(app_id, policy_url, article_content, article_plain_content, article_plain_text):
    """Function to report an error to the database.

    :param policy_id: The ID of the corresponding row of the raw_policy table.
    :param article_content: The HTML result of cleaning the raw policy.
    :param article_plain_content: A simplified version of the article_content.
    :param article_plain_text: A text only version of article_plain_content.
    :return:
    """

    # Encode HTML and Text Content
    article_content = quote(article_content, encoding='utf-8', errors='replace')
    article_plain_content = quote(article_plain_content, encoding='utf-8', errors='replace')
    article_plain_text = quote(article_plain_text, encoding='utf-8', errors='replace')
    
    # Establish a database connection
    database_connection = Database().get_database_connection()

    # Try with the database connection as a resource.
    with database_connection:
        with database_connection.cursor() as cursor:
            # Insert a row in the error log table.
            cursor.execute(sql_statements.insert_cleaned_policy,
                           (app_id, policy_url, article_content, article_plain_content, article_plain_text))

            # Commit to save changes.
            database_connection.commit()


# Function to split list into chunk size sized chunks.
def split_list_into_chunks(list_to_split_into_chunks, chunk_size):
    # Yield successive chunk_size sized chunks from the list to split into chunks.
    for start_of_chunk in range(0, len(list_to_split_into_chunks), chunk_size):
        yield list_to_split_into_chunks[start_of_chunk:start_of_chunk + chunk_size]

def get_segment_text(segment_id):
    """Function to extract segment text from the policy table.

    :param segment_id: The ID of the corresponding row of the segment table.
    """

    # Establish a database connection
    database_connection = Database().get_database_connection()

    # Try with the database connection as a resource.
    with database_connection:
        with database_connection.cursor() as cursor:
            # Insert a row in the error log table.
            cursor.execute(sql_statements.select_segment_text,
                           (segment_id))

            # Fetch all app urls.
            result_rows = cursor.fetchall()
    
    # Initialize a segment text string variable
    segment_text = ''

    # Parse the returned list and extract a single element
    for row in result_rows:
        segment_text = unquote(row['segment_text'], encoding='utf-8', errors='replace')
    
    return segment_text

def get_policy_text(policy_id):
    """Function to extract policy text from the policy table.

    :param policy_id: The ID of the corresponding row of the policy table.
    """

    # Establish a database connection
    database_connection = Database().get_database_connection()

    # Try with the database connection as a resource.
    with database_connection:
        with database_connection.cursor() as cursor:
            # Insert a row in the error log table.
            cursor.execute(sql_statements.select_policy_text,
                           (policy_id))

            # Fetch all app urls.
            result_rows = cursor.fetchall()
    
    # Initialize a policy text and html content string variable
    policy_text = ''
    policy_html = ''

    # Parse the returned list and extract a single element
    for row in result_rows:
        policy_text = unquote(row['cleaned_text'], encoding='utf-8', errors='replace')
        policy_html = unquote(row['cleaned_html'], encoding='utf-8', errors='replace')
    
    return (policy_text, policy_html)

def merge_lists(policy_text):
    policy_text_filtered_lists = []
    for line_index in range(len(policy_text)):
        if policy_text[line_index][-1] == ',':
            whole_segment = policy_text[line_index].split('*')
            avg_len = 0
            for list_element in whole_segment:
                avg_len += len(list_element.split())
            avg_len = avg_len / len(whole_segment)
            if (avg_len >= 20):
                for list_element in whole_segment:
                    policy_text_filtered_lists.append(list_element.strip())
            else:
                if (len(policy_text_filtered_lists) == 0):
                    policy_text_filtered_lists = [policy_text[line_index]]
                else:
                    policy_text_filtered_lists[-1] += policy_text[line_index]
        else:
            policy_text_filtered_lists.append(policy_text[line_index]) 
    return policy_text_filtered_lists

def filter_out_headings(policy_text, html_content):
    def getTextFromTag(html_string, tag):
        header_lines = []
        soup = BeautifulSoup(html_string, 'html.parser')
        for element in soup.find_all(tag):
            header_lines.append(element.text)
        return header_lines
    policy_headings_text = getTextFromTag(html_content, ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    policy_text_filtered_headers = [x for x in policy_text if x not in policy_headings_text]
    return policy_text_filtered_headers

def main_label_to_attribute(main_label):
    if (main_label == 'First Party Collection/Use'):
        return ['Does or Does Not',
                'Collection Mode',
                'Action First-Party',
                'Identifiability',
                'Personal Information Type',
                'Purpose',
                'User Type',
                'Choice Type',
                'Choice Scope']
    if (main_label == 'Third Party Sharing/Collection'):
        return ['Third Party Entity',
                'Does or Does Not',
                'Action Third-Party',
                'Identifiability',
                'Personal Information Type',
                'Purpose',
                'User Type',
                'Choice Type',
                'Choice Scope']
    if (main_label == 'User Choice/Control'):
        return ['Choice Type',
                'Choice Scope',
                'Personal Information Type',
                'Purpose',
                'User Type']
    if (main_label == 'User Access, Edit and Deletion'):
        return ['Access Type',
                'Access Scope',
                'User Type']
    if (main_label == 'Data Retention'):
        return ['Retention Period',
                'Retention Purpose',
                'Personal Information Type']
    if (main_label == 'Data Security'):
        return ['Security Measure']
    if (main_label == 'Policy Change'):
        return ['Change Type',
                'Notification Type',
                'User Choice']
    if (main_label == 'Do Not Track'):
        return ['Do Not Track Policy']
    if (main_label == 'International and Specific Audiences'):
        return ['Audience Type']
    return []

def label_to_variable(label):
    if label == 'Retention Period':
        return 'retention_period'
    elif label == 'Retention Purpose':
        return 'retention_purpose'
    elif label == 'Notification Type':
        return 'notification_type'
    elif label == 'Security Measure':
        return 'security_measure'
    elif label == 'Audience Type':
        return 'audience_type'
    elif label == 'User Type':
        return 'user_type'
    elif label == 'Access Scope':
        return 'access_scope'
    elif label == 'Does or Does Not':
        return 'does_or_does_not'
    elif label == 'Access Type':
        return 'access_type'
    elif label == 'Action First-Party':
        return 'action_first_party'
    elif label == 'Action Third-Party':
        return 'action_third_party'
    elif label == 'Third Party Entity':
        return 'third_party_entity'
    elif label == 'Choice Scope':
        return 'choice_scope'
    elif label == 'Choice Type':
        return 'choice_type'
    elif label == 'User Choice':
        return 'user_choice'
    elif label == 'Change Type':
        return 'change_type'
    elif label == 'Collection Mode':
        return 'collection_mode'
    elif label == 'Identifiability':
        return 'identifiability'
    elif label == 'Personal Information Type':
        return 'personal_information_type'
    elif label == 'Purpose':
        return 'purpose'
    elif label == 'Do Not Track Policy':
        return 'do_not_track'