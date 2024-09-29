# Import necessary libraries
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# Load the SpaceX launch data
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# TASK 1: Add a Launch Site Drop-down Input Component
launch_sites = spacex_df['Launch Site'].unique()

# Create the dropdown options, including the "All Sites" option
options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Define the layout for the Dash app
app.layout = html.Div(children=[
    # Heading for the app
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Dropdown for Launch Site selection (Task 1)
    dcc.Dropdown(
        id='site-dropdown',
        options=options,  # List of launch site options, including 'All Sites'
        value='ALL',  # Default value is 'ALL', meaning all sites
        placeholder="Select a Launch Site here",  # Placeholder text
        searchable=True  # Enable the search functionality in the dropdown
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Heading for the payload range slider
    html.P("Payload range (Kg):"),

    # TASK 3: Add a range slider to select payload mass (kg)
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Add a scatter chart to show correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function to render the success-pie-chart based on selected site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success Launches for site {selected_site}')
    
    return fig

# TASK 4: Add a callback function to render the success-payload-scatter-chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {selected_site}')
    
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
