#/bin/sh
curl -s -a 'https://api.jcdecaux.com/vls/v1/stations?contract=Bruxelles-Capitale&apiKey=2e560d36eef088ef968fd0a6ceab9971111d9fd4' -o $OUTPUT/Users/mdtahar/Desktop/BigData/MongoDb/Projet/Bruxelles-Capitale.json
/usr/local/mongodb/bin/mongoimport --jsonArray --host localhost:27017 --db velos --collection bruxelles < $OUTPUT/Users/mdtahar/Desktop/BigData/MongoDb/Projet/Bruxelles-Capitale.json
echo "Chargement réussi à : $(date) ! Merci " >>/users/mdtahar/Desktop/BigData/MongoDb/Projet/tache.txt
