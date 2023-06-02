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
        dict: Dictionary of today's entries.
    """
    
    warnings.warn('update journal')

    # Get today's date to organize entries
    current_date = datetime.now().strftime('%Y-%m-%d')
    today_entries_dir = entries_path / current_date
    today_entries_dir.mkdir(exist_ok=True)

    # Write time and input text to journal_entries file
    today_entries = today_entries_dir / 'entries.csv'
    current_time = datetime.now().strftime('%H:%M:%S')

    # Initialize empty dataframe
    df = pd.DataFrame(columns=['Time', 'Entry'])

    # Read in today's entries
    try:
        df = pd.read_csv(today_entries)
    except FileNotFoundError:
        df = pd.DataFrame({'Time': current_time, 'Entry': "No entries yet - add your first entry for today!"}, index=[0])

    # Check if input text is empty
    if input_text is None or len(input_text) < 1:  # Check for empty input
        return df.to_dict('records')

    # Check if input text is the same as the last entry
    if input_text == df['Entry'].iloc[-1] and len(df) > 1:
        return df.to_dict('records')

    # Write to journal entries file
    try:
        df = pd.read_csv(today_entries)
        df.loc[len(df)] = {'Time': current_time, 'Entry': input_text}
    except FileNotFoundError:
        df = pd.DataFrame({'Time': current_time, 'Entry': input_text}, index=[0])
    finally:
        df.to_csv(today_entries, index=False)

    return df.to_dict('records')