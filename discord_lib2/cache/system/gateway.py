class Gateway:
  gateway_url: str = ""
  heartbeat_sended: int = 0 # counter
  heartbeat_recved: int = 0 # counter
  heartbeat_interval: int = -1
  last_recv_seq: int | None = None