from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# import data
df = pd.read_csv(r'C:\Users\Admin\Desktop\Projelerim\Cars\cars_EDA.csv')

# Initialize the app
app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#FFFFFF'  
}


# adjust the layout of the dashboard
app.layout = html.Div(
    [
        ###################################### Brand and column radioitems settings ######################
        html.Div( 
            [
                html.H1("Car dataset Outlier Check", style={'color': colors['text'], 'textAlign': 'center'}),
            ],
            style={'backgroundColor': colors['background'], 'padding': '20px', 'marginBottom': '20px'}
        ),
        ###################################### Brand and column radioitems settings ######################
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Marke", style={'color': colors['text'], 'margin-bottom': '10px'}),
                        dcc.RadioItems(
                            options=[{'label': brand, 'value': brand} for brand in df.Brand.unique()],
                            value='Audi',
                            id='brand-dropdown',
                            labelStyle={'display': 'block', 'color': colors['text'], 'margin-bottom': '10px'}
                        ),
                        html.H3("Spalten", style={'color': colors['text'], 'margin-top': '20px'}),
                        dcc.RadioItems(
                            options=[
                                {'label': 'Price', 'value': 'Price'},
                                {'label': 'Kilometer', 'value': 'km'},
                                {'label': 'Kilowatts', 'value': 'kw'}
                            ],
                            value='Price',
                            id='column-dropdown',
                            labelStyle={'display': 'block', 'color': colors['text'], 'margin-bottom': '10px'}
                        ),
                    ],
                    style={'width': '20%', 'padding': '10px', 'float': 'left'}  
                ),
                ###################################### Graphic positions ##################################
                # boxplot position
                html.Div(
                    [
                        dcc.Graph(figure={}, id='brand-column-graph', config={'displayModeBar': False}),
                    ],
                    style={'width': '80%', 'padding': '10px'}
                )
            ],
            style={'display': 'flex'}
        ),
        # Barchart and Pie chart position
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(figure={}, id='model-bar-chart', config={'displayModeBar': False}),
                    ],
                    style={'width': '50%', 'padding': '10px', 'float': 'left'}
                ),
                html.Div(
                    [
                        dcc.Graph(id='model-pie-graph', config={'displayModeBar': False}),
                    ],
                    style={'width': '50%', 'padding': '10px', 'float': 'right'}
                )
            ],
            style={'display': 'flex'}
        )
    ],
    style={'backgroundColor': colors['background']}
)

###################################### Graphic positions ##################################
# Add controls to build the interaction
@app.callback(
    Output(component_id='brand-column-graph', component_property='figure'),
    Input(component_id='brand-dropdown', component_property='value'),
    Input(component_id='column-dropdown', component_property='value')
)
def update_graph(brand_chosen, column_chosen):
    filtered_df = df[df['Brand'] == brand_chosen]
    fig = px.box(filtered_df, x='Model', y=column_chosen)
    fig.update_layout(template="plotly_dark")
    return fig


@app.callback(
    Output(component_id='model-pie-graph', component_property='figure'),
    Input(component_id='brand-dropdown', component_property='value')
)
def update_pie(brand_chosen):
    brand_counts = df['Brand'].value_counts()

    fig = px.pie(
        values=brand_counts.values,
        names=brand_counts.index,
        title=f"Marke - {brand_chosen}",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(template="plotly_dark")

    return fig

@app.callback(
    Output(component_id='model-bar-chart', component_property='figure'),
    Input(component_id='brand-dropdown', component_property='value')
)
def update_bar_chart(brand_chosen):
    if brand_chosen:
        filtered_df = df[df['Brand'] == brand_chosen]
        model_counts = filtered_df['Model'].value_counts()

        fig = px.bar(filtered_df, x=model_counts.index, y=model_counts.values, color=model_counts.index)
        fig.update_xaxes(title_text="Modelle")  # x ekseni etiketi
        fig.update_yaxes(title_text="Anzahl") 
        fig.update_layout(template = "plotly_dark")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
