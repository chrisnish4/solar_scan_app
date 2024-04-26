import json
import shutil
from flask import Flask, render_template, request
from src.predict_pipeline import CustomData, PredictPipeline
from src.data_ingestion import DataIngestionConfig
from src.utils import generate_hash, read_gcs # for beta

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
        address = request.form['address'] ### JSON ###########how to deal with this
        data_in = DataIngestionConfig()
        data = data_in.initiate_data_ingestion([address])

        # Process the images
        image_dir = 'tmp/'
        cust_data = CustomData(image_dir)
        image_list = cust_data.get_data()
        pred_pipe = PredictPipeline()
        _, results_dict = pred_pipe.predict(image_list)

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
        )

@app.route('/beta_index')
def beta_index():
    return render_template('beta_index.html')

@app.route('/beta', methods=["GET", "POST"])
def beta():
    if request.method == 'GET':
        return render_template('beta_index.html')
    elif request.method == 'POST':
        address = request.form['address']
        hash_value = generate_hash(address)
        object_name = f'{hash_value}.png'
        local_file_path = f'static/{object_name}'
        
        read_gcs('beta-area', object_name, local_file_path)
        
        with open('get_beta/beta_bools.json') as f:
            json_data = json.load(f)

        has_solar = json_data[hash_value]['has_solar']
        has_pool = json_data[hash_value]['has_pool']
        return render_template(
            'beta_result.html',
            address = address,
            has_solar = has_solar,
            has_pool = has_pool,
            file_name = local_file_path
        )

#def shutdown_function():
#    """
#    Deletes the static folder
#    """
#    shutil.rmtree('static')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
