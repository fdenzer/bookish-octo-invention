import argparse
import socket
from fritzconnection import FritzConnection

def resolve_local_camera(hostname="camera.local"):
    try:
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.gaierror:
        return None

def get_external_ip(address, password, user=None):
    try:
        fc = FritzConnection(address=address, user=user, password=password)
        res = fc.call_action('WANIPConn1', 'GetExternalIPAddress')
        return res.get('NewExternalIPAddress')
    except Exception as e:
        return f"Error retrieving external IP: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find local camera and get Fritz!Box external IP.")
    parser.add_argument("--address", default="192.168.178.1", help="Fritz!Box IP address (default: 192.168.178.1)")
    parser.add_argument("--user", help="Fritz!Box username (optional)")
    parser.add_argument("--password", required=True, help="Fritz!Box password")
    parser.add_argument("--camera", default="camera.local", help="Camera hostname (default: camera.local)")
    parser.add_argument("--port", type=int, default=81, help="Camera port (default: 81)")

    args = parser.parse_args()

    print(f"--- FritzStream Publisher ---")

    # 1. Resolve local camera
    print(f"Looking for camera at {args.camera}...")
    local_ip = resolve_local_camera(args.camera)
    if local_ip:
        print(f"Found camera locally at: {local_ip}")
    else:
        print(f"Warning: Could not resolve {args.camera} locally. Ensure it's powered on and mDNS is working.")

    # 2. Get external IP
    print(f"Connecting to Fritz!Box at {args.address}...")
    external_ip = get_external_ip(args.address, args.password, args.user)

    if external_ip and not external_ip.startswith("Error"):
        print(f"External IP found: {external_ip}")
        print(f"\nYour stream should be accessible at:")
        print(f"http://{external_ip}:{args.port}/stream")
        print(f"\nUpdate your index.html or use the 'Update Stream URL' button on the site.")
    else:
        print(external_ip)
