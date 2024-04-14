import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import pickle
import os.path


class ARIMAModel:
    def __init__(self, data_file):
        self.data_file = data_file
        self.model_filename = "future_fuel_demand_arima_model.pkl"

    def train_models(self):
        try:
            data = pd.read_excel(self.data_file)
            data['date'] = pd.to_datetime(data['date'])
            ms_model = ARIMA(data['MS Indent (KL)'], order=(5, 1, 0))
            hsd_model = ARIMA(data['HSD Indent (KL)'], order=(5, 1, 0))
            ms_model_fit = ms_model.fit()
            hsd_model_fit = hsd_model.fit()
            with open(self.model_filename, 'wb') as f:
                pickle.dump((ms_model_fit, hsd_model_fit), f)
        except Exception as e:
            print("An error occurred during model training:", str(e))

    def load_or_train_models(self):
        try:
            if os.path.exists(self.model_filename):
                with open(self.model_filename, 'rb') as f:
                    ms_model_fit, hsd_model_fit = pickle.load(f)
            else:
                self.train_models()
                with open(self.model_filename, 'rb') as f:
                    ms_model_fit, hsd_model_fit = pickle.load(f)
            return ms_model_fit, hsd_model_fit
        except Exception as e:
            print("An error occurred during model loading/training:", str(e))
            return None, None

    def predict_sales(self):
        try:
            ms_model_fit, hsd_model_fit = self.load_or_train_models()
            if ms_model_fit is None or hsd_model_fit is None:
                return {}
            data = pd.read_excel(self.data_file)
            data['date'] = pd.to_datetime(data['date'])
            predicted_sales = {}
            for (customer, terminal), terminal_data in data.groupby(['Customer', 'terminal_locations']):
                ms_forecast = ms_model_fit.forecast(steps=30)
                hsd_forecast = hsd_model_fit.forecast(steps=30)
                predicted_sales[(customer, terminal)] = {'MS Indent (KL)': ms_forecast, 'HSD Indent (KL)': hsd_forecast}
            return predicted_sales
        except Exception as e:
            print("An error occurred during sales prediction:", str(e))
            return {}

    def save_predictions_to_excel(self):
        try:
            excel_filename = "predicted_sales_per_customer_per_terminal.xlsx"
            if os.path.exists(excel_filename):
                return excel_filename
            predicted_sales = self.predict_sales()
            if not predicted_sales:
                print("No predictions available to save.")
                return None
            predicted_df_list = []
            date_range = [datetime.today() + timedelta(days=i) for i in range(30)]
            for (customer, terminal), values in predicted_sales.items():
                ms_forecast = values['MS Indent (KL)']
                hsd_forecast = values['HSD Indent (KL)']
                for i, (ms_value, hsd_value) in enumerate(zip(ms_forecast, hsd_forecast)):
                    date = date_range[i]
                    predicted_total = ms_value + hsd_value
                    predicted_df_list.append({'date': date, 'Customer': customer, 'MS Indent (KL)': ms_value,
                                              'HSD Indent (KL)': hsd_value, 'Total Indent (KL)': predicted_total,
                                              'terminal_locations': terminal})
            predicted_df = pd.DataFrame(predicted_df_list)
            excel_filename = "predicted_sales_per_customer_per_terminal.xlsx"
            predicted_df.to_excel(excel_filename, index=False)
            return excel_filename
        except Exception as e:
            print("An error occurred while saving predictions to Excel:", str(e))
            return None
