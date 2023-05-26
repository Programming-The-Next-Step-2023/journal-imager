# Import packages
import pandas as pd
import warnings
import re

from dash import Dash, html, dcc, callback, Input, Output, State, dash_table
from datetime import datetime
from pathlib import Path
from natsort import natsorted

import src.journal_imager.update_journal as uj
import src.journal_imager.load_glove as lg


# Initialize the app
app = Dash(__name__)

# Paths
base_path = Path(__file__).parent
entries_path = base_path / 'journal_entries'
entries_path.mkdir(exist_ok=True)

# Create today's entries directory
current_date = datetime.now().strftime('%Y-%m-%d')
today_entries_dir = entries_path / current_date
today_entries_dir.mkdir(exist_ok=True)


# App layout
app.layout = html.Div(
    id = "app_container",
    style = {'display': 'flex', 'flex-direction': 'column', 'height': '100vh', 'margin': '10px'},
    children = [
        html.Div(
            id = "banner",
            style = {'height': '10%', 'width': '100%', 'display': 'flex', 'justify-content': 'flex-start'},
            children = [
                html.Img(
                    src = app.get_asset_url("uva_logo.png"),
                    style = {'maxHeight':'75%', 'maxWidth':'75%'}
                ),
                html.H3(
                    "Journal Imager",
                    style={'margin-left': '15px'}
                ),
            ]
        ),
        html.Div(
            id = "body_container",
            style={'display': 'flex', 'flex-direction': 'row', 'height': '90%'},
            children=[
                html.Div(
                    id = "left_column",
                    style={'width': '30%', 'margin-right': '10px'},
                    children = [
                        html.Div(
                            id = "app_info",
                            children = [
                                html.P("This app allows you to write journal entries and view them as weird images."),
                                html.Br(),
                                html.P("Enter your journal entry below and press enter to submit."),
                                html.Div(
                                    id = "inputter",
                                    children = [
                                        dcc.Input(
                                            id = 'input_journal_entry',
                                            type = 'text',
                                            placeholder = 'Enter journal entry',
                                            debounce = True,
                                            disabled = False,
                                            style = {'width':'98%'}
                                        )
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            id = "user_controls",
                            style = {'width':'25%'},
                            children = [
                                html.P("Select Date:"),
                                dcc.Dropdown(
                                    id = "date_select",
                                    # Get list of all paths in entries_path, then get the last directory in each path,
                                    # which is the date, which becomes the label and value for the dropdown
                                    options = [{"label": date, "value": date} for date in \
                                               natsorted([re.search(r"/([^/]+)$", str(path)).group(1) \
                                                          for path in entries_path.iterdir() if path.is_dir()],
                                                          reverse=True)],
                                    value = datetime.now().strftime('%Y-%m-%d'),
                                    clearable = False
                                ),
                                html.Br(),
                            ]
                        ),
                        html.Div(
                            id = "image_controls",
                            children=[
                                html.P("Image Controls:"),
                                html.Button(
                                    id = "generate_button",
                                    children = "Generate",
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    id = "right-column",
                    style={'width': '70%'},
                    children = [
                        dash_table.DataTable(
                            id = 'entries_table',
                            style_data={'whiteSpace': 'normal', 'height': 'auto'},
                            style_cell={'textAlign': 'left'},
                        ),
                        html.Img(
                            id = "gen_image",
                            src = app.get_asset_url("uva_logo.png"),
                            style = {'maxHeight':'100%', 'maxWidth':'100%'}
                        )
                    ]
                ),
            ]
        )
    ]
)

## Callbacks
# Update journal entries table with today's entries
@callback(
    Output(component_id='entries_table', component_property='data'),
    Input(component_id='input_journal_entry', component_property='value'),
    Input(component_id='date_select', component_property='value')
)
def update_journal(input_text, date_select, entries_path = entries_path):
    
    # If date is today, use update_journal function
    if date_select == datetime.now().strftime('%Y-%m-%d'):
        entries_dict = uj.update_journal(input_text, entries_path)
    else:
        date_select_entries = entries_path / date_select / 'entries.csv'
        df = pd.read_csv(date_select_entries, sep=',')
        entries_dict = df.to_dict('records')

    return entries_dict


# Disable input box if date is not today
@callback(
    Output(component_id='input_journal_entry', component_property='disabled'),
    Input(component_id='date_select', component_property='value')
)
def button_on_off(date_select):
    if date_select == datetime.now().strftime('%Y-%m-%d'):
        warnings.warn("ENABLED")
        return False
    else:
        warnings.warn("DISABLED")
        return True

# Generate image
@callback(
    Output(component_id='gen_image', component_property='src'),
    [
    Input(component_id='generate_button', component_property='n_clicks'),
    Input(component_id='entries_table', component_property='data')
    ]
)
def generate_image(n_clicks, entries_table):
    # Load the model
    try:
        model.most_similar('hello')
    except NameError:
        warnings.warn("Loading model...")
        model = lg.load_glove()

    warnings.warn("Generating image...")
    
    # warnings.warn(type(entries_table).__name__)

    # troy = list(entries_table[0].values())
    # warnings.warn(str(troy[0]))

    # Get the text from the entries table

    # Get most surprising words

    # Generate image

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)

# # Get list of all directories in entries_path
# clinic_list = [x for x in entries_path.iterdir() if x.is_dir()]
# match = [re.search(r"/([^/]+)$", str(date)).group(1) for date in entries_path.iterdir() if date.is_dir()]

# # Get list of all directories in entries_path, then get the last directory in each path,
# # which is the date, which becomes the label and value for the dropdown
# [{"label": i, "value": i} for i in [re.search(r"/([^/]+)$", str(date)).group(1) for date in entries_path.iterdir() if date.is_dir()]]

# # Example dictionary
# dictdict = {'Entry': 'This is a test entry. I am testing the journal imager app. I hope it works.',
#             'Date': '2021-03-01',}