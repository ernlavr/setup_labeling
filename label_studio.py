import subprocess
import sys
import time
import requests
from pathlib import Path

def start_label_studio(host="127.0.0.1", port=8081, data_dir=None):
    """
    Start a Label Studio server programmatically.
    
    Args:
        host (str): Server host address (default: 127.0.0.1)
        port (int): Server port (default: 8080)
        data_dir (str): Path to data directory. If None, uses default location.
    
    Returns:
        subprocess.Popen: The server process object
    """
    
    # Build the command
    label_studio_exec = sys.executable.replace("/python", "/label-studio")
    cmd = [label_studio_exec]
    
    # Add host and port
    cmd.extend(["start", "--host", host, "--port", str(port)])
    
    print(" ".join(cmd))
    
    # Add data directory if specified
    if data_dir:
        data_path = Path(data_dir)
        data_path.mkdir(parents=True, exist_ok=True)
        cmd.extend(["--data-dir", str(data_path)])
    
    print(f"Starting Label Studio server on {host}:{port}...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            cmd,
            text=True
        )
        
        # Wait for server to be ready
        url = f"http://{host}:{port}"
        max_retries = 3
        retry_count = 0
        time.sleep(5)
        
        while retry_count < max_retries:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✓ Label Studio server is running at {url}")
                    return process
            except requests.exceptions.RequestException as e:
                print(e)
                
                retry_count += 1
                time.sleep(5)
        
        print(f"⚠ Server started but couldn't verify it's ready. Check {url}")
        return process
    
    except FileNotFoundError:
        print("Error: Label Studio is not installed. Install it with:")
        print("  pip install label-studio")
        sys.exit(1)

def stop_label_studio(process):
    """Stop the Label Studio server."""
    if process:
        process.terminate()
        try:
            process.wait(timeout=5)
            print("✓ Label Studio server stopped")
        except subprocess.TimeoutExpired:
            process.kill()
            print("✓ Label Studio server forcefully stopped")

if __name__ == "__main__":
    # Start the server with default settings
    server_process = start_label_studio(
        host="127.0.0.1",
        port=8000,
        data_dir="tmp/"
    )
    
    try:
        # Keep the server running
        print("\nServer is running. Press Ctrl+C to stop.")
        server_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_label_studio(server_process)