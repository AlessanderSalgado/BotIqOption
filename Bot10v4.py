import subprocess
from logging import ERROR
from xml.etree.ElementTree import parse
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTime, Qt
from PyQt5.QtWidgets import QMessageBox
try:
    from iqoptionapi.stable_api import IQ_Option
except ModuleNotFoundError as e:
    pass
import time
from datetime import datetime, timedelta
import threading
import sched
import _thread
from decimal import Decimal
import time as time_module 
import os
from Crypto.Cipher import AES 
scheduler = sched.scheduler()
scheduler1 = sched.scheduler(time_module.time, time_module.sleep)

###############Verificação de integridade dos dados######
def TesteSys(): 
    if os.path.exists("error.ui") == False:
        arquivo = open('error.ui','w')
        arquivo.write('<?xml version="1.0" encoding="UTF-8"?><ui version="4.0"><class>MainWindow</class><widget class="QMainWindow" name="MainWindow"><property name="geometry"><rect><x>0</x><y>0</y><width>94</width><height>57</height></rect></property><property name="windowTitle"><string>MainWindow</string></property><widget class="QWidget" name="centralwidget"/><widget class="QMenuBar" name="menubar"><property name="geometry"><rect><x>0</x><y>0</y><width>94</width><height>21</height></rect></property></widget><widget class="QStatusBar" name="statusbar"/></widget><resources/><connections/></ui>')
        arquivo.close()
    if os.path.exists("config_n.txt") == False:
        arquivo = open('config_n.txt','w')
        arquivo.write(";;;;;;;;;;;;;;;")
        arquivo.close()
    if os.path.exists("hora_n.txt") == False:
        arquivo = open('hora_n.txt','w')
        arquivo.write("00:01,23:59")
        arquivo.close() 
    if os.path.exists("reset.txt") == False:
        arquivo = open('reset.txt','w')
        arquivo.write("True,10:00")
        arquivo.close()
    if os.path.exists("iqoptionapi") == False:
        app=QtWidgets.QApplication([])
        global error_t
        error_t=uic.loadUi('error.ui')
        QMessageBox.about(error_t, "Error Falta de pasta", "Pasta da API IqOption não encontrada")
        error_t.show()
        app.exec()
        exit()
    if os.path.exists("map_loss.txt") == False:
        arquivo = open('map_loss.txt','w')
        arquivo.write("00-00-0000 00:00:00|-1|P|padrao@padrao.com")
        arquivo.close()
    if os.path.exists("map_win.txt") == False:
        arquivo = open('map_win.txt','w')
        arquivo.write("00-00-0000 00:00:00|-1|P|padrao@padrao.com")
        arquivo.close()
TesteSys()
###############FIM#######################################
#inicialização da tela########################
app=QtWidgets.QApplication([])
global bot10v2
bot10v2=uic.loadUi('fonttela\\bot10v3.ui')
width_ = bot10v2.geometry().width()
height_ = bot10v2.geometry().height()
bot10v2.setFixedSize(width_,height_)
bot10v2.setWindowTitle('Bot10 version 4.0 Beta')


##################FIM################################
##############Ajusta hora do WINDOWS#####################
def AjustaHora():
    bot10v2.ajusta_hora.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';") 
    caminho = str(os.path.dirname(os.path.abspath(__file__))+"\\horasync\\timedateajuste.exe")
    os.system(caminho)
    time.sleep(3)
    bot10v2.ajusta_hora.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
AjustaHora()
###############FIM#######################################
################Funções lembrar de mim###############
def LembrarDeMim():
    login_senha = os.path.exists("Mark1.dll")
    if login_senha == True:
        key = b'(\x02\x800\x85\xc0\xcc\xd4\xa3Kx\xea\x9f\x97\xccP'
        file_in = open("Mark1.dll", "rb")
        nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        data = data.decode()
        data = data.split(',')
        login = data[0]
        senha = data[1]
        if data[2] == "True":
            ischecked = True
        elif data[2] == "False":
            ischecked = False
        else:
            ischecked = False
    else:
        ischecked = False
    bot10v2.lembrar.setChecked(ischecked)
    if bot10v2.lembrar.isChecked():
        bot10v2.login.setText(str(login))
        bot10v2.senha.setText(str(senha))
    else:
        bot10v2.login.setText("")
        bot10v2.senha.setText("")
LembrarDeMim()
def LembrarDeMim_gr():
    if bot10v2.lembrar.isChecked():
        password = bot10v2.login.text()+','+bot10v2.senha.text()+',True'
    else:
        password = ',,False'
    data = bytes(password, 'utf-8') 
    key = b'(\x02\x800\x85\xc0\xcc\xd4\xa3Kx\xea\x9f\x97\xccP'
    #print(key)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    file_out = open("Mark1.dll", "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()
####################fim#############################
#lista comboBox 
stop_win_list = (['1 Win','2 Win','3 Win','4 Win','5 Win','6 Win','7 Win','8 Win','9 Win','10 Win'])
soros_list = (['x 0.0','x 0.3','x 0.5','x 0.8','x 1.0'])
qtd_gale_list = (['0 Gale','1 Gale','2 Gale','3 Gale','4 Gale','5 Gale','6 Gale','7 Gale','8 Gale'])
perc_gale_list = (['x 0.0','x 1.1','x 1.2','x 1.3','x 1.8','x 2.0','x 2.1','x 2.2','x 2.3','x 2.6','x 3.0'])
direc_gale_list = (['Favor','Contra'])
tipo_list = (['digital','binary'])
divisor_list = (['5','6','7','8','9','10'])
meta_mes_list = (['3','5','8','10','12','15','18','20','25','30','35','40'])
otc_list = (['Sim','Não'])
contra_list = (['Favor','Contra'])
semana_list = (['Todos','Segunda','Terça','Quarta','Quinta','Sexta','Sabado','Domingo'])
reset_tempo_list = (['Nenhum','30 Minutos','1 Hora','2 Horas','3 Horas','4 Horas','6 Horas'])
payout_minimo_list = (['50 %','55 %','60 %','65 %','70 %','75 %','80 %','85 %','90 %','95 %'])
#Funcao para variaveis globais
def variaveis():
    conected = False
    relativo = ''
    qtdent = ''
    ve_v = ''
    tipo = ''
    tipo_aut_manu = ''
    intervalo = 0.0
    timeframe_minute = 0
    timeframe_second = 0
    valor_ent = ''
    m_entrada = ''
    salved = False
    liberado = False
    progress_ = 0
    Liberasis = False
    martingale = 0
    ag_par_mhi = ''
    ag_hora_mhi = ''
    ag_estrategia_mhi = ''
    ag_par_est1 = ''
    ag_hora_est1 = ''
    ag_estrategia_est1 = ''
    cont_win = 0
    cont_loss = 0
    contagem_win = 0
    contagem_loss = 0
    soros = 0.0
    qtd_gale = 0
    perc_gale = 0.0
    direc_gale = ''
    reset_stops = 0
    divisor = 0
    meta_mes = 0
    tipo_conta = ''
    chave = ''
    login = ''
    crypto = ''
    contra = ''
    control = 'off'
    recuperativo = False
    gale_na_proxima = 'False'
    gale_na_proxima_ = 0
    semana = ''
    reset_tempo = ''
    otc = True
    guard_ent = 0
    ten_merca = 'False'
    payout_minimo = '80' 
#Funcao conectar na iq
def conectar():
    bot10v2.bnt_logar.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    login=bot10v2.login.text()
    senha=bot10v2.senha.text()
    LembrarDeMim_gr()
    if login == "" or senha == "":
        #conected = False
        variaveis.conected = False
        print("Por favor preencha os campos de Login e Senha")
        QMessageBox.about(bot10v2, "Erro de Login", "Vc precisa preencher os campos login e senha")
    else:
        print(login)
        global Iq
        Iq=IQ_Option(login,senha)
        Iq.connect()
        #Iq.logout()
        while True:
            if Iq.check_connect()==False:#detect the websocket is close
                print("Tentando conectar")
                print('Confira Seu Login e senha.')
                Iq.connect()#try to connect
                #conected = False
                variaveis.conected = False
                variaveis.Liberasis = False
                QMessageBox.about(bot10v2, "Erro de Login", "Login ou senha invalida.")
                break
            else:
                #conected = True
                variaveis.conected = True
                variaveis.Liberasis = True
                #carregaconfig()
                #_thread.start_new_thread(liberasis,(0,0))
                print('Conectado');
                print(variaveis.conected)
                break;
        time.sleep(1);
        if variaveis.conected == True:
            bot10v2.login.setText('')
            bot10v2.senha.setText("")
            bot10v2.frame_conta.setVisible(True)
            bot10v2.tabWidget.setVisible(True)
            Iq.change_balance('PRACTICE') #PRACTICE\REAL
            variaveis.tipo_conta = 'P'
            variaveis.chave = login
            variaveis.login = login
            bot10v2.tipo_c.setStyleSheet("color: #ff5500;background-color: #ffffff; font: 75 8pt 'Verdana';")
            bot10v2.saldo.setStyleSheet("color: #ff5500;background-color: #ffffff; font: 75 8pt 'Verdana';")
            banca_tipo = Iq.get_balance_mode()
            bot10v2.tipo_c.setText(str(banca_tipo))
            banca_valor = Iq.get_balance()
            bot10v2.saldo.setText(str(banca_valor))
            carregaconfig()
            _thread.start_new_thread(liberasis,(0,0))
            #_thread.start_new_thread(media_moveis,(0,0))
        else:
            print('Error')
#Fancao desconectar na iq
def logout():
    bot10v2.bnt_logar.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
    if variaveis.conected == True:
        if Iq.check_connect() == True:
            variaveis.conected = False
            variaveis.Liberasis = False
            Iq.logout()
            bot10v2.frame_conta.setVisible(False)
            bot10v2.frame_login.setVisible(True)
            bot10v2.tabWidget.setVisible(False)
        elif Iq.check_connect() == False:
            bot10v2.frame_conta.setVisible(False)
            bot10v2.frame_login.setVisible(True)
            bot10v2.tabWidget.setVisible(False)
        else:
            print('Error ao tentar sair')
    LembrarDeMim()
#Funcao troca conta iq
def troca_conta():
    if variaveis.conected == True:
        if Iq.get_balance_mode() == 'PRACTICE':
            print('Estou na conta REAL');
            Iq.change_balance('REAL') #PRACTICE\REAL
            variaveis.tipo_conta = 'R'
            banca_tipo = Iq.get_balance_mode();
            banca_valor = Iq.get_balance();
            bot10v2.tipo_c.setStyleSheet("color: #00aa00;background-color: #ffffff; font: 75 8pt 'Verdana';")
            bot10v2.saldo.setStyleSheet("color: #00aa00;background-color: #ffffff; font: 75 8pt 'Verdana';")
            bot10v2.tipo_c.setText(str(banca_tipo));
            bot10v2.saldo.setText(str(banca_valor));
        else:
            print('Estou na conta PRACTICE');
            Iq.change_balance('PRACTICE') #PRACTICE\REAL
            variaveis.tipo_conta = 'P'
            banca_tipo = Iq.get_balance_mode();
            banca_valor = Iq.get_balance();
            bot10v2.tipo_c.setStyleSheet("color: #ff5500;background-color: #ffffff; font: 75 8pt 'Verdana';")
            bot10v2.saldo.setStyleSheet("color: #ff5500;background-color: #ffffff; font: 75 8pt 'Verdana';")
            bot10v2.tipo_c.setText(str(banca_tipo));
            bot10v2.saldo.setText(str(banca_valor));
    else:
        print('Não estou conectado')
#Fucao para pegar as configuracoes do bot
def carregaconfig():
    #_thread.start_new_thread(media_moveis,(0,0))
    variaveis.contagem_win = 0
    variaveis.contagem_loss = 0
    variaveis.relativo = '0'
    variaveis.control = 'off'
    variaveis.gale_na_proxima_ = 0
    bot10v2.relativo.setText(variaveis.relativo)
    bot10v2.cont_win.setText(str(variaveis.contagem_win))
    bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
    arquivo = open("config_n.txt", "r");
    for linha in arquivo:
        linha = linha.split(';')
        bot10v2.v_ent.setText(linha[0])
        stop_win = linha[1]
        soros = linha[2]
        qtd_gale = linha[3]
        perc_gale = linha[4]
        direc_gale = linha[5]
        tipo = linha[6]
        divisor = linha[7]
        #meta_mes = linha[8]
        contra = linha[8]
        otc = linha[9]
        semana = linha[10]
        reset_tempo = linha[11]
        gale_proxima = linha[13]
        recuperativo = linha[12]
        ten_merca = linha[14]
        payout_minimo = linha[15]
    arquivo.close()
    
    if stop_win in stop_win_list:
        bot10v2.stop_win.setCurrentIndex(stop_win_list.index(stop_win))
        stop_win = stop_win.split(' ')
        variaveis.cont_win = int(stop_win[0])
    if soros in soros_list:
        bot10v2.soros.setCurrentIndex(soros_list.index(soros))
        soros = soros.split(' ')
        variaveis.soros = float(soros[1])
    if qtd_gale in qtd_gale_list:
        bot10v2.qtd_gale.setCurrentIndex(qtd_gale_list.index(qtd_gale))
        qtd_gale = qtd_gale.split(' ')
        variaveis.qtd_gale = int(qtd_gale[0])
    if perc_gale in perc_gale_list:
        bot10v2.perc_gale.setCurrentIndex(perc_gale_list.index(perc_gale))
        perc_gale = perc_gale.split(' ')
        variaveis.perc_gale = float(perc_gale[1])
    if direc_gale in direc_gale_list:
        bot10v2.direc_gale.setCurrentIndex(direc_gale_list.index(direc_gale))
        variaveis.direc_gale = str(direc_gale)
    if tipo in tipo_list:
        bot10v2.tipo.setCurrentIndex(tipo_list.index(tipo))
        variaveis.tipo = str(tipo)
    if divisor in divisor_list:
        bot10v2.divisor.setCurrentIndex(divisor_list.index(divisor))
        variaveis.divisor = int(divisor)
    if otc in otc_list:
        bot10v2.otc.setCurrentIndex(otc_list.index(otc))
        variaveis.otc = otc
    if semana in semana_list:
        bot10v2.semana.setCurrentIndex(semana_list.index(semana))
        variaveis.semana = str(semana)
    if reset_tempo in reset_tempo_list:
        bot10v2.reset_tempo.setCurrentIndex(reset_tempo_list.index(reset_tempo))
        variaveis.reset_tempo = str(reset_tempo)
    if contra in contra_list:
        bot10v2.contra.setCurrentIndex(contra_list.index(contra))
        variaveis.contra = str(contra)
    if payout_minimo in payout_minimo_list:
        bot10v2.payout_minimo.setCurrentIndex(payout_minimo_list.index(payout_minimo))
        variaveis.payout_minimo = str(payout_minimo)

    arquivo = open("hora_n.txt", "r")
    for linha in arquivo:
        linha = linha.split(',')
        ini = linha[0]
        fim = linha[1]
    arquivo.close()
    ini = ini.split(':')
    time_ini = QTime()
    time_ini.setHMS(int(ini[0]),int(ini[1]),00)
    bot10v2.ini.setTime(time_ini)
    fim = fim.split(':')
    time_fim = QTime()
    time_fim.setHMS(int(fim[0]),int(fim[1]),00)
    bot10v2.fim.setTime(time_fim) 
    arquivo = open("reset.txt", "r");
    for linha in arquivo:
        linha = linha.split(',')
        ativa_reset = linha[0]
        hora_reset = linha[1]
    arquivo.close()
    
    if recuperativo == 'True':
        bot10v2.recuperativo.setChecked(True)
    else:
        bot10v2.recuperativo.setChecked(False)
    
    if gale_proxima == 'True':
        bot10v2.gale_na_proxima.setChecked(True)
        variaveis.gale_na_proxima = 'True'
    else:
        bot10v2.gale_na_proxima.setChecked(False)
        variaveis.gale_na_proxima = 'False'
        
    if ten_merca == 'True':
        bot10v2.ten_merca.setChecked(True)
        variaveis.ten_merca = 'True'
    else:
        bot10v2.ten_merca.setChecked(False)
        variaveis.ten_merca = 'False'
    
    if ativa_reset == 'True':
        bot10v2.check_reset.setChecked(True)
        bot10v2.h_reset.setVisible(True)
        bot10v2.reset_tempo.setEnabled(False)    
        hora_reset = hora_reset.split(':')
        time_reset = QTime()
        time_reset.setHMS(int(hora_reset[0]),int(hora_reset[1]),00)
        bot10v2.h_reset.setTime(time_reset)
        variaveis.reset_stops = 1 
    else:
        bot10v2.check_reset.setChecked(False) 
        variaveis.reset_stops = 0 
#funcao que grava as alteracoes das configuracoes
def salvaconfig():
    v_ent = bot10v2.v_ent.text()
    variaveis.ve_v = v_ent
    variaveis.salved = True
    h_ini = bot10v2.ini.text()
    h_fim = bot10v2.fim.text()
    stop_win = bot10v2.stop_win.currentText()
    soros = bot10v2.soros.currentText()
    qtd_gale = bot10v2.qtd_gale.currentText()
    perc_gale = bot10v2.perc_gale.currentText()
    direc_gale = bot10v2.direc_gale.currentText()
    tipo = bot10v2.tipo.currentText()
    divisor = bot10v2.divisor.currentText()
    #meta_mes = bot10v2.meta_mes.currentText()
    contra = bot10v2.contra.currentText()
    otc = bot10v2.otc.currentText()
    semana = bot10v2.semana.currentText()
    reset_tempo = bot10v2.reset_tempo.currentText()
    payout_minimo = bot10v2.payout_minimo.currentText()

    if h_ini == '00:00':
        QMessageBox.about(bot10v2, "Error", "Hora de inicio não pode ser 00")
    elif h_fim == '00:00':
        QMessageBox.about(bot10v2, "Error", "Hora fim não pode ser 00")
    else:
        arq_hora = open('hora_n.txt', 'w+')
        arq_hora.writelines(str(h_ini)+','+str(h_fim))
        arq_hora.close()

    if bot10v2.recuperativo.isChecked():
        recuperativo = True
    else:
        recuperativo = False
        
    if bot10v2.gale_na_proxima.isChecked():
        gale_na_proxima = True
    else:
        gale_na_proxima = False
        
    if bot10v2.ten_merca.isChecked():
        ten_merca = True
    else:
        ten_merca = False

    if bot10v2.check_reset.isChecked():
        reset_valor = 'True'
        h_reset = bot10v2.h_reset.text()
        arquivo = open('reset.txt','w')
        arquivo.writelines(reset_valor+','+h_reset)
        arquivo.close()
        bot10v2.check_reset.setEnabled(False)
        bot10v2.h_reset.setEnabled(False)
    else:
        reset_valor = 'False'
        arquivo = open('reset.txt','w')
        arquivo.writelines(reset_valor+','+'error')
        arquivo.close()
        bot10v2.check_reset.setEnabled(False)

    arquivo = open("config_n.txt", "w+")
    arquivo.writelines(v_ent+';'+stop_win+';'+soros+';'+qtd_gale+';'+perc_gale+';'+direc_gale+';'+tipo+';'+divisor+';'+contra+';'+otc+';'+semana+';'+reset_tempo+';'+str(recuperativo)+';'+str(gale_na_proxima)+';'+str(ten_merca)+';'+str(payout_minimo))
    arquivo.close()
    
    bot10v2.recuperativo.setEnabled(False)
    bot10v2.gale_na_proxima.setEnabled(False)
    bot10v2.ten_merca.setEnabled(False)
    bot10v2.payout_minimo.setEnabled(False)
    bot10v2.otc.setEnabled(False)
    bot10v2.semana.setEnabled(False)
    bot10v2.reset_tempo.setEnabled(False)
    
    bot10v2.contra.setEnabled(False)
    bot10v2.salvar.setEnabled(False)
    bot10v2.divisor.setEnabled(False)
    bot10v2.iniciar_bot.setVisible(True)
    bot10v2.parar_bot.setVisible(True)
    bot10v2.parar_bot.setEnabled(False)
    bot10v2.troca_conta.setEnabled(False)
    bot10v2.v_ent.setEnabled(False)
    bot10v2.ini.setEnabled(False)
    bot10v2.fim.setEnabled(False)
    bot10v2.stop_win.setEnabled(False)
    bot10v2.soros.setEnabled(False)
    bot10v2.qtd_gale.setEnabled(False)
    bot10v2.perc_gale.setEnabled(False)
    bot10v2.direc_gale.setEnabled(False)
    bot10v2.tipo.setEnabled(False)
    bot10v2.painel.setText('Bot pronto para operar')
    QMessageBox.about(bot10v2, "Salvando", "Configurações salvas com sucesso")
    bot10v2.editar.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.salvar.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.troca_conta.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.parar_bot.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.listWidget.setSortingEnabled(True)
    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Configurações carreagadas com sucesso: ')
    carregaconfig()
#Funcao quelibera as configuracoes para edicao
def editconf():
    bot10v2.contra.setEnabled(True)
    bot10v2.recuperativo.setEnabled(True)
    bot10v2.gale_na_proxima.setEnabled(True)
    bot10v2.ten_merca.setEnabled(True)
    bot10v2.payout_minimo.setEnabled(True)
    bot10v2.otc.setEnabled(True)
    bot10v2.semana.setEnabled(True)
    bot10v2.reset_tempo.setEnabled(True)
    bot10v2.divisor.setEnabled(True)
    bot10v2.salvar.setEnabled(True)
    bot10v2.iniciar_bot.setVisible(False)
    bot10v2.parar_bot.setVisible(False)
    bot10v2.check_reset.setEnabled(True)
    if bot10v2.check_reset.isChecked():
        bot10v2.h_reset.setEnabled(True)
    bot10v2.troca_conta.setEnabled(True)
    bot10v2.v_ent.setEnabled(True)
    bot10v2.ini.setEnabled(True)
    bot10v2.fim.setEnabled(True)
    bot10v2.stop_win.setEnabled(True)
    bot10v2.soros.setEnabled(True)
    bot10v2.qtd_gale.setEnabled(True)
    bot10v2.perc_gale.setEnabled(True)
    bot10v2.direc_gale.setEnabled(True)
    bot10v2.tipo.setEnabled(True)
    bot10v2.painel.setText('Bot em modo edit.')
    bot10v2.editar.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.salvar.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.troca_conta.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
#Funcao para so rodar no horario setado, roda enquanto o sistema estiver aberto
def liberasis(arg1,arg2): 
    while True:
        if Iq.check_connect()==False:
            break
        resultados()
        if variaveis.Liberasis == False:
            break
        hora_atual = time.time()
        hora_atual = time.strftime('%H:%M')
        arquivo = open('hora_n.txt','r')
        for linha in arquivo:
            linha = linha.split(',')
            ini = linha[0].strip()
            fim = linha[1].strip()
        arquivo.close()
        ini = datetime.strptime(ini,'%H:%M')
        fim = datetime.strptime(fim,'%H:%M')
        hora_atual = datetime.strptime(hora_atual,'%H:%M')
        #print('HA '+str(hora_atual))
        #print('INI '+str(ini))
        #print('FIM '+str(fim))

        if hora_atual >= ini and hora_atual <= fim:
            #print('entrei')
            #telaPrincipal.liga.setText('Bot em operçao')
            variaveis.liberado = True
            #print(variaveis.liberado)
        elif hora_atual < ini:
            #print('Nao esta na hora de iniciar')
            #telaPrincipal.liga.setText('Bot paralizado, fora de horario')
            variaveis.liberado = False
            #print(variaveis.liberado)
        elif hora_atual > fim:
            #telaPrincipal.liga.setText('Bot paralizado, fora de horario')
            #print('Ja passamos da hora')
            variaveis.liberado = False
            #print(variaveis.liberado)
        else:
            #print('error de conferencia')
            variaveis.liberado = False
            #print(variaveis.liberado)

        if variaveis.reset_stops == 1:
            hora_reset1 = bot10v2.h_reset.text()
            hora_reset1 = datetime.strptime(hora_reset1,'%H:%M')
            #print(hora_reset1)
            #print(hora_atual)
            if hora_atual == hora_reset1:
                print('reset stop')
                #variaveis.contagem_win = 0
                carregaconfig()
        time.sleep(29)
    _thread.exit()
#Funcao que mostra a hora para reset stop
def hora_reset():
    if bot10v2.check_reset.isChecked():
        bot10v2.h_reset.setVisible(True)
        bot10v2.reset_tempo.setEnabled(False)
    else:
        bot10v2.h_reset.setVisible(False)
        bot10v2.reset_tempo.setEnabled(True)
#fncao aviso max win max peras
def maxwinloss():
    #print('teste')
    v_ent = bot10v2.v_ent.text()
    v_ent_g = bot10v2.v_ent.text()
    v_ent = round(Decimal(v_ent) / 100,2)
    v_ent = round(Decimal(75) * Decimal(v_ent),2)
    
    stop_win = bot10v2.stop_win.currentText()
    stop_win = stop_win.split(' ')
    stop_win = int(stop_win[0])

    soros = bot10v2.soros.currentText()
    soros = soros.split(' ')
    soros = round(Decimal(soros[1]),2)
    soros = round(Decimal(v_ent) * Decimal(soros),2)
    v_ent = round(Decimal(v_ent) + Decimal(soros),2)
    v_ent_g = round(Decimal(v_ent_g) + Decimal(soros),2)
    
    qtd_gale = bot10v2.qtd_gale.currentText()
    qtd_gale = qtd_gale.split(' ')
    qtd_gale = int(qtd_gale[0])
    
    perc_gale = bot10v2.perc_gale.currentText()
    perc_gale = perc_gale.split(' ')
    perc_gale = round(Decimal(perc_gale[1]),2)

    maxloss = '0'
    if qtd_gale == 0:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
    elif qtd_gale == 1:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1
    elif qtd_gale == 2:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss2 = round(Decimal(maxloss1) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1 + maxloss2
    elif qtd_gale == 3:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss2 = round(Decimal(maxloss1) * Decimal(perc_gale),2)
        maxloss3 = round(Decimal(maxloss2) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1 + maxloss2 + maxloss3
    elif qtd_gale == 4:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss2 = round(Decimal(maxloss1) * Decimal(perc_gale),2)
        maxloss3 = round(Decimal(maxloss2) * Decimal(perc_gale),2)
        maxloss4 = round(Decimal(maxloss3) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1 + maxloss2 + maxloss3 + maxloss4
    elif qtd_gale == 5:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss2 = round(Decimal(maxloss1) * Decimal(perc_gale),2)
        maxloss3 = round(Decimal(maxloss2) * Decimal(perc_gale),2)
        maxloss4 = round(Decimal(maxloss3) * Decimal(perc_gale),2)
        maxloss5 = round(Decimal(maxloss4) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1 + maxloss2 + maxloss3 + maxloss4 + maxloss5
    elif qtd_gale == 6:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss2 = round(Decimal(maxloss1) * Decimal(perc_gale),2)
        maxloss3 = round(Decimal(maxloss2) * Decimal(perc_gale),2)
        maxloss4 = round(Decimal(maxloss3) * Decimal(perc_gale),2)
        maxloss5 = round(Decimal(maxloss4) * Decimal(perc_gale),2)
        maxloss6 = round(Decimal(maxloss5) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1 + maxloss2 + maxloss3 + maxloss4 + maxloss5 + maxloss6
    elif qtd_gale == 7:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss2 = round(Decimal(maxloss1) * Decimal(perc_gale),2)
        maxloss3 = round(Decimal(maxloss2) * Decimal(perc_gale),2)
        maxloss4 = round(Decimal(maxloss3) * Decimal(perc_gale),2)
        maxloss5 = round(Decimal(maxloss4) * Decimal(perc_gale),2)
        maxloss6 = round(Decimal(maxloss5) * Decimal(perc_gale),2)
        maxloss7 = round(Decimal(maxloss6) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1 + maxloss2 + maxloss3 + maxloss4 + maxloss5 + maxloss6 + maxloss7
    elif qtd_gale == 8:
        maxloss = round(Decimal(v_ent_g * (-1)),2)
        maxloss1 = round(Decimal(maxloss) * Decimal(perc_gale),2)
        maxloss2 = round(Decimal(maxloss1) * Decimal(perc_gale),2)
        maxloss3 = round(Decimal(maxloss2) * Decimal(perc_gale),2)
        maxloss4 = round(Decimal(maxloss3) * Decimal(perc_gale),2)
        maxloss5 = round(Decimal(maxloss4) * Decimal(perc_gale),2)
        maxloss6 = round(Decimal(maxloss5) * Decimal(perc_gale),2)
        maxloss7 = round(Decimal(maxloss6) * Decimal(perc_gale),2)
        maxloss8 = round(Decimal(maxloss7) * Decimal(perc_gale),2)
        maxloss = maxloss + maxloss1 + maxloss2 + maxloss3 + maxloss4 + maxloss5 + maxloss6 + maxloss7 + maxloss8

    maxwin = ((v_ent * stop_win) - soros)
    bot10v2.maxwinloss.setText('Max win: '+str(maxwin)+' Max loss: '+str(maxloss))

def ten_merca():
    if bot10v2.check_reset.isChecked():
        bot10v2.h_reset.setVisible(True)
        bot10v2.reset_tempo.setEnabled(False)
    else:
        bot10v2.h_reset.setVisible(False)
        bot10v2.reset_tempo.setEnabled(True)

#Media moveis
def media_moveis(par_testado,arg2):
    indicators = {}
    try:
        indicators = Iq.get_technical_indicators(par_testado)
    except KeyError as e:
        print(e)
        pass
    #print(indicators)
    global code_
    code_ = 'o'
    m1 = {} 
    m5 = {} 
    m15 = {}
    global call_mm
    call_mm = 0
    global call_mm_m1
    call_mm_m1 = 0
    global put_mm
    put_mm = 0
    global put_mm_m1
    put_mm_m1 = 0
    #global par_teste_
    try:
        code_ = indicators['code']
    except TypeError as e:
        code_ = 't'
        pass
    except KeyError as j:
        code_ = 't'
        pass
    # 'code': 'no_technical_indicator_available'
    if code_ == 'no_technical_indicator_available':
        print('Par nao suporta')
        code_ = 't' 
        pass
    else:
        code_ = 'i'
        par_teste_ = par_testado
        for indicador in indicators:
            v = indicador['action']
            group = indicador['group']
            candle_size = indicador['candle_size']
            if group == 'MOVING AVERAGES':
                if candle_size == 60:
                    if v not in m1:
                        m1[v] = 0
                    m1[v] += 1             
                if candle_size == 300:
                    if v not in m5:
                        m5[v] = 0
                    m5[v] += 1
                if candle_size == 900:
                    if v not in m15:
                        m15[v] = 0
                    m15[v] += 1
        try:
            if m1['buy']:
                call_mm += m1['buy']
                call_mm_m1 += m1['buy']
        except KeyError as e:
                call_mm += 0
                call_mm_m1 += 0 
        try: 
            if m1['sell']:
                put_mm += m1['sell']
                put_mm_m1 += m1['sell']
        except KeyError as e: 
            put_mm += 0
            put_mm_m1 += 0
        try:
            if m5['buy']:
                call_mm += m5['buy']
        except KeyError as e:
            call_mm += 0
        try:
            if m5['sell']:
                put_mm += m5['sell']
        except KeyError as e: 
            put_mm += 0
        try:
            if m15['buy']:
                call_mm += m15['buy']
        except KeyError as e:
            call_mm += 0
        try:
            if m15['sell']:
                put_mm += m15['sell']
        except KeyError as e: 
            put_mm += 0
        #print('Par ',par_testado,'M1: ', m1)
        #print('Par ',par_testado,'M5: ', m5)
        #print('Par ',par_testado,'M15: ', m15)
        print('Par ',par_testado,' Compra ',call_mm,' Venda ', put_mm)  
#osciladores
def oscilador(par_testado,arg2):
    indicators = {}
    try: 
        indicators = Iq.get_technical_indicators(par_testado)
    except KeyError as e:
        print(e)
        pass
    #print(indicators)
    global code_
    code_ = 'o'
    m1 = {} 
    m5 = {} 
    m15 = {}
    global call_os
    call_os = 0
    global put_os
    put_os = 0
    #global par_teste_
    try:
        code_ = indicators['code']
    except TypeError as e:
        code_ = 't'
        pass
    except KeyError as j:
        code_ = 't'
        pass
    # 'code': 'no_technical_indicator_available'
    if code_ == 'no_technical_indicator_available':
        print('Par nao suporta')
        code_ = 't' 
        pass
    else:
        code_ = 'i'
        par_teste_ = par_testado
        for indicador in indicators:
            v = indicador['action']
            group = indicador['group']
            candle_size = indicador['candle_size']
            if group == 'OSCILLATORS':
                if candle_size == 60:
                    if v not in m1:
                        m1[v] = 0
                    m1[v] += 1 
        try:
            if m1['buy']:
                call_os += m1['buy']
        except KeyError as e:
                call_os += 0 
        try: 
            if m1['sell']:
                put_os += m1['sell']
        except KeyError as e: 
            put_os += 0 
        print('Par ',par_testado,' Compra ',call_os,' Venda ', put_os) 
#Estrategia primeira
def montavela_retracao15(open_,close_,max_,min_):
    retorno = True
    direcao_ = ''
    pavio_max = False
    pavio_min = False
    pavio_max_min = False
    valor_vela_open_close = '0'
    valor_vela_max_min = '0'
    valor_vela_max_open ='0'
    valor_vela_max_close = '0'
    valor_vela_min_open = '0'
    valor_vela_min_close = '0'
    rabo_vela_pbaixo = Decimal(0.0)
    rabo_vela_pcima = Decimal(0.0)
    try:
        retorno = bool(abs(close_ - open_) / (max_ - min_) < 0.1 and \
                    (max_ - max(close_, open_)) > (4 * abs(close_ - open_)) and \
                    (min(close_, open_) - min_) > (4 * abs(close_ - open_)))
    except ZeroDivisionError as e:
        retorno = True
        #print(e)
    if close_ > open_ and retorno == False:
        direcao_ = 'call'
        pavio_max = bool(abs(max_ > close_) and abs(min_ == open_))
        pavio_min = bool(abs(max_ == close_) and abs(min_ < open_))
        pavio_max_min = bool(abs(max_ > close_) and abs(min_ < open_))
        valor_vela_open_close = close_ - open_
        valor_vela_max_min = max_ - min_
        valor_vela_max_open = max_ - open_
        valor_vela_max_close = max_ - close_
        valor_vela_min_open = min_ - open_
        valor_vela_min_close = min_ - close_
        rabo_vela_pbaixo = Decimal(((min_ / open_)* 100))
        rabo_vela_pcima = Decimal(((max_ / close_)* 100))
    elif close_ < open_ and retorno == False:
        direcao_ = 'put'
        pavio_max = bool(abs(max_ > open_) and abs(min_ == close_))
        pavio_min = bool(abs(max_ == open_) and abs(min_ < close_))
        pavio_max_min = bool(abs(max_ > open_) and abs(min_ < close_))
        valor_vela_open_close = open_ - close_
        valor_vela_max_min = max_ - min_
        valor_vela_max_open = max_ - open_
        valor_vela_max_close = max_ - close_
        valor_vela_min_open = min_ - open_
        valor_vela_min_close = min_ - close_
        rabo_vela_pbaixo = Decimal(((min_ / close_)* 100))
        rabo_vela_pcima = Decimal(((open_ / max_)* 100))
    elif close_ == open_ and retorno == False:
        direcao_ = 'doji'
        retorno = True
        pavio_max = False
        pavio_min = False
        pavio_max_min = False
        valor_vela_open_close = '0'
        valor_vela_max_min = '0'
        valor_vela_max_open = '0'
        valor_vela_max_close = '0'
        valor_vela_min_open = '0'
        valor_vela_min_close = '0'
    elif close_ == open_ and retorno == True:
        direcao_ = 'doji'
        pavio_max = False
        pavio_min = False
        pavio_max_min = False
        valor_vela_open_close = '0'
        valor_vela_max_min = '0'
        valor_vela_max_open = '0'
        valor_vela_max_close = '0'
        valor_vela_min_open = '0'
        valor_vela_min_close = '0'
    elif retorno == True:
        direcao_ = 'doji'
        pavio_max = False
        pavio_min = False
        pavio_max_min = False
        valor_vela_open_close = '0'
        valor_vela_max_min = '0'
        valor_vela_max_open = '0'
        valor_vela_max_close = '0'
        valor_vela_min_open = '0'
        valor_vela_min_close = '0'
    return direcao_, rabo_vela_pcima, rabo_vela_pbaixo, valor_vela_open_close

def resultados():
    #print()
    banca_valor = Iq.get_balance()
    bot10v2.satual.setText('Saldo Atual:      '+str(banca_valor))
    hoje = datetime.fromtimestamp(Iq.get_server_timestamp())
    hoje_ = str(datetime.strftime(hoje,'%d-%m-%Y'))
    hoje__ = str(datetime.strftime(hoje,'%d/%m'))
    bot10v2.hoje.setText(str(hoje__))
    ontem = hoje - timedelta(days=1)
    ontem_ = str(datetime.strftime(ontem,'%d-%m-%Y'))
    ontem__ = str(datetime.strftime(ontem,'%d/%m'))
    bot10v2.ontem.setText(str(ontem__))
    antontem = hoje - timedelta(days=2)
    antontem_ = str(datetime.strftime(antontem,'%d-%m-%Y'))
    antontem__ = str(datetime.strftime(antontem,'%d/%m'))
    bot10v2.antontem.setText(str(antontem__))
    este_mes = str(datetime.strftime(hoje,'%m-%Y'))
    estemes__ = str(datetime.strftime(hoje,'%m/%Y'))
    bot10v2.estemes.setText(str(estemes__))
    mespass = hoje - timedelta(days=30) #month
    mespass_ = str(datetime.strftime(mespass,'%m/%Y'))
    mespass__ = str(datetime.strftime(mespass,'%m-%Y'))
    bot10v2.mespass.setText(str(mespass_))
    ano_ = str(datetime.strftime(hoje,'%Y'))
    bot10v2.ano.setText(str(ano_))
    valor_win_hoje = 0
    valor_loss_hoje = 0
    valor_win_ontem = 0
    valor_loss_ontem = 0
    valor_win_antontem = 0
    valor_loss_antontem = 0
    valor_win_estemes = 0
    valor_loss_estemes = 0
    valor_win_mespass = 0
    valor_loss_mespass = 0
    valor_win_ano = 0
    valor_loss_ano = 0
    arquivo = open('map_win.txt','r')
    for linha in arquivo:
        #print(linha)
        linha = linha.split('|')
        data = linha[0].split(' ')
        data = data[0].strip()
        estemes = data.split('-')
        estemes = estemes[1]+'-'+estemes[2]
        data2 = linha[0].split(' ')
        data2 = data2[0].strip()
        mespass_arq = data2.split('-')
        ano__ = mespass_arq[2]
        mespass_arq = mespass_arq[1]+'-'+mespass_arq[2]
        #print(estemes)
        valor = float(linha[1].strip())
        tipo_conta = linha[2].strip()
        login = linha[3].strip()
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and data == hoje_:
            valor_win_hoje += round(Decimal(valor),2)
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and data == ontem_:
            valor_win_ontem += round(Decimal(valor),2)
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and data == antontem_:
            valor_win_antontem += round(Decimal(valor),2)
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and estemes == este_mes:
            valor_win_estemes += round(Decimal(valor),2) 
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and mespass_arq == mespass__:
            valor_win_mespass += round(Decimal(valor),2) 
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and ano__ == ano_:
            valor_win_ano += round(Decimal(valor),2) 
    arquivo.close()
    arquivo = open('map_loss.txt','r')
    for linha in arquivo:
        #print(linha)
        linha = linha.split('|')
        data = linha[0].split(' ')
        data = data[0].strip()
        estemes = data.split('-')
        estemes = estemes[1]+'-'+estemes[2]
        data2 = linha[0].split(' ')
        data2 = data2[0].strip()
        mespass_arq = data2.split('-')
        ano__ = mespass_arq[2]
        mespass_arq = mespass_arq[1]+'-'+mespass_arq[2]
        valor = float(linha[1].strip())
        tipo_conta = linha[2].strip()
        login = linha[3].strip()
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and data == hoje_:
            valor_loss_hoje += round(Decimal(valor),2)
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and data == ontem_:
            valor_loss_ontem += round(Decimal(valor),2)
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and data == antontem_:
            valor_loss_antontem += round(Decimal(valor),2)
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and estemes == este_mes:
            valor_loss_estemes += round(Decimal(valor),2) 
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and mespass_arq == mespass__:
            valor_loss_mespass += round(Decimal(valor),2)
        if tipo_conta == variaveis.tipo_conta and login == variaveis.login and ano__ == ano_:
            valor_loss_ano += round(Decimal(valor),2)
    arquivo.close()
    bot10v2.winhoje.setText(str(valor_win_hoje))
    bot10v2.losshoje.setText(str(valor_loss_hoje))
    resulthoje = valor_win_hoje + valor_loss_hoje
    bot10v2.resulthoje.setText(str(resulthoje))
    bot10v2.winontem.setText(str(valor_win_ontem))
    bot10v2.lossontem.setText(str(valor_loss_ontem))
    resultontem = valor_win_ontem + valor_loss_ontem
    bot10v2.resultontem.setText(str(resultontem))
    bot10v2.winantontem.setText(str(valor_win_antontem))
    bot10v2.lossantontem.setText(str(valor_loss_antontem))
    resultantontem = valor_win_antontem + valor_loss_antontem
    bot10v2.resultantontem.setText(str(resultantontem))
    bot10v2.winestemes.setText(str(valor_win_estemes))
    bot10v2.lossestemes.setText(str(valor_loss_estemes))
    resultestemes = valor_win_estemes + valor_loss_estemes
    bot10v2.resultestemes.setText(str(resultestemes))
    
    bot10v2.winmespass.setText(str(valor_win_mespass))
    bot10v2.lossmespass.setText(str(valor_loss_mespass))
    resultmespass = valor_win_mespass + valor_loss_mespass
    bot10v2.resultadomespass.setText(str(resultmespass))
    
    bot10v2.winano.setText(str(valor_win_ano))
    bot10v2.lossano.setText(str(valor_loss_ano))
    resultano = valor_win_ano + valor_loss_ano
    bot10v2.resultano.setText(str(resultano))

def travaBotoes():
    bot10v2.editar.setEnabled(False)
    bot10v2.sair.setEnabled(False)
    bot10v2.parar_bot.setEnabled(True)
    bot10v2.iniciar_bot.setEnabled(False)
    bot10v2.iniciar_bot.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.parar_bot.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.sair.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.editar.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")

def destravaBotoes():
    print('teste')

def retracao15():
    hora_iq = datetime.fromtimestamp(Iq.get_server_timestamp())
    if variaveis.control == 'on':
        scheduler.enter(delay=16, priority=0, action=iniretracao15)
        scheduler.run(blocking=True)
        _thread.exit()
    #print(variaveis.liberado)
    if variaveis.liberado == False:
        bot10v2.painel_2.setText('Bot fora de horario.')
        scheduler.enter(delay=13, priority=0, action=iniretracao15)
        scheduler.run(blocking=True)
        _thread.exit()
    else:
        pass
    if variaveis.contagem_win >= variaveis.cont_win:
        bot10v2.cont_win.setText('Stop')
        bot10v2.painel_2.setText('Bot stop win ok.')
        scheduler.enter(delay=16, priority=0, action=iniretracao15)
        scheduler.run(blocking=True)
        _thread.exit()
    else:
        pass

    variaveis.control = 'on'
    bot10v2.painel_2.setText('Bot iniciado.') 
    #hora_iq_min = hora_iq.minute
    hora_iq_second = hora_iq.second
    print(str(datetime.strftime(hora_iq,'%Y-%m-%d %H:%M:%S'))) 
    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Ret 15 Buscando pares abertos, acumulando informações ')
    bot10v2.listWidget.sortItems(Qt.DescendingOrder)  #currentRow
    if hora_iq_second >= 9 and hora_iq_second <= 12:
        hora_iq = hora_iq - timedelta(seconds=hora_iq_second)
        hora_iq_ = hora_iq - timedelta(minutes=1)
        print(str(datetime.strftime(hora_iq,'%Y-%m-%d %H:%M:%S')))
        hora_iq_from_get_c = hora_iq.timestamp()
        hora_iq_ = hora_iq_.timestamp()
        if Iq.check_connect()==True:
            try:
                Par_list_ret15 = Iq.get_all_open_time()
            except UnboundLocalError as e:
                print(e)
                pass
            for par_ret15 in Par_list_ret15[variaveis.tipo]: #binary / digital
                if Par_list_ret15[variaveis.tipo][par_ret15]['open'] == True:
                    velas_ret15 = Iq.get_candles(par_ret15, 15, 5, hora_iq_from_get_c)
                    velas_ret15.reverse()
                    velas_ret15_ = Iq.get_candles(par_ret15, 60, 1, hora_iq_)
                    cons = 1
                    call = 0
                    put = 0
                    doji = 0
                    call_v2 = 0
                    put_v2 = 0
                    doji_v2 = 0
                    call_v3 = 0
                    put_v3 = 0
                    doji_v3 = 0
                    v1 = 0
                    v2 = 0
                    v3 = 0
                    v4 = 0
                    v5 = 0
                    direcao = 'Error'
                    #print(par_ret15)
                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Analizando Par: '+par_ret15)
                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                    #Qt.SortOrder 
                    doji_ = 0
                    for velas_ in velas_ret15_:
                        montavela_retracao15.direcao_, montavela_retracao15.rabo_vela_pcima, montavela_retracao15.rabo_vela_pbaixo, montavela_retracao15.valor_vela_open_close = montavela_retracao15(velas_['open'],velas_['close'],velas_['max'],velas_['min'])
                        if montavela_retracao15.direcao_ == 'doji':
                            doji_ += 1
                    for velas in velas_ret15:
                        if cons == 1:
                            montavela_retracao15.direcao_, montavela_retracao15.rabo_vela_pcima, montavela_retracao15.rabo_vela_pbaixo, montavela_retracao15.valor_vela_open_close = montavela_retracao15(velas['open'],velas['close'],velas['max'],velas['min'])
                            if montavela_retracao15.direcao_ == 'call':
                                call += 1
                            elif montavela_retracao15.direcao_ == 'put':
                                put += 1
                            elif montavela_retracao15.direcao_ == 'doji':
                                doji += 1
                            v1 = Decimal(montavela_retracao15.valor_vela_open_close)
                            #print('V1 antes ', v1)
                            v1 = v1 / 10
                            v1 = v1 * variaveis.divisor
                            #print('V1 apos ',v1)
                        elif cons == 2:
                            montavela_retracao15.direcao_, montavela_retracao15.rabo_vela_pcima, montavela_retracao15.rabo_vela_pbaixo, montavela_retracao15.valor_vela_open_close = montavela_retracao15(velas['open'],velas['close'],velas['max'],velas['min']) 
                            v2 = Decimal(montavela_retracao15.valor_vela_open_close)
                            if montavela_retracao15.direcao_ == 'call':
                                call_v2 += 1
                            elif montavela_retracao15.direcao_ == 'put':
                                put_v2 += 1
                            elif montavela_retracao15.direcao_ == 'doji':
                                doji_v2 += 1
                            #print('V2 ',v2)
                        elif cons == 3:
                            montavela_retracao15.direcao_, montavela_retracao15.rabo_vela_pcima, montavela_retracao15.rabo_vela_pbaixo, montavela_retracao15.valor_vela_open_close = montavela_retracao15(velas['open'],velas['close'],velas['max'],velas['min']) 
                            v3 = Decimal(montavela_retracao15.valor_vela_open_close)
                            if montavela_retracao15.direcao_ == 'call':
                                call_v3 += 1
                            elif montavela_retracao15.direcao_ == 'put':
                                put_v3 += 1
                            elif montavela_retracao15.direcao_ == 'doji':
                                doji_v3 += 1
                            #print('V3 ',v3)
                        elif cons == 4:
                            montavela_retracao15.direcao_, montavela_retracao15.rabo_vela_pcima, montavela_retracao15.rabo_vela_pbaixo, montavela_retracao15.valor_vela_open_close = montavela_retracao15(velas['open'],velas['close'],velas['max'],velas['min']) 
                            v4 = Decimal(montavela_retracao15.valor_vela_open_close)
                            #print('V4 ',v4)

                        elif cons == 5:
                            montavela_retracao15.direcao_, montavela_retracao15.rabo_vela_pcima, montavela_retracao15.rabo_vela_pbaixo, montavela_retracao15.valor_vela_open_close = montavela_retracao15(velas['open'],velas['close'],velas['max'],velas['min']) 
                            v5 = Decimal(montavela_retracao15.valor_vela_open_close)
                            #print('V5 ',v5)
                        cons += 1
                    if doji >= 1:
                        pass
                    if v1 > v2 and v1 > v3 and v1 > v4 and v1 > v5 and doji_v2 != 1 and doji_v3 != 1 and doji_ != 1:
                        if call >= 1:
                            if call_v2 == 1 and call_v3 == 1:
                                direcao = 'call'
                            elif put_v2 == 1 and put_v3 == 1:
                                direcao = 'put'
                            else:
                                direcao = 'error'
                        elif put >= 1:
                            if put_v2 == 1 and put_v3 == 1:
                                direcao = 'put'
                            elif call_v2 == 1 and call_v3 == 1:
                                direcao = 'call'
                            else:
                                direcao = 'error'
                        #print(direcao)
                        if variaveis.ten_merca == 'True':
                            if direcao == 'call':
                                media_moveis(par_ret15,0)
                                if code_ != 't':
                                    if call_mm > put_mm:
                                        direcao = 'call'
                                    else:
                                        direcao = 'error'
                                else:
                                    print('Par nao suporta mm')
                                    direcao = 'error'
                            elif direcao == 'put':
                                media_moveis(par_ret15,0)
                                if code_ != 't':
                                    if put_mm > call_mm:
                                        direcao = 'put'
                                    else:
                                        direcao = 'error'
                                else:
                                    print('Par nao suporta mm')
                                    direcao = 'error'
                            else:
                                direcao = 'error'
                            print('pos media  ',direcao)
                        
                        payout = 0
                        try:
                            payout = Iq.get_digital_payout(par_ret15)
                        except KeyError as e:
                            payout = 0
                            pass
                        print(payout)
                        payout_ = variaveis.payout_minimo.split(' ')
                        if payout < int(payout_[0]):
                            direcao = 'error'
                            print('Payout minimo nao atingido')
                        #profile = Iq.get_profile_ansyc()
                        #print(profile)
                        if variaveis.otc == 'Não':
                            try:
                                par = par_ret15.split('-')
                                if par[1] == 'OTC':
                                    direcao = 'error'  
                                print(par[1])
                            except IndexError as e:
                                print('sem otc')
                                #direcao = direcao
                        
                        if direcao != 'error':        
                            if variaveis.tipo == 'digital':
                                if variaveis.gale_na_proxima == 'False':
                                    entradigitalret15(direcao, par_ret15)
                                else:
                                    entradigitalgaleproxima(direcao,par_ret15)
                                variaveis.control = 'off'
                                scheduler.enter(delay=13, priority=0, action=iniretracao15)
                                scheduler.run(blocking=True) 
                                _thread.exit() 
                            else:
                                entrabinaryret15(direcao, par_ret15)
                                variaveis.control = 'off'
                                scheduler.enter(delay=13, priority=0, action=iniretracao15)
                                scheduler.run(blocking=True) 
                                _thread.exit() 
                    else:
                        pass
    else:
        print('Fora de segundos')
        variaveis.control = 'off'
        scheduler.enter(delay=13, priority=0, action=iniretracao15)
        scheduler.run(blocking=True) 
        _thread.exit()
    variaveis.control = 'off'
    scheduler.enter(delay=13, priority=0, action=iniretracao15)
    scheduler.run(blocking=True) 
    _thread.exit()

def est4():
    time.sleep(2)
    if variaveis.control == 'on':
        scheduler.enter(delay=29, priority=0, action=iniest4)
        scheduler.run(blocking=True)
        _thread.exit()
    #print(variaveis.liberado)
    if variaveis.liberado == False:
        bot10v2.painel_2.setText('Bot fora de horario.')
        scheduler.enter(delay=29, priority=0, action=iniest4)
        scheduler.run(blocking=True)
        _thread.exit()
    else:
        pass
    if variaveis.contagem_win >= variaveis.cont_win:
        bot10v2.cont_win.setText('Stop')
        bot10v2.painel_2.setText('Bot stop win ok.')
        scheduler.enter(delay=29, priority=0, action=iniest4)
        scheduler.run(blocking=True)
        _thread.exit()
    else:
        pass
    
    variaveis.control = 'on'
    print(str(datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))) 
    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Est 4 Buscando pares abertos, acumulando informações ')
    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
    print('ini est 4')
    time_t_ = datetime.fromtimestamp(Iq.get_server_timestamp())
    if time_t_.second >= 00 and time_t_.second <= 6 or time_t_.second >= 56 and time_t_.second <= 59:
        try:
            P_est4 = Iq.get_all_open_time()
        except UnboundLocalError as e:
            print(e)
            pass
        for par_est4 in P_est4[variaveis.tipo]: #binary / digital
            if P_est4[variaveis.tipo][par_est4]['open'] == True: 
                oscilador(par_est4,0)
                media_moveis(par_est4,0)
                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Est 4 Analizando Par: '+par_est4)
                #bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                direcao = 'error'
                direcao_mm = 'error'
                direcao_os = 'error'
                if call_os > put_os:
                    if call_os >= 1:
                        direcao_os = 'call'
                    else:
                        direcao_os = 'error'
                elif call_os < put_os:
                    if put_os >= 1:
                        direcao_os = 'put'
                    else:
                        direcao_os = 'error'
                else:
                    direcao_os = 'error'
                if call_mm_m1 > put_mm_m1:            
                    if call_mm_m1 >= 12:
                        if put_os >= 1 and call_os <= 0:
                            direcao_mm = 'call'
                        else:
                            direcao_mm = 'error'
                    else:
                            direcao_mm = 'error'
                elif call_mm_m1 < put_mm_m1:
                    if put_mm_m1 >= 12:
                        if call_os >= 1 and put_os <= 0:
                            direcao_mm = 'put'
                        else:
                            direcao_mm = 'error'
                    else:
                        direcao_mm = 'error'
                else:
                    direcao_mm = 'error'
                        
                if direcao_mm == 'call' and direcao_os == 'put':
                    direcao = 'call'
                elif direcao_mm == 'put' and direcao_os == 'call':
                    direcao = 'put'
                elif direcao_os == 'error' and direcao_mm == 'put':
                    direcao = 'put'
                elif direcao_os == 'error' and direcao_mm == 'call':
                    direcao = 'call'
                else:
                    direcao = 'error'
                print(direcao_os)
                print(direcao_mm)
                print(direcao)
                print(call_mm_m1)
                print(put_mm_m1)
                payout = 80
                print('Antes payout')
                #try:
                #    print('Peguei payout')
                #    payout = Iq.get_digital_payout(par_est4)
                    
                #except KeyError as e:
                #    payout = 0
                #    print('Error payout')
                #    print(e)
                    #pass
                print(payout)
                payout_ = variaveis.payout_minimo.split(' ')
                if payout < int(payout_[0]):
                    direcao = 'error'
                    print('Payout minimo nao atingido') 
                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Payout minimo nao atingido')
                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                if variaveis.otc == 'Não':
                    try:
                        print('Sem OTC')
                        par = par_est4.split('-')
                        if par[1] == 'OTC':
                            direcao = 'error'  
                            print(par[1])
                    except IndexError as e:
                        print('sem otc')
                        pass
                if direcao != 'error':
                    if variaveis.tipo == 'digital':
                        entradigitalret15(direcao, par_est4)
                        variaveis.control = 'off'
                        scheduler.enter(delay=59, priority=0, action=iniest4)
                        scheduler.run(blocking=True) 
                        _thread.exit() 
                    else:
                        entrabinaryret15(direcao, par_est4)
                        variaveis.control = 'off'
                        scheduler.enter(delay=59, priority=0, action=iniest4)
                        scheduler.run(blocking=True) 
                        _thread.exit()
        else:
            variaveis.control = 'off'
            scheduler.enter(delay=29, priority=0, action=iniest4)
            scheduler.run(blocking=True)
            _thread.exit    
    else:
        variaveis.control = 'off'
        scheduler.enter(delay=29, priority=0, action=iniest4)
        scheduler.run(blocking=True)
        _thread.exit

def entradigitalret15(direcao,par_ret15):
    ent = float(variaveis.ve_v)
    razao_gale = round(float(variaveis.perc_gale),2)
    soros = round(float(variaveis.soros),2)
    if soros > 0.0:
        if variaveis.contagem_win >= 1:
            cont_win = variaveis.contagem_win
            ent_ = round(((ent / 100)*80)*cont_win,2)
            
            ent_ = round(ent_ * soros,2)
            ent = round(ent + ent_,2)
    if variaveis.contra == 'Contra':
        if direcao == 'call':
            direcao = 'put'
        elif direcao == 'put':
            direcao = 'call'
             
    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando Par: '+par_ret15+' '+'Direção: '+direcao)
    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
    status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
    print(status,id)
    if isinstance(id, int):
        while True:
            status1, lucro = Iq.check_win_digital_v2(id)
            if status1:
                if lucro > 0:
                    print('RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                    banca = variaveis.relativo
                    banca = round(float(banca) + float(lucro),2)
                    variaveis.relativo = str(banca)
                    bot10v2.relativo.setText(str(banca))
                    variaveis.contagem_win += 1
                    bot10v2.cont_win.setText(str(variaveis.contagem_win))
                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                    bot10v2.ultima.setStyleSheet("color: blue;font: 75 14pt 'Verdana';")
                    bot10v2.ultima.setText(str(round(lucro,2)))
                    arquivo = open("map_win.txt", "a+")
                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                    arquivo.close()
                    time.sleep(15)
                else:
                    print('RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                    banca = variaveis.relativo
                    banca = round(float(banca) + float(lucro),2)
                    variaveis.relativo = str(banca)
                    bot10v2.relativo.setText(str(banca))
                    variaveis.contagem_loss += 1
                    bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                    bot10v2.ultima.setStyleSheet("color: red;font: 75 14pt 'Verdana';")
                    bot10v2.ultima.setText(str(round(lucro,2)))
                    arquivo = open("map_loss.txt", "a+")
                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                    arquivo.close()
                    if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 1:
                        if variaveis.direc_gale == 'Contra':
                            if direcao == 'call':
                                direcao = 'put'
                            elif direcao == 'put':
                                direcao = 'call'
                        ent = round(ent * razao_gale,2)
                        status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                        print(status,id)
                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 1')
                        bot10v2.listWidget.sortItems(Qt.DescendingOrder) 
                        if isinstance(id, int):
                            while True:
                                status1, lucro = Iq.check_win_digital_v2(id)
                                if status1:
                                    if lucro > 0:
                                        print('Gale 1 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                        banca = variaveis.relativo
                                        banca = round(float(banca) + float(lucro),2)
                                        variaveis.relativo = str(banca)
                                        bot10v2.relativo.setText(str(banca))
                                        variaveis.contagem_win += 1
                                        bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 1 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                        bot10v2.ultima.setStyleSheet("color: blue;font: 75 14pt 'Verdana';")
                                        bot10v2.ultima.setText(str(lucro))
                                        arquivo = open("map_win.txt", "a+")
                                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                        arquivo.close()
                                        time.sleep(15)
                                    else:
                                        print('Gale 1 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                        banca = variaveis.relativo
                                        banca = round(float(banca) + float(lucro),2)
                                        variaveis.relativo = str(banca)
                                        bot10v2.relativo.setText(str(banca))
                                        variaveis.contagem_loss += 1
                                        bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 1 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                        bot10v2.ultima.setStyleSheet("color: red;font: 75 14pt 'Verdana';")
                                        bot10v2.ultima.setText(str(lucro))
                                        arquivo = open("map_loss.txt", "a+")
                                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                        arquivo.close()
                                        if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 2:
                                            bot10v2.listWidget.insertItem(0, str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 2')
                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                            ent = ent * razao_gale
                                            status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                                            print(status,id)
                                            if isinstance(id, int):
                                                while True:
                                                    status1, lucro = Iq.check_win_digital_v2(id)
                                                    if status1:
                                                        if lucro > 0:
                                                            print('Gale 2 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                            banca = variaveis.relativo
                                                            banca = round(float(banca) + float(lucro),2)
                                                            variaveis.relativo = str(banca)
                                                            bot10v2.relativo.setText(str(banca))
                                                            variaveis.contagem_win += 1
                                                            bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 2 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                            bot10v2.ultima.setStyleSheet("color: blue;font: 75 14pt 'Verdana';")
                                                            bot10v2.ultima.setText(str(lucro))
                                                            arquivo = open("map_win.txt", "a+")
                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                            arquivo.close()
                                                            time.sleep(15)
                                                        else:
                                                            print('Gale 2 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                            banca = variaveis.relativo
                                                            banca = round(float(banca) + float(lucro),2)
                                                            variaveis.relativo = str(banca)
                                                            bot10v2.relativo.setText(str(banca))
                                                            variaveis.contagem_loss += 1
                                                            bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 2 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                            bot10v2.ultima.setStyleSheet("color: red;font: 75 14pt 'Verdana';")
                                                            bot10v2.ultima.setText(str(lucro))
                                                            arquivo = open("map_loss.txt", "a+")
                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                            arquivo.close()
                                                            if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 3:
                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 3')
                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                ent = ent * razao_gale
                                                                status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                                                                print(status,id)
                                                                if isinstance(id, int):
                                                                    while True:
                                                                        status1, lucro = Iq.check_win_digital_v2(id)
                                                                        if status1:
                                                                            if lucro > 0:
                                                                                print('Gale 3 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                banca = variaveis.relativo
                                                                                banca = round(float(banca) + float(lucro),2)
                                                                                variaveis.relativo = str(banca)
                                                                                bot10v2.relativo.setText(str(banca))
                                                                                variaveis.contagem_win += 1
                                                                                bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 3 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                arquivo = open("map_win.txt", "a+")
                                                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                arquivo.close()
                                                                                time.sleep(15)
                                                                            else:
                                                                                print('Gale 3 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                banca = variaveis.relativo
                                                                                banca = round(float(banca) + float(lucro),2)
                                                                                variaveis.relativo = str(banca)
                                                                                bot10v2.relativo.setText(str(banca))
                                                                                variaveis.contagem_loss += 1
                                                                                bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 3 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                arquivo = open("map_loss.txt", "a+")
                                                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                arquivo.close()
                                                                                
                                                                                if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 4:
                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 4')
                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                    ent = ent * razao_gale
                                                                                    status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                                                                                    print(status,id)
                                                                                    if isinstance(id, int):
                                                                                        while True:
                                                                                            status1, lucro = Iq.check_win_digital_v2(id)
                                                                                            if status1:
                                                                                                if lucro > 0:
                                                                                                    print('Gale 4 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                    banca = variaveis.relativo
                                                                                                    banca = round(float(banca) + float(lucro),2)
                                                                                                    variaveis.relativo = str(banca)
                                                                                                    bot10v2.relativo.setText(str(banca))
                                                                                                    variaveis.contagem_win += 1
                                                                                                    bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 4 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                    arquivo = open("map_win.txt", "a+")
                                                                                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                    arquivo.close()
                                                                                                    time.sleep(15)
                                                                                                else:
                                                                                                    print('Gale 4 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                    banca = variaveis.relativo
                                                                                                    banca = round(float(banca) + float(lucro),2)
                                                                                                    variaveis.relativo = str(banca)
                                                                                                    bot10v2.relativo.setText(str(banca))
                                                                                                    variaveis.contagem_loss += 1
                                                                                                    bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 4 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                    arquivo = open("map_loss.txt", "a+")
                                                                                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                    arquivo.close()
                                                                                                
                                                                                                    if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 5:
                                                                                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 5')
                                                                                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                        ent = ent * razao_gale
                                                                                                        status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                                                                                                        print(status,id)
                                                                                                        if isinstance(id, int):
                                                                                                            while True:
                                                                                                                status1, lucro = Iq.check_win_digital_v2(id)
                                                                                                                if status1:
                                                                                                                    if lucro > 0:
                                                                                                                        print('Gale 5 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                        banca = variaveis.relativo
                                                                                                                        banca = round(float(banca) + float(lucro),2)
                                                                                                                        variaveis.relativo = str(banca)
                                                                                                                        bot10v2.relativo.setText(str(banca))
                                                                                                                        variaveis.contagem_win += 1
                                                                                                                        bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 5 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                        arquivo = open("map_win.txt", "a+")
                                                                                                                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                        arquivo.close()
                                                                                                                        time.sleep(15)
                                                                                                                    else:
                                                                                                                        print('Gale 5 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                        banca = variaveis.relativo
                                                                                                                        banca = round(float(banca) + float(lucro),2)
                                                                                                                        variaveis.relativo = str(banca)
                                                                                                                        bot10v2.relativo.setText(str(banca))
                                                                                                                        variaveis.contagem_loss += 1
                                                                                                                        bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 5 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                        arquivo = open("map_loss.txt", "a+")
                                                                                                                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                        arquivo.close()
                                                                                                                    
                                                                                                                        if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 6:
                                                                                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 6')
                                                                                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                            ent = ent * razao_gale
                                                                                                                            status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                                                                                                                            print(status,id)
                                                                                                                            if isinstance(id, int):
                                                                                                                                while True:
                                                                                                                                    status1, lucro = Iq.check_win_digital_v2(id)
                                                                                                                                    if status1:
                                                                                                                                        if lucro > 0:
                                                                                                                                            print('Gale 6 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                                            banca = variaveis.relativo
                                                                                                                                            banca = round(float(banca) + float(lucro),2)
                                                                                                                                            variaveis.relativo = str(banca)
                                                                                                                                            bot10v2.relativo.setText(str(banca))
                                                                                                                                            variaveis.contagem_win += 1
                                                                                                                                            bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 6 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                            arquivo = open("map_win.txt", "a+")
                                                                                                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                                            arquivo.close()
                                                                                                                                            time.sleep(15)
                                                                                                                                        else:
                                                                                                                                            print('Gale 6 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                                            banca = variaveis.relativo
                                                                                                                                            banca = round(float(banca) + float(lucro),2)
                                                                                                                                            variaveis.relativo = str(banca)
                                                                                                                                            bot10v2.relativo.setText(str(banca))
                                                                                                                                            variaveis.contagem_loss += 1
                                                                                                                                            bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 6 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                            arquivo = open("map_loss.txt", "a+")
                                                                                                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                                            arquivo.close()
                                                                                                                                        
                                                                                                                                            if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 7:
                                                                                                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 7')
                                                                                                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                                ent = ent * razao_gale
                                                                                                                                                status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                                                                                                                                                print(status,id)
                                                                                                                                                if isinstance(id, int):
                                                                                                                                                    while True:
                                                                                                                                                        status1, lucro = Iq.check_win_digital_v2(id)
                                                                                                                                                        if status1:
                                                                                                                                                            if lucro > 0:
                                                                                                                                                                print('Gale 7 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                banca = variaveis.relativo
                                                                                                                                                                banca = round(float(banca) + float(lucro),2)
                                                                                                                                                                variaveis.relativo = str(banca)
                                                                                                                                                                bot10v2.relativo.setText(str(banca))
                                                                                                                                                                variaveis.contagem_win += 1
                                                                                                                                                                bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                                                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 7 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                                                arquivo = open("map_win.txt", "a+")
                                                                                                                                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                                                                arquivo.close()
                                                                                                                                                                time.sleep(15)
                                                                                                                                                            else:
                                                                                                                                                                print('Gale 7 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                banca = variaveis.relativo
                                                                                                                                                                banca = round(float(banca) + float(lucro),2)
                                                                                                                                                                variaveis.relativo = str(banca)
                                                                                                                                                                bot10v2.relativo.setText(str(banca))
                                                                                                                                                                variaveis.contagem_loss += 1
                                                                                                                                                                bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                                                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 7 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                                                arquivo = open("map_loss.txt", "a+")
                                                                                                                                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                                                                arquivo.close()
                                                                                                                                                            
                                                                                                                                                                if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 8:
                                                                                                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 8')
                                                                                                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                                                    ent = ent * razao_gale
                                                                                                                                                                    status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
                                                                                                                                                                    print(status,id)
                                                                                                                                                                    if isinstance(id, int):
                                                                                                                                                                        while True:
                                                                                                                                                                            status1, lucro = Iq.check_win_digital_v2(id)
                                                                                                                                                                            if status1:
                                                                                                                                                                                if lucro > 0:
                                                                                                                                                                                    print('Gale 8 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                                    banca = variaveis.relativo
                                                                                                                                                                                    banca = round(float(banca) + float(lucro),2)
                                                                                                                                                                                    variaveis.relativo = str(banca)
                                                                                                                                                                                    bot10v2.relativo.setText(str(banca))
                                                                                                                                                                                    variaveis.contagem_win += 1
                                                                                                                                                                                    bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                                                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 8 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                                                                    arquivo = open("map_win.txt", "a+")
                                                                                                                                                                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                                                                                    arquivo.close()
                                                                                                                                                                                    time.sleep(15)
                                                                                                                                                                                else:
                                                                                                                                                                                    print('Gale 8 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                                    banca = variaveis.relativo
                                                                                                                                                                                    banca = round(float(banca) + float(lucro),2)
                                                                                                                                                                                    variaveis.relativo = str(banca)
                                                                                                                                                                                    bot10v2.relativo.setText(str(banca))
                                                                                                                                                                                    variaveis.contagem_loss += 1
                                                                                                                                                                                    bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                                                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 8 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                                                                                                    arquivo = open("map_loss.txt", "a+")
                                                                                                                                                                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                                                                                                    arquivo.close()
                                                                                                                                                                                break
                                                                                                                                                                                
                                                                                                                                                            break
                                                                                                                                        
                                                                                                                                        break
                                                                                                                    
                                                                                                                    break
                                                                                                
                                                                                                break
                                                                                
                                                                            break
                                                                    #break
                                                        break
                                                #break    
                                    break
                            #break
                break
    else:
        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'DIGITAL   Não foi possivel abrir a operação.')
        bot10v2.listWidget.sortItems(Qt.DescendingOrder)

def entrabinaryret15(direcao,par_ret15):
    ent = int(variaveis.ve_v)
    razao_gale = round(float(variaveis.perc_gale),2)
    soros = round(float(variaveis.soros),2)
    if soros > 0.0:
        if variaveis.contagem_win >= 1:
            cont_win = variaveis.contagem_win
            ent_ = round(((ent / 100)*80)*cont_win,2)
            ent_ = round(ent_ * soros,2)
            ent = round(ent + ent_,2)
    if variaveis.contra == 'Contra':
        if direcao == 'call':
            direcao = 'put'
        elif direcao == 'put':
            direcao = 'call'
    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando Par: '+par_ret15+' '+'Direção: '+direcao)
    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
    status, id = Iq.buy(ent,par_ret15,direcao,1)
    print(status,id)
    if status:
        resultado, lucro = Iq.check_win_v4(id)
        #print('RESULTADO: '+resultado+' / LUCRO: '+str(round(lucro,2)))
        if lucro > 0:
            print('RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
            banca = variaveis.relativo
            banca = round(float(banca) + float(lucro),2)
            variaveis.relativo = str(banca)
            bot10v2.relativo.setText(str(banca))
            variaveis.contagem_win += 1
            bot10v2.cont_win.setText(str(variaveis.contagem_win))
            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
            arquivo = open("map_win.txt", "a+")
            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
            arquivo.close()
            time.sleep(15)
        elif lucro == 0:
            print('RESULTADO: EMPATE / LUCRO: '+str(round(lucro,2)))
            banca = variaveis.relativo
            banca = round(float(banca) + float(lucro),2)
            variaveis.relativo = str(banca)
            bot10v2.relativo.setText(str(banca))
            #variaveis.contagem_win += 1
            bot10v2.cont_win.setText(str(variaveis.contagem_win))
            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
            arquivo = open("map_win.txt", "a+")
            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
            arquivo.close()
            time.sleep(15)
        elif lucro < 0:
            print('RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
            banca = variaveis.relativo
            banca = round(float(banca) + float(lucro),2)
            variaveis.relativo = str(banca)
            bot10v2.relativo.setText(str(banca))
            variaveis.contagem_loss += 1
            bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
            arquivo = open("map_loss.txt", "a+")
            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
            arquivo.close()
            if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 1:
                if variaveis.direc_gale == 'Contra':
                    if direcao == 'call':
                        direcao = 'put'
                    elif direcao == 'put':
                        direcao = 'call'
                ent = round(ent * razao_gale,2)
                status, id = Iq.buy(ent,par_ret15,direcao,1)
                print(status,id)
                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 1')
                bot10v2.listWidget.sortItems(Qt.DescendingOrder) 
                if status:
                    resultado, lucro = Iq.check_win_v4(id) 
                    if lucro > 0:
                        print('Gale 1 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                        banca = variaveis.relativo
                        banca = round(float(banca) + float(lucro),2)
                        variaveis.relativo = str(banca)
                        bot10v2.relativo.setText(str(banca))
                        variaveis.contagem_win += 1
                        bot10v2.cont_win.setText(str(variaveis.contagem_win))
                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 1 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                        arquivo = open("map_win.txt", "a+")
                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                        arquivo.close()
                        time.sleep(15)
                    elif lucro <= 0:
                        print('Gale 1 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                        banca = variaveis.relativo
                        banca = round(float(banca) + float(lucro),2)
                        variaveis.relativo = str(banca)
                        bot10v2.relativo.setText(str(banca))
                        variaveis.contagem_loss += 1
                        bot10v2.cont_loss.setText(str(variaveis.contagem_loss)) 
                        arquivo = open("map_loss.txt", "a+")
                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                        arquivo.close()
                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 1 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                        print('ate aqui')
                        if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 2:
                            bot10v2.listWidget.insertItem(0, str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 2')
                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                            ent = ent * razao_gale
                            status, id = Iq.buy(ent,par_ret15,direcao,1)
                            print(status,id)
                            if status:
                                resultado, lucro = Iq.check_win_v4(id) 
                                if lucro > 0:
                                    print('Gale 2 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                    banca = variaveis.relativo
                                    banca = round(float(banca) + float(lucro),2)
                                    variaveis.relativo = str(banca)
                                    bot10v2.relativo.setText(str(banca))
                                    variaveis.contagem_win += 1
                                    bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 2 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                    arquivo = open("map_win.txt", "a+")
                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                    arquivo.close()
                                    time.sleep(15)
                                elif lucro <= 0:
                                    print('Gale 2 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                    banca = variaveis.relativo
                                    banca = round(float(banca) + float(lucro),2)
                                    variaveis.relativo = str(banca)
                                    bot10v2.relativo.setText(str(banca))
                                    variaveis.contagem_loss += 1
                                    bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 2 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                    #bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                    arquivo = open("map_loss.txt", "a+")
                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                    arquivo.close()
                                    if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 3:
                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 3')
                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                        ent = ent * razao_gale
                                        status, id = Iq.buy(ent,par_ret15,direcao,1)
                                        print(status,id)
                                        if status:
                                            resultado, lucro = Iq.check_win_v4(id) 
                                            if lucro > 0:
                                                print('Gale 3 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                banca = variaveis.relativo
                                                banca = round(float(banca) + float(lucro),2)
                                                variaveis.relativo = str(banca)
                                                bot10v2.relativo.setText(str(banca))
                                                variaveis.contagem_win += 1
                                                bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 3 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                arquivo = open("map_win.txt", "a+")
                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                arquivo.close()
                                                time.sleep(15)
                                            elif lucro <= 0:
                                                print('Gale 3 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                banca = variaveis.relativo
                                                banca = round(float(banca) + float(lucro),2)
                                                variaveis.relativo = str(banca)
                                                bot10v2.relativo.setText(str(banca))
                                                variaveis.contagem_loss += 1
                                                bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 3 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                arquivo = open("map_loss.txt", "a+")
                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                arquivo.close()
                                                if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 4:
                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 4')
                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                    ent = ent * razao_gale
                                                    status, id = Iq.buy(ent,par_ret15,direcao,1)
                                                    print(status,id)
                                                    if status:
                                                        resultado, lucro = Iq.check_win_v4(id) 
                                                        if lucro > 0:
                                                            print('Gale 4 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                            banca = variaveis.relativo
                                                            banca = round(float(banca) + float(lucro),2)
                                                            variaveis.relativo = str(banca)
                                                            bot10v2.relativo.setText(str(banca))
                                                            variaveis.contagem_win += 1
                                                            bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 4 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                            arquivo = open("map_win.txt", "a+")
                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                            arquivo.close()
                                                            time.sleep(15)
                                                        elif lucro <= 0:
                                                            print('Gale 4 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                            banca = variaveis.relativo
                                                            banca = round(float(banca) + float(lucro),2)
                                                            variaveis.relativo = str(banca)
                                                            bot10v2.relativo.setText(str(banca))
                                                            variaveis.contagem_loss += 1
                                                            bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 4 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                            arquivo = open("map_loss.txt", "a+")
                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                            arquivo.close()
                                                            if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 5:
                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 5')
                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                ent = ent * razao_gale
                                                                status, id = Iq.buy(ent,par_ret15,direcao,1)
                                                                print(status,id)
                                                                if status:
                                                                    resultado, lucro = Iq.check_win_v4(id) 
                                                                    if lucro > 0:
                                                                        print('Gale 5 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                        banca = variaveis.relativo
                                                                        banca = round(float(banca) + float(lucro),2)
                                                                        variaveis.relativo = str(banca)
                                                                        bot10v2.relativo.setText(str(banca))
                                                                        variaveis.contagem_win += 1
                                                                        bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 5 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                        arquivo = open("map_win.txt", "a+")
                                                                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                        arquivo.close()
                                                                        time.sleep(15)
                                                                    elif lucro <= 0:
                                                                        print('Gale 5 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                        banca = variaveis.relativo
                                                                        banca = round(float(banca) + float(lucro),2)
                                                                        variaveis.relativo = str(banca)
                                                                        bot10v2.relativo.setText(str(banca))
                                                                        variaveis.contagem_loss += 1
                                                                        bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 5 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                        arquivo = open("map_loss.txt", "a+")
                                                                        arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                        arquivo.close() 
                                                                        if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 6:
                                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 6')
                                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                            ent = ent * razao_gale
                                                                            status, id = Iq.buy(ent,par_ret15,direcao,1)
                                                                            print(status,id)
                                                                            if status:
                                                                                resultado, lucro = Iq.check_win_v4(id) 
                                                                                if lucro > 0:
                                                                                    print('Gale 6 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                    banca = variaveis.relativo
                                                                                    banca = round(float(banca) + float(lucro),2)
                                                                                    variaveis.relativo = str(banca)
                                                                                    bot10v2.relativo.setText(str(banca))
                                                                                    variaveis.contagem_win += 1
                                                                                    bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 6 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                    arquivo = open("map_win.txt", "a+")
                                                                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                    arquivo.close()
                                                                                    time.sleep(15)
                                                                                elif lucro <= 0:
                                                                                    print('Gale 6 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                    banca = variaveis.relativo
                                                                                    banca = round(float(banca) + float(lucro),2)
                                                                                    variaveis.relativo = str(banca)
                                                                                    bot10v2.relativo.setText(str(banca))
                                                                                    variaveis.contagem_loss += 1
                                                                                    bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 6 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                    arquivo = open("map_loss.txt", "a+")
                                                                                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                    arquivo.close()
                                                                                    if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 7:
                                                                                        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 7')
                                                                                        bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                        ent = ent * razao_gale
                                                                                        status, id = Iq.buy(ent,par_ret15,direcao,1)
                                                                                        print(status,id)
                                                                                        if status:
                                                                                            resultado, lucro = Iq.check_win_v4(id) 
                                                                                            if lucro > 0:
                                                                                                print('Gale 7 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                banca = variaveis.relativo
                                                                                                banca = round(float(banca) + float(lucro),2)
                                                                                                variaveis.relativo = str(banca)
                                                                                                bot10v2.relativo.setText(str(banca))
                                                                                                variaveis.contagem_win += 1
                                                                                                bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 7 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                arquivo = open("map_win.txt", "a+")
                                                                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                arquivo.close()
                                                                                                time.sleep(15)
                                                                                            elif lucro <= 0:
                                                                                                print('Gale 7 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                banca = variaveis.relativo
                                                                                                banca = round(float(banca) + float(lucro),2)
                                                                                                variaveis.relativo = str(banca)
                                                                                                bot10v2.relativo.setText(str(banca))
                                                                                                variaveis.contagem_loss += 1
                                                                                                bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                                bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 7 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                arquivo = open("map_loss.txt", "a+")
                                                                                                arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                arquivo.close()
                                                                                                if variaveis.qtd_gale > 0 and variaveis.qtd_gale >= 8:
                                                                                                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando no Gale 8')
                                                                                                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                    ent = ent * razao_gale
                                                                                                    status, id = Iq.buy(ent,par_ret15,direcao,1)
                                                                                                    print(status,id)
                                                                                                    if status:
                                                                                                        resultado, lucro = Iq.check_win_v4(id) 
                                                                                                        if lucro > 0:
                                                                                                            print('Gale 8 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                            banca = variaveis.relativo
                                                                                                            banca = round(float(banca) + float(lucro),2)
                                                                                                            variaveis.relativo = str(banca)
                                                                                                            bot10v2.relativo.setText(str(banca))
                                                                                                            variaveis.contagem_win += 1
                                                                                                            bot10v2.cont_win.setText(str(variaveis.contagem_win))
                                                                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 8 RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                                                                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                            arquivo = open("map_win.txt", "a+")
                                                                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                            arquivo.close()
                                                                                                            time.sleep(15)
                                                                                                        elif lucro <= 0:
                                                                                                            print('Gale 8 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                            banca = variaveis.relativo
                                                                                                            banca = round(float(banca) + float(lucro),2)
                                                                                                            variaveis.relativo = str(banca)
                                                                                                            bot10v2.relativo.setText(str(banca))
                                                                                                            variaveis.contagem_loss += 1
                                                                                                            bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                                                                                                            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Gale 8 RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                                                                                                            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                                                                                                            arquivo = open("map_loss.txt", "a+")
                                                                                                            arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                                                                                                            arquivo.close() 
    else:
        bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Não foi possivel abrir a operação.')
        bot10v2.listWidget.sortItems(Qt.DescendingOrder)

def entradigitalgaleproxima(direcao,par_ret15):
    print('New Meto')
    ent = int(variaveis.ve_v)
    razao_gale = round(float(variaveis.perc_gale),2)
    soros = round(float(variaveis.soros),2)
    if soros > 0.0:
        if variaveis.contagem_win >= 1:
            cont_win = variaveis.contagem_win
            ent_ = round(((ent / 100)*80)*cont_win,2) 
            ent_ = round(ent_ * soros,2)
            ent = round(ent + ent_,2)
    
    if variaveis.direc_gale == 'Contra':
        if direcao == 'call':
            direcao = 'put'
        elif direcao == 'put':
            direcao = 'call'
    
    if variaveis.gale_na_proxima_ == 0:
        variaveis.guard_ent = ent
    elif variaveis.gale_na_proxima_ <= variaveis.qtd_gale:
        if variaveis.gale_na_proxima_ == 1:
            ent = round(ent * razao_gale,2)
            variaveis.guard_ent = ent
        elif variaveis.gale_na_proxima_ == 2:
            ent = round(variaveis.guard_ent * razao_gale,2)
            variaveis.guard_ent = ent
        elif variaveis.gale_na_proxima_ == 3:
            ent = round(variaveis.guard_ent * razao_gale,2)
            variaveis.guard_ent = ent
        elif variaveis.gale_na_proxima_ == 4:
            ent = round(variaveis.guard_ent * razao_gale,2)
            variaveis.guard_ent = ent
        elif variaveis.gale_na_proxima_ == 5:
            ent = round(variaveis.guard_ent * razao_gale,2)
            variaveis.guard_ent = ent
        elif variaveis.gale_na_proxima_ == 6:
            ent = round(variaveis.guard_ent * razao_gale,2)
            variaveis.guard_ent = ent
        elif variaveis.gale_na_proxima_ == 7:
            ent = round(variaveis.guard_ent * razao_gale,2)
            variaveis.guard_ent = ent
        elif variaveis.gale_na_proxima_ == 8:
            ent = round(variaveis.guard_ent * razao_gale,2)
            variaveis.guard_ent = ent
    
    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Entrando Par: '+par_ret15+' '+'Direção: '+direcao)
    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
    status,id=(Iq.buy_digital_spot_v2(par_ret15,ent,direcao,1))
    print(status,id)
    if isinstance(id, int):
        while True:
            status1, lucro = Iq.check_win_digital_v2(id)
            if status1:
                if lucro > 0:
                    print('RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                    banca = variaveis.relativo
                    banca = round(float(banca) + float(lucro),2)
                    variaveis.relativo = str(banca)
                    bot10v2.relativo.setText(str(banca))
                    variaveis.contagem_win += 1
                    bot10v2.cont_win.setText(str(variaveis.contagem_win))
                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'RESULTADO: WIN / LUCRO: '+str(round(lucro,2)))
                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                    arquivo = open("map_win.txt", "a+")
                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                    arquivo.close()
                    variaveis.gale_na_proxima_ = 0
                    time.sleep(15)
                else:
                    print('RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                    banca = variaveis.relativo
                    banca = round(float(banca) + float(lucro),2)
                    variaveis.relativo = str(banca)
                    bot10v2.relativo.setText(str(banca))
                    variaveis.contagem_loss += 1
                    bot10v2.cont_loss.setText(str(variaveis.contagem_loss))
                    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'RESULTADO: LOSS / LUCRO: '+str(round(lucro,2)))
                    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
                    arquivo = open("map_loss.txt", "a+")
                    arquivo.writelines(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+'|'+str(round(lucro,2))+'|'+variaveis.tipo_conta+'|'+variaveis.login+'\n')
                    arquivo.close()
                    variaveis.gale_na_proxima_ += 1
                break

def limphist():
    bot10v2.listWidget.clear()

def iniretracao15():
    thre = threading.Thread(target=retracao15)
    thre.start()

def iniest4():
    thre = threading.Thread(target=est4)
    thre.start()

def matathread():
    bot10v2.parar_bot.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';")
    cont = 0
    while cont <= 20:
        if scheduler.empty() == True or scheduler1.empty() == True:
            #print('Nenhum agendamento existente')
            list(map(scheduler.cancel,scheduler.queue))
            list(map(scheduler1.cancel,scheduler1.queue))
            bot10v2.parar_bot.setEnabled(False)
            bot10v2.iniciar_bot.setEnabled(True)
            bot10v2.editar.setEnabled(True)
            bot10v2.sair.setEnabled(True)
            bot10v2.painel_2.setText('Bot paralisado.')
            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Parando operações em '+str(cont))
            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
        else:
            list(map(scheduler.cancel,scheduler.queue))
            list(map(scheduler1.cancel,scheduler1.queue))
            bot10v2.parar_bot.setEnabled(False)
            bot10v2.iniciar_bot.setEnabled(True)
            bot10v2.editar.setEnabled(True)
            bot10v2.sair.setEnabled(True)
            bot10v2.painel_2.setText('Bot paralisado.')
            #print('Bot paralizado')
            bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Parando operações em '+str(cont))
            bot10v2.listWidget.sortItems(Qt.DescendingOrder)
        time.sleep(1)
        cont += 1
    print('bot paralizado')
    bot10v2.listWidget.addItem(str(datetime.strftime(datetime.now(),'%d-%m-%Y %H:%M:%S'))+' | '+'Bot paralizado. Pode editar as configurações ou sair.')
    bot10v2.listWidget.sortItems(Qt.DescendingOrder)
    bot10v2.iniciar_bot.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.sair.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")
    bot10v2.editar.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';") 

def inimatathread():
    thre = threading.Thread(target=matathread)
    thre.start()

bot10v2.editar.setStyleSheet("color: gray;background-color: #aa0000;font: 75 9pt 'Verdana';") 
bot10v2.salvar.setStyleSheet("color: #ffffff;background-color: #aa0000;font: 75 9pt 'Verdana';")

bot10v2.contra.addItems(contra_list)
bot10v2.stop_win.addItems(stop_win_list)
bot10v2.soros.addItems(soros_list)
bot10v2.qtd_gale.addItems(qtd_gale_list)
bot10v2.perc_gale.addItems(perc_gale_list)
bot10v2.direc_gale.addItems(direc_gale_list)
bot10v2.tipo.addItems(tipo_list)
bot10v2.divisor.addItems(divisor_list)
#bot10v2.meta_mes.addItems(meta_mes_list)
bot10v2.otc.addItems(otc_list)
bot10v2.semana.addItems(semana_list)
bot10v2.reset_tempo.addItems(reset_tempo_list)
bot10v2.payout_minimo.addItems(payout_minimo_list)

bot10v2.v_ent.textChanged.connect(maxwinloss)
bot10v2.stop_win.currentIndexChanged.connect(maxwinloss)
bot10v2.soros.currentIndexChanged.connect(maxwinloss)
bot10v2.qtd_gale.currentIndexChanged.connect(maxwinloss)
bot10v2.perc_gale.currentIndexChanged.connect(maxwinloss)
#bot10v2.stop_win.clicked.connect(maxwinloss)
bot10v2.parar_bot.clicked.connect(inimatathread)
bot10v2.limpar_hist.clicked.connect(limphist)
bot10v2.iniciar_bot.clicked.connect(travaBotoes)
bot10v2.iniciar_bot.clicked.connect(iniretracao15)
bot10v2.iniciar_bot.clicked.connect(iniest4)
bot10v2.bnt_logar.clicked.connect(conectar)
bot10v2.sair.clicked.connect(logout)
bot10v2.troca_conta.clicked.connect(troca_conta)
bot10v2.salvar.clicked.connect(salvaconfig)
bot10v2.editar.clicked.connect(editconf)
bot10v2.check_reset.clicked.connect(hora_reset)
bot10v2.ajusta_hora.clicked.connect(AjustaHora)

bot10v2.iniciar_bot.setVisible(False)
bot10v2.parar_bot.setVisible(False)
bot10v2.h_reset.setVisible(False)
bot10v2.frame_conta.setVisible(False)
bot10v2.frame_login.setVisible(True)
bot10v2.tabWidget.setVisible(False)


#funcao para executar a tela
bot10v2.show()
app.exec()