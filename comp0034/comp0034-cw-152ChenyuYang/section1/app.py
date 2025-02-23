import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import sqlite3
import pandas as pd
import os

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SQLite database path
db_path = os.path.join(
    BASE_DIR, "..", "data0035", "coursework1", "database", "local_authority_housing.db"
)

# CSV latitude and longitude file path
geo_path = os.path.join(BASE_DIR, "geo_locations.csv")

# **Make sure geo_locations.csv exists**
if not os.path.exists(geo_path):
    raise FileNotFoundError(f" File not found: {geo_path}")


# **Read database data**
def load_data():
    with sqlite3.connect(db_path) as conn:
        df_housing = pd.read_sql_query("SELECT * FROM Affordable_Housing_Data", conn)
        df_waiting = pd.read_sql_query("SELECT * FROM Waiting_List_Data", conn)

    df_housing["year"] = df_housing["year"].astype(int)
    df_waiting["year"] = df_waiting["year"].astype(int)

    return df_housing, df_waiting


df_housing, df_waiting = load_data()

# **Read longitude and latitude data**
df_geo = pd.read_csv(geo_path)

# **COMBINING HOUSING DATA AND LATITUDE AND LONGITUDE DATA**
df_housing = df_housing.merge(df_geo, on="area_code", how="left")

# **Using Bootstrap Themes**
external_stylesheets = [dbc.themes.BOOTSTRAP]

# **Creating Dash Apps**
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# **Get area_code option**
area_options = [
    {"label": area, "value": area} for area in df_housing["area_code"].unique()
]

# **APP LAYOUT**
app.layout = dbc.Container(
    [
        # **title**
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        " Housing Supply & Demand Visualization",
                        className="text-center",
                    ),
                    width=12,
                )
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.P(
                        "Select area codes to compare housing supply and waiting list trends over time.",
                        className="text-center",
                    ),
                    width=12,
                )
            ],
            className="mb-3",
        ),
        # **Selection box**
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Area Codes:", className="fw-bold"),
                        dcc.Dropdown(
                            id="area-dropdown",
                            options=area_options,
                            value=[
                                df_housing["area_code"].unique()[0]
                            ],  # A region is selected by default
                            multi=True,
                            clearable=False,
                            className="mb-3",
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        # **Two independent data type selection boxes**
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "Select Data Type for Line Chart:", className="fw-bold"
                        ),
                        dcc.Dropdown(
                            id="line-data-dropdown",
                            options=[
                                {"label": "Total Households", "value": "total"},
                                {"label": "Percentage Change", "value": "pct_change"},
                                {"label": "Normalized", "value": "normalized"},
                            ],
                            value="total",
                            clearable=False,
                            className="mb-3",
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Label(
                            "Select Data Type for Bar Chart:", className="fw-bold"
                        ),
                        dcc.Dropdown(
                            id="bar-data-dropdown",
                            options=[
                                {"label": "Total Housing Units", "value": "total"},
                                {"label": "Percentage Change", "value": "pct_change"},
                                {"label": "Normalized", "value": "normalized"},
                            ],
                            value="total",
                            clearable=False,
                            className="mb-3",
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        # **chart**
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="waiting-line-chart"), width=6),
                dbc.Col(dcc.Graph(id="housing-bar-chart"), width=6),
            ],
            className="mb-4",
        ),
        # **Map (scatter plot)**
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="housing-map"), width=6),
                dbc.Col(dcc.Graph(id="housing-pie-chart"), width=6),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)


# **Waiting List Line Chart**
@app.callback(
    Output("waiting-line-chart", "figure"),
    [Input("area-dropdown", "value"), Input("line-data-dropdown", "value")],
)


def update_waiting_chart(selected_areas, data_type):
    filtered_df = df_waiting[df_waiting["area_code"].isin(selected_areas)].copy()

    if data_type == "pct_change":
        filtered_df["households_count"] = (
            filtered_df.groupby("area_code")["households_count"].pct_change() * 100
        )
        y_label = "Percentage Change (%)"
    elif data_type == "normalized":
        filtered_df["households_count"] = filtered_df.groupby("area_code")[
            "households_count"
        ].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        y_label = "Normalized Value"
    else:
        y_label = "Total Households"

    fig = px.line(
        filtered_df,
        x="year",
        y="households_count",
        color="area_code",
        title="Households Waiting List Over Time",
        labels={"households_count": y_label, "year": "Year"},
    )

    return fig


# **HOUSING SUPPLY HISTOCRAFT**
@app.callback(
    Output("housing-bar-chart", "figure"),
    [Input("area-dropdown", "value"), Input("bar-data-dropdown", "value")],
)


def update_housing_chart(selected_areas, data_type):
    filtered_df = df_housing[df_housing["area_code"].isin(selected_areas)].copy()

    if data_type == "pct_change":
        filtered_df["housing_units"] = (
            filtered_df.groupby("area_code")["housing_units"].pct_change() * 100
        )
        y_label = "Percentage Change (%)"
    elif data_type == "normalized":
        filtered_df["housing_units"] = filtered_df.groupby("area_code")[
            "housing_units"
        ].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
        y_label = "Normalized Value"
    else:
        y_label = "Total Housing Units"

    fig = px.bar(
        filtered_df,
        x="year",
        y="housing_units",
        color="area_code",
        title="Housing Supply Over Time",
        labels={"housing_units": y_label, "year": "Year"},
    )

    return fig


# **HOUSING SUPPLY MAP**
@app.callback(Output("housing-map", "figure"), [Input("area-dropdown", "value")])


def update_map(selected_areas):
    filtered_df = df_housing[df_housing["area_code"].isin(selected_areas)].dropna(
        subset=["latitude", "longitude"]
    )

    if filtered_df.empty:
        return px.scatter_geo(title="No Data Available for Selected Areas")

    fig = px.scatter_geo(
        filtered_df,
        lat="latitude",
        lon="longitude",
        size="housing_units",
        color="housing_units",
        hover_name="area_code",
        scope="europe",
        title="Housing Supply Distribution",
        hover_data=["area_name"],  # Added area name to hover info
    )

    # Center the map on London coordinates
    fig.update_geos(
        center=dict(lat=51.51, lon=-0.09),  # London center coordinates
        projection_scale=50,  # Increased zoom level
        showcoastlines=True,
        coastlinecolor="black",
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
    )

    return fig


# **HOUSING SUPPLY PIE CHART**
@app.callback(Output("housing-pie-chart", "figure"), [Input("area-dropdown", "value")])


def update_pie_chart(selected_areas):

    # SCREENING DATA
    filtered_df = df_housing[df_housing["area_code"].isin(selected_areas)].copy()

    # **If the data is empty, return prompt**
    if filtered_df.empty:
        print(" No data available for selected areas!")
        return px.pie(title="No Data Available for Selected Areas")

    # **Summarize by area_code**
    summary_df = filtered_df.groupby("area_code")["housing_units"].sum().reset_index()

    # **If housing_units are all 0, return a prompt**
    if summary_df["housing_units"].sum() == 0:
        print(" No valid housing data available!")
        return px.pie(title="No Housing Data Available")

    # **If there is only one area_code, switch to a bar chart**
    if len(summary_df) == 1:
        print(" Only one area selected, switching to bar chart!")
        fig = px.bar(
            summary_df,
            x="area_code",
            y="housing_units",
            title="Housing Units for Selected Area",
            labels={"housing_units": "Housing Units", "area_code": "Area Code"},
        )
        return fig

    # **Draw the pie chart normally**
    fig = px.pie(
        summary_df,
        names="area_code",
        values="housing_units",
        title="Housing Distribution by Area",
        hole=0.4,
    )

    return fig


# **Run the application**
if __name__ == "__main__":
    app.run_server(debug=True, port=5050)
