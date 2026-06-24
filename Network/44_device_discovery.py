import json
import socket
import time
from zeroconf import ServiceBrowser, Zeroconf

def process_input(data):
    """
    Scans the local network for services based on JSON input.
    Input format: {"service_type": "_http._tcp.local.", "scan_time": 5}
    """
    try:
        # Parse input (handles both string and dict)
        params = json.loads(data) if isinstance(data, str) else data

        # Default to searching for HTTP services if not specified
        target_service = params.get("service_type", "_http._tcp.local.")
        scan_duration = params.get("scan_time", 3)

        discovered_devices = []

        # Internal listener class to handle mDNS events
        class DiscoveryListener:
            def add_service(self, zc, type_, name):
                info = zc.get_service_info(type_, name)
                if info:
                    # Convert binary addresses to human-readable strings
                    addresses = [socket.inet_ntoa(addr) for addr in info.addresses]
                    discovered_devices.append({
                        "name": name,
                        "server": info.server.strip('.'),
                        "addresses": addresses,
                        "port": info.port,
                        "properties": {k.decode(): v.decode() if isinstance(v, bytes) else v
                                       for k, v in info.properties.items()}
                    })

            def update_service(self, zc, type_, name):
                pass # Optional: handle IP changes during scan

            def remove_service(self, zc, type_, name):
                pass # Optional: handle devices dropping off

        # Initialize Zeroconf and start browsing
        zeroconf = Zeroconf()
        listener = DiscoveryListener()
        browser = ServiceBrowser(zeroconf, target_service, listener)

        # Block the function for the duration of the scan
        #time.sleep(scan_duration)

        # Cleanup
        zeroconf.close()

        return json.dumps({
            "status": "success",
            "found_count": len(discovered_devices),
            "devices": discovered_devices
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Discovery failed: {str(e)}"
        })

# --- Quick Test ---
# if __name__ == "__main__":
#     test_input = '{"service_type": "_http._tcp.local.", "scan_time": 2}'
#     print(process_input(test_input))
