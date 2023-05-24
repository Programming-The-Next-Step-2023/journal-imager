# Import packages
import src.journal_imager.update_journal as uj

from dash import Dash, html, dcc, callback, Input, Output
from datetime import datetime
from pathlib import Path


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    id = "app_container",
    children = [
        html.Div(
            id = "banner",
            className = "banner",
            children = [html.Img(src=app.get_asset_url("uva_logo.png"),
                                 style={'height':'4%', 'width':'4%'})]
            ),
        html.Div(children='input journal entry'),
        dcc.Input(id='input_journal_entry', placeholder='Enter journal entry', type='text', debounce=True),
        html.Br(),
        html.Div(id='output_journal_entry')
])

# Callbacks
@callback(
    Output(component_id='output_journal_entry', component_property='children'),
    Input(component_id='input_journal_entry', component_property='value')
)
def update_journal(input_text):
    
    # Call journal update function
    output_text = uj.update_journal(input_text)
    return output_text

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)