from django_plotly_dash import DjangoDash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from inventory.models import Part

app = DjangoDash('ProductionDashboard')

app.layout = html.Div([
    html.H1("Parts Inventory Dashboard", style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}),
    
    html.Div([
        html.Label("Filter by Status:", style={'fontFamily': 'Arial, sans-serif'}),
        dcc.Dropdown(
            id='status-dropdown',
            options=[
                {'label': 'All Parts', 'value': 'All'},
                {'label': 'In Stock', 'value': 'In Stock'},
                {'label': 'Low', 'value': 'Low'}
            ],
            value='All',
            clearable=False,
            style={'width': '300px', 'marginTop': '10px'}
        )
    ], style={'padding': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    
    html.Div([
        dcc.Graph(id='inventory-graph')
    ], style={'width': '80%', 'margin': '0 auto'})
])

@app.callback(
    Output('inventory-graph', 'figure'),
    [Input('status-dropdown', 'value')]
)
def update_graph(selected_status):
    # Fetch real data inside callback so it's always up-to-date
    part_query = Part.objects.all().values('name', 'quantity', 'status')
    
    # Convert queryset to Pandas DataFrame
    df = pd.DataFrame(list(part_query))
    
    # Handle empty database scenario
    if df.empty:
        df = pd.DataFrame(columns=['name', 'quantity', 'status'])
        
    # Filter by user dropdown selection
    if selected_status != 'All' and not df.empty:
        filtered_df = df[df['status'] == selected_status]
        title = f'Inventory Quantities: {selected_status}'
    else:
        filtered_df = df
        title = 'Inventory Quantities: All Parts'
        
    # Create Bar Chart instead of Line Chart (more appropriate for inventory)
    fig = px.bar(
        filtered_df, 
        x='name', 
        y='quantity',
        color='status' if not df.empty else None,
        title=title,
    )
    
    fig.update_layout(
        xaxis_title="Part Name",
        yaxis_title="Quantity",
        template="plotly_white",
        title_x=0.5,
        hovermode="x unified"
    )
    
    return fig
