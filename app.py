from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_ip import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

# =========================
# Create FastAPI App
# =========================
app = FastAPI()

# =========================
# Home Route
# =========================
@app.get("/")
def home():

    return {
        "message": "Insurance Premium Prediction API Running"
    }

# machine readable
@app.get('/health')
def health_check():
    return{
        'status': "ok",
        'version': MODEL_VERSION,
        'model_load': model is not None
    }

# =========================
# Prediction Route
# =========================
# @app.post("/predict", response_model=predictionResponse)
@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):

    try:

        user_input ={
            "bmi": data.bmi,
            "age_group": data.age_group,
            "life_risk": data.life_risk,
            "city_tier": data.city_tier,
            "income_lpa": data.income_lpa,
            "occupation": data.occupation
        }

        # print(input_df)

        prediction = predict_output(user_input)

        return JSONResponse(
            status_code=200,
            content={
                "predicted_category": prediction
            }
        )

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )