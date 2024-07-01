import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import numpy as np


class StockPrediction():

    def __init__(self):
        self.START = "2000-01-01"
        self.TODAY = date.today().strftime("%Y-%m-%d")

    def load_data(self, ticker):
        try:
            data = yf.download(ticker, self.START, self.TODAY)
        except Exception as e:
            st.error(f"Error: {e}")
            return None
        return data

    def plot_raw_data(self, data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data["Open"], name="stock_open"))
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="stock_close"))
        fig.update_layout(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    def forecast_data(self, data, period, m):
        df_train = data[["Close"]].reset_index().rename(columns={"Date": "ds", "Close": "y"})
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        return forecast

    def accuracy_data(self, data, forecast):
        actual = data['Close']
        predicted = forecast['yhat'].values
        actual = np.array(actual)
        predicted = np.array(predicted)
        predicted = predicted[:len(actual)]
        accuracy = np.mean(np.abs((actual - predicted) / actual)) * 100
        return accuracy

    def start_app(self):
        st.title("Analysis")
        selected_stock = st.text_input("Stock")

        if selected_stock:
            n_years = st.slider("Years of prediction:", 1, 4)
            period = n_years * 365
            data_load_state = st.text("Loading data...")
            data = self.load_data(selected_stock)

            if data is not None:
                data_load_state.text("Done")
                m = Prophet()
                forecast = self.forecast_data(data, period, m)
                
                if forecast is not None:
                    st.subheader("Model Accuracy")
                    accuracy = self.accuracy_data(data, forecast)
                    st.write(f"Accuracy: {100-accuracy:.2f}%")

                    st.subheader("Raw data")
                    st.write(data.tail())
                    self.plot_raw_data(data)

                    st.subheader("Forecast Data")
                    st.write(forecast.tail())

                    st.subheader("Forecast Plot")
                    fig1 = plot_plotly(m, forecast)
                    st.plotly_chart(fig1)
                else:
                    st.warning("Forecasting failed.")
            else:
                st.warning("Please enter a valid stock symbol.")


def main():
    predictor = StockPrediction()
    predictor.start_app()

if __name__ == "__main__":
    main()