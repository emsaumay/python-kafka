# Python Kafka-like Server

This project implements a minimal Kafka-like server in Python from scratch, following a staged approach. Each stage adds new features and capabilities.

## Stage 1: Initial Server
  - Correlation ID
  - API Key
  - API Version
  - Responds with a minimal ApiVersions response

## Stage 2: Concurrent Clients
 - Supports multiple clients connecting simultaneously
 - Handles serial and concurrent requests using threads
 - Each client connection is managed in a separate thread
 - Server can process requests from multiple clients in parallel
### Usage

```bash
python kafka_server.py
```

The server will listen for incoming Kafka protocol requests. This is a minimal implementation for protocol exploration and learning purposes.


## Stage 3: Listing Partitions
 - Includes DescribeTopicPartitions in APIVersions response
 - Handles requests to list partitions for topics
 - Returns stub partition info for unknown, single, and multiple topics/partitions
 - Prepares for more advanced topic/partition handling in future stages

## Next Stages
Further stages will add support for message consumption.

---

For details on the protocol, see [Kafka Protocol Documentation](https://kafka.apache.org/protocol.html).
