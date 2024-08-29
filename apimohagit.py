from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Créer une instance de FastAPI
app = FastAPI()

# Charger le modèle globalement lors du démarrage de l'application
model = joblib.load("iris_regressor.pkl")

# Définir un modèle de requête
class IrisRequest(BaseModel):
    sepal_width: float
    petal_length: float
    petal_width: float

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
