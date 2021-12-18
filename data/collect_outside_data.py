
from collections import defaultdict
from pathlib import Path
import csv
import time
import string


DATA_DIR = 'E:/Data/Raw/Keystrokes/files'
OUT_DIR = 'E:/Data/Modified'

SENTENCE_INDEX = 2
PRESS_TIME_INDEX = 5
LETTER_INDEX = 7
PARTICIPANT_ID_INDEX = 0

WHITELISTED_LETTERS = [c for c in string.ascii_letters + string.digits + string.punctuation + ' '] + ['BKSP']

def main():
    data_dir = Path(DATA_DIR)
    out_dir = Path(OUT_DIR)
    file_no = 0
    sentence_ids = defaultdict(id_maker())
    legal_letters = set(WHITELISTED_LETTERS)

    num_files = len([x for x in data_dir.iterdir()])
    time_checked = False
    start_time = time.time()
    for data_file_path in (direc for direc in data_dir.iterdir() if direc.suffix == '.txt'):
        if not time_checked and file_no == 500:
            deltat = time.time() - start_time
            print(f'500 of the files took {deltat} seconds')
            print(f'Estimating a runtime of {deltat / (file_no / num_files)} seconds') 
            time_checked = True
        file_no += 1


        with open(data_file_path) as data_file:
            #skip first line
            next(data_file)
            previous_out_path = ''
            rows_to_save = []
            for line in data_file:
                raw_data = line.split('\t')
                
                # This happens when \n is a char in the data
                if len(raw_data) <= max(SENTENCE_INDEX, PRESS_TIME_INDEX, LETTER_INDEX, PARTICIPANT_ID_INDEX):
                    continue
                sentence = raw_data[SENTENCE_INDEX]
                sentence_id = sentence_ids[sentence]
                out_file_path = out_dir / f'{sentence_id}.csv'

                if previous_out_path == '':
                    previous_out_path = out_file_path

                # If we got all data from the previous file name
                if previous_out_path != out_file_path:
                    with open(previous_out_path, 'a') as out_file:
                        csv_writer = csv.writer(out_file)
                        csv_writer.writerows(rows_to_save)
                    previous_out_path = out_file_path
                    rows_to_save.clear()
                letter = raw_data[LETTER_INDEX]
                if letter in legal_letters:
                    rows_to_save.append((letter, raw_data[PRESS_TIME_INDEX], raw_data[PARTICIPANT_ID_INDEX]))

            with open(out_file_path, 'a') as out_file:
                csv_writer = csv.writer(out_file)
                csv_writer.writerows(rows_to_save)
    
    write_sentences(sentence_ids)

def write_sentences(sentence_ids: dict):
    with open(Path(OUT_DIR) / 'sentences.txt', 'w') as sentence_file:
        ordered_sentences = sorted(sentence_ids.items(), key = lambda item: item[1])
        sentence_file.writelines(f'{item[0]}\n' for item in ordered_sentences)

class id_maker():
    def __init__(self):
        self.current_id = 0
    
    def __call__(self):
        old_id = self.current_id
        self.current_id += 1
        return old_id

if __name__ == '__main__':
    main()