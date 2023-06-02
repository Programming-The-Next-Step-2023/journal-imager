# Import packages
import pandas as pd
import re

from dash import Dash, html, dcc, callback, Input, Output, State, dash_table, callback_context
from datetime import datetime
from pathlib import Path
from natsort import natsorted

import src.journal_imager.update_journal as uj
import src.journal_imager.load_glove as lg
import src.journal_imager.get_salient_words as gsw
import src.journal_imager.generate_image as gi


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
    style = {
        'display': 'flex',
        'flex-direction': 'column',
        'height': '100vh',
        'padding': '10px',
        'font-family': 'Arial, sans-serif',
        'background-color': 'white'
    },
    children = [
        html.Div(
            id = "banner",
            style = {
                'height': '10%',
                'width': '100%',
                'display': 'flex',
                'align-items': 'center',
                'text-align': 'left',
                'justify-content': 'flex-start',
                'background-color': '#f2f2f2',
                'border-radius': '15px',
                'box-shadow': '0px 0px 5px 0px rgba(0,0,1,0.1)',
                'padding': '10px'
            },
            children = [
                html.Img(
                    src = app.get_asset_url(
                        "uva_logo.png"
                    ),
                    style = {
                        'maxHeight':'75%',
                        'maxWidth':'75%'
                    }
                ),
                html.H1(
                    "Journal Imager",
                    style={
                        'margin-left': '15px'
                    }
                )
            ]
        ),
        html.Br(),
        html.Div(
            id = "body_container",
            style={
                'display': 'flex',
                'flex-direction': 'row',
                # 'height': '90%',
                'background-color': 'white'
            },
            children=[
                html.Div(
                    id = "left_column",
                    style={
                        'width': '30%',
                        'margin-right': '10px',
                        'border-radius': '15px',
                        'box-shadow': '0px 0px 5px 0px rgba(0,0,1,0.1)',
                        'padding': '10px'
                    },
                    children = [
                        html.Div(
                            id = "app_info",
                            children = [
                                html.P("This app allows you to write journal entries and view them as weird images."),
                                html.P("It uses GloVe embeddings to process your text and Stable Diffusion v2.1 to generate images."),
                                html.Br(),
                                html.H4("Entry & Date Controls:"),
                            ]
                        ),
                        html.Div(
                            id = "entry_inputter",
                            hidden=False,
                            children = [
                                html.P("Enter your journal entry below and press Enter to submit."),
                                dcc.Input(
                                    id = 'input_journal_entry',
                                    type = 'text',
                                    placeholder = 'Today, I...',
                                    debounce = True,
                                    style = {
                                        'width':'98%'
                                    }
                                )
                            ],
                        ),
                        html.Div(
                            id = "date_control",
                            style = {
                                'width':'30%'
                            },
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
                                html.Br()
                            ]
                        ),
                        html.Div(
                            id = "image_controls",
                            children=[
                                html.H4("Imaging Tutorial"),
                                dcc.Markdown('''
                                              1. Once you are done journaling, run [this Colab notebook](https://colab.research.google.com/drive/1PrUchYM-GOhSCxK9tmj8AgLrcXfZBhfO).
                                              2. Paste the ngrok URL into the input box below.
                                              3. Adjust the image controls as desired.
                                              4. Click the Generate button.
                                              5. Wait for the image to load.
                                              6. Repeat steps 3-5 as desired.'''),
                                html.H4("Image Controls"),
                                html.Div(
                                    id = "image_style_container",
                                    children = [
                                        dcc.Dropdown(
                                            id = "image_style",
                                            options = [
                                                {"label": "Normal", "value": "photo of "},
                                                {"label": "HQ Render", "value": "octane render of "},
                                                {"label": "Impressionist", "value": "impressionist painting of "},
                                                {"label": "Whacky", "value": "whacky cartoon art of "},
                                                {"label": "Abstract", "value": "abstract art of "},
                                                {"label": "Surreal", "value": "surrealist art of "},
                                            ],
                                            value = "photo of ",
                                            clearable = False
                                        )
                                    ],
                                    style={'width':'30%'}
                                ),
                                html.P("Number of Images:"),
                                dcc.Slider(
                                    id = "n_images",
                                    min = 1,
                                    max = 6,
                                    step = 1,
                                    value = 3,
                                    included = False
                                ),
                                html.Br(),
                                html.P("Closeness to Text (%):"),
                                dcc.Slider(
                                    id = "guidance_scale",
                                    min = 1.01,
                                    max = 20,
                                    value = 7.5,
                                    marks = {
                                        1.01: "0",
                                        5: "25",
                                        10: "50",
                                        15: "75",
                                        20: "100"
                                    },
                                    included = False
                                ),
                                html.Br(),
                                html.P("Number of Inference Steps:"),
                                dcc.Slider(
                                    id = "num_inference_steps",
                                    min = 1,
                                    max = 100,
                                    value = 50,
                                    marks = {
                                        1: "1",
                                        25: "25",
                                        50: "50",
                                        75: "75",
                                        100: "100"
                                    },
                                    included = False
                                ),
                                html.Br(),
                                html.Div(
                                    id = "ngrok_url_inputter",
                                    children = [
                                        html.P("Enter the ngrok URL from Google Colab below."),
                                        dcc.Input(
                                            id = 'ngrok_url',
                                            type = 'text',
                                            placeholder = 'https://12345abcde.ngrok-free.app',
                                            debounce = True,
                                            style = {
                                                'width':'98%'
                                            }
                                        )
                                    ]
                                ),
                                html.Br(),
                                html.Button(
                                    id = "generate_button",
                                    children = "Generate",
                                    disabled=True
                                ),
                                html.Br()                                
                            ]
                        )
                    ]
                ),
                html.Div(
                    id = "right-column",
                    style={
                        'width': '70%'
                    },
                    children = [
                        dash_table.DataTable(
                            id = 'entries_table',
                            style_table={
                                'border-radius': '15px',
                                'box-shadow': '0px 0px 5px 0px rgba(0,0,1,0.1)',
                                'padding': '10px'
                            },
                            style_header={
                                'fontWeight': 'bold',
                                'backgroundColor': 'white'
                            },
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_cell={
                                'textAlign': 'left',
                                'font-family': 'Arial, sans-serif',
                                'backgroundColor': 'white',
                                'border': '0px',
                                'padding': '5px'
                            },
                            style_as_list_view = True,
                            editable=True,
                            row_deletable=True,
                        ),
                        html.Br(),
                        html.Div(
                            id = "gen_image_container",
                            children=[] # This will be populated by the callback
                        )
                    ]
                )
            ]
        ),
        html.Br()
    ]
)

## Callbacks
# Update journal entries table with today's entries
@callback(
    Output(component_id='entries_table', component_property='data'),
    Output(component_id='input_journal_entry', component_property='value'),
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

    return entries_dict, '' # Return today's entries and clear input box

# Delete entry
@callback(
        Output(component_id='generate_button', component_property='children'),
        Input(component_id='entries_table', component_property='data'),
        State(component_id='date_select', component_property='value')
)
def delete_entry(entries_dict, date_select):

    # Convert to dataframe
    entries = pd.DataFrame.from_records(entries_dict)

    # Get path to entries.csv
    date_entries = entries_path / date_select / 'entries.csv'

    # Delete entry
    if not entries.empty:
        if entries['Entry'][0] == "No entries yet - add your first entry for today!":
            entries = entries.iloc[1:] # Delete default entry
            return "Generate"
        # Save to csv
        entries.to_csv(date_entries, index=False)

    return "Generate"

# Disable input box if date is not today
@callback(
    Output(component_id='entry_inputter', component_property='hidden'),
    Input(component_id='date_select', component_property='value')
)
def box_on_off(date_select):
    if date_select == datetime.now().strftime('%Y-%m-%d'):
        return False
    else:
        return True
    
# Disable generate button if no ngrok URL is entered
@callback(
    Output(component_id='generate_button', component_property='disabled'),
    Input(component_id='ngrok_url', component_property='value')
)
def button_on_off(ngrok_url):
    if ngrok_url == '' or ngrok_url == None:
        return True
    else:
        return False

# Generate image
@callback(
    Output(component_id='gen_image_container', component_property='children'),
    Output(component_id='generate_button', component_property='n_clicks'),
    [
    Input(component_id='date_select', component_property='value'),
    Input(component_id='generate_button', component_property='n_clicks'),
    State(component_id='entries_table', component_property='data'),
    State(component_id='n_images', component_property='value'),
    State(component_id='guidance_scale', component_property='value'),
    State(component_id='num_inference_steps', component_property='value'),
    State(component_id='ngrok_url', component_property='value'),
    State(component_id='image_style', component_property='value')
    ]
)
def generate_image(date_select, n_clicks, entries_table, n_images, guidance_scale, num_inference_steps, ngrok_url, image_style):
    
    # Create directory for images
    img_dir = base_path / "assets/gen_images" / date_select
    img_dir.mkdir(parents=True, exist_ok=True)

    def image_layout(img_files):
        """Returns a list of image components.
        
        Args:
            date_select (str): Date selected in date_select dropdown.
            n_images (int): Number of images to display.
        
        Returns:
            list: List of image components.
        """
        return [
            html.Img(
                id = {
                    'type': 'gen_image',
                    'index': idx
                },
                src = re.search(r"\/assets\/.*", str(image_path)).group(0),
                style= {
                    'display':'inline-block',
                    'float':'center',
                    'maxHeight':'33%',
                    'maxWidth':'33%',
                    'padding':'1.5px',
                    'boxShadow':'0 0 5px 0 rgba(0, 0, 1, 0.1)',
                    'borderRadius':'15px'
                    }
            )
            for idx, image_path in enumerate(img_files)
        ]

    # If the callback is triggered but the button hasn't been clicked yet (i.e., only date_select has changed)
    if n_clicks is None or n_clicks == 0:
        img_files = [img_file for img_file in img_dir.glob("*.png")]
        return image_layout(img_files), 0
    
    ## If the callback is triggered and the button has been clicked
    # Load the model
    try:
        model.most_similar('hello')
    except NameError:
        print("Loading model...")
        model = lg.load_glove()

    # Get the text from the entries table
    entries = pd.DataFrame.from_records(entries_table)['Entry'].to_list()

    # Get most salient words and split into triples
    most_salient = gsw.get_most_surprising_words(entries, model, n_images)
    most_salient_triples = [most_salient[i:i+3] for i in range(0, len(most_salient), 3)]

    # Delete any existing images
    for img_file in img_dir.glob("*.png"):
        img_file.unlink()

    
    # Generate new images
    for image in range(n_images):
        # Generate image
        print("Generating image " + str(image))
        gi.generate_image(ngrok_url,
                          image_style + ', '.join(most_salient_triples[image]),
                          guidance_scale,
                          int(round(num_inference_steps)),
                          img_path = img_dir / f"image_{image+1}_{datetime.now().strftime('%H-%M-%S')}.png"
        )
    
    # Get list of image files
    img_files = [img_file for img_file in img_dir.glob("*.png")]

    # Return list of image components
    return image_layout(img_files), 0


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
