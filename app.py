from flask import Flask, render_template, request
from src.predict_pipeline import CustomData

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        address = request.form['address'] ### JSON
        #lat, lon = geocode(address)
        return render_template('result.html', address=address)#, lat=lat, lon=lon)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
