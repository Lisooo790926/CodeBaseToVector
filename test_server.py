#!/usr/bin/env python3

import json
import sys

# Initialize request
init_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "0.1.0",
        "capabilities": {},
        "clientInfo": {
            "name": "test",
            "version": "1.0.0"
        }
    }
}

# List tools request
list_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
}

# Send requests
print(json.dumps(init_request))
print(json.dumps(list_request)) 