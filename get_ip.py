import argparse
from fritzconnection import FritzConnection

def get_external_ip(address, password, user=None):
    try:
        # FritzConnection handles either password or user+password
        fc = FritzConnection(address=address, user=user, password=password)
        res = fc.call_action('WANIPConn1', 'GetExternalIPAddress')
        return res.get('NewExternalIPAddress')
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the external IP address from a Fritz!Box.")
    parser.add_argument("--address", default="192.168.178.1", help="Fritz!Box IP address (default: 192.168.178.1)")
    parser.add_argument("--user", help="Fritz!Box username (optional)")
    parser.add_argument("--password", required=True, help="Fritz!Box password")

    args = parser.parse_args()

    ip = get_external_ip(args.address, args.password, args.user)
    print(f"External IP: {ip}")
