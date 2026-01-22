import json

def process_mission_data(file_path):
    print("--- Day 2: Data Intelligence Processing ---")
    
    # 1. List to store structured data
    structured_data = []

    try:
        # 2. Reading the file (File I/O)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
        print(f"Raw Intelligence Found: {len(lines)} records.")

        # 3. Processing loop (String Manipulation)
        for line in lines:
            parts = line.strip().split(' | ')
            
            # 4. Creating a Dictionary (Key-Value pairs)
            mission_entry = {
                "operation_name": parts[0].split(': ')[1],
                "status": parts[1].split(': ')[1],
                "agent_id": parts[2].split(': ')[1]
            }
            structured_data.append(mission_entry)

        # 5. Writing to JSON (The language of LLMs)
        output_file = 'mission_report.json'
        with open(output_file, 'w') as json_file:
            json.dump(structured_data, json_file, indent=4)
            
        print(f"Success: Data structured and saved to '{output_file}'")
        print("JSON Preview:", json.dumps(structured_data[0], indent=2))

    except FileNotFoundError:
        print("Error: Mission data file not found.")

if __name__ == "__main__":
    process_mission_data('mission_data.txt')