from flask import Flask, render_template, request
from src.predict_pipeline import CustomData, PredictPipeline
from src.data_ingestion import DataIngestionConfig

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_data', methods=["GET", "POST"])
def predict_data():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        # Get the images
        address = request.form['address'] ### JSON
        data_in = DataIngestionConfig()
        data = data_in.initiate_data_ingestion([address])

        # Process the images
        image_dir = 'tmp/'
        cust_data = CustomData(image_dir)
        image_paths = cust_data.image_paths
        image_list = cust_data.get_data()
        pred_pipe = PredictPipeline()
        img_output, results_dict = pred_pipe.predict(image_list)

        has_solar = list()
        has_pool = list()
        for multi_dict in results_dict:
            solar_panel = 0 in multi_dict['labels']
            pool = 1 in multi_dict['labels']

            has_solar.append(solar_panel)
            has_pool.append(pool)

        return render_template(
            'result.html',
            address=address,
            has_pool=has_pool,
            has_solar=has_solar,
            check = image_paths
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
