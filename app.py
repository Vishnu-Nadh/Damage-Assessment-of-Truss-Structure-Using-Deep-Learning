from flask import Flask, request, render_template, jsonify, send_file, url_for, flash
import os
import pandas as pd
from dataLoader import Load_Data
from preprocessor import Preprocess
from trainModel import Train_Model
from prediction import Predict_Output
from plotTruss import Plot_Truss

app = Flask(__name__)
app.config["SECRET_KEY"] = "80c2f0634018c50157ef1ff885b0fa3190423755"

img_path = os.path.join("static", "images")

root_dir = os.getcwd()
input_data_path = os.path.join(root_dir, "Prediction_Input")
app.config["INPUT_DATA"] = input_data_path
app.config["SEND_RESULT"] = os.path.join(root_dir, "Predicted_Output")
app.config["UPLOAD_FOLDER"] = img_path


@app.route("/train", methods=["GET", "POST"])
def train():
    if request.method == "POST":
        if request.json["key"] == "start":
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
            input_file.save(
                os.path.join(app.config["INPUT_DATA"], "prediction_data.csv")
            )
            load_data = Load_Data()
            data = load_data.loadDataPred()
            preprocess = Preprocess(data)
            pred_arr = preprocess.preprocessPred()
            predict = Predict_Output(pred_arr)
            prediction = predict.predictOutput()
            prediction.to_csv(
                os.path.join(app.config["SEND_RESULT"], "predictions_.csv"),
                index=False,
                header=None,
            )

            img = os.path.join(app.config["UPLOAD_FOLDER"], "nodamage_truss.png")
            return render_template("result.html", image=img)
    else:
        img = os.path.join(app.config["UPLOAD_FOLDER"], "truss.jpg")
        return render_template("index.html", image=img)


@app.route("/download_result", methods=["GET", "POST"])
def download_result():
    path = os.path.join(app.config["SEND_RESULT"], "predictions_.csv")
    return send_file(path, "predictions.csv", as_attachment=True)


@app.route("/show_truss", methods=["GET", "POST"])
def show_truss():
    if request.method == "POST":
        index = int(request.form["index"])
        path = os.path.join(app.config["SEND_RESULT"], "predictions_.csv")
        result = pd.read_csv(path, header=None)
        max_id = result.shape[0]
        print(max_id)
        print(index)
        if index > max_id:
            flash("Entered index exceed maximum index of the input csv")
            img = os.path.join(app.config["UPLOAD_FOLDER"], "nodamage_truss.png")
            return render_template("result.html", image=img)
        else:
            damage_dict = {}
            result = result.iloc[index - 1]
            for index, value in result.iteritems():
                damage_dict[index + 1] = value
            print(damage_dict)

            plot = Plot_Truss(damage_dict=damage_dict)
            plot.plotTruss()
            img = os.path.join(app.config["UPLOAD_FOLDER"], "damageplot.png")
            return render_template("result.html", image=img)
    else:
        img = os.path.join(app.config["UPLOAD_FOLDER"], "nodamage_truss.png")
        return render_template("result.html", image=img)


if __name__ == "__main__":
    app.run(debug=True)

