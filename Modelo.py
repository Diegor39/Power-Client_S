import os
from flask import Flask, render_template, redirect, request, url_for, session
from flaskext.mysql import MySQL
import urllib.request
import azure.cognitiveservices.speech as speechsdk
import time
import azure.cognitiveservices.speech as speechsdk
import time
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


app = Flask(__name__)

app.secret_key ='007Rincon'

app.config['MYSQL_DATABASE_USER'] = 'sepherot_diego'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ywx1pqRn5y'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_diegoBD'
app.config['MYSQL_DATABASE_HOST'] = 'sepheroth.com'
mysql = MySQL()
mysql.init_app(app)

def insertardatos(correopos, bodypos1,bodypos2):
    try:
        status = 1
        conn = mysql.connect()
        cursor = conn.cursor()
        ins=cursor.execute('INSERT INTO S_C_REFUND1 (EMAIL_R, PRODUCT_R, REASON_R, STATUS_R) VALUES (%s,%s,%s,%s)', (correopos,bodypos1,bodypos2,status))
        if ins:
            return True
        else:
            return False
        
        cursor.close()
    except Exception as e:
        return e

def Ttickets(correo):
    cur = mysql.get_db().cursor()
    cur.execute('SELECT COUNT(EMAIL_R) FROM S_C_REFUND1 WHERE STATUS_R = 2 and EMAIL_R = %s',correo)
    tta = cur.fetchall()
    

    return tta

def Ttickett(correo):
    cur = mysql.get_db().cursor()
    cur.execute('SELECT COUNT(EMAIL_R) FROM S_C_REFUND1 WHERE STATUS_R = 1 and  EMAIL_R = %s',correo)
    ttt = cur.fetchall()
  
    
    return ttt

def Tticketf(correo):
    cur = mysql.get_db().cursor()
    cur.execute('SELECT COUNT(EMAIL_R) FROM S_C_REFUND1 WHERE STATUS_R = 0 and EMAIL_R = %s',correo)
    ttf = cur.fetchall()

    return ttf

def nomuser(user):
    cur1 = mysql.get_db().cursor()
    cur1.execute('SELECT NAME FROM S_C_USER WHERE NAME = %s',user)
    nomre = cur1.fetchall()
    return nomre

def Ultimomail():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT EMAIL_R FROM S_C_REFUND1 ORDER BY ID_REFUND DESC LIMIT 1')
    ultima = cursor.fetchall()
    return ultima

def pasos(user, stage, stageinfo):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('Insert into S_C_PASOS (USER, STAGE, STAGEINFO) VALUES (%s,%s,%s)', (user,stage,stageinfo))
     

def BUSTI(SERCHT):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM S_C_REFUND1 WHERE ID_REFUND = %s', SERCHT)
    ENCON = cursor.fetchall()
    return ENCON

def DATOUSER(CORREUSER):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM S_C_USER WHERE EMAIL = %s', CORREUSER)
    datuse = cursor.fetchall()
    return datuse

def editart(editicket1, ediestado1, ediproducto1, edidireccion1, edirazon1):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE S_C_REFUND1 SET PRODUCT_R = %s, REASON_R = %s, ADRRESS = %s WHERE ID_REFUND = %s;', (ediproducto1,edirazon1,edidireccion1,editicket1)) 
    return True
   

def borrarticket(Borrar):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE S_C_REFUND1 SET STATUS_R = 5 WHERE ID_REFUND =  %s;', Borrar)
    return True

def all_info():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT NAME,LAST_NAME, EMAIL, COUNT(EMAIL_R), PHONE FROM S_C_REFUND1, S_C_USER WHERE EMAIL_R = EMAIL AND (STATUS_R=1 OR STATUS_R=2) GROUP BY NAME ORDER BY COUNT(EMAIL_R) DESC')
    allinf = cursor.fetchall()
    return allinf

def tickets_tod(correo):
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM S_C_REFUND1 WHERE STATUS_R in (1, 2) AND EMAIL_R = %s ORDER BY ID_REFUND DESC',correo)
    tickets = cur.fetchall()
    return tickets

def llamada():
    
    speech_key, service_region = "e21c5662cc5c4e7aa983ba12c67f6a90", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,language="es-MX")
    print("Se ha iniciado la grabación de la llamada...")
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    
    #result = 2
    return result.text
    #return result



def analisis():
    document = llamada()
    ta_credential = AzureKeyCredential("669021d295c9482e96114324804b22c8")
    text_analytics_client = TextAnalyticsClient(endpoint="https://text-a-powe-client.cognitiveservices.azure.com/", credential=ta_credential)
    client = text_analytics_client
    documents = [document]
    response = client.analyze_sentiment(documents = documents)[0]
    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral, 
        response.confidence_scores.negative,
    ))
    respuestas = [response.sentiment, response.confidence_scores.positive, response.confidence_scores.neutral, response.confidence_scores.negative, document]
    
    #respuestas= 3
    return respuestas

def anali_llama(mensaje, senti, pos, neutra, nega, clieb, tick):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('Insert into S_C_CALL (NAME_C, ID_TICKET_C, CALL_TEXT, SENTIMENT, NUM_PO, NUM_NEU, NUM_NEG) VALUES (%s,%s,%s,%s,%s,%s,%s)', (clieb,tick,mensaje,senti,pos,neutra,nega))

    conn1 = mysql.connect()
    cursor1 = conn1.cursor()
    cursor1.execute('UPDATE S_C_REFUND1 SET STATUS_R = 2 WHERE ID_REFUND =  %s;', tick)
    return True











if __name__ == '__main__': 
    app.run(debug=True)
