import os
import json
import time
from datetime import datetime

OUTPUT_DIR = os.getenv("TARGET_DIR",default='/data') #or '/data' 

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_data():
    timestamp = datetime.now().isoformat()
    filename = f"data-{timestamp.replace(':', '-').replace('.', '-')}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Generate sample data
    data = {
        'timestamp': timestamp,
        'records': [
            {
                'id': i + 1,
                'name': f'Record {i + 1}',
                'value': hash(str(i)) % 1000,
                'category': ['A', 'B', 'C'][hash(str(i)) % 3]
            }
            for i in range(10)
        ]
    }

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'Generated: {filename}')

    # Keep only last 10 files
    files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.json')], reverse=True)[:10]
    all_files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.json')])

    for file in all_files:
        if file not in files:
            os.remove(os.path.join(OUTPUT_DIR, file))
            print(f'Deleted old file: {file}')

if __name__ == '__main__':
    print('Batch job started. Generating data every 30 seconds...')
    generate_data()
    while True:
        time.sleep(30)
        generate_data()
