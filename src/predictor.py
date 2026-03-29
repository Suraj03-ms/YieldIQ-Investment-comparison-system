import pickle
import pandas as pd

# Load model
with open("src/model.pkl", "rb") as f:
    model = pickle.load(f)

# Load columns
with open("src/columns.pkl", "rb") as f:
    model_columns = pickle.load(f)


def predict_investment(year, total_investment, investment_type):
    # Create input dictionary
    data = {
        'Year': year,
        'Total_Investment': total_investment,
        'Profit': 0,
        'ROI_%': 0
    }

    # Add one-hot encoding
    for col in model_columns:
        if 'Investment_Type_' in col:
            data[col] = 1 if col == f'Investment_Type_{investment_type}' else 0

    # Convert to DataFrame
    input_df = pd.DataFrame([data])

    # Align columns
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    # Predict
    prediction = model.predict(input_df)[0]

    return round(prediction, 2)


# 🔥 Example usage
if __name__ == "__main__":
    result = predict_investment(
        year=10,
        total_investment=1660000,
        investment_type="Mutual Fund"
    )
    
    print("Predicted Final Value:", result)