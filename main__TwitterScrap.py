#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import shutil
import json
from sys import platform
from selenium import webdriver
from datetime import datetime
from PIL import Image
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import SessionNotCreatedException #COMPROVAR 
import pytesseract #VEURE API --> https://pypi.org/project/pytesseract/

from webdriver_manager.chrome import ChromeDriverManager

#si no esta tesseract a les variables d'entorn cal dir-li on es troba:
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
rutaDriverChrome = "chromedriver.exe"



def netejaPantalla():
	"""La funcio clear screen es diferent en funcio del OS. 
	Ho controlem perquè funcioni després en unix"""
	unix = ["linux","darwin"]
	wind = ["win32","cygwin"]
	if platform in unix:
	    os.system("clear")
	elif platform in wind:
	    os.system("cls")
	else:
		print("Estas a mac o a un altre OS desconegut")

def espera(nreSegons):
	for i in range(nreSegons):
		netejaPantalla()
		print("#############")
		print("# queden: "+str(nreSegons - i)+" #")
		print("#############")
		time.sleep(1)
	netejaPantalla()

		
def espera2(nreSegons):
	for i in range(nreSegons):
		netejaPantalla()
		print("Pausa {}/{} segons fins reexecutar programa".format(i, nreSegons))
		time.sleep(1)


def generaStringData():
	"""mira l'hora que és i fes un string separat per _ amb format
	any_mes_dia_hora_minut"""
	t = datetime.now()
	data = ".".join((str(t.day).zfill(2),str(t.month).zfill(2),str(t.year)))
	hora = ".".join((str(t.hour).zfill(2),str(t.minute).zfill(2),str(t.second).zfill(2)))+" h"
	return data+"_"+hora

def fesCropAnovaImatge_i_esborraLaPrevia(nomImatge):
	"""METODE QUE PREN LA IMATGE SCREENSHOT SENCER DEL NAVEGADOR, DE NOM "nomImatge" i la converteix
	a una imatge cropejada amb una millor acotacio de la ROI -ultim twit del feed-
	 amb la informacio del twit i la guarda com a "nomImatge_CROPEJADA_.png. Esborra la imatge original." """
	img = Image.open(nomImatge+".png") #https://www.geeksforgeeks.org/python-pil-image-crop-method/
	amplada, altura = img.size
	#DEFINEIXO PUNTS DE TALL DEL RECTANGLE 
	left = 80
	top = (1/8)*altura 
	right = amplada - 20
	bottom = (2/8)*altura
	#RETALLO I MOSTRO
	imatge_cropejada = img.crop((left, top, right, bottom))# Cropped image of above dimension
	imatge_cropejada.save(nomImatge+"_CROPEJADA_.png")  #imatge_cropejada.show() #[SI NOMES VOLS VEURE-LA]
	os.remove(nomImatge+".png")

def esborraStringsBuits(ll):
	"""PRE: Una llista amb un o múltiples elements que són STRINGS BUITS
	   POST: La mateixa llista sense els STRINGS BUITS"""
	n = len(ll)
	i = 0
	while i < n:
		if len(ll[i]) == 0:
			del ll[i]
			n = n - 1
		else:
			i = i + 1
	return ll	   

def imatgeCropejada_a_txt_OCR():
	"""converteix el text de la imatge cropejada (LA IMATGE CROPEJADA JA EXISTEIX I CONTE UN TWIT) 
	a un text en un fitxer TXT que despres  despres poder ser analitzat. 
	Ho fa nomes per a l'ultima imatge que trobi al directori (CAL QUE EXISTEIXI UNA IMATGE AMB EL GRUP _CROPEJADA_.png o .PNG AL DIRECTORI).
	"""

	os.chdir("./__captures__")
	directori = os.listdir()
	directori.sort(reverse = True, key=lambda x: os.path.getmtime(x)) #ordeno captures de pantalla de mes nova a mes antiga (StackOverflowhow-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
	i = 0
	TrobatPNG = False
	#iterem de mes recents a mes antics
	while not TrobatPNG:
		#string captura conte el nom del png || stringTXT conte el nom del txt
		stringCaptura = directori[i]
		if "_CROPEJADA_.png" in stringCaptura or "_CROPEJADA_.PNG" in stringCaptura:
			stringTXT = stringCaptura[:-4]+".txt"

			f = open(stringTXT,"w")

			#paso a text de la imatge CROPEJADA i despres el tracto
			text = pytesseract.image_to_string(Image.open(stringCaptura))

			#SERPARO LA REGIO D'INTERES DEL TWIT (PRIMERA LINIA DESPRES DE L'ARROBA DE L'ENCAPSALAT DE LTWIT) 
			#DE LA REGIO PREVIA A AQUESTA ROI (DE VEGADES NO HI ES: Hi es quan surt "retuitat" o "retweeted")
			try:
				text_Twit = text[text.index("@"):len(text)] #eliminem el que hi ha abans de la primera arroba (lo eliminat esta a text_pre_Twit)
				text_pre_Twit = text[:text.index("@")] #nomes l'usarem per determinar si es un retweet

			except ValueError: #@arroba no trobada --> aixo es dona quan no s'ha llegit b el twit (per problemes de connexio si s'atura en tornar a l'internet aleshore sapareix un twit blanc)
				print("eliminant ultim png i ultim txt, que CASI SEGUR estan en blanc o mal registrats. Els fitxers eliminats passen a __capturesConflictives__ per a la seva posterior revisio visual si s'escau.")
				f.close()
				time.sleep(2)
				shutil.move(stringCaptura,"../__capturesConflictives__/"+stringCaptura)
				shutil.move(stringTXT,"../__capturesConflictives__/"+stringTXT)
				print("eliminats TXT i PNG conflictius i moguts!")
				time.sleep(1)
				os.chdir("../")
				return False
				
			text_Twit = text_Twit.replace("Show this thread","").replace("Mostrar este hilo","").replace("Mostra el fil","")#treiem text vestigial del final si hi es.
			ll_text_Twit = text_Twit.split("\n") #treiem salts de linia (de vegades esta MOOLT liat...)
			print("SENSE BORRAR ESPAIS --> ",ll_text_Twit)
			ll_text_Twit = esborraStringsBuits(ll_text_Twit) #treiem els strings buits que de vegades apareixen
			print("BORRANT ESPAIS --> ",ll_text_Twit)
			time.sleep(5)



			global boolea_retwit
			boolea_retwit = "retuitat" in text_pre_Twit or "Retweeted" in text_pre_Twit #amb aixo determino si es retwit
			
			
			#ESCRIBIM EL TWIT (tot lo que va desprs de la PRIMERA arroba) AL FITXER DE TEXT I SENSE ESPAIS (ABANS ELS HEM TRET)
			for liniaTwit in ll_text_Twit:
				f.write(liniaTwit+"\n") #NOMES VOLEM UN SOL SALT DEL INIA
			
			f.close()
			TrobatPNG = True
		i = i + 1

	os.chdir("../")	
	return True


def roiTwit(twit):
	"""PRE: un txt que conte la info d'un twit com una llista, SENSE salts de linia ni elements de llista buits.
	   POST: Una linia del twit que contribueix a diferenciar ambdós twits (les ROIs).
	   NOTA: roiTwit no contindrà tot el twit si aquest està posat en dues línies diferents, només conté la PRIMERA linea del 
	   text del twit per sota de la linia 0 (linia zero es @dilapidant - 1h.). Cal tenir en compte que pot ser 

	   A) un retweet [SOLUCIONAT A la funcio de imatge a OCR  --> global boolea_retwit || boolea_retwit = "retuitat"
	   B) un twit/retwit amb imatge i sense text --> TODO CAS COMPLICAT
	   C) una respota --> E

	   que pot ser un twit amb imatge"""

	grupsResp = ["En resposta a", "Replying to"]
	if len(twit) == 1:
		print("NOMES UN ELEMENT A LA LLISTA: PROBABLEMETN UNA IMATGE SENSE TEXT")
		return "PROBLEMA A SOLUCIONAR: imatge sense text molt probablement"

	elif len(twit) > 1:
		parar = False
		i = 0
		#bulce que cerca la primera arroba (encas que aparegui algo raro, un caracter raro abans de l'arroba -crec que mai passa-)
		while not parar:
			if "@" in twit[i]:
				#twit[i+1]pot ser la 1a linia d'un twit simple o pot ser el grup "replying to @quiSigui",
				#i seria en aquest ultim cas en el que la primera linia del twit estaria en twit[i+2]
				for grup in grupsResp:
					if grup in twit[i+1]: 
						ROI = "[Replying to someone]: "+twit[i+2] #CAS DE TWIT EN RESPOSTA A ALGU
						return ROI
				try:
					ROI = twit[i+1] #CAS NORMAL DE TWIT NORMAL (PILLO LA LINIA QUE SURT PER SOTA DE )
					return ROI
				except IndexError:
					return "AN IMAGE WITH NO TOP TEXT IS HERE"
				parar = True
			i = i + 1
		return "No Data"

def comparaRoi(ROI1,ROI2):
	""" PRE: dues seqüencies de caràcters.
		POST: Retorna, una llista que, PER ORDRE, conté els següents elements:
				- String per indicar si la longitud d'ambdues seqüències de caràcterses la mateixa
				- concordància entre ambdues seqüències (miro paraula a paraula).
				- Judici final de l'string. Si son diferents (implica nou twit) torna si. En cas contrari, si son iguals ç
					(implica no existeix nou twit) aleshores torna No

		FUNCIONAMENT: Si longitud de les dues sequencies es diferent ja no miro res mes i dic que twits son diferents. En cas contrari
		miro si hi ha coincidencia, paraula a paraula (podria haver dos strings de la mateixa longitud, però paraula a paraula
		ja no es pot produir confusió).

		NOTA: Assumim que pyteseract OCR és estable i que sempre retorna els mateixos caràcters en fer captures de dos twits iguals en diferents
		moments en el temps.
	"""
	n = len(ROI1)
	m = len(ROI2)
	llJudici = ["No","-","No"] #longitud igual, concordancia, judici si ambdos strings son iguals o no

	if n == m:
		llJudici[0] = "Si"
		ROI1, ROI2 = ROI1.split(), ROI2.split() #tallo per esais buits (tinc paraules a cada element de la llista).
		if len(ROI1) != len(ROI2):
			llJudici[1] = "No" #no concordancia entre paraules
			llJudici[2] = "Si" #VOL DIR QUE HI HA UN NOU TWIT (les dues ROIs dels twits tenen longitud diferent)
			return llJudici
		else:				   #concordància longituds caracters de l'string
			llJudici[0] = llJudici[1] = "Si"
			for i in range(len(ROI1)): #miro paraula a paraula
				if ROI1[i] != ROI2[i]:
					llJudici[1] = "No"
					llJudici[2] = "Si"
					return llJudici
	else:
		llJudici[2] = "Si" #cas que n!=m
	return llJudici





def twitsSonIguals(nomTxt1, nomTxt2):
	"""agafa dos noms de txt (amb extensio inclosa), obre els arxius corresponent i compara si son suficientment iguals com per poder dir
	que son el mateix twit. Per fer la comparacio SOLSAMENT agafa la SEGONA linia del twit -despres de la linia que conté l'arroba-, es a dir
	la primera linia amb text. Nota que no és un mètode infalible perquè pot no comparar tot el twit, però així s'evita comparar la part
	on surten les estadístiquesde likes i comentaris (que poden fer erròniament pensar que el txt del twit ha variat) 

	RETURNS: Si els dos twits representats en els txt son iguals retorna True, en cas contrari torna False. Nomes mira la primera linia del post del trwit ojo."""
	os.chdir("./__captures__")
	f1 = open(nomTxt1,"r")
	f2 = open(nomTxt2,"r")
	print("_____________________COMPARACIO EN PROCES_____________________:")
	print("   TXT TWIT MES RECENT [twit1] ->", nomTxt1)
	print("2n TXT TWIT MES RECENT [twit2] ->", nomTxt2)
	print("_______________________________________________________________\n")
	
	time.sleep(1)

	twit1 = f1.readlines()
	twit2 = f2.readlines()

	print("----------------------------------------------------------------")
	print("[IMPRIMIM TWIT 1]\n")	
	for i in range(len(twit1)):
		twit1[i] = twit1[i][:-1] #netejo salts de linia
		print("   ",twit1[i])
	print("----------------------------------------------------------------")
	print("[IMPRIMIM TWIT 2]\n")
	for i in range(len(twit2)):
		twit2[i] = twit2[i][:-1] #netejo salts de linia
		print("   ",twit2[i])
	print("_______________________________________________________________")

	time.sleep(2)

	global ROI_twit1 #vull fer-la servir despres de cridar aquesta funcio
	ROI_twit1 = roiTwit(twit1)
	ROI_twit2 = roiTwit(twit2)

	print("\nIMPRIMEIXO 1a Líniea de cada TWIT i les comparo:\n")
	print("    [ROI_TWIT1]")
	print("    ",ROI_twit1)

	print("    [ROI_TWIT2]")
	print("    ",ROI_twit2)	
	print("_______________________________________________________________")
	time.sleep(2)

	a = comparaRoi(ROI_twit1,ROI_twit2)
	print("""|LONGITUD IGUAL:                {}\n|CONCORDANCIA PARAULA-PARAULA:  {}\n|HI HA NOU TWIT?         ¡¡---> {} <---!!""".format(a[0],a[1],a[2]))


	f1.close()
	f2.close()

	os.chdir("../")

	if a[2] == "Si": #CAS EN QUE HI HA NOU TWIT
		return False #TORNO QUE ELS STRINGS NO SON IGUALS
	else: #CAS EN QUE NO HI HA UN NOU TWIT
		return True #TORNO QUE ELS STRINGS SON IGUALS

def hiHaNouTwit(URLperfilTwitter, notificacioPrimerMissatge):
	"""
	PRE: Una URL amb el perfil de twitter.
	POST: Un boolea que indica si hem demanat produir notificacio per l'inici del programa amb carpeta __captures__ buida o no.
	FUNCIONAMENT: quan s'inicia el programa amb la carpeta __captures__ amb dos arxius (els que acaba de crear mirant el twiter) 
	torna False i despres nomes torna cert quan realment s'ha detectat un nou twit. En l'ultim cas ho fara comparant els documents
	TXT que contenen els dos ultims twits scrapejats,que poden ser iguals -no s'ha creat nou twit- o diferents -s'ha creat nou twit-. Aixo es fa cridant la funcio twitsSonIguals. 
	""" 
	os.chdir("./__captures__")
	directori = os.listdir()
	n = len(directori)	#nombre d'arxius que hi ha al directori
	
	#cas en que nomes s'ha escanejat un twit (el primer twit haura generat 2 arxius9
	if n == 2:
		os.chdir("../")
		if notificacioPrimerMissatge:
			enviarNotificacio_Pushover("Programa iniciat!")
		else:
			netejaPantalla()
			print("Programa iniciat! Pero s'ha escollit no enviar notificacio d'inicialització de programa!")
			time.sleep(3)
			netejaPantalla()
		return False

	#cas en que el programa ja havia escrapejat un twit en png i txt, i ara vol comparar-lo amb el que ha escrapejat ara
	elif n > 2:		 #podria ser 4,6,8,10,12...parell sempre (simplement perque cada twit capturat genera un .png i el seu txt corresponent).
		directori.sort(reverse = True, key=lambda x: os.path.getmtime(x)) #ordeno captures de pantalla de mes nova a mes antiga
		os.chdir("../")	
		ExisteixnouTwit = not twitsSonIguals(directori[0],directori[2]) #nota que aixo sempre compara TXT mes recent -directori[0]- amb el penultim TXT -directori[2]- mes recent quan hi es.
		if ExisteixnouTwit:
			print("Notificació a enviar:")
			time.sleep(1)
			if boolea_retwit:
				cosNotificacio = "@"+URLperfilTwitter.split("https://twitter.com/")[1]+" (scraped at "+directori[0].split("_")[2].replace(".",":")+") Retweeted: "+"'"+ROI_twit1+"'" #CONTE EL RETWIT!!! ES VARIABLE GLOBAL DE L'ALTRA FUNCIO
				enviarNotificacio_Pushover(cosNotificacio+" <"+URLperfilTwitter+">")
			else:
				cosNotificacio = "new tweet made by @"+URLperfilTwitter.split("https://twitter.com/")[1]+" (scraped at "+directori[0].split("_")[2].replace(".",":")+"): "+"'"+ROI_twit1+"'" #CONTE EL TWIT!!! ES VARIABLE GLOBAL DE L'ALTRA FUNCIO
				enviarNotificacio_Pushover(cosNotificacio+" <"+URLperfilTwitter+">")
			time.sleep(0.5)
			print("enviada")
			time.sleep(1)
		return ExisteixnouTwit


def netejarDirectori_i_copiaAnou(nomCarpetaDesti):
	"""PRE: Un directori amb 4 arxius (o 6, o 8, o 10, etc).
	   POST: Directori arrel queda netejat, deixant nomes els 6 
	   arxius mes recents. Tota la resta d'arxius passen a "nomCarpetaDesti"""
	os.chdir("./__captures__")

	directori = os.listdir()
	nFitxers = len(directori)
	if nFitxers >= 6: #TAL I COM ESTA PROGRAMAT SEMRE ACTUARA AMB nFit == 6, no caldria posar nFit => 6
		directori.sort(reverse = False, key=lambda x: os.path.getmtime(x)) #ordeno captures de pantalla de mes ANTIGA a mes NOVA (StackOverflowhow-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
		for i in range(nFitxers - 4): #directori ordenat de mes VELL a mes NOU
			shutil.move(directori[i],"../"+nomCarpetaDesti+"/"+directori[i])
	else:
		pass

	os.chdir("../")

def enviarNotificacio_Pushover(stringNotificacio):
	"""TO DO: ENVIAR NOTIFICACIO DE QUE EL PROGRAMA HA ESTAT INICIAT"""
	netejaPantalla()
	print("Inici notificació!")
	import http.client, urllib
	conn = http.client.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	  urllib.parse.urlencode({
	    "token": "aucaq78oopn8f5eq9x6m67qpw62ien",  #TOKEN CORRESPONENT a l'app twitterBot_SS
	    "user": "us2o7tz49v2dbbyp9j8raq6r1m5q1m", #USUARI DE PUSHOVER --> aquesta clau n'hi ha una per cada usuari (en aquest cas jo i altres que vulguins fer ho servir)
	    "message": stringNotificacio,
	  }), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()
	print("Notificació feta a Pushover!")
	time.sleep(1)
	netejaPantalla()

def espera3(wait):
	for i in range(wait):
		print("No s'ha carregat. Esperem {}/{}s i ho tornem a intentar".format(i,wait))
		time.sleep(1)
		netejaPantalla()

def obreNavegadorTwitter(driver,URLperfilTwitter):
	"""funcio que obre la pagina del navegador. Te en compte quan no carrega
	la pagina i va afegint timeouts incrementals fins al proper intent, fent 
	un catch dels errors que vna sortint. Bucle infinit.
	
	https://stackoverflow.com/questions/65372252/selenium-python-page-down-unknown-error-neterr-name-not-resolved
	"""
	connexioCorrecta = False
	espera = 5
	j = 0
	while not connexioCorrecta:
		try:
			j = j + 1
			driver.get(URLperfilTwitter)
			connexioCorrecta = True
		except WebDriverException: 
			espera3(espera*j)



def guarda_log_a_JSON(clau,valor,nomArxiu):
	"""PRE: la clau, valor i nom d'arxiu al qual ho vols guardar(tots strings) 
	   POST: l'arxius amb el nomArxiu actualitzat amb el parell clau:valor afegit (si l'arxiu existia) o l'arxiu json creat
	         amb el parell clau:valor afegits en cas que l'arxiu no exist´´is.
	"""
	try:
		#LLEGEIXO ARXIU SI JA EXISTEIX
		with open(nomArxiu, 'r') as f:
			d = json.load(f)
		#AFEGEIXO LOG I REESCRIC ARXIU
		d[clau] = valor
		with open(nomArxiu, 'w') as f:
			json.dump(d, f, indent=4) 
	except FileNotFoundError:
		with open(nomArxiu, 'w') as f:
			d = {}
			d[clau] = valor
			json.dump(d, f) #poso el diccionari d a l'arxiu f



def main(URLperfilTwitter, segonsPausa, notificacioPrimerMissatge):
	"""
	This program will detect and classify correctly the following twitter events (those who a appear on top of the twitter feed) 
	by sending a notification to the user via pushover containing the first line of the twit. This will be done with a sampling rate of around 1/segonsPausa (with sampling intervals of
	segonsPausa) PLUS the algorithm execution time (which includes inner time intervals thought for, mainly, print call legibility
	but also time for 
	

	The program detects new...

		- ..Pinned responses, by which the user's profile makes them on top of the twitter feed.
		- ..twits with text
		- ..retweets with text (it'll inform that it is retweet)
		- ..twits/retweets with text

	TO DO:
		- Detection of twits with image and no text on top of it (on the go... not working perfectly)
		- If last twit gets deleted it would send a notification with the previous twit (this is a FLAW --> TO DO)
		- If THERE IS A PINNED RESPONSE then new twits appear below of it, which means the algorithm will not find them... (this is a flaw --> to do)
		- A l'except del main cal fer que la notificacio nomes sigui per a tu: busca "#NOTIFICACIO QUE HA DE SER NOMES PER A MI"	
	"""
	while True:
		imatgeApta = False #COMPROVO SI LA ULTIMA IMATGE CROPEJADA TE ASPECTE DE TWIT. EN CAS CONTRARI REPETEIXO L'SCANEIG INDEFINIDAMENT
		while not imatgeApta:
			netejaPantalla()
			print("#########################")
			print("##### IniciPrograma #####")
			print("#########################")
			time.sleep(1)
			netejaPantalla()

			ScrollVertical = 400 #la mida adequada perque l'script funcioni
			
			#SI CHROMEDRIVER I CHROME TENEN MATCH EN LA VERSIO (CAS IDEAL, TIRA MILLES)
			try:
				driver = webdriver.Chrome(rutaDriverChrome)
			#EN CAS CONTRARI ENVIEM NOTIFICACIO (HAURAS D INSTAL·LAR CHROMEDRIVER ACTUALITZAT A VERSIO DE CHORME, EL MES AVIAT POSSIBLE)
			except SessionNotCreatedException:
				missatgeErrorDriver_llarg = "Chromedriver i versio Chrome NO ENCAIXEN. TODO: Cal descarregar chromedriver.exe de nou! En cas contrari es decscarrega chromedriver a la catxe cada cop. NOTA: ErrorGuardatAlLog"
				missatgeErrorDriver_curt = "Chromedriver i versio Chrome NO ENCAIXEN. TODO: Cal descarregar chromedriver.exe de nou!"
				stringHoraActual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
				guarda_log_a_JSON(clau=stringHoraActual,valor=missatgeErrorDriver_curt,nomArxiu="LogErrors.json")
				netejaPantalla()
				print(missatgeErrorDriver_llarg)
				time.sleep(5)

				#NOTIFICACIO QUE HA DE SER NOMES PER A MI
				enviarNotificacio_Pushover(missatgeErrorDriver)
				
				driver = webdriver.Chrome(ChromeDriverManager().install())				
				

			obreNavegadorTwitter(driver,URLperfilTwitter)

			driver.set_window_position(0,0) 	#NO CALDRIA PERO AIXI VISUALMENT ES VEU MILLOR.
			driver.set_window_size(1920/3,1080) #DEFINEIXO AMPLADA I ALTURA DE LA FINESTRA
			espera(5) 							#cal pq funcioni b
			driver.execute_script("window.scrollTo(0, "+str(ScrollVertical)+")") #fem scroll abaix per veure el twit, informem i fem screenshot
			netejaPantalla()
			print("MOGUT "+str(ScrollVertical)+" px (eix Y)")
			time.sleep(1)
			data_ara = generaStringData()
			nomImatge = "__captures__/"+URLperfilTwitter.split("https://twitter.com/")[1]+"_"+data_ara
			driver.save_screenshot(nomImatge+".png")
			driver.quit() #tanquem navegador i sessio

			fesCropAnovaImatge_i_esborraLaPrevia(nomImatge) #FAIG CROP DE L'SCREENSHOT PREVI A UN PNG ACTOTAT AMB L'ULTIM TWIT (LA ROI ES PRIMERA LINIA DE L'ULTIM TWIT)
			imatgeApta = imatgeCropejada_a_txt_OCR()		#GENERO TXT A PARTIR DE LA IMATGE CROPEJADA I EL BOOLEA DE SI LA IMATGE ES APTA
			netejaPantalla()
		
		#evaluo si hi ha nou twit
		if hiHaNouTwit(URLperfilTwitter, notificacioPrimerMissatge):
			print("Hi havia un nou twit.\nUna notificació a pushover amb la 1a linia del nou twit ha sigut enviada!!!")
			time.sleep(2)
		else:
			print("No hi ha nous twits!") 
			time.sleep(2)
		
		
		espera2(segonsPausa)
		netejarDirectori_i_copiaAnou("__capturesAntigues__") #neteja el directori de png i txt superflus (si no s'acumukarien i estariem ordenant directoris enormes, computacionalment expensive -sense contar amb tota la memoria que gastariem-)	




if __name__ == "__main__":
	main(URLperfilTwitter = "https://twitter.com/elonmusk",
		segonsPausa = 5, #posar 120 segons, funciona b 
		notificacioPrimerMissatge = False)
	
	
	
	#imatgeCropejada_a_txt_OCR()
	#guarda_log_a_JSON(clau="2",valor="GUAPO GUAPO",nomArxiu="LogErrors.json")
	
	#FUNCIO EN PRINCIPI VA B! PROVA EN CONTEXT. CREC QUE PODRIES INCREMENTAR ELS ARXIUS BORRATS EN DOS MES, PERO CALDRIA COMPROVAR-HO
	#netejarDirectori_i_copiaAnou("__capturesAntigues__") #neteja el directori de png i txt superflus.	


#driver.get(pagina) -- obre la pagina
#driver.close() ------	tanca pestanya actual + sessio driver oberta.
#driver.quit()  ------ tana el navegador + tanca la sessio del driver
#driver.title() ------- imprimeix el titol de la pagina web (el <title></title>)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #si vols moure-ho tot avall.