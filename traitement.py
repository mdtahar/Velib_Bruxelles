#!/usr/bin/python3.4
# coding: utf-8
import math
import pymongo
import pprint 
from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt 
import numpy as np
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.velos
def convertirHeure(heure):
	heureN = datetime.utcfromtimestamp(heure/1000).strftime('%Y-%m-%d %H:%M:%S')
	return heureN
def liste_nomStations():
	nomStations = db.bruxelles.distinct("name")
	# pprint.pprint(nomStations)
	return nomStations
# ([{$group:{_id:"$name",velo:{$min:"$available_bikes"}}},{$project:{_id:1,name:1,velo:1}},{$sort:{velo:-1}}])
# difference entre le max de velo disponible et le min de velo dispo 
# db.bruxelles.aggregate([{$group:{_id:"$name",maxi:{$max:"$available_bikes"},mini:{$min:"$available_bikes"}}},{$addFields:{difference:{ $subtract: ["$maxi","$mini"]}}},{$project:{_id:1,name:1,max:1,min:1,difference:1}},{$sort:{id:1}}])

# selecionner que l heure !!! 
# db.bruxelles.aggregate({$match:{name:"339 - MEUDON"}},{$project:{_id:0,available_bikes:1,available_bike_stands:1,"maj":{$toDate:"$last_update"}}},{$addFields:{majh:{$hour:"$maj"}}},{$project:{majh:1,available_bikes:1,available_bike_stands:1}})

# selectionner l heure et le jour 
# db.bruxelles.aggregate({$match:{name:"339 - MEUDON"}},{$project:{_id:0,available_bikes:1,available_bike_stands:1,"maj":{$toDate:"$last_update"}}},{$addFields:{majD:{$dayOfMonth:"$maj"},majH:{$hour:"$maj"}}},{$project:{majH:1,majD:1,available_bikes:1,available_bike_stands:1}})

# h = db.bruxelles.aggregate([{"$match":{"name":station}},{"$project":{"_id":0,"available_bike_stands":1,"available_bikes":1,"date":{"$toDate":"$last_update"}}},{"$addFields":{"heure":{"$hour":"$date"},"jour":{"$dayOfMonth":"$date"}}},{"$match":{"jour":jour}}])
# pour un jour diffinie 
def statistique(): 
	print('Il y a',len(list(liste_nomStations())),'stations a Bruxelles')
	maxi = db.bruxelles.aggregate([{"$addFields":{"bikes":{"$sum":["$available_bikes","$available_bike_stands"]}}},{"$project":{"_id":0,"name":1,"address":1,"bikes":1}},{"$sort":{"bikes":-1}}])
	liste = list(maxi)
	print('La plus grande station est : ',liste[0]["name"])
	print('Son adresse est : ',liste[0]["address"])
	print('Le nombre de place est : ',liste[0]["bikes"])
def position_gps(): 
	lat = []
	lng = []
	p = db.bruxelles.distinct("position")
	for a in list(p):
		lat.append(a.values()[0])
		lng.append(a.values()[1])

	pprint.pprint(lat)
	pprint.pprint(lng)

	plt.scatter(lng,lat,s=50,color='black')
	plt.title('Position GPS de toutes les stations')
	plt.xlabel('lng')
	plt.ylabel('lat')
	plt.show()
	
# def emprunt_retour_jour(station,jour): 
# 	j = db.bruxelles.aggregate([{"$match":{"name":station}},{"$project":{"_id":0,"available_bike_stands":1,"available_bikes":1,"date":{"$toDate":"$last_update"}}},{"$addFields":{"jour":{"$dayOfMonth":"$date"}}},{"$match":{"jour":jour}}])
# 	pprint.pprint(list(j))
# 	dispo_emprunt = []	
# 	dispo_retour = []
# 	list_heure = []
	
def dispo_velo(heure):
	j = db.bruxelles.aggregate([{"$project":{"_id":0,"available_bikes":1,"position":1,"date":{"$toDate":"$last_update"}}},{"$addFields":{"heure":{"$hour":"$date"}}},{"$match":{"heure":heure}},{"$sort":{"available_bikes":1}}])
	lat = []
	lng = []
	for a in list(j):
		# pprint.pprint(a["position"]
		lat.append(a["position"].values()[0])
		lng.append(a["position"].values()[1])
	# pprint.pprint(lng)
	if(len(lat)== 0 ):
		print("Nous n'avons pas de données pour cette heure  ... :( ! ")
	else :
		labels = range(1,len(lng)+1)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		for x,y,lab in zip(lng,lat,labels):
			ax.scatter(x,y,s=50,label=lab)
		colormap = plt.cm.Reds #, BuPu  Reds
		colorst = [colormap(i) for i in np.linspace(0,1,len(ax.collections))]  
		for t,j1 in enumerate(ax.collections):
			j1.set_color(colorst[t])
		plt.xlabel('lng',fontsize = 17)
		plt.ylabel('lat',fontsize = 17)
		plt.grid(True)
		# plt.legend()
		plt.show()
def place_place_dispo(heure):
	j = db.bruxelles.aggregate([{"$project":{"_id":0,"available_bike_stands":1,"position":1,"date":{"$toDate":"$last_update"}}},{"$addFields":{"heure":{"$hour":"$date"}}},{"$match":{"heure":heure}},{"$sort":{"available_bike_stands":1}}])
	lat = []
	lng = []
	for a in list(j):
		# pprint.pprint(a["position"]
		lat.append(a["position"].values()[0])
		lng.append(a["position"].values()[1])
	# pprint.pprint(lng)
	if(len(lat)== 0 ):
		print("Nous n'avons pas de données pour cette heure  ... :( ! ")
	else :
		labels = range(1,len(lng)+1)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		for x,y,lab in zip(lng,lat,labels):
			ax.scatter(x,y,s=50,label=lab)
		colormap = plt.cm.Reds #, BuPu  Reds
		colorst = [colormap(i) for i in np.linspace(0,1,len(ax.collections))]  
		for t,j1 in enumerate(ax.collections):
			j1.set_color(colorst[t])
		plt.xlabel('lng',fontsize = 17)
		plt.ylabel('lat',fontsize = 17)
		plt.grid(True)
		# plt.legend()
		plt.show()	
def histo_velo_dispo(heure,taille) : 
	p = db.bruxelles.aggregate([{"$project":{"_id":0,"name":1,"available_bike_stands":1,"date":{"$toDate":"$last_update"}}},{"$addFields":{"heure":{"$hour":"$date"}}},{"$match":{"heure":heure}}])
	# pprint.pprint(list(p))
	velos_dispo = []
	nom_station = []
	for a in list(p) :
		velos_dispo.append(a["available_bike_stands"])
		nom_station.append(a["name"])
	# pprint.pprint(nom_station)
	x = np.arange(len(nom_station[:taille]))
	fig, ax = plt.subplots()
	plt.bar(x, velos_dispo[:taille])
	plt.xticks(x,tuple(nom_station[:taille]))
	plt.xticks(rotation = 'vertical',fontsize = 4)
	plt.ylabel('Velos',fontsize = 17)
	plt.show()

def emprunt_retour(station):
	d = db.bruxelles.aggregate([{"$match":{"name":station}},{"$project":{"_id": 0,"available_bike_stands":1,"available_bikes":1,"last_update":{"$toDate":"$last_update"}}},{"$sort":{"last_update":1}}])
	# pprint.pprint(list(d))
	dispo_emprunt = []	
	dispo_retour = []
	list_heure = []
	for a in list(d) :
		for b in a.keys() : 
			if b in "available_bike_stands" : #points d attache disponibles pour y ranger un velo
				dispo_retour.append(a.values()[0])
			if b in "available_bikes":  #velos disponible 
				dispo_emprunt.append(a.values()[1])
			if b in "last_update" : 
				list_heure.append(a.values()[2])
				# pprint.pprint(a.values()[0])
	# for heures in list_heure : 
	# 	pprint.pprint(heures)
	plt.plot(list_heure,dispo_emprunt, color = 'green', linewidth = 2,linestyle = "-.",alpha = 1,label="Velos disponible") #velos disponible
	plt.plot(list_heure,dispo_retour, color = 'red', linewidth = 2 ,alpha = 1,label="Place disponible")  #points d attache disponibles pour y ranger un velo
	plt.ylim(2,20)
	plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])
	plt.xticks(rotation = 'vertical')
	plt.legend()
	plt.show()

def distance(a,b):
	R = 6371
	x = (b[1] - a[1]) * math.cos( 0.5*(b[0]+a[0]) )
	y = b[0] - a[0]
	d = R * math.sqrt( x*x + y*y )
	# print(int(d))
	return int(d)
def prediction(action,heure,position): #action est un boolen 1 pour prendre un velo 0 pour déposer 
	if action == 1:
		j = db.bruxelles.aggregate([{"$project":{"_id":0,"name":1,"available_bikes":1,"position":1,"date":{"$toDate":"$last_update"}}},{"$addFields":{"heure":{"$hour":"$date"}}},{"$match":{"heure":heure}},{"$sort":{"available_bikes":-1}}])
		# lj = list(j)
		station = list(j)[:30]
		print("Voici les stations ou vous avez le plus de chances de trouver un vélo :")
		resultat = []
		proche = 99999999
		for a in station :
			dist = distance(position,(a["position"]["lat"],a["position"]["lng"]))

			resultat.append(({"NOM":a["name"],"Nbr Velo":a["available_bikes"],"Distance":dist}))
			print("NOM",a["name"],"Nbr Velo",a["available_bikes"])
			print("Distance",dist)
			proche = min(proche,dist)
		# print(proche)
		# pprint.pprint(resultat)
		for i in range(0,len(resultat)):
			if (resultat[i]["Distance"] == proche): 
				pprint.pprint(resultat[i])
				r = resultat[i]["NOM"]
		# proche = 
				print("la station la plus proche est : ",r )
	else : 
		j = db.bruxelles.aggregate([{"$project":{"_id":0,"name":1,"available_bike_stands":1,"position":1,"date":{"$toDate":"$last_update"}}},{"$addFields":{"heure":{"$hour":"$date"}}},{"$match":{"heure":heure}},{"$sort":{"available_bike_stands":-1}}])
		station = list(j)[:30]
		print("Voici les stations ou vous avez le plus de chances de trouver Une place : ")
		resultat = []
		proche = 99999999
		for a in station :
			dist = distance(position,(a["position"]["lat"],a["position"]["lng"]))

			resultat.append(({"NOM":a["name"],"Nbr place":a["available_bike_stands"],"Distance":dist}))
			print("NOM",a["name"],"Nbr place",a["available_bike_stands"])
			print("Distance",dist)
			proche = min(proche,dist)
		# print(proche)
		# pprint.pprint(resultat)
		for i in range(0,len(resultat)):
			if (resultat[i]["Distance"] == proche): 
				# pprint.pprint(resultat[i])
				z = resultat[i]["NOM"]
		# proche = 
				print("la station la plus proche est : ",z )

if __name__ == '__main__':
	# statistique()
	# liste_nomStations()
	# emprunt_retour("261 - CONSCIENCE")
	# position_gps()
	dispo_velo(00)
	# place_place_dispo(23)
	# histo_velo_dispo(23,100)
	# prediction(1,23,(50.8733,4.42641))