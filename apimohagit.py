from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os

load_dotenv()
# Créer une instance de FastAPI
app = FastAPI()

# Charger le modèle globalement lors du démarrage de l'application
model = joblib.load("iris_regressor.pkl")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

# Définir un modèle de requête
class IrisRequest(BaseModel):
    sepal_width: float
    petal_length: float
    petal_width: float

class FeedbackRequest(BaseModel):
    sepal_width: float
    petal_length: float
    petal_width: float
    observation: float
    prediction: float

# Point de terminaison pour faire une prédiction
@app.post("/predict")
def predict(iris: IrisRequest):
    # Faire une prédiction
    prediction = model.predict([[iris.sepal_width, iris.petal_length, iris.petal_width]])

    # Retourner la prédiction
    return {"predicted_sepal_length": prediction[0]}

# Point de terminaison pour vérifier que l'API est en cours d'exécution
@app.get("/status")
def status():
    return {"message": "API is up and running!"}
@app.get("/quentin")
def quentin():
    return {"message": "L'expert excel est là!"}
@app.post("/feedback")
def feedback(feedback: FeedbackRequest):
    # Connexion à la base de données
    connection = create_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Erreur de connexion à la base de données.")

    try:
        cursor = connection.cursor()

        # Requête SQL pour insérer les données de feedback dans la table 'monitoring'
        sql = """
        INSERT INTO monitoring (sepal_width, petal_length, petal_width, observation, prediction)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            feedback.sepal_width,
            feedback.petal_length,
            feedback.petal_width,
            feedback.observation,
            feedback.prediction
        )

        cursor.execute(sql, values)
        connection.commit()

        # Fermer le curseur et la connexion
        cursor.close()
        connection.close()

        return {"message": "Feedback enregistré avec succès."}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement du feedback : {e}")
