from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)


# DATA LOADING

df = pd.read_csv("C:\\Users\\pc\\Desktop\\python, sir zfar iqbal\\simple_linearRegression\\dropout22_clean.csv")

print("Data loaded successfully")

print(df)

#  DATA CLEANING

#  missing values 
# df = df.fillna({
#     "attendance": 65.0,
#     "fee_delay_days" :  39.0,
#     "marks_avg": 65.0,
#     "months_enrolled" : 23.5,
#     "risk_score": 34.5
# })

# Duplicate rows 

# df = df.drop_duplicates()



lr = LinearRegression()

lr.fit(df[["attendance", "fee_delay_days", "marks_avg", "months_enrolled"]], df.risk_score)

pridict = lr.predict([[80, 10, 70, 12]])

print("Model trained successfully")

print("Coefficients:", lr.coef_)
print("Intercept:", lr.intercept_)
print("Predicted risk score for [80, 10, 70, 12]:", pridict)



# Home page — frontend dikhao
@app.route("/")
def home():
    return render_template("index.html")


# Predict API — frontend yahan 4 values bhejta hai (JSON)
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    attendance = float(data["attendance"])
    fee_delay = float(data["fee_delay_days"])
    marks = float(data["marks_avg"])
    months = float(data["months_enrolled"])

    # Model se andaza lo (2D array — double bracket!)
    risk = lr.predict([[attendance, fee_delay, marks, months]])[0]

    # Risk ko 0-100 ke beech rakho

    risk = max(0, min(100, round(risk, 1)))

   # Risk level decision
    if risk >= 60:
        level = "HIGH"
        action = "Contact the parents immediately — there is still time to retain this student."
    elif risk >= 35:
        level = "MEDIUM"
        action = "Keep a close watch — start attendance and fee follow-up."
    else:
        level = "LOW"
        action = "All good — no risk detected."

    return jsonify({
        "risk": risk,
        "level": level,
        "action": action
    })


if __name__ == "__main__":
    app.run(debug=True)
