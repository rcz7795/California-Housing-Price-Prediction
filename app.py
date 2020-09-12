from flask import Flask, request, render_template
from flask_cors import cross_origin

import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("chpp.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        total_rooms = float(request.form["tot_rooms"])
        total_bedrooms = float(request.form["tot_bedrooms"])
        population = float(request.form["population"])
        household = float(request.form["household"])
        median_income = float(request.form["median_income"])
        ocean_proximity = request.form['Source']

        if (ocean_proximity == "1H_OCEAN"):
            ocean_proximity_list = [1, 0, 0, 0, 0]
        elif (ocean_proximity == "INLAND"):
            ocean_proximity_list = [0, 1, 0, 0, 0]
        elif (ocean_proximity == "NEAR_OCEAN"):
            ocean_proximity_list = [0, 0, 1, 0, 0]
        elif (ocean_proximity == "NEAR_BAY"):
            ocean_proximity_list = [0, 0, 0, 1, 0]
        elif (ocean_proximity == "ISLAND"):
            ocean_proximity_list = [0, 0, 0, 0, 1]
        else:
            ocean_proximity_list = [0, 0, 0, 0, 0]

        new_sample = [[median_income, total_bedrooms / total_rooms, household / population] + ocean_proximity_list]
        
        prediction = round(model.predict(new_sample)[0], 2)

        return render_template('home.html', prediction_text = "The house price is US ${}".format(prediction))

    return render_template("home.html")



if __name__ == "__main__":
    app.run(debug = True)