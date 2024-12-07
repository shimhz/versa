import json

def write_scp_from_json_line_by_line(json_file_path, scp_file_path):
    with open(json_file_path, 'r') as json_file, open(scp_file_path, 'w') as scp_file:
        for line in json_file:
            try:
                entry = json.loads(line.strip())
                if "audio_filepath" in entry:
                    scp_file.write(f"test /data/user_data/hyejinsh/corpus/dsta-maritime-comms/{entry['audio_filepath']}\n")
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {line.strip()} - {e}")


if __name__ == "__main__":

    json_file_path = "/data/user_data/hyejinsh/corpus/dsta-maritime-comms/manifest_with_snr.json"  # Replace with your .json file path
    scp_file_path = "./dsta-maritime.scp"  # Replace with your .scp file path
    write_scp_from_json_line_by_line(json_file_path, scp_file_path)