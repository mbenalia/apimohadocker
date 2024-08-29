import unittest
from fastapi.testclient import TestClient
from apimohagit import app  # Remplacez 'apimohagit' par le nom réel de votre fichier

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_predict_endpoint(self):
        # Créer un exemple de requête valide
        test_data = {
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }

        # Envoyer une requête POST au point de terminaison /predict
        response = self.client.post("/predict", json=test_data)

        # Vérifier la réponse
        self.assertEqual(response.status_code, 200)
        self.assertIn("predicted_sepal_length", response.json())

if __name__ == "__main__":
    unittest.main()
