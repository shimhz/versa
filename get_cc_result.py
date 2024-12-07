import json
import numpy as np


def write_scp_from_json_line_by_line(json_file_path, scp_file_path):
    with open(json_file_path, "r") as json_file, open(scp_file_path, "w") as scp_file:
        ch_01 = []
        ch_11 = []
        ch_12 = []
        for line in json_file:
            try:
                entry = json.loads(line.strip())

                if "audio_filepath" in entry:
                    if entry["audio_filepath"].split("/")[1] == "01":
                        ch_01.append(float(entry["estimated_snr"]))
                    if entry["audio_filepath"].split("/")[1] == "11":
                        ch_11.append(float(entry["estimated_snr"]))
                    if entry["audio_filepath"].split("/")[1] == "12":
                        ch_12.append(float(entry["estimated_snr"]))
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {line.strip()} - {e}")

        scp_file.write(f"ch_01 = #num_utt: {len(ch_01)}, mean_snr: {np.mean(ch_01)}\n")
        scp_file.write(f"ch_11 = #num_utt: {len(ch_11)}, mean_snr: {np.mean(ch_11)}\n")
        scp_file.write(f"ch_12 = #num_utt: {len(ch_12)}, mean_snr: {np.mean(ch_12)}\n")


if __name__ == "__main__":

    json_file_path = "/data/user_data/hyejinsh/corpus/dsta-maritime-comms/manifest_with_snr.json"  # Replace with your .json file path
    scp_file_path = (
        "./dsta-maritime_snr_statistics.scp"  # Replace with your .scp file path
    )
    write_scp_from_json_line_by_line(json_file_path, scp_file_path)
