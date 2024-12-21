import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv("heart.csv")

# Data preprocessing
categorical_columns = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
for col in categorical_columns:
    data[col] = data[col].astype('category')
data['Cholesterol'] = data['Cholesterol'].replace(0, data['Cholesterol'].median())
data['RestingBP'] = data['RestingBP'].replace(0, data['RestingBP'].median())
numerical_columns = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']

# Initialize the Dash app with dark theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Heart Disease Data Analysis - Dark Theme"

# Layout
def create_card(title, value, icon):
    return dbc.Card(
        dbc.CardBody([ 
            html.H5(title, className="card-title text-light"),
            html.H3(value, className="card-text text-primary"),
            html.I(className=f"bi {icon} text-secondary", style={"fontSize": "2rem"})
        ]),
        className="shadow-sm"
    )

app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("About", href="#")),
            dbc.NavItem(dbc.NavLink("Contact", href="#"))
        ],
        brand="Heart Disease Data Analysis",  # Changed this line to match your requested title
        brand_href="#",
        color="dark",
        dark=True
    ),

    dbc.Row([
        dbc.Col(create_card("Total Records", len(data), "bi-people"), width=4),
        dbc.Col(create_card("Average Age", f"{data['Age'].mean():.1f}", "bi-calendar"), width=4),
        dbc.Col(create_card("Heart Disease Cases", data['HeartDisease'].sum(), "bi-heart"), width=4)
    ], className="my-4"),

    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Select Feature for Analysis:", className="text-light"),
                dcc.Dropdown(
                    id="feature-dropdown",
                    options=[{'label': col, 'value': col} for col in numerical_columns],
                    value="Age",
                    clearable=False
                ),
                dbc.Label("Filter by Gender:", className="text-light"),
                dcc.RadioItems(
                    id="gender-filter",
                    options=[
                        {'label': "All", 'value': "all"},
                        {'label': "Male", 'value': "M"},
                        {'label': "Female", 'value': "F"}
                    ],
                    value="all",
                    inline=True
                )
            ], className="p-3 bg-dark text-light rounded shadow-sm")
        ], width=3),

        dbc.Col([
            dbc.Tabs([
                dbc.Tab(dcc.Graph(id="line-chart"), label="Line Chart"),
                dbc.Tab(dcc.Graph(id="bar-chart"), label="Bar Chart"),
                dbc.Tab(dcc.Graph(id="pie-chart"), label="Pie Chart"),
                dbc.Tab(dcc.Graph(id="box-plot"), label="Box Plot")
            ])
        ], width=9)
    ])
], fluid=True)

# Callbacks
@app.callback(
    [
        Output("line-chart", "figure"),
        Output("bar-chart", "figure"),
        Output("pie-chart", "figure"),
        Output("box-plot", "figure")
    ],
    [
        Input("feature-dropdown", "value"),
        Input("gender-filter", "value")
    ]
)
def update_charts(selected_feature, gender_filter):
    filtered_data = data.copy()
    if gender_filter != "all":
        filtered_data = filtered_data[filtered_data["Sex"] == gender_filter]

    # Line Chart
    line_fig = px.line(
        filtered_data, x="Age", y=selected_feature, color="HeartDisease",
        title="Line Chart of Age vs. Feature", 
        hover_data=["Age", selected_feature, "HeartDisease"]
    )

    # Bar Chart
    bar_fig = px.bar(
        filtered_data, x="HeartDisease", y=selected_feature, color="Sex",
        title="Bar Chart of Feature by Gender and Heart Disease",
        hover_data=["HeartDisease", selected_feature]
    )

    # Pie Chart
    pie_fig = px.pie(
        filtered_data, names="HeartDisease",
        title="Distribution of Heart Disease", 
        hover_data=["HeartDisease"]
    )

    # Box Plot
    box_fig = px.box(
        filtered_data, x="HeartDisease", y=selected_feature, color="HeartDisease",
        title="Box Plot of Feature by Heart Disease", 
        hover_data=["HeartDisease", selected_feature]
    )

    return line_fig, bar_fig, pie_fig, box_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
