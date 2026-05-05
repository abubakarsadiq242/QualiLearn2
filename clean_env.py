import os

env_path = '.env'
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        if '=' in line:
            key, val = line.split('=', 1)
            cleaned_lines.append(f"{key.strip()}={val.strip()}\n")
        else:
            cleaned_lines.append(line)
            
    with open(env_path, 'w') as f:
        f.writelines(cleaned_lines)
    print("Cleaned .env file successfully.")
else:
    print(".env file not found.")
