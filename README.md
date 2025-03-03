# Python Kafka-like Server

This project implements a minimal Kafka-like server in Python from scratch, following a staged approach. Each stage adds new features and capabilities.

## Stage 1: Initial Server
- Binds to a port (default: 127.0.0.1:9092)
- Accepts TCP connections
- Parses incoming requests for:
  - Correlation ID
  - API Key
  - API Version
- Handles ApiVersions requests (API key 18)
  - Responds with a minimal ApiVersions response
- Sends error responses for unknown API keys

### Usage

```bash
python kafka_server.py
```

The server will listen for incoming Kafka protocol requests. This is a minimal implementation for protocol exploration and learning purposes.

## Next Stages
Further stages will add support for concurrent clients, partition listing, and message consumption.

---

For details on the protocol, see [Kafka Protocol Documentation](https://kafka.apache.org/protocol.html).
