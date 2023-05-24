import unittest
import shutil

from pathlib import Path
from datetime import datetime
from src.journal_imager.update_journal import update_journal

class TestUpdateJournal(unittest.TestCase):

    # Test normal functionality, no exising journal entries
    def test_update_journal_no_entries(self):
        
        # Input text
        input_text = 'test_1'

        # Create journal_entries directory if it doesn't exist
        journal_entries_dir = Path.home() / 'journal_entries'
        journal_entries_dir.mkdir(exist_ok=True)

        # Create today directory if it doesn't exist
        current_date = datetime.now().strftime('%Y-%m-%d')
        today_entries_dir = journal_entries_dir / current_date
        today_entries_dir.mkdir(exist_ok=True)

        # Write input text to journal_entries file
        today_entries = today_entries_dir / 'entries.txt'
        update_journal(input_text)

        # Read output text
        with open(today_entries, 'r') as f:
            output_text = f.read()
        
        # Remove journal_entries directory
        shutil.rmtree(today_entries_dir)
        
        # Should be input_text + '\n' + '\n'
        self.assertEqual(input_text + '\n' + '\n', output_text)

    # # Test normal functionality, exising journal entries, couldn't figure this one out for now
    # def test_update_journal_existing_entries(self):
    #     input_text = 'test_2'

    #     journal_entries_dir = Path.home() / 'journal_entries'

    #     current_date = datetime.now().strftime('%Y-%m-%d')
    #     today_entries_dir = journal_entries_dir / current_date
    #     today_entries_dir.mkdir(exist_ok=True)

    #     today_entries = today_entries_dir / 'entries.txt'

    #     with open(today_entries, 'r') as f:
    #         existing_text = f.read()
        
    #     update_journal(input_text)

    #     with open(today_entries, 'r') as f:
    #         output_text = f.read()

    #     self.assertEqual(existing_text + input_text + '\n' + '\n', output_text)


    # Test TypeError handling
    def test_update_journal_type_error(self):
        
        # Input text
        input_text = None

        # Create journal_entries directory if it doesn't exist
        journal_entries_dir = Path.home() / 'journal_entries'
        journal_entries_dir.mkdir(exist_ok=True)

        # Create today directory if it doesn't exist
        current_date = datetime.now().strftime('%Y-%m-%d')
        today_entries_dir = journal_entries_dir / current_date
        today_entries_dir.mkdir(exist_ok=True)

        # Write input "text" to journal_entries file
        today_entries = today_entries_dir / 'entries.txt'
        update_journal(input_text)

       # Read output text
        with open(today_entries, 'r') as f:
            output_text = f.read()

        # Remove journal_entries directory
        shutil.rmtree(today_entries_dir)

        # Should be empty string
        self.assertEqual('', output_text)

if __name__ == '__main__':
    unittest.main()