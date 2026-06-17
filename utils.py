import pandas as pd
import numpy as np


# ===========================================
# CREATE INPUT DATAFRAME
# ===========================================

def prepare_input(
    feature_columns,
    vehicle_age,
    km_driven,
    mileage,
    engine,
    max_power,
    seats,
    brand,
    model_name,
    fuel_type,
    seller_type,
    transmission_type
):

    input_data = pd.DataFrame(
        np.zeros((1, len(feature_columns))),
        columns=feature_columns
    )

    # ----------------------------
    # Numerical Features
    # ----------------------------

    numeric = {
        "vehicle_age": vehicle_age,
        "km_driven": km_driven,
        "mileage": mileage,
        "engine": engine,
        "max_power": max_power,
        "seats": seats
    }

    for col, value in numeric.items():

        if col in input_data.columns:
            input_data[col] = value

    # ----------------------------
    # One Hot Encoding
    # ----------------------------

    categorical_columns = [
        f"brand_{brand}",
        f"model_{model_name}",
        f"fuel_type_{fuel_type}",
        f"seller_type_{seller_type}",
        f"transmission_type_{transmission_type}"
    ]

    for col in categorical_columns:

        if col in input_data.columns:
            input_data[col] = 1

    return input_data


# ===========================================
# PREDICT PRICE
# ===========================================

def predict_price(model, input_data):

    prediction = model.predict(input_data)[0]

    return round(float(prediction), 2)


# ===========================================
# VEHICLE HEALTH SCORE
# ===========================================

def vehicle_health(
    vehicle_age,
    km_driven,
    mileage
):

    score = 100

    score -= vehicle_age * 3

    score -= km_driven / 12000

    if mileage < 10:
        score -= 15

    elif mileage < 15:
        score -= 8

    elif mileage < 20:
        score -= 3

    score = max(0, min(100, score))

    return round(score)


# ===========================================
# CONDITION
# ===========================================

def vehicle_condition(score):

    if score >= 85:

        return (
            "🟢 Excellent",
            "#00E676"
        )

    elif score >= 70:

        return (
            "🟢 Good",
            "#43A047"
        )

    elif score >= 50:

        return (
            "🟡 Fair",
            "#FFC107"
        )

    else:

        return (
            "🔴 Poor",
            "#E53935"
        )


# ===========================================
# PRICE CATEGORY
# ===========================================

def price_category(price):

    if price < 300000:
        return "Budget"

    elif price < 800000:
        return "Mid Range"

    elif price < 1500000:
        return "Premium"

    else:
        return "Luxury"


# ===========================================
# DEPRECIATION
# ===========================================

def depreciation(price):

    year1 = price * 0.90
    year2 = year1 * 0.92
    year3 = year2 * 0.93
    year4 = year3 * 0.94
    year5 = year4 * 0.95

    return {
        "Current": round(price),
        "After 1 Year": round(year1),
        "After 2 Years": round(year2),
        "After 3 Years": round(year3),
        "After 4 Years": round(year4),
        "After 5 Years": round(year5)
    }


# ===========================================
# HEALTH COLOR
# ===========================================

def health_color(score):

    if score >= 85:
        return "green"

    elif score >= 70:
        return "lime"

    elif score >= 50:
        return "orange"

    return "red"


# ===========================================
# FORMAT PRICE
# ===========================================

def indian_price(price):

    return f"₹ {price:,.0f}"


# ===========================================
# SUMMARY
# ===========================================

def summary(
    prediction,
    health_score
):

    category = price_category(prediction)

    condition, color = vehicle_condition(
        health_score
    )

    return {
        "price": indian_price(prediction),
        "category": category,
        "condition": condition,
        "health": health_score,
        "color": color
    }