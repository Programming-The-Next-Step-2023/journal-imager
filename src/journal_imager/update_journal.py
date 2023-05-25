import pandas as pd

from pathlib import Path
from datetime import datetime
import warnings

def update_journal(input_text, entries_path):
    """ Update journal entries with input text.
    
    Parameters:
        input_text (str): Input text to be written to journal entries.
        entries_path (str): Path to journal entries directory.

    Returns:
        str: Output text to be displayed on the app.
    """
    
    # Get today's date to organize entries
    current_date = datetime.now().strftime('%Y-%m-%d')
    today_entries_dir = entries_path / current_date
    today_entries_dir.mkdir(exist_ok=True)

    # Write time and input text to journal_entries file
    today_entries = today_entries_dir / 'entries.csv'
    current_time = datetime.now().strftime('%H:%M:%S')

    # Initialize empty dataframe
    df = pd.DataFrame(columns=['time', 'entry'])

    # Write input text to journal_entries file
    if input_text is not None and len(input_text) >= 1:  # Check for empty input
        try:
            warnings.warn('This is a warning')
            df = pd.read_csv(today_entries, sep=';')
            df.loc[len(df)] = {'time': current_time, 'entry': input_text}
        except FileNotFoundError:
            warnings.warn('This is a warning, too')
            df = pd.DataFrame({'time': current_time, 'entry': input_text}, index=[0])
        finally:
            df.to_csv(today_entries, index=False, sep=';')
    else:
        pass

    return df.to_dict('records')