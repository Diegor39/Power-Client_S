import os
from flask import Flask, render_template, redirect, request, url_for, session
from flaskext.mysql import MySQL
import urllib.request
import Modelo as Modelo
import time
import json

app = Flask(__name__)

app.secret_key ='007Rincon'

app.config['MYSQL_DATABASE_USER'] = 'sepherot_diego'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ywx1pqRn5y'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_diegoBD'
app.config['MYSQL_DATABASE_HOST'] = 'sepheroth.com'
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def Index():
    return render_template('login.html')

@app.route('/close')
def close():
    Modelo.pasos(session['name'],'CERRAR SESION', 'USUARIO FINALIZA PROCESOS')
    session.clear()
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        correo = request.form['correo']
        password = request.form['password']
        #print(correo)
        #print(password)
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM S_C_USER WHERE EMAIL=%s', (correo))
        user = cur.fetchone()
        #print(user)
        cur.close()
        if len(user)>0:
            if password == user[3]:                
                session['name']=user[1]
                #print(session['name'])
                session['correo'] =user[4]
                session['type'] =user[8]
                print(session['type'])
                Modelo.pasos(session['name'],'LOGIN', 'LOGIN EXITOSO DEL USUARIO')
                if session['type'] == "CALL_CENTER":
                    return redirect('call_center')
                else:
                    return redirect('mis_pedidos')
        else:
            Modelo.pasos(session['name'],'LOGIN.FAIL', 'ERROR EN EL LOGIN DEL USUARIO')
            return redirect('')
    else:
        #Modelo.pasos(correo,'LOGIN.FAIL', 'ERROR EN EL LOGIN DEL USUARIO')
        return render_template('login.html')

@app.route('/mis_pedidos', methods=['GET', 'POST'])
def mis_pedidos():
    _username=Modelo.nomuser(session['name'])
    Modelo.pasos(session['name'],'P.PEDIDOS', 'USUARIO VE SUS PEDIDOS')
    return render_template('mis_pedidos.html', nomre = _username[0][0])

@app.route('/devoluciones_reembolsos')
def devoluciones_reembolsos():
    Modelo.pasos(session['name'],'P.DEVOLUCION', 'USUARIO VE TODOS SUS TICKETS')
    tickets=Modelo.tickets_tod(session['correo'])
    _ticketactivos=Modelo.Ttickets(session['correo'])
    _tickettotal=Modelo.Ttickett(session['correo'])
    _ticketfinal=Modelo.Tticketf(session['correo'])
    _username=Modelo.nomuser(session['name'])
    #print(session['correo'])
    #print(tickets)

    return render_template('devoluciones_reembolsos.html', tickets = tickets,tta= _ticketactivos[0][0],ttt= _tickettotal[0][0],ttf= _ticketfinal[0][0], nomre= _username[0][0]) 

@app.route('/ticket', methods=['GET','POST'])
def ticket():
    if request.method == 'POST':
        SERCHT = request.form['SERCHT']
        _SERCHT = Modelo.BUSTI(SERCHT)
        #print(_SERCHT)
        _username=Modelo.nomuser(session['name'])
        Modelo.pasos(session['name'],'P.DETALLE_TICKET', 'USUARIO VE EL DETALLE DE UN TICKET')
        tickets=Modelo.tickets_tod(session['correo'])
        _ticketactivos=Modelo.Ttickets(session['correo'])
        _tickettotal=Modelo.Ttickett(session['correo'])
        _ticketfinal=Modelo.Tticketf(session['correo'])
        _username=Modelo.nomuser(session['name'])
        _DATAUSER=Modelo.DATOUSER(session['correo'])
        

        return render_template('ticket.html', tickets = tickets,tta= _ticketactivos[0][0],ttt= _tickettotal[0][0],ttf= _ticketfinal[0][0], nomre= _username[0][0],SERCHTIK=_SERCHT[0][0],SERCHTIK1=_SERCHT[0][1],SERCHTIK2=_SERCHT[0][2],SERCHTIK3=_SERCHT[0][3],SERCHTIK4=_SERCHT[0][4],SERCHTIK5=_SERCHT[0][5],SERCHTIK6=_SERCHT[0][6], DU =_DATAUSER)
    return redirect('mis_pedidos')

@app.route('/editar', methods=['GET','POST'])
def editar():
    if request.method == 'POST':
        Modelo.pasos(session['name'],'EDICION DE TICKET', 'USUARIO EDITA UN TICKET')
        data=request.get_json()
        print("#############")
        print(data)
        editicket1=data['editicket']
        ediestado1=data['ediestado']
        ediproducto1=data['ediproducto']
        edidireccion1=data['edidireccion']
        edirazon1=data['edirazon']
        _editarticket = Modelo.editart(editicket1, ediestado1, ediproducto1, edidireccion1, edirazon1)
        print(editicket1)
        print("°°°°°°°°°°°°°°°")
        if _editarticket:
            return json.dumps("bien")
        return json.dumps("algo")
    
@app.route('/borrar', methods=['GET','POST'])
def borrar():
    if request.method == 'POST':
        Modelo.pasos(session['name'],'BORRADO DE TICKET', 'USUARIO ELIMINA UN TICKET')
        data=request.get_json()
        borrid=data['borrid']
        _borrarticket = Modelo.borrarticket(borrid)
        print(_borrarticket)
        if _borrarticket:
            return json.dumps(True)
        return json.dumps("algo")

@app.route('/call_center')
def call_center():
    Modelo.pasos(session['name'],'P.TAMAÑO DE USUARIO', 'CC VE LA CANTIDAD DE USUARIOS')
    _username=Modelo.nomuser(session['name'])
    _allinfos = Modelo.all_info()
    #print(_allinfos)
    return render_template('call_center.html', _allinfos = _allinfos, nomre = _username[0][0])

@app.route('/call_sc')
def call_sc():
    Modelo.pasos(session['name'],'P.LLAMADAS', 'CC VE EL ANALISIS DE LA LLAMADA')
    #time.sleep(1)
    _username=Modelo.nomuser(session['name'])
    #_inicio_llamada = Modelo.llamada()
    _analisis_llamada = Modelo.analisis()
    _allinfos = Modelo.all_info()
    
    
    return render_template('call_sc.html', nomre = _username[0][0],_analisis_llamada =_analisis_llamada )

@app.route('/tcs_usuario', methods=['GET','POST'])
def tsc_usuario():
    if request.method == 'POST':
        Modelo.pasos(session['name'],'P.TICKET POR USUARIO', 'CC VE LA LISTA DE LOS TICKETS POR USUARIO')
        _username=Modelo.nomuser(session['name'])
        corre_tcs = request.form['corre_tcs']
        print(corre_tcs)
        tickets=Modelo.tickets_tod(corre_tcs)
        _ticketactivos=Modelo.Ttickets(corre_tcs)
        _tickettotal=Modelo.Ttickett(corre_tcs)
        _ticketfinal=Modelo.Tticketf(corre_tcs)
        _DATAUSER=Modelo.DATOUSER(corre_tcs)
        return render_template('tcs_usuario.html', tickets = tickets,nomre = _username[0][0],tta= _ticketactivos[0][0],ttt= _tickettotal[0][0],ttf= _ticketfinal[0][0], DU =_DATAUSER )

@app.route('/add_llamada', methods=['GET','POST'])
def add_llamada():
    if request.method == 'POST':
        Modelo.pasos(session['name'],'GUARDAR LLAMADA', 'CC GUARDA EL ANALISIS DE LA LLAMADA')
        data=request.get_json()
        #print(data)
        mensaje=data['texto_llamada']
        senti=data['sentimiento']
        pos=data['positivo']
        neutra=data['neutral']
        nega=data['negativo']
        clieb=data['cliente']
        tick=data['ticket_c']
        dat_llam=Modelo.anali_llama(mensaje, senti, pos, neutra, nega, clieb, tick)
        if dat_llam:
            return json.dumps(True)
        return json.dumps("algo")

@app.route('/edi_tc', methods=['GET','POST'])
def edi_tc():
    if request.method == 'POST':
        Modelo.pasos(session['name'],'P.EDICION DE TICKET CC', 'CC EDITA UN TICKET DE UN USUARIO')
        SERCHT = request.form['SERCHT']
        _SERCHT = Modelo.BUSTI(SERCHT)
        #print(_SERCHT)
        _username=Modelo.nomuser(session['name'])
        Modelo.pasos(session['name'],'P.PEDIDOS', 'USUARIO VE SUS PEDIDOS')
        tickets=Modelo.tickets_tod(session['correo'])
        _ticketactivos=Modelo.Ttickets(session['correo'])
        _tickettotal=Modelo.Ttickett(session['correo'])
        _ticketfinal=Modelo.Tticketf(session['correo'])
        _username=Modelo.nomuser(session['name'])
        _DATAUSER=Modelo.DATOUSER(session['correo'])
        

        return render_template('edi_tc.html', tickets = tickets,tta= _ticketactivos[0][0],ttt= _tickettotal[0][0],ttf= _ticketfinal[0][0], nomre= _username[0][0],SERCHTIK=_SERCHT[0][0],SERCHTIK1=_SERCHT[0][1],SERCHTIK2=_SERCHT[0][2],SERCHTIK3=_SERCHT[0][3],SERCHTIK4=_SERCHT[0][4],SERCHTIK5=_SERCHT[0][5],SERCHTIK6=_SERCHT[0][6], DU =_DATAUSER)
    return redirect('mis_pedidos')


if __name__ == '__main__': 
    app.run(debug=True)
