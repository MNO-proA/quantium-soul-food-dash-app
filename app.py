import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the processed sales data
data_file_path = 'output/processed_sales_data.csv'
sales_data = pd.read_csv(data_file_path)

# Convert 'date' to datetime format for proper sorting and filtering
sales_data['date'] = pd.to_datetime(sales_data['date'])

# sort data by date
sales_data = sales_data.sort_values('date')

# Create a Dash app
app = dash.Dash(__name__)

# Create a line chart using Plotly Express
line_chart = px.line(sales_data, x='date', y='sales', title='Sales Over Time',
              labels={'sales': 'Sales ($)', 'date': 'Date'})

# Convert the price increase date to datetime
price_increase_date = pd.to_datetime('2021-01-15')

# Add a shape for the vertical line
line_chart.add_shape(type='line',
              x0=price_increase_date,
              x1=price_increase_date,
              y0=sales_data['sales'].min(),
              y1=sales_data['sales'].max(),
              line=dict(color='red', dash='dash'))

# Update layout for annotation
line_chart.add_annotation(x=price_increase_date,
                   y=sales_data['sales'].max() * 0.9, 
                   text='Price Increase',
                   showarrow=True,
                   arrowhead=2,
                   font=dict(size=14, weight='bold') )

# Create a dcc gragh with the line chart
visualizer = dcc.Graph(id="visualizer", figure=line_chart)

# Create a header
header = html.H2("Pink Morsel Visualizer", id="header")


# Layout of the Dash app
app.layout = html.Div([
    header,
    visualizer
])
    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

