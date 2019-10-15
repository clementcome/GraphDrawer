import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

nodes = [
    {
        "data": {'id': short, 'label': label}
    }
    for short, label in (
        ("1","1"),
        ("2","2"),
        ("Alice","Alice"),
        ("1975","1975"),
        ("Bob", "Bob"),
        ("1985", "1985")
    )
]

edges = [
    {
        "data": {"source": source, "target": target, "label": label, "id": id_edge}
    }
    for source,target, label, id_edge in (
        ("1","Alice", 'name', 'edge1'),
        ("1","1975", 'birth', 'edge2'),
        ("1","2", 'friend', 'edge3'),
        ("2","Bob", 'name', 'edge4'),
        ("2","1985", 'birth', 'edge5'),
    )
]

last_data = [{'data': {'id': '4', 'label': '"Bob"'}, 'classes': 'square'}, {'data': {'id': '5', 'label': '"Alice"'}, 'classes': 'square'}, {'data': {'id': '6', 'label': 'D1'}, 'classes': 'round'}, {'data': {'id': '7', 'label': 'D2'}, 'classes': 'round'}, {'data': {'id': '8', 'label': 'P1'}, 'classes': 'round'}, {'data': {'id': '9', 'label': 'P2'}, 'classes': 'round'}, {'data': {'id': '10', 'label': '"Carl"'}, 'classes': 'square'}, {'data': {'id': '11', 'label': '"David"'}, 'classes': 'square'}, {'data': {'source': '6', 'target': '5', 'id': '-1', 'label': 'name'}, 'classes': 'directed'}, {'data': {'source': '7', 'target': '4', 'id': '-2', 'label': 'name'}, 'classes': 'directed'}, {'data': {'source': '8', 'target': '10', 'id': '-3', 'label': 'name'}, 'classes': 'directed'}, {'data': {'source': '9', 'target': '11', 'id': '-4', 'label': 'name'}, 'classes': 'directed'}, {'data': {'source': '6', 'target': '9', 'id': '-5', 'label': 'treats'}, 'classes': 'directed'}, {'data': {'source': '6', 'target': '8', 'id': '-6', 'label': 'treats'}, 'classes': 'directed'}, {'data': {'source': '7', 'target': '8', 'id': '-7', 'label': 'treats'}, 'classes': 'directed'}]

app.layout = html.Div([
    html.Div([
        html.H1("GraphDrawer"),
        html.H2("Handling of nodes"),
        html.Div([
            "Enter a name for the new node :",
            dcc.Input(id='input-node-name', type='text', placeholder= 'Name'),
        "Type of node : ",
        dcc.Dropdown(
            options = [
                {'label': 'Round', 'value': 'round'},
                {'label': 'Square', 'value': 'square'},
                {'label': 'Dotted', 'value': 'dotted'},
            ],
            value = 'round',
            id = 'node-type',
            style = {'width': '200px', 'display': 'inline-block'}
        ),
        ]),
        html.Button('Create a new node', id='button-create-node'),
        html.Div([
            "Do you want to delete this node : ",
            html.Span(id='delete-node-name'),
            ' ?',
            html.Button('Yes', id='button-delete-node')
        ]),
        html.H2('Handling of edges'),
        html.Div([
            "To create a new edge, enter its name, then click the source node and after click the target node. You can tick the box if you want the edge to be directed."
        ]),
        html.Div([
            "Enter a name for the new edge :",
            dcc.Input(id='input-edge-name', type='text', placeholder= 'Name'),
        html.Div([
            "What type of edge do you want ?",
            dcc.RadioItems(
                id='edge-direction',
                options=[
                    {'label': 'Undirected edge', 'value': 'undirected'},
                    {'label': 'Directed edge', 'value': 'directed'},
                ],
                value= 'undirected',
                style={'border-style': 'solid', 'border-width': "1px", "margin":"2px"}
            ),
            dcc.RadioItems(
                id='edge-dotted',
                options=[
                    {'label': 'Solid edge', 'value': 'solid'},
                    {'label': 'Dotted edge', 'value': 'dotted'},
                ],
                value= 'solid',
                style={'border-style': 'solid', 'border-width': "1px", "margin":"2px"}
            ),
        ], style={"margin":"5px"}),
            "Source node :",
            html.Span(id='source-node-name'),
            ". Target node : ",
            html.Span(id='target-node-name'),
        ],),
        html.Button('Create a new edge', id='button-create-edge'),
        html.Div([
            "Do you want to delete this edge : ",
            html.Span(id='delete-edge-name'),
            ' ?',
            html.Button('Yes', id='button-delete-edge')
        ]),
        html.Div(id='timestamps'),
        html.Button('Save json',id='save-json'),
        html.Button('Use saved json',id='use-saved-json'),
    ], style={"flex": "1"}),
    html.Div([
        cyto.Cytoscape(
            id='cytoscape-graph',
            layout={'name': 'cose'},
            elements = [],
            style = {'width': '100%', 'height': '100%'},
            stylesheet = [
                {
                    'selector': 'edge',
                    'style': {
                        'label': 'data(label)',
                        'font-size': '12',
                        'curve-style': 'bezier',
                        'text-rotation': 'autorotate'
                    }
                },
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)',
                        'font-size': '12',
                        'border-width': '2',
                        'background-color': 'white',
                    }
                },
                {
                    'selector':'.square',
                    'style': {
                        'shape': 'rectangle'
                    }
                },
                {
                    'selector':'node.dotted',
                    'style': {
                        'border-style': 'dashed'
                    }
                },
                {
                    'selector':'edge.dotted',
                    'style': {
                        'line-style': 'dashed'
                    }
                },
                {
                    'selector':'.directed',
                    'style': {
                        'target-arrow-shape': 'triangle',
                    }
                },
            ]
        ),
        html.Pre(id='useless', style={'display': 'none'}),
        html.Div(json.dumps([]) , id='store-data', style={'display':'none'}),
        html.Div(id='delete-node-id', style={'display': 'none'}),
        html.Div(id='delete-edge-id', style={'display': 'none'}),
        html.Div(id='source-node-id', style={'display': 'none'}),
        html.Div(id='target-node-id', style={'display': 'none'}),
        html.Div(id='next-node-id', style={'display': 'none'}),
        html.Div(id='next-edge-id', style={'display': 'none'}),
    ], style={"flex": "1"})
],style={"display": "flex"})

# Utils
def button_was_fired(ts, li_other_ts):
    if ts:
        for other_ts in li_other_ts:
            if other_ts and other_ts > ts:
                return False
        return True

def depend(element, id):
    if "id" in element["data"].keys():
        if element["data"]["id"] == id:
            return True
    if "source" in element["data"].keys():
        if element["data"]["source"] == id:
            return True
    if "target" in element["data"].keys():
        if element["data"]["target"] == id:
            return True
    return False   

def clear(elements, id):
    new_elements = [
        el for el in elements if not depend(el, id)
    ]
    return new_elements

@app.callback(
    Output('timestamps', 'children'),
    [Input('button-create-node', 'n_clicks_timestamp'),
    Input('button-delete-node', 'n_clicks_timestamp')]
)
def display_timestamps(*args):
    if button_was_fired(args[0], args):
        return "Creation"
    elif button_was_fired(args[1], args):
        return "Deletion"

@app.callback(
    Output('useless','children'),
    [Input('save-json','n_clicks')],
    [State('next-node-id','children'),
    State('next-edge-id','children'),
    State('store-data', 'children')]
)
def print_json(n_clicks, next_node_id, next_edge_id, stored_json):
    if n_clicks:
        stored_graph = json.loads(stored_json)
        output_data = {
            "next_node_id": next_node_id,
            "next_edge_id": next_edge_id,
            "graph": stored_graph
        }
        with open('last_data.json','w') as output_file:
            output_file.write(json.dumps(output_data, indent=2))
    return ""


# Node creation and deletion
@app.callback(
    [Output('store-data', 'children'),
    Output('next-node-id','children'),
    Output('next-edge-id','children'),],
    [Input('button-create-node', 'n_clicks_timestamp'),
    Input('button-delete-node', 'n_clicks_timestamp'),
    Input('button-create-edge', 'n_clicks_timestamp'),
    Input('button-delete-edge', 'n_clicks_timestamp'),
    Input('use-saved-json', 'n_clicks_timestamp'),],
    [State('input-node-name', 'value'),
    State('node-type','value'),
    State('delete-node-id','children'),
    State('input-edge-name', 'value'),
    State('edge-direction', 'value'),
    State('edge-dotted', 'value'),
    State('source-node-id','children'),
    State('target-node-id','children'),
    State('delete-edge-id','children'),
    State('next-node-id','children'),
    State('next-edge-id','children'),
    State('store-data', 'children')]
)
def create_node(ts_clicks_create_node, ts_clicks_delete_node, ts_clicks_create_edge, ts_clicks_delete_edge, ts_clicks_use_saved_json,
    name_create_node, node_type, delete_id_node,
    name_create_edge, edge_direction, edge_dotted, source_id, target_id,
    delete_id_edge, next_node_id, next_edge_id, stored_json):
    if button_was_fired(ts_clicks_create_node,[ts_clicks_delete_node, ts_clicks_create_edge, ts_clicks_delete_edge, ts_clicks_use_saved_json]):
        new_data = [{"data": {'id':next_node_id, 'label': name_create_node}, 'classes': node_type}]
        stored_data = json.loads(stored_json)
        new_stored_data = stored_data + new_data
        new_stored_json = json.dumps(new_stored_data)
        print("Added new {} node".format(node_type))
        new_next_node_id = str(int(next_node_id) + 1)
        return new_stored_json, new_next_node_id, next_edge_id
    if button_was_fired(ts_clicks_delete_node, [ts_clicks_create_edge, ts_clicks_create_edge, ts_clicks_delete_edge, ts_clicks_use_saved_json]):
        stored_data = json.loads(stored_json)
        new_stored_data = clear(stored_data, delete_id_node)
        new_stored_json = json.dumps(new_stored_data)
        print("Node {} deleted".format(delete_id_node))
        return new_stored_json, next_node_id, next_edge_id
    if button_was_fired(ts_clicks_create_edge,[ts_clicks_delete_edge, ts_clicks_create_node, ts_clicks_delete_node, ts_clicks_use_saved_json]):
        new_data = [{"data": {'source':source_id, 'target': target_id, 'id':next_edge_id, 'label': name_create_edge}, 'classes': edge_direction + " " + edge_dotted}]
        stored_data = json.loads(stored_json)
        new_stored_data = stored_data + new_data
        new_stored_json = json.dumps(new_stored_data)
        print("Added new {} edge".format(edge_direction))
        new_next_edge_id = str(int(next_edge_id) - 1)
        return new_stored_json, next_node_id, new_next_edge_id
    if button_was_fired(ts_clicks_delete_edge, [ts_clicks_create_edge, ts_clicks_create_node, ts_clicks_delete_node, ts_clicks_use_saved_json]):
        stored_data = json.loads(stored_json)
        new_stored_data = clear(stored_data, delete_id_edge)
        new_stored_json = json.dumps(new_stored_data)
        print("Edge {} deleted".format(delete_id_edge))
        return new_stored_json, next_node_id, next_edge_id
    if button_was_fired(ts_clicks_use_saved_json, [ts_clicks_create_edge, ts_clicks_create_node, ts_clicks_delete_node, ts_clicks_delete_edge]):
        try:
            with open('last_data.json') as input_file:
                last_json = input_file.read()
            last_data = json.loads(last_json)
            graph_json = json.dumps(last_data["graph"])
            print("Updating graph with last_data.json")
            return graph_json, last_data["next_node_id"], last_data["next_edge_id"]
        except FileNotFoundError:
            print("No saved graph to load")
            return stored_json, next_node_id, next_edge_id
    return stored_json, "0", "-1"

#Prepare node deletion
@app.callback(
    [Output('delete-node-name', 'children'),
    Output('delete-node-id','children')],
    [Input('cytoscape-graph', 'tapNodeData')]
)
def prepare_deletion_node(data):
    if data:
        print("Prepare deletion")
        return data["label"], data["id"]
    return None, None

#Prepare edge deletion
@app.callback(
    [Output('delete-edge-name', 'children'),
    Output('delete-edge-id','children')],
    [Input('cytoscape-graph', 'tapEdgeData')]
)
def prepare_deletion_edge(data):
    if data:
        print("Prepare deletion")
        return data["label"], data["id"]
    return None, None

#Prepare edge creation
@app.callback(
    [Output('source-node-name', 'children'),
    Output('source-node-id','children'),
    Output('target-node-name', 'children'),
    Output('target-node-id','children'),],
    [Input('cytoscape-graph', 'tapNodeData')],
    [State('target-node-name', 'children'),
    State('target-node-id','children'),]
)
def prepare_creation(data, last_target_name, last_target_id):
    if data:
        print("Prepare new edge")
        return last_target_name, last_target_id, data["label"], data["id"]
    return None, None, None, None


#Updating graph
@app.callback(
    Output('cytoscape-graph', 'elements'),
    [Input('store-data','children')]
)
def display_graph(stored_json):
    print("Graph updated")
    stored_data = json.loads(stored_json)
    return stored_data


if __name__ == "__main__":
    app.run_server(debug=True)