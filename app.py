from flask import Flask, render_template, request
import pickle
import numpy as np

# Crear una instancia de Flask
app = Flask(__name__)

# Cargar los modelos desde pickle
try:
    with open('pickle_files/knn_classifier (2).pkl', 'rb') as f:
        classification_model = pickle.load(f)

    with open('pickle_files/knn_regressor (2).pkl', 'rb') as f:
        regression_model = pickle.load(f)
except Exception as e:
    print(f"Error loading models: {e}")
    classification_model = None
    regression_model = None

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if not classification_model or not regression_model:
            return render_template('index.html', error="Models not loaded")
        
        try:
            data = request.form

            # Asegurarse de que todos los valores estén presentes
            required_fields = [
                'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 
                'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 
                'density', 'ph', 'sulphates', 'alcohol'
            ]

            # Verificar que todos los campos estén presentes y no vacíos
            for field in required_fields:
                if field not in data or data[field] == '':
                    return render_template('index.html', error=f"Missing or empty field: {field}")

            # Convertir a array de NumPy
            features = np.array([[float(data[field]) for field in required_fields]])

            # Realizar predicciones
            classification = classification_model.predict(features)[0]
            regression = regression_model.predict(features)[0]

            # Devolver los resultados como HTML
            return render_template('index.html', 
                                 classificationResult = classification,
                                 regressionResult=regression)

        except Exception as e:
            # Mostrar error detallado en la página
            return render_template('index.html', error=f"Prediction error: {str(e)}")

    else:
        # Renderizar el archivo index.html para solicitudes GET
        return render_template('index.html')


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
