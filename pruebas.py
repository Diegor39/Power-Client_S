'''
import requests
# pprint is used to format the JSON response
from pprint import pprint
import os

subscription_key = "10ed6ba7b3d4497096beabf32a4c9d39"
endpoint = "https://nrrecluters.cognitiveservices.azure.com/"
language_api_url = endpoint + "/text/analytics/v3.0/languages"

documents = {"documents": [
    {"id": "1", "text": "de den store hvide kanin sprang over hegnet og breakkede benet"}
    
]}
print("teamovic")
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(language_api_url, headers=headers, json=documents)
languages = response.json()
pprint(languages)

import azure.cognitiveservices.speech as speechsdk

speech_key, service_region = "e21c5662cc5c4e7aa983ba12c67f6a90", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

result = speech_recognizer.recognize_once()

print(result)

speech_config.speech_recognition_language="es-MX"


import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "e21c5662cc5c4e7aa983ba12c67f6a90", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Se ha iniciado la grabación de la llamada...")


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
result = speech_recognizer.recognize_once()

# Checks result.
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))


from flask import Flask, render_template, redirect, request, url_for, session
from flask import json
from flask import jsonify
import requests
import os
import azure.cognitiveservices.speech as speechsdk


app = Flask(__name__)

speech_key, service_region = "e21c5662cc5c4e7aa983ba12c67f6a90", "eastus"

def detectar():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Se ha iniciado la grabación de la llamada...")

    result = speech_recognizer.recognize_once()
    speech_config.speech_recognition_language="es-MX"

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return result    

@app.route('/')
def Index():
    detectar()
    return render_template('Pruebas.html')


if __name__ == '__main__': 
    app.run(debug=True)
'''
'''
import glob
import azure.cognitiveservices.speech as speechsdk
import time
import json
import pandas as pd

# Create a config file with your own configuration
# config_file_dev.json has my dev config
config_file_name = "config_file/config_file_dev.json"

with open(config_file_name, 'r') as json_data_file:
    configuration = json.load(json_data_file)

print("################################")
print(configuration)
print("################################")

# Speech SDK
speech_key = configuration["speech_api"]["speech_key"]
service_region = configuration["speech_api"]["service_region"]

# File location
location = configuration["location"]["full_file_path"]

print("speech_key: " + speech_key)
print("service_region: " + service_region)

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
speech_key, service_region = speech_key, service_region
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

print ("####################################################################################")
print ("PROGRAM START")
print ("####################################################################################")

def speech_recognize_continuous_from_file(file):
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=file)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    all_results = []
    def handle_final_result(evt):
        all_results.append(evt.result.text)

    speech_recognizer.recognized.connect(handle_final_result)
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    print("Printing all results:")
    print(all_results)

    df = pd.DataFrame(all_results)
    df

    file_name = file + r"-speech-to-text-csv-output.csv"
    df.to_csv(file_name)


    print ("Audio File: "+file+" converted successfully")
    print ("####################################################################################")


# Define the files locations and list audio files (*.wav)
#location = 'C:\\Users\\camoren\\Documents\\GitHub\\Microsoft-Cognitive-Services\\speech-to-text\\data'
location = location

fileset = [file for file in glob.glob(location + "**/*.wav", recursive=True)]

# Loop to call function to convert audio files to text
for file in fileset:
    #run_speech_to_text_small_audio_files(file)
    speech_recognize_continuous_from_file(file)
    print(file)

print ("####################################################################################")
print ("PROGRAM END")
print ("####################################################################################")
print ("Thank you for using this code")
'''


import azure.cognitiveservices.speech as speechsdk
import time
# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "e21c5662cc5c4e7aa983ba12c67f6a90", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="es-MX")

print("Se ha iniciado la grabación de la llamada...")


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
result = speech_recognizer.recognize_once()

# Checks result.
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

key = "669021d295c9482e96114324804b22c8"
endpoint = "https://text-a-powe-client.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()
print(result)
document = result.text
print(document)
#input("Introduce una frase feliz:" )

def sentiment_analysis_example(client):

    documents = [document]
    response = client.analyze_sentiment(documents = documents)[0]
    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral, 
        response.confidence_scores.negative,
    ))
    for idx, sentence in enumerate(response.sentences):
        print("Sentence: {}".format(sentence.text))
        print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
        print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))
sentiment_analysis_example(client) 

    
def key_phrase_extraction_example(client):

    try:

        documents = [document]

        response = client.extract_key_phrases(documents = documents)[0]

        if not response.is_error:
            print("\tKey Phrases:")
            for phrase in response.key_phrases:
                print("\t\t", phrase)
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))
        
key_phrase_extraction_example(client)
