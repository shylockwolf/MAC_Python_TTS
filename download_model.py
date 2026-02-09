import requests
import os

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Done.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

models_dir = os.path.join(os.getcwd(), "models")
os.makedirs(models_dir, exist_ok=True)


models_to_download = [
    "https://hf-mirror.com/rhasspy/piper-voices/resolve/main/zh/zh_CN/huayan/medium/zh_CN-huayan-medium",
    "https://hf-mirror.com/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium"
]

for base_url in models_to_download:
    onnx_url = f"{base_url}.onnx"
    json_url = f"{base_url}.onnx.json"
    
    filename = os.path.basename(base_url)
    
    onnx_path = os.path.join(models_dir, f"{filename}.onnx")
    json_path = os.path.join(models_dir, f"{filename}.onnx.json")

    if not os.path.exists(onnx_path):
        download_file(onnx_url, onnx_path)
    else:
        print(f"Skipping {filename}.onnx (already exists)")

    if not os.path.exists(json_path):
        download_file(json_url, json_path)
    else:
        print(f"Skipping {filename}.onnx.json (already exists)")

