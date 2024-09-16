from flask import Flask, request, jsonify
import util
app = Flask(__name__)
from flask_cors import CORS
CORS(app)
@app.route('/get_gender_and_smoking_status')
def get_gender_and_smoking_status():
    response = jsonify({
        'gender': util.get_gender(),
        'smoking_status': util.get_smoking_status()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/heart_stroke_prediction', methods=['POST'])
def heart_stroke_prediction():
    try:
        # Log the incoming request data to debug
        data = request.get_json()

        required_fields = ['smoking_status', 'gender', 'age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']

        # Check if all fields are present
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing parameters: {", ".join(missing_fields)}'}), 400

        # Extract form data
        smoking_status = data['smoking_status']
        gender = data['gender']
        age = int(data['age'])
        hypertension = int(data['hypertension'])
        heart_disease = int(data['heart_disease'])
        avg_glucose_level = float(data['avg_glucose_level'])
        bmi = float(data['bmi'])

        # Call util function to get prediction
        prediction = util.get_heart_stroke(smoking_status, gender, age, hypertension, heart_disease, avg_glucose_level, bmi)

        # Convert the prediction to a native Python type to avoid the "int64 not serializable" issue
        prediction = float(prediction)

        # Return the response in JSON format
        response = jsonify({
            'heart_stroke': prediction
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except ValueError as e:
        return jsonify({'error': f'Invalid data type: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == "__main__":
    print("Python server running for Heart_stroke_prediction")
    util.load_saved_artifacts()
    app.run(debug=True)


