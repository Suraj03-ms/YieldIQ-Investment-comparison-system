import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load data
df = pd.read_csv(r"C:\Users\Suraj\Desktop\combined_dataset.csv")

# Feature Engineering
df['Profit'] = df['Final_Value'] - df['Total_Investment']
df['ROI_%'] = (df['Profit'] / df['Total_Investment']) * 100

# Encode categorical
df = pd.get_dummies(df, columns=['Investment_Type'])

# Features & target
X = df.drop(['Final_Value'], axis=1)
y = df['Final_Value']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Save model
with open("src/model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save feature columns
with open("src/columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("✅ Model trained and saved!")