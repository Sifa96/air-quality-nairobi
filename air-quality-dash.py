# import necessary packages
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# import data
sensor_data = pd.read_csv(r'C:\Users\admin\Downloads\sensor_data.csv',low_memory=False)

#mapbox token
token = 'pk.eyJ1Ijoic2lmYWtpbm90aSIsImEiOiJjbDVzN2xpeTUwMmd1M2NzM2ZqZXJ1eWxsIn0.kVmfzNVq0ZJWQ3QeAU4d2A' 

# define dash app
app = Dash(__name__)

# filter location(s) and show line graph filtered by time
# slider for date
# checkbox for location
# checkbox for pm, temp, humidity
# line_location = px.line(sensor_data, x='date', y='value', color='location')

# filter location to show bar graph comparison of day, time, month
# dropdown for time/ month/ day
# checkbox for location
# checkbox for pm, temp, humidity
# bar_time = px.bar(sensor_data, x="time", y="value", color="time", barmode="group") # add location filter
# bar_month = px.bar(sensor_data, x="month", y="value", color="City", barmode="group") # add location filter
# bar_day = px.bar(sensor_data, x="day", y="value", color="City", barmode="group") # add location filter

# map the average of chosen time in all locations
# date picker
# checkbox for pm, temp, humidity
# choropleth map

# add bucket to visualization

# add lstm model

app.layout = html.Div([
    html.Div([
        html.H1('Nairobi Air Quality Monitor (Nov 2021 - Nov 2022)'),
        html.Div([
            dcc.Markdown('''
                        This dashboard is developed to analyse the PM 1, PM2.5, PM10, humidity and temperature values.
                        The values are recorded by Sensors Africa between November 2021 and November 2022.
                        '''),
                       
            html.P('Select the time you want to analyze'),
            dcc.Dropdown(
                sensor_data['time'].unique(),
                'time_of_day',
                id='time_of_day'
            ),
                    
            html.P('Select the day you want to analyze'),
            dcc.Dropdown(
                sensor_data['day'].unique(),
                'day_of_week',
                id='day_of_week'
            ),

            html.P('Select the value type you want to analyze'),
            dcc.Dropdown(
                sensor_data['value_type'].unique(),
                'value_type',
                id='value_type'
            ),
                    
            html.P('Select the location you want to analyze'),
            dcc.Checklist(
                sensor_data['location'].unique(),
                'location',
                id='location'
            ),
                    
            html.P('Pick a date range'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=sensor_data['timestamp'].min(),
                end_date=sensor_data['timestamp'].max()
            ),
            
            html.H6('Line graph showing trend of values over time'),
            dcc.Graph(id = 'line_values'),
            html.H6('Bar graph of values in different times'),
            dcc.Graph(id = 'bar_times'),
            html.H6('Choropleth map showing intensity of values in different locations'),
            dcc.Graph(id = 'choropleth'),
            ])
        ])
])

@app.callback(
    Output('line_values', 'figure'),
    Output('bar_times', 'figure'),
    Output('day_of_week', 'figure'),
    Input('time_of_day', 'value'),
    Input('value_type', 'value'),
    Input('location', 'value'),
    Input('date-picker-range', 'value')
    )

def line_graph(value_type, location):
    fig = px.scatter(x=sensor_data['value'],
                     y=sensor_data['timestamp'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    # fig.update_xaxes(title=xaxis_column_name,
    #                  type='linear' if xaxis_type == 'Linear' else 'log')

    # fig.update_yaxes(title=yaxis_column_name,
    #                  type='linear' if yaxis_type == 'Linear' else 'log')

    return line_graph

def time_graph(value_type, location):

    time_graph = px.scatter(x= sensor_data['value'],
                     y=time_of_day)

    time_graph.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    # bar_graph.update_xaxes(title=xaxis_column_name,
    #                  type='linear' if xaxis_type == 'Linear' else 'log')

    # bar_graph.update_yaxes(title=yaxis_column_name,
    #                  type='linear' if yaxis_type == 'Linear' else 'log')

    return time_graph

def day_graph(value_type, location):

    day_graph = px.scatter(x= sensor_data['value'],
                     y=day_of_week)

    day_graph.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    # bar_graph.update_xaxes(title=xaxis_column_name,
    #                  type='linear' if xaxis_type == 'Linear' else 'log')

    # bar_graph.update_yaxes(title=yaxis_column_name,
    #                  type='linear' if yaxis_type == 'Linear' else 'log')

    return day_graph

def chorpleth_graph(value_type):
    choro_graph = px.choropleth_mapbox(
        sensor_data, 
        color=location,
        locations=location, 
        # featureidkey="properties.district",
        # center={"lat": 45.5517, "lon": -73.7073}, 
        zoom=9)
        # range_color=[0, 6500])
    choro_graph.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken=token)
    return choro_graph

### load ML model ###########################################
# with open('xgb_model_iris.pickle', 'rb') as f:
#     clf = pickle.load(f)
### Callback to produce the prediction ######################### 
# @app.callback(
#     Output('prediction output', 'children'),
#     Input('submit-val', 'n_clicks'),
#     State('sepal_length', 'value'),
#     State('sepal_width', 'value'),
#     State('petal_length', 'value'), 
#     State('petal_width', 'value')
# )
   
# def update_output(n_clicks, sepal_length, sepal_width, petal_length, petal_width):    
#     x = np.array([[float(sepal_length), float(sepal_width), float(petal_length), float(petal_width)]])
#     prediction = clf.predict(x)[0]
#     if prediction == 0:
#         output = 'Iris-Setosa'
#     elif prediction == 1:
#         output = 'Iris-Versicolor'
#     else:
#         output = 'Iris-Virginica'
#     return f'The predicted Iris species is {output}.'

if __name__ == '__main__':
    app.run_server(debug=True)

