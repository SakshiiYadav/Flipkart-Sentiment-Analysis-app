from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load('svc.pkl')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        input_text = request.form['text']
        
        if not input_text.strip():  
            error = "Please enter your text."
            return render_template('index.html', error=error)
        
        
        prediction = model.predict([input_text])[0]
        
        return render_template('index.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
