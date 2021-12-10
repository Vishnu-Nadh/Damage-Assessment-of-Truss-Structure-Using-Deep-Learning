from re import X
from flask import (
    Flask,
    request,
    render_template,
    jsonify,
    send_file,
    url_for,
)
import os
from dataLoader import Load_Data
from preprocessor import Preprocess
from trainModel import Train_Model
from plotTruss import Plot_Truss


app = Flask(__name__)
img_path = os.path.join("static", "images")

root_dir = os.getcwd()
input_data_path = os.path.join(root_dir, "Input_Data")
app.config["UPLOAD_FOLDER"] = img_path
app.config["INPUT_DATA"] = input_data_path
app.config["SEND_RESULT"] = os.path.join(root_dir, "Predicted_Output")


@app.route("/train", methods=["GET", "POST"])
def train():
    if request.method == "POST":
        if request.json['key'] == 'start':
            load_data = Load_Data()
            data = load_data.loadData()
            preoprocess = Preprocess(data)
            x_train, y_train = preoprocess.preprocessTrain()
            model_train = Train_Model(x_train, y_train)
            output = model_train.trainModel()
            
            
    return jsonify(output)




@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if request.files:
            input_file = request.files["upload-btn"]
            print(input_file.filename)
            input_file.save(os.path.join(app.config["INPUT_DATA"], "input_data.csv"))

            ## do the prediction work

            img = os.path.join(app.config["UPLOAD_FOLDER"], "nodamage_truss.png")
            return render_template("result.html", image=img)
    else:
        img = os.path.join(app.config["UPLOAD_FOLDER"], "truss.jpg")
        return render_template("index.html", image=img)


@app.route("/download_result", methods=["GET", "POST"])
def download_result():
    path = os.path.join(app.config["SEND_RESULT"], "input_data.csv")
    return send_file(path, "predictions.csv", as_attachment=True)


@app.route("/show_truss", methods=["GET", "POST"])
def show_truss():
    if request.method == "POST":
        index = float(request.form["index"])
        print(index)
        # get result and extract damage for index passed in
        damages = {
            1: 0.3,
            2: 0,
            3: 0.2,
            4: 0,
            5: 0.1,
            6: 0,
            7: 0,
            8: 0.5,
            9: 0.3,
        }
        plot = Plot_Truss(damage_dict=damages)
        plot.plotTruss()
        img = os.path.join(app.config["UPLOAD_FOLDER"], "damageplot.png")
        return render_template("result.html", image=img)
    else:
        return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)
