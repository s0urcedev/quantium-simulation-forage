import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


def load_sales_data(path: str) -> pd.DataFrame:
	df = pd.read_csv(path)

	# Convert sales values like "$1638.0" into numeric values.
	df["sales"] = df["sales"].str.replace("$", "", regex=False).astype(float)
	df["date"] = pd.to_datetime(df["date"])
	return df


def create_sales_figure(sales_data: pd.DataFrame, region: str):
	if region == "all":
		filtered_data = sales_data
		title = "Pink Morsel Daily Sales Across All Regions"
	else:
		filtered_data = sales_data[sales_data["region"] == region]
		title = f"Pink Morsel Daily Sales in the {region.title()} Region"

	daily_sales = (
		filtered_data.groupby("date", as_index=False)
		.agg(sales=("sales", "sum"))
	)

	fig = px.line(
		daily_sales,
		x="date",
		y="sales",
		title=title,
		labels={"date": "Date", "sales": "Total Sales (USD)"},
	)

	price_increase_date = "2021-01-15"
	fig.add_shape(
		type="line",
		x0=price_increase_date,
		x1=price_increase_date,
		y0=0,
		y1=1,
		xref="x",
		yref="paper",
		line={"color": "#E63946", "dash": "dash"},
	)
	fig.add_annotation(
		x=price_increase_date,
		y=1,
		xref="x",
		yref="paper",
		text="Price increase: 2021-01-15",
		showarrow=False,
		xanchor="left",
		yanchor="bottom",
		font={"color": "#E63946", "size": 12},
	)

	fig.update_layout(
		margin={"l": 40, "r": 24, "t": 70, "b": 40},
		paper_bgcolor="rgba(0,0,0,0)",
		plot_bgcolor="rgba(0,0,0,0)",
		font={"family": "Georgia, serif", "color": "#F4F1DE"},
		title={"x": 0.02, "font": {"size": 24}},
	)
	fig.update_traces(line={"color": "#81B29A", "width": 3})
	fig.update_xaxes(showgrid=False, title_font={"size": 16})
	fig.update_yaxes(gridcolor="rgba(244, 241, 222, 0.18)", title_font={"size": 16})
	return fig


def create_app() -> Dash:
	sales_data = load_sales_data("./data/output.csv")

	app = Dash(__name__)
	app.title = "Soul Foods Pink Morsel Visualizer"
	layout = html.Div(
		children=[
			html.Div(
				children=[
					html.P("Quantium Simulation", className="eyebrow"),
					html.H1("Soul Foods Pink Morsel Sales Visualizer"),
					html.P(
						"Use the region filter to compare sales before and after the Pink Morsel price increase on 15 January 2021.",
						className="subtitle",
					),
				],
				className="hero",
			),
			html.Div(
				children=[
					html.Label("Filter by region", className="control-label"),
					dcc.RadioItems(
						id="region-filter",
						options=[
							{"label": "North", "value": "north"},
							{"label": "East", "value": "east"},
							{"label": "South", "value": "south"},
							{"label": "West", "value": "west"},
							{"label": "All", "value": "all"},
						],
						value="all",
						inline=True,
						className="region-radio",
					),
				],
				className="control-card",
			),
			html.Div(
				children=[
					dcc.Graph(id="sales-chart", figure=create_sales_figure(sales_data, "all")),
				],
				className="chart-card",
			),
		],
		className="page-shell",
		style={
			"minHeight": "100vh",
			"padding": "40px 20px",
			"background": "radial-gradient(circle at top left, #264653 0%, #1d3557 45%, #0b1320 100%)",
		},
	)

	@app.callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
	def update_chart(selected_region: str):
		return create_sales_figure(sales_data, selected_region)

	app.layout = layout
	return app


app = create_app()


if __name__ == "__main__":
	app.run(debug=True)
