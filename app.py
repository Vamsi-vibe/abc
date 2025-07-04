# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bwGVHiE9y4tkI6FrZq8QSxa1zlqV2xIJ
"""

!pip install streamlit pyngrok xgboost scikit-learn pandas matplotlib statsmodels tensorflow --quiet
!pip install streamlit
!pip install pyngrok
!pip install xgboost
!pip install tensorflow

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from statsmodels.tsa.arima.model import ARIMA
# from statsmodels.tsa.api import Holt
# import xgboost as xgb
# import tensorflow as tf
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from sklearn.metrics import mean_absolute_error, mean_squared_error
# 
# # Title
# st.title('Sales Forecasting App')
# 
# # File uploader for CSV
# uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
# 
# if uploaded_file is not None:
#     # Load the dataset
#     df = pd.read_csv(uploaded_file)
# 
#     # Show the first few rows of the dataframe
#     st.write(df.head())
# 
#     # Select columns
#     date_column = st.selectbox("Select the Date Column", df.columns)
#     target_column = st.selectbox("Select the Target Column", df.columns)
# 
#     # Convert date column to datetime
#     df[date_column] = pd.to_datetime(df[date_column])
#     df.set_index(date_column, inplace=True)
# 
#     # Split the data into train and test sets (80% train, 20% test)
#     train_size = int(len(df) * 0.8)
#     train, test = df[target_column][:train_size], df[target_column][train_size:]
# 
#     # ARIMA model
#     def arima_forecast(train, test):
#         model = ARIMA(train, order=(1, 1, 1))
#         model_fit = model.fit()
#         forecast = model_fit.forecast(steps=len(test))
#         return forecast
# 
#     # Holt-Winters model
#     def holt_winters_forecast(train, test):
#         model = Holt(train).fit()
#         forecast = model.forecast(len(test))
#         return forecast
# 
#     # XGBoost model
#     def xgboost_forecast(train, test):
#         model = xgb.XGBRegressor()
#         X_train = np.array(range(len(train))).reshape(-1, 1)
#         X_test = np.array(range(len(train), len(train) + len(test))).reshape(-1, 1)
#         model.fit(X_train, train)
#         forecast = model.predict(X_test)
#         return forecast
# 
#     # LSTM model
#     def lstm_forecast(train, test):
#         X_train = np.array(range(len(train))).reshape(-1, 1)
#         X_test = np.array(range(len(train), len(train) + len(test))).reshape(-1, 1)
#         y_train = np.array(train)
#         model = tf.keras.Sequential([
#             tf.keras.layers.LSTM(64, input_shape=(1, 1)),
#             tf.keras.layers.Dense(1)
#         ])
#         model.compile(optimizer='adam', loss='mean_squared_error')
#         model.fit(X_train, y_train, epochs=10, verbose=0)
#         forecast = model.predict(X_test)
#         return forecast.flatten()
# 
#     # SARIMA model
#     def sarima_forecast(train, test):
#         model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
#         model_fit = model.fit()
#         forecast = model_fit.forecast(steps=len(test))
#         return forecast
# 
#     # Forecasting
#     model_type = st.selectbox("Select the Forecasting Model", ['ARIMA', 'Holt-Winters', 'XGBoost', 'LSTM', 'SARIMA'])
# 
#     if model_type == 'ARIMA':
#         forecast = arima_forecast(train, test)
#     elif model_type == 'Holt-Winters':
#         forecast = holt_winters_forecast(train, test)
#     elif model_type == 'XGBoost':
#         forecast = xgboost_forecast(train, test)
#     elif model_type == 'LSTM':
#         forecast = lstm_forecast(train, test)
#     elif model_type == 'SARIMA':
#         forecast = sarima_forecast(train, test)
# 
#     # Plotting the results
#     forecast_df = pd.DataFrame(forecast, index=test.index, columns=['forecast'])
# 
#     st.subheader(f'{model_type} Forecast')
#     st.write(forecast_df)
# 
#     plt.figure(figsize=(10, 6))
#     plt.plot(train.index, train, label='Training Data')
#     plt.plot(test.index, test, label='Test Data')
#     plt.plot(forecast_df.index, forecast_df['forecast'], label='Forecast', linestyle='--')
#     plt.legend()
#     st.pyplot(plt)
# 
#     # Performance Metrics
#     mae = mean_absolute_error(test, forecast)
#     mse = mean_squared_error(test, forecast)
#     rmse = np.sqrt(mse)
# 
#     st.write(f'Mean Absolute Error: {mae}')
#     st.write(f'Mean Squared Error: {mse}')
#     st.write(f'Root Mean Squared Error: {rmse}')
#



# Step 1: Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Step 2: Simulate sales data (monthly for 3 years)
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=36, freq='M')
sales = 200 + np.linspace(0, 50, 36) + np.random.normal(0, 10, 36)
ad_spend = 20 + 5 * np.sin(np.linspace(0, 3 * np.pi, 36)) + np.random.normal(0, 2, 36)

df = pd.DataFrame({
    'Date': dates,
    'Sales': sales,
    'Ad_Spend': ad_spend
})
df.set_index('Date', inplace=True)

# Step 3: Linear Regression
X = df[['Ad_Spend']]
y = df['Sales']
model_lr = LinearRegression()
model_lr.fit(X, y)
df['LR_Predicted'] = model_lr.predict(X)

# Step 4: SARIMA Model
# Define the SARIMA parameters (p, d, q)x(P, D, Q, s)
# Here, s=12 for monthly data with yearly seasonality
sarima_model = SARIMAX(df['Sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
sarima_result = sarima_model.fit(disp=False)

# Forecast next 12 months
forecast_steps = 12
forecast = sarima_result.forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=df.index[-1] + pd.DateOffset(months=1), periods=forecast_steps, freq='M')
forecast_df = pd.DataFrame({'SARIMA_Forecast': forecast}, index=forecast_index)

# Step 5: Evaluation
mae = mean_absolute_error(y, df['LR_Predicted'])
rmse = np.sqrt(mean_squared_error(y, df['LR_Predicted']))
r2 = r2_score(y, df['LR_Predicted'])

# Step 6: Plotting
plt.figure(figsize=(12, 6))
plt.plot(df['Sales'], label='Actual Sales', linewidth=2)
plt.plot(df['LR_Predicted'], label='Linear Regression Prediction', linestyle='--')
plt.plot(forecast_df['SARIMA_Forecast'], label='SARIMA Forecast (Next 12 Months)', linestyle='--', color='orange')
plt.title('Predictive Sales Analysis with SARIMA')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Step 7: Output results
print("📊 Linear Regression Evaluation Metrics:")
print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.2f}")

print("\n📈 SARIMA Forecast (Next 12 Months):")
print(forecast_df)

