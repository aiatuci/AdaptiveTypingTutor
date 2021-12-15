from os import read
from typing import Tuple
import keyboard
import csv
import pandas as pd
from string import ascii_letters, punctuation

times = []
prev_time = 0


USER_ID = "user_id"


def log_keys(text: str) -> list[Tuple[str, str, float]]:
  data: list[Tuple[str, float]] = []

  allowed_chars: set[str] = set(
    [p for p in punctuation] + [letters for letters in ascii_letters] + ['space', 'enter', 'backspace'] + [str(i) for i in range(10)]
    )

  print('Type the following text: ' + text)
  while True:
    event: keyboard.KeyboardEvent = keyboard.read_event()
    if event.event_type == "down" and event.name in allowed_chars:
      data.append((event.name, event.event_type, event.time))

    if event.name == "esc":
      data.pop() # Remove the escape 
      return data


def save_data(data: list[Tuple[str, str, float]], user_id: str) -> None:

  # Save data
  with open(f"{user_id}.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(data)

def main():
  data = log_keys("Hello world!")
  save_data(data, '69420')
  print(data)


def get_data(user_id: str) -> pd.DataFrame:
  return pd.read_csv(f"{user_id}.csv")


if __name__ == "__main__":
  main()

