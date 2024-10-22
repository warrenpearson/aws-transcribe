import json
import sys


class StitchSpeakers:
    def __init__(self):
        self._current_speaker = ""
        self._buffer = ""

    def stitch(self, input_file):
        data = self.get_json(input_file)
        items = data["results"]["items"]
        for item in items:
            self.render_item(item)

    def get_json(self, input_file):
        with open(input_file, "r") as jinf:
            data = json.load(jinf)

        return data

    def render_item(self, item):
        speaker = item["speaker_label"]
        content = item["alternatives"][0]["content"]
        if item.get("start_time"):
             timestamp = self.format_timestamp(item["start_time"])
        else:
             timestamp = ""

        if speaker != self._current_speaker:
            print("\n")
            print(f"{timestamp} | {self._current_speaker}: {self._buffer}")
            self._current_speaker = speaker
            self._buffer = ""

        self._buffer += " " + content

    def format_timestamp(self, timestamp):
        timestamp = int(float(timestamp))
        hours = timestamp // 3600
        minutes = (timestamp % 3600) // 60
        remaining_seconds = timestamp % 60
        return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"
        


if __name__ == "__main__":
    input_json_file = sys.argv[1]
    StitchSpeakers().stitch(input_json_file)
