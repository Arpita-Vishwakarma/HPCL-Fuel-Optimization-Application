# from flask import Flask, render_template, request, jsonify, send_file
# import pandas as pd
# from datetime import datetime, timedelta

# app = Flask(__name__)

# # Load the dataset
# df = pd.read_excel('merged_sales_data_with_distance_time.xlsx')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Perform prediction for all customers and locations
#     predictions = []
#     for customer in df['Customer'].unique():
#         for location in df['terminal_locations'].unique():
#             prediction = predict_sales(customer, location)
#             predictions.append(prediction)
    
#     # Concatenate all predictions into a single DataFrame
#     all_predictions = pd.concat(predictions, ignore_index=True)
    
#     # Define filename for the Excel file
#     excel_filename = 'sales_predictions.xlsx'
    
#     # Write the Excel file to disk
#     all_predictions.to_excel(excel_filename, index=False)
    
#     return render_template('prediction.html', excel_filename=excel_filename)

# def predict_sales(customer, location):
#     # Placeholder function for prediction
#     # You'll need to implement your own prediction logic here
#     # This is just a dummy example
#     future_dates = [datetime.now() + timedelta(days=i) for i in range(90)]
#     future_sales = [1000 + i*10 for i in range(90)]
#     prediction = pd.DataFrame({'Date': future_dates, 'Customer': customer, 'Location': location, 'Sales': future_sales})
#     return prediction



# @app.route('/download/<filename>')
# def download(filename):
#     return send_file(filename, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, render_template, request, jsonify, send_file
# import pandas as pd
# from datetime import datetime, timedelta
# from arima_model import ARIMAModel

# app = Flask(__name__)

# # Load the dataset
# df = pd.read_excel('merged_sales_data_with_distance_time.xlsx')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Create ARIMAModel instance
#         arima_model = ARIMAModel("past_fuel_demand_data.xlsx")

#         # Save predictions to Excel
#         excel_filename = arima_model.save_predictions_to_excel()

#         if excel_filename:
#             return render_template('prediction.html', excel_filename=excel_filename)
#         else:
#             return render_template('error.html', message="Failed to generate predictions.")
#     except Exception as e:
#         return render_template('error.html', message=str(e))

# @app.route('/download/<filename>')
# def download(filename):
#     return send_file(filename, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, render_template, request, send_file
import pandas as pd
from model.arima_model import ARIMAModel

app = Flask(__name__)

# Load the dataset
df = pd.read_excel('merged_sales_data_with_distance_time.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        # Create ARIMAModel instance
        arima_model = ARIMAModel("past_fuel_demand_data.xlsx")

        # Save predictions to Excel
        excel_filename = arima_model.save_predictions_to_excel()

        if excel_filename:
            return render_template('prediction.html', excel_filename=excel_filename)
        else:
            return render_template('error.html', message="Failed to generate predictions.")
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)