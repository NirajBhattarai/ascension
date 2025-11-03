## Travily Agent (A2A JSON-RPC)

### Run the agent server

```bash
cd backend/agents/travily
uv run .
```

Server starts at `http://0.0.0.0:9999/`.

### Send a non-streaming request (message/send)

```bash
curl --location 'http://0.0.0.0:9999/' \
  --header 'Content-Type: application/json' \
  --data '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": {
      "message": {
        "kind": "message",
        "message_id": "00000000-0000-0000-0000-000000000001",
        "role": "user",
        "parts": [
          { "kind": "text", "text": "testing" }
        ]
      }
    }
  }'
```

### Send a streaming request (message/stream)

```bash
curl --location 'http://0.0.0.0:9999/' \
  --header 'Content-Type: application/json' \
  --header 'Accept: text/event-stream' \
  --no-buffer \
  --data '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/stream",
    "params": {
      "message": {
        "kind": "message",
        "message_id": "00000000-0000-0000-0000-000000000002",
        "role": "user",
        "parts": [
          { "kind": "text", "text": "testing" }
        ]
      }
    }
  }'
```

The sample executor returns a single text message: "Travily Agent is running".


