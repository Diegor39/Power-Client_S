import os
from flask import Flask, render_template, redirect, request, url_for, session
from flaskext.mysql import MySQL
import urllib.request
import azure.cognitiveservices.speech as speechsdk
import time



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

def editart(editicket, ediestado, ediproducto, edidireccion, edirazon):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE S_C_REFUND1 SET PRODUCT_R = %s, REASON_R = %s, ADRRESS = %s WHERE ID_REFUND = %s;', (ediproducto,edirazon,edidireccion,editicket))
    edir = cursor.fetchall()
    return edir
   

def borrarticket(Borrar):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE S_C_REFUND1 SET STATUS_R = 5 WHERE ID_REFUND =  %s;', Borrar)
    borrar = cursor.fetchall()
    return borrar

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
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = "e21c5662cc5c4e7aa983ba12c67f6a90", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    #Creates a recognizer with the given settings
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

    return result

if __name__ == '__main__': 
    app.run(debug=True)
