# import necessary packages
import dash
from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd
# from keras.models import load_model

# import data
sensor_data = pd.read_csv(r'E:\Users\admin\air-quality-project\sensor_data.csv',low_memory=False)

# convert timestamp column to datetime
pd.to_datetime(sensor_data['timestamp'])

# load model
# model = load_model('your_model.h5')

#mapbox token
token = 'pk.eyJ1Ijoic2lmYWtpbm90aSIsImEiOiJjbDVzN2xpeTUwMmd1M2NzM2ZqZXJ1eWxsIn0.kVmfzNVq0ZJWQ3QeAU4d2A' 

# define dash app
app = Dash(__name__)

# add lstm model
# add state, input button and output for def prediction

app.layout = html.Div([
    html.Div([
        html.H1('Nairobi Air Quality Monitor (Nov 2021 - Nov 2022)'),
        html.Div([
            dcc.Markdown('''
                        This dashboard is developed to analyse the PM 1, PM2.5, PM10, humidity and temperature values.
                        The values are recorded by Sensors Africa between November 2021 and November 2022.
                        '''),
            
            html.P('Select the location you want to analyze'),
            dcc.Checklist(
                options = [{'label':str(i), 'value':i} for i in sorted(sensor_data['location'].unique())],
                value = [i for i in sorted(sensor_data['location'].unique())],
                id='location'),
            
            html.P('Select the value type you want to analyze'),
            dcc.Dropdown(
                options = [{'label':str(j), 'value':j} for j in sorted(sensor_data['value_type'].unique())],
                value=[j for j in sorted(sensor_data['value_type'].unique())],
                multi=True,
                id='value_type'
            ), 
            # UNCOMMENT LATER
            # html.P('Select the time you want to analyze'),
            # dcc.Dropdown(
                # options= [{'label':str(a), 'value':a} for a in sorted(sensor_data['time'].unique())],
                # value = [a for a in sorted(sensor_data['time'].unique())],
                # id='time_of_day'
            # ),
                        #   UNCOMMENT LATER
            html.Label('Map showing intensity of values in different locations'),
            dcc.Graph(id = 'map_values', figure = {}),
                    
            # html.P('Select the day you want to analyze'),
            # dcc.Dropdown(
            #     options = [{'label':str(b), 'value':b} for b in sorted(sensor_data['day'].unique())],
            #     value = [b for b in sorted(sensor_data['day'].unique())],
            #     id='day_of_week'
            # ),
                    
            html.P('Pick a date'),
            dcc.DatePickerSingle(
                id='date_picker_single',
                min_date_allowed=sensor_data['timestamp'].min(),
                max_date_allowed=sensor_data['timestamp'].max()
            ),
            
            # html.H4('Line graph showing trend of values over time'),
            # dcc.Graph(id = 'line_values', figure = {}),
            # html.H4('Bar graph of values in different times'),
            # dcc.Graph(id = 'bar_times', figure = {}),
            # html.H4('Bar graph of values in different days'),
            # dcc.Graph(id = 'bar_days', figure = {}),
            ])
        ])
])

# UNCOMMENT LATER
# graph of intensity of values per location
@app.callback(
    Output('map_values', 'figure'),
    [Input('location', 'value'),
    Input('value_type', 'value'),               
    Input('date_picker_single', 'date')])

def update_mapbox(chosen_location, chosen_value_type, chosen_date):
    data_map = sensor_data[(sensor_data['location'].isin(chosen_location))&
                           (sensor_data['value_type'].isin(chosen_value_type))&
                           (sensor_data['timestamp']==(chosen_date))]
    map_graph = [go.Scattermapbox(
        lon = sensor_data['lon'],
        lat = sensor_data['lat'],
        marker=go.scattermapbox.Marker(
                    size=(sensor_data['value'].mean()),
                    color=sensor_data['location']
                ),
        hovertext=sensor_data['location']
        )]
    
    return{
        'data': map_graph,
        'layout': go.Layout(
            uirevision='foo',
            mapbox=dict(
                accesstoken=token,
                zoom=10
            )

        )
    }
    
    # IS OK CAN UNCOMMENT
# # line graph of values against time for specific location and value type
# @app.callback(Output('line_values', 'figure'),
#               [Input('location', 'value'),
#                Input('value_type', 'value'),
#                Input('date_picker_single', 'date')])


# def update_line_graph(chosen_location, chosen_value_type, chosen_date):
#     data_line = sensor_data[(sensor_data['location'].isin(chosen_location))&
#                            (sensor_data['value_type'].isin(chosen_value_type))&
#                            (sensor_data['timestamp']==(chosen_date))]
#     line_g = px.line(data_line, x=sensor_data['timestamp'], y=sensor_data['value'], color=sensor_data['location'], title='Timeseries')
#     return line_g

# UNCOMMENT LATER
# # bar graph of times of day vs pollution value for specific location, value type and date
# @app.callback(Output('bar_times', 'figure'),
#               [Input('location', 'value'),
#                Input('value_type', 'value'),
#                Input('date_picker_single', 'date')])

# def update_time_graph(chosen_location, chosen_value_type, chosen_date):
#     data_time = sensor_data[(sensor_data['location'].isin(chosen_location))&
#                            (sensor_data['value_type'].isin(chosen_value_type))&
#                            (sensor_data['timestamp']==(chosen_date))]
#     time_g = px.bar(data_time, x=sensor_data['time'], y=sensor_data['value'],color=sensor_data['location'], title="Bar Graph of time of day vs value")
#     return time_g

# CAN BE DELETED
# # bar graph of average pollution on day of week
# @app.callback(Output('bar_days', 'figure'),
#               [Input('location', 'value'),
#                Input('value_type', 'value'),
#                Input('date_picker_single', 'date')])

# def update_day_graph(chosen_location, chosen_value_type, chosen_date):
#     data_day = sensor_data[(sensor_data['location'].isin(chosen_location))&
#                            (sensor_data['value_type'].isin(chosen_value_type))&
#                            (sensor_data[(sensor_data['timestamp'] == chosen_date)])]    
#     day_g = px.bar(data_day, x=data_day['day'], y=data_day['value'], title="Bar Graph of day vs value")
#     return day_g

### load ML model ###########################################
# app.layout = html.Div([
#     dcc.Graph(id='live-update-graph'),
#     dcc.Interval(
#         id='interval-component',
#         interval=1 * 1000,  # Update every second (adjust as needed)
#         n_intervals=0
#     )
# ])
   
# @app.callback(dash.dependencies.Output('live-update-graph', 'figure'),
#               [dash.dependencies.Input('interval-component', 'n_intervals')])
# def update_graph(n):
#     # Generate or load new data for prediction
#     # Perform any preprocessing necessary
#     # Make predictions using your LSTM model
#     # Here's a placeholder example:
#     data = np.random.rand(100)  # Replace with your actual data
#     predictions = model.predict(data)

#     # Create a Plotly figure
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=np.arange(len(data)), y=data, name='Data'))
#     fig.add_trace(go.Scatter(x=np.arange(len(predictions)), y=predictions[:, 0], name='Predictions'))

#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# '''