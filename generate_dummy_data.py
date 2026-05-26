import os
import sys
from datetime import datetime, timedelta, timezone

# Add the client repo to path if running locally
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "psstracker", "aw-client"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "psstracker", "aw-core"))

try:
    from aw_client import ActivityWatchClient
    from aw_core.models import Event
except ImportError:
    print("Error: aw_client or aw_core not found. Run this from within the pss-tracker pipenv.")
    sys.exit(1)

def generate_dummy_data(host="127.0.0.1", port=5700, employee_id="emp001"):
    print(f"Connecting to PSS Tracker server at {host}:{port}...")
    
    # Initialize client (bypassing normal config to connect to specific server)
    client = ActivityWatchClient("dummy-data-generator", testing=False)
    if "https" in host:
        client.server_address = f"{host}:{port}" if port else host
    elif "http" in host:
        client.server_address = f"{host}:{port}" if port else host
    else:
        client.server_address = f"http://{host}:{port}"
    
    # We mock the config lookup for employee ID by monkey-patching
    import aw_client.config
    original_load_config = aw_client.config.load_config
    
    def mock_load_config():
        config = original_load_config()
        config['client'] = {'employee_id': employee_id}
        return config
        
    aw_client.config.load_config = mock_load_config
    
    hostname = "LAPTOP-DUMMY"
    bucket_window = f"aw-watcher-window_{hostname}"
    bucket_afk = f"aw-watcher-afk_{hostname}"
    
    print("Creating buckets...")
    client.create_bucket(bucket_window, "currentwindow")
    client.create_bucket(bucket_afk, "afkstatus")
    
    now = datetime.now(timezone.utc)
    
    print("Generating window events...")
    window_events = []
    apps = [
        ("Google Chrome", "PSS Tracker - Dashboard"),
        ("Visual Studio Code", "main.py - pss-tracker"),
        ("Slack", "General Channel"),
        ("Microsoft Teams", "Daily Standup")
    ]
    
    for i in range(50):
        app, title = apps[i % len(apps)]
        timestamp = now - timedelta(minutes=(50-i)*5)
        event = Event(timestamp=timestamp, duration=timedelta(minutes=4), data={"app": app, "title": title})
        window_events.append(event)
        
    client.insert_events(bucket_window, window_events)
    
    print("Generating AFK events...")
    afk_events = []
    for i in range(50):
        status = "not-afk" if i % 5 != 0 else "afk"
        timestamp = now - timedelta(minutes=(50-i)*5)
        event = Event(timestamp=timestamp, duration=timedelta(minutes=4), data={"status": status})
        afk_events.append(event)
        
    client.insert_events(bucket_afk, afk_events)
    
    print("Dummy data successfully generated!")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5700
    
    if len(sys.argv) > 1:
        if "phylon.in" in sys.argv[1]:
            host = "https://" + sys.argv[1] if not sys.argv[1].startswith("http") else sys.argv[1]
            port = 443
            print(f"Targeting remote server: {host}:{port}")
        else:
            host = sys.argv[1]
            
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        
    generate_dummy_data(host, port)
