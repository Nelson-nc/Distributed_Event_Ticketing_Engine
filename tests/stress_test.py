import concurrent.futures
import requests


EVENT_ID = 1
URL = f"http://127.0.0.1:8000/api/events/{EVENT_ID}/reserve/"

def make_reservation(user_id):
    try:
        # Simulate a unique user making a request
        response = requests.post(f"{URL}?user_id={user_id}")
        return f"User {user_id}: Status {response.status_code} -> {response.json().get('message' or 'error')}"
    except Exception as e:
        return f"User {user_id}: Failed -> {e}"

def run_stress_test():
    print("🚀 Simulating a high-traffic ticket drop...")
    print("Targeting an event with only 3 tickets remaining using 20 concurrent buyers...\n")
    
    # Create a pool of concurrent threads running at the same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Assign user IDs 1 through 20
        user_ids = list(range(1, 21))
        
        # Fire all requests concurrently!
        results = executor.map(make_reservation, user_ids)
        
        for result in results:
            print(result)

if __name__ == "__main__":
    run_stress_test()