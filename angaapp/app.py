"""
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Configuration MySQL
mysql_host = '207.180.223.199'
mysql_user = 'angafu'
mysql_password = 'Angafu@2023'
mysql_db = 'angafu'

# Établir une connexion MySQL
conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db)
cursor = conn.cursor()

# Endpoint pour recevoir les données de Firebase
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json  # Les données JSON envoyées par Firebase

    # Insérer les données dans MySQL
    try:
        query = f"INSERT INTO Confirme (num_trans, trans_id, ...) VALUES (%s, %s, ...)"
        cursor.execute(query, (data['num_trans'], data['trans_id'], ...))
        conn.commit()
        return jsonify({"message": "Données insérées avec succès dans MySQL"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)  # Port sur lequel le serveur écoutera 


"""