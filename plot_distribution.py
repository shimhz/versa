import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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


def plot_distributions(json_file_path, key="estimated_snr"):
    """
    Reads data from a JSON file and plots distributions.

    Args:
        json_file_path (str): Path to the JSON file.
        key (str, optional): Key to access specific data if the JSON is a dictionary.
                             If None, assumes the JSON is a list of values.
    """
    # Read JSON data
    with open(json_file_path, "r") as json_file:
        d_channel = {"ch_01": [], "ch_11": [], "ch_12": []}
        for line in json_file:
            try:
                entry = json.loads(line.strip())

                if "audio_filepath" in entry:
                    if entry["audio_filepath"].split("/")[1] == "01":
                        d_channel["ch_01"].append(float(entry["estimated_snr"]))
                    if entry["audio_filepath"].split("/")[1] == "11":
                        d_channel["ch_11"].append(float(entry["estimated_snr"]))
                    if entry["audio_filepath"].split("/")[1] == "12":
                        d_channel["ch_12"].append(float(entry["estimated_snr"]))
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {line.strip()} - {e}")

    # Plot the distribution
    for key, item in d_channel.items():
        plt.figure(figsize=(8, 6))
        sns.histplot(item, kde=True, bins=30, color="blue")
        plt.title(f"SNR Distribution of {key}")
        # plt.xlabel("Channel")
        plt.ylabel("Estimated SNR")
        plt.xticks(range(0, 35))
        plt.yticks(range(0, 160))
        plt.gca().set_yticks([])
        # splt.grid(True)
        plt.show()
        plt.savefig(f"./{key}.png")


if __name__ == "__main__":

    json_file = (
        "/data/user_data/hyejinsh/corpus/dsta-maritime-comms/manifest_with_snr.json"
    )
    plot_distributions(json_file, key="estimated_snr")
