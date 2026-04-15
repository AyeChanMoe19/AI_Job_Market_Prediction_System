from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# load trained model
model = joblib.load("D:/Dissertation/AI_Job_Market_Project/model/ai_skill_model.pkl")
print("Model features:", model.feature_names_in_)

@app.route("/predict_ai_skill_demand", methods=["GET"])
def predict():

    try:
        year = int(request.args.get("year"))
        print("Year received:", year)

        # estimate features based on trend
        total_skill_count = 5 + (year - 2010) * 0.5
        ai_skill_count = 1 + (year - 2010) * 0.35
        job_count = 200 + (year - 2010) * 12

        input_data = pd.DataFrame({
            "posting_year": [year],
            "total_skill_count": [total_skill_count],
            "ai_skill_count": [ai_skill_count],
            "job_count": [job_count]
        })

        print("Input features:", input_data)

        prediction = model.predict(input_data)
        print("Prediction:", prediction)

        return jsonify({
            "year": year,
            "predicted_ai_skill_ratio": float(prediction[0])
        })

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route("/predict_high_demand_jobs", methods=["GET"])
def predict_high_demand_jobs():

    try:
        year = int(request.args.get("year"))

        df = pd.read_csv(
            "D:/Dissertation/AI_Job_Market_Project/Dataset/future_job_predictions.csv"
        )

        result = df[df["year"] == year]

        jobs = result.sort_values(
            "predicted_job_count", ascending=False
        )["job_title"].head(5).tolist()
        
        print("Top jobs:", jobs)

        return jsonify({
            "year": year,
            "top_jobs": jobs
        })

    except Exception as e:
        return jsonify({"error": str(e)}) 

@app.route("/predict_top_skills", methods=["GET"])
def predict_top_skills():

    try:
        year = int(request.args.get("year"))

        df = pd.read_csv(
            "D:/Dissertation/AI_Job_Market_Project/Dataset/future_skill_predictions.csv"
        )

        result = df[df["year"] == year]

        skills = result.sort_values(
            "predicted_skill_demand",
            ascending=False
        )["skill"].head(5).tolist()

        return jsonify({
            "year": year,
            "top_skills": skills
        })

    except Exception as e:
        return jsonify({"error": str(e)})  

@app.route("/predict_ai_automation_risk", methods=["GET"])
def predict_ai_automation_risk():

    try:
        year = request.args.get("year")

        if year is None:
            return jsonify({"error": "Year parameter is required"}), 400

        year = int(year)

        df = pd.read_csv(
            "D:/Dissertation/AI_Job_Market_Project/Dataset/future_automation_risk_updated.csv"
        )

        result = df[df["posting_year"] == year]

        if result.empty:
            return jsonify({
                "year": year,
                "high_risk_jobs": []
            })

        top_jobs = result.sort_values("rank")[[
            "job_title", "predicted_risk", "risk_percentage", "rank"
        ]].head(10)

        return jsonify({
            "year": year,
            "high_risk_jobs": top_jobs.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": str(e)})     

if __name__ == "__main__":
    app.run(port=5000, debug=True)



    