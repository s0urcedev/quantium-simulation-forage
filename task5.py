from dash import dcc, html

from task4 import create_app


def walk_components(component):
	yield component
	children = getattr(component, "children", None)
	if children is None:
		return
	if isinstance(children, list):
		for child in children:
			yield from walk_components(child)
	else:
		yield from walk_components(children)


def test_header_is_present():
	app = create_app()
	headers = [
		component
		for component in walk_components(app.layout)
		if isinstance(component, html.H1)
	]
	assert any(header.children == "Soul Foods Pink Morsel Sales Visualizer" for header in headers)


def test_visualisation_is_present():
	app = create_app()
	graphs = [
		component
		for component in walk_components(app.layout)
		if isinstance(component, dcc.Graph)
	]
	assert any(getattr(graph, "id", None) == "sales-chart" for graph in graphs)


def test_region_picker_is_present():
	app = create_app()
	radio_items = [
		component
		for component in walk_components(app.layout)
		if isinstance(component, dcc.RadioItems)
	]
	matching = [item for item in radio_items if getattr(item, "id", None) == "region-filter"]
	assert len(matching) == 1

	options = getattr(matching[0], "options", [])
	option_values = {option["value"] for option in options}
	assert option_values == {"north", "east", "south", "west", "all"}
