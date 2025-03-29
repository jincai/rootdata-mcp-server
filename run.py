#!/usr/bin/env python
import os
import socket
import random
import sys
import subprocess

def find_available_port(start_port=8000, max_port=9000):
    """Find an available port by checking a range of ports"""
    # First try the specified start_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', start_port))
            s.close()
            return start_port
        except OSError:
            # Port is not available
            pass
    
    # If start_port is not available, try random ports in the range
    ports_to_try = list(range(start_port + 1, max_port))
    random.shuffle(ports_to_try)  # Randomize to reduce collision chance
    
    for port in ports_to_try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                s.close()
                return port
            except OSError:
                continue
    
    raise RuntimeError(f"No available ports found in range {start_port}-{max_port}")

def main():
    # Get port from environment variable or find an available port
    port = os.getenv("PORT")
    if port:
        port = int(port)
    else:
        port = find_available_port()
    
    # Determine if reload mode should be enabled
    use_reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"Starting server on port {port} (reload mode: {use_reload})")
    
    # Build the uvicorn command
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "server:app", 
        "--host", "0.0.0.0", 
        "--port", str(port)
    ]
    
    if use_reload:
        cmd.append("--reload")
    
    # Run the server
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
