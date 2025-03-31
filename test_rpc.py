import json
import requests

def test_rpc_call():
    url = "http://localhost:3000/jsonrpc"
    headers = {'content-type': 'application/json'}
    
    # Test payload for tool/list
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tool/list",
        "params": {}
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Connection Error: Failed to connect to the server")
        return False

if __name__ == "__main__":
    print("Testing RPC connection...")
    success = test_rpc_call()
    print(f"\nTest {'succeeded' if success else 'failed'}") 