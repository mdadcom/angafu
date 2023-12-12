"""
import pymysql
from firebase import firebase

# Configuration Firebase
firebase_url = 'https://transreceiv-default-rtdb.firebaseio.com/'
firebase = firebase.FirebaseApplication(firebase_url, None)

# Configuration MySQL
mysql_host = '207.180.223.199'
mysql_user = 'angafu'
mysql_password = 'Angafu@2023'
mysql_db = 'angafu'

# Établir une connexion MySQL
conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db)
cursor = conn.cursor()

# Récupérer les données depuis Firebase
firebase_data = firebase.get('/', None)

# Formater les données et les insérer dans MySQL
for key, value in firebase_data.items():
    # Accéder à la valeur du message
    message = value.get('message', '')

    # Diviser le message
    message_parts = message.split(',')

    # Vérifier si la liste a suffisamment d'éléments
    if len(message_parts) >= 3:
        # Utiliser les parties du message pour remplir la table MySQL
        # Assurez-vous d'ajuster cette partie en fonction de votre modèle Django
        query = f"INSERT INTO your_table (num_trans, trans_id, montant_paye, date_paiement) VALUES ('{message_parts[0]}', '{message_parts[1]}', '{message_parts[2]}', NOW())"
        cursor.execute(query)
    else:
        print(f"Le message n'a pas assez de parties : {message_parts}")



# Valider et fermer la connexion MySQL
conn.commit()
conn.close()

"""