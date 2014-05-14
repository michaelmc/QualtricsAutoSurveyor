import time
import csv
import json
import urllib
import random
import sys
# import os
# import datetime
# import httplib

def main():
    '''Reads a list of individuals and sends a survey to a selection of them.'''
    
    user = '' // Add username
    token = '' // Add API token
    library_id = '' // Add Library ID
    survey_id = '' // Add Survey ID
    from_email = '' // Add the From: email
    from_name = '' // Add the From: name
    subject = '' // Add the email subject line
    message_id = '' // Add the Message ID
    
    log_string = ''
    
    #
    # First, create a new Qualtrics panel based on the current date and time.
    #
    panel_response = json.load(urllib.urlopen(url_builder('new_panel', user, token, None, library_id)))
    log_string = logger('create', panel_response, log_string)
    if panel_response['Meta']['Status'] == 'Error':
        return error_handler("Error creating panel.")
    panel_id = panel_response['Result']['PanelID'] # get the panel ID number to use later
    
    #
    # Next, read the file, shuffle the names, and determine how many 
    # recipients will receive a survey.
    #
    source = open('DailyExternal.csv', 'r')
    names = csv.reader(source, delimiter=',', quotechar='"')
    names_array = []
    map((lambda x: names_array.append(x)),names)
    names_array = names_array[1:len(names_array)]
    random.shuffle(names_array)
    target = len(names_array) / 4
    if len(names_array) % 4 >= 2:
        target += 1
        
    #
    # Iterate through the list and choose unique individuals to survey; 
    # add them to the panel.
    #
    n = 0
    i = 0
    recipients = []
    recipient_names = []
    while n < target and i < len(names_array):
        name = names_array[i]
        i += 1
        first_name = name[0].strip().title()
        last_name = name[1].strip().title()
        email = name[2].strip().replace('@', '%40')
        remedy_number = name[3].strip()
        remedy_number = remedy_number[len(remedy_number)-6:len(remedy_number)]
        summary = name[4].strip()
        data_ref = urllib.quote("Ticket " + remedy_number + ": " + summary,"")
        
        if email not in recipients:
            recipients.append(email)
            recipient_names.append(first_name + " " + last_name + ", " + email.strip().replace('%40', '@') + ", " + data_ref)
            n += 1
            url = url_builder('add_recipient', user, token, panel_id, library_id, first_name=first_name, last_name=last_name, email=email, remedy_number=data_ref)
            person_response = json.load(urllib.urlopen(url))
            log_string = logger('add', person_response, log_string)
            
    #
    # Send the survey via Qualtrics.
    #
    send_survey_URL = url_builder('send', user, token, panel_id, library_id, survey_id=survey_id, from_email=from_email, from_name=from_name, subject=subject, message_id=message_id, message_library_id=library_id)
    survey_response = json.load(urllib.urlopen(send_survey_URL))
    log_string = logger('send', survey_response, log_string)
    if survey_response['Meta']['Status'] == 'Error':
        return error_handler('Error sending survey.')
    print "Survey sent"
    
    write_log(log_string)
    source.close()

def error_handler(error):
    log_file = open('./SurveyLogs/' + time.strftime("%Y-%m-%d-%H%M%S", time.localtime()) + '.log', 'w')
    log_file.write(log_string)
    log_file.close()
    sys.exit()

def logger(message, response, log_string):
    if message == 'delete':
        response_message = ' Delete panel: '
    elif message == 'send':
        response_message = ' Send survey: '
    elif message == 'add':
        response_message = ' Add user to panel: '
    elif message == 'create':
        response_message = ' Create new panel: '
    log_string = log_string + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + response_message + json.dumps(response) + '\n'
    return log_string

def write_log(log_string):
    log_file = open('SurveyLogs/' + time.strftime("%Y-%m-%d-%H%M%S", time.localtime()) + '.log', 'w')
    log_file.write(log_string)
    log_file.close()

def url_builder(request_type, user, token, panel_id, panel_library_id, survey_id=None, from_email=None, from_name=None, subject=None, message_id=None, message_library_id=None, first_name=None, last_name=None, email=None, remedy_number=None):
    if request_type == 'send':
        url = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php?Request=sendSurveyToPanel&User=" + user + "&Token=" + token + "&Format=JSON&Version=2.0&SurveyID=" + survey_id + "&SendDate=" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.localtime())-7200)) + "&FromEmail=" + from_email + "&FromName=" + from_name + "&Subject=" + subject + "&MessageID=" + message_id + "&MessageLibraryID=" + message_library_id + "&PanelID=" + panel_id + "&PanelLibraryID=" + panel_library_id + "&LinkType=Individual"
    elif request_type == 'new_panel':
        url = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php?Request=createPanel&User=" + user + "&Token=" + token + "&Format=JSON&Version=2.0&LibraryID=" + panel_library_id + "&Name=" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    elif request_type == 'add_recipient':
        url = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php?Request=addRecipient&User=" + user + "&Token=" + token + "&Format=JSON&Version=2.0&LibraryID=" + panel_library_id + "&PanelID=" + panel_id + "&FirstName=" + first_name + "&LastName=" + last_name + "&Email=" + email + "&ExternalDataRef=" + remedy_number
    elif request_type == 'delete_panel':
        url = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php?Request=deletePanel&User=" + user + "&Token=" + token + "&Format=JSON&Version=2.0&LibraryID=" + panel_library_id + "&PanelID=" + panel_id
    return url if url else error_handler('Error building URL.')

if __name__ == '__main__':
    main()
