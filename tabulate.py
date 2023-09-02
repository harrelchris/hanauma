import csv
import datetime
import json
import pathlib

DATA_DIR = pathlib.Path("data")
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def main():
    events = []
    for file_path in DATA_DIR.iterdir():
        file_content = read_json_file(file_path)
        event_sessions = file_content["data"]["event_sessions"]
        file_events = extract_events(event_sessions)
        events.extend(file_events)
    output_file_path = str(DATA_DIR / "hanauma.csv")
    write_csv(output_file_path, events)


def read_json_file(file_path):
    file = open(file_path, "r", encoding="utf-8")
    content = json.load(file)
    file.close()
    return content


def extract_events(event_sessions):
    events = []

    for event_session in event_sessions:
        start_date_time = event_session["start_date_time"]

        local_date_and_time = event_session["local_date_and_time"]
        start_time = local_date_and_time["start_time"]
        start_day_of_the_week = local_date_and_time["start_day_of_the_week"]

        meta_data = event_session["meta_data"]
        tickets_issued_and_valid = meta_data["tickets_issued_and_valid"]
        last_ticket_created_at = meta_data["last_ticket_created_at"]

        event_datetime = datetime.datetime.strptime(start_date_time, TIMESTAMP_FORMAT)
        reservation_start_datetime_timedelta = event_datetime - datetime.timedelta(days=2)
        reservation_start_datetime = reservation_start_datetime_timedelta.replace(hour=17, minute=0, second=0, microsecond=0)
        elapsed = datetime.datetime.strptime(last_ticket_created_at, TIMESTAMP_FORMAT) - reservation_start_datetime

        events.append({
            "year": event_datetime.year,
            "month": event_datetime.month,
            "day": event_datetime.day,
            "weekday": start_day_of_the_week,
            "start_time": start_time,
            "capacity": event_session["capacity"],
            "tickets_issued": tickets_issued_and_valid,
            "elapsed_seconds": elapsed.total_seconds(),
        })

    return events


def write_csv(file_path, events):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, events[0].keys())
        writer.writeheader()
        writer.writerows(events)


if __name__ == '__main__':
    main()
