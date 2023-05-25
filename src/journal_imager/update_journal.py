from pathlib import Path
from datetime import datetime

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
    today_entries = today_entries_dir / 'entries.txt'
    current_time = datetime.now().strftime('%H:%M:%S')

    if input_text is not None and len(input_text) >= 1:
        with open(today_entries, 'a') as f:
            f.write(current_time + '\n' + input_text + '\n' + '\n')
    else:
        pass

    return f'Output: {input_text}'