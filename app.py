import dash
from dash import dcc, html, Output, Input
import pandas as pd
import plotly.express as px

# Load the processed sales data
data_file_path = 'output/processed_sales_data.csv'
sales_data = pd.read_csv(data_file_path)

# Convert 'date' to datetime format for proper sorting and filtering
sales_data['date'] = pd.to_datetime(sales_data['date'])

# sort data by date
sales_data = sales_data.sort_values('date')

# Get unique regions from the sales data
regions = sales_data['region'].unique()


# Create a Dash app
app = dash.Dash(__name__)

# Create a line chart using Plotly Express
def create_line_chart(data):
    line_chart = px.line(data, x='date', y='sales', title='Sales Over Time',
                labels={'sales': 'Sales ($)', 'date': 'Date'})

    # Convert the price increase date to datetime
    price_increase_date = pd.to_datetime('2021-01-15')

    # Add a shape for the vertical line
    line_chart.add_shape(type='line',
                x0=price_increase_date,
                x1=price_increase_date,
                y0=data['sales'].min(),
                y1=data['sales'].max(),
                line=dict(color='blue', dash='dash'))

    # Update layout for annotation
    line_chart.add_annotation(x=price_increase_date,
                    y=data['sales'].max() * 0.9, 
                    text='Price Increase',
                    showarrow=True,
                    arrowhead=2,
                    font=dict(size=14, weight='bold') )
    
    line_chart.update_traces(line_color='#f0467e')
    line_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Removes background of the plot
    paper_bgcolor='rgba(0,0,0,0)',  xaxis=dict(
        showgrid=True, 
        gridcolor='rgba(148, 148, 148, 0.699)',  
    ),
    yaxis=dict(
        showgrid=True,  
        gridcolor='rgba(148, 148, 148, 0.699)',  
    ),)
    return line_chart

# Create a dcc gragh with the line chart
visualizer = dcc.Graph(id="sales-graph", figure=create_line_chart(sales_data))

# Create a header
header = html.H2("Pink Morsel Sales Data Visualizer", id="header", className="header")

 
# Create radio button options dynamically
radio_buttons = dcc.RadioItems(
    id='region-selector',

    # Dictionary comprehension to create options from unique regions
   options=[{'label': region.capitalize(), 'value': region} for region in regions] + 
            [{'label': 'All', 'value': 'all'}],  # Add 'All' option manually

    value='all',  # Default selection is 'all'
    labelStyle={'display': 'inline-block', 'margin-right': '20px'},
    className='radio-items'
)

# Layout of the Dash app
app.layout = html.Div([
    header,
    radio_buttons,
    html.Br(),  # Add a line break for better readability
    visualizer
])

# Callback to update the line chart based on region selection
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('region-selector', 'value')]
)
def update_graph(selected_region):
    # Filter data based on the selected region
    if selected_region == 'all':
        filtered_data = sales_data
    else:
        filtered_data = sales_data[sales_data['region'] == selected_region]
    
    # Create a new line chart with the filtered data
    updated_line_chart = create_line_chart(filtered_data)
    return updated_line_chart
    






# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

