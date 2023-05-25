# Import packages
import src.journal_imager.update_journal as uj

from dash import Dash, html, dcc, callback, Input, Output, dash_table
from datetime import datetime
from pathlib import Path


# Initialize the app
app = Dash(__name__)

# Paths
base_path = Path(__file__).parent
entries_path = base_path / 'journal_entries'
entries_path.mkdir(exist_ok=True)


# App layout
app.layout = html.Div(
    id = "app_container",
    children = [
        html.Div(
            id = "banner",
            children = [
                html.Img(
                    src = app.get_asset_url("uva_logo.png"),
                    style = {'height':'4%', 'width':'4%'}
                )
            ]
        ),
        html.Div(
            id = "left-column",
            children = [
                html.Div(
                    id = "app_info",
                    children = [
                        html.H3("Journal Imager"),
                        html.P("This app allows you to write journal entries \n and view them as weird images."),
                        html.P("Enter your journal entry below and press enter to submit."),
                        html.Div(
                            id = "inputter",
                            children = [
                                dcc.Input(
                                    id = 'input_journal_entry',
                                    type = 'text',
                                    placeholder = 'Enter journal entry',
                                    debounce = True,
                                    style = {'width':'10%'}
                                ),
                            ],
                            # style = dict(display='flex', justifyContent='center')
                        ),
                    html.Br(),
                    html.Br(),
                    ]
                ),
                html.Div(
                    id = "user_controls",
                    children = [
                        html.P("Select date(s) to view journal entries."),
                        dcc.DatePickerRange(
                            id = "date_picker",
                            start_date = datetime(2023, 5, 17).strftime('%Y-%m-%d'),
                            end_date = datetime.now().strftime('%Y-%m-%d'),
                        )
                    ]
                )
            ]
        ),
        dash_table.DataTable(
            id = 'entries_table'
        ),
    ]
)

# Callbacks
@callback(
    Output(component_id='entries_table', component_property='data'),
    Input(component_id='input_journal_entry', component_property='value')
)
def update_journal(input_text, entries_path = entries_path):
    
    # Call journal update function
    entries_dict = uj.update_journal(input_text, entries_path)
    return entries_dict

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)