from django_plotly_dash import DjangoDash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

data = {
    'Date': pd.date_range(start='2024-01-01', periods=7).tolist() * 2,
    'Machine': ['Machine A'] * 7 + ['Machine B'] * 7,
    'Production': [150, 160, 145, 170, 180, 165, 175, 120, 130, 125, 140, 135, 150, 145]
}
df = pd.DataFrame(data)

app = DjangoDash('ProductionDashboard')

app.layout = html.Div([
    html.H1("Production Dashboard", style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}),
    
    html.Div([
        html.Label("Select Machine:", style={'fontFamily': 'Arial, sans-serif'}),
        dcc.Dropdown(
            id='machine-dropdown',
            options=[
                {'label': 'Machine A', 'value': 'Machine A'},
                {'label': 'Machine B', 'value': 'Machine B'},
                {'label': 'All Machines', 'value': 'All'}
            ],
            value='Machine A', # Default value
            clearable=False,
            style={'width': '300px', 'marginTop': '10px'}
        )
    ], style={'padding': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    
    html.Div([
        dcc.Graph(id='production-graph')
    ], style={'width': '80%', 'margin': '0 auto'})
])

@app.callback(
    Output('production-graph', 'figure'),
    [Input('machine-dropdown', 'value')]
)
def update_graph(selected_machine):
    if selected_machine == 'All':
        filtered_df = df
        title = 'Production Over Time: All Machines'
        color = 'Machine'
    else:
        filtered_df = df[df['Machine'] == selected_machine]
        title = f'Production Over Time: {selected_machine}'
        color = None
    
    fig = px.line(
        filtered_df, 
        x='Date', 
        y='Production',
        color=color,
        title=title,
        markers=True,
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Units Produced",
        template="plotly_white",
        title_x=0.5,
        hovermode="x unified",
        legend_title_text='Machine Type'
    )
    
    return fig
