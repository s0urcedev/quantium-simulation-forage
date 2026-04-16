import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


def load_sales_data(path: str) -> pd.DataFrame:
	df = pd.read_csv(path)

	# Convert sales values like "$1638.0" into numeric values.
	df["sales"] = df["sales"].str.replace("$", "", regex=False).astype(float)
	df["date"] = pd.to_datetime(df["date"])

	daily_sales = (
		df.groupby("date", as_index=False)
		.agg(sales=("sales", "sum"))
		.sort_values(by="date")
	)
	return daily_sales


def create_app() -> Dash:
	sales_data = load_sales_data("./data/output.csv")

	fig = px.line(
		sales_data,
		x="date",
		y="sales",
		title="Pink Morsel Daily Sales Over Time",
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
		line={"color": "red", "dash": "dash"},
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
	)

	app = Dash(__name__)
	app.layout = html.Div(
		children=[
			html.H1("Soul Foods Pink Morsel Sales Visualizer"),
			dcc.Graph(figure=fig),
		],
		style={"maxWidth": "1000px", "margin": "0 auto", "padding": "20px"},
	)
	return app


app = create_app()


if __name__ == "__main__":
	app.run(debug=True)
