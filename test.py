import pdb
import asyncio
import struct
import argparse

from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived

class Protocol(QuicConnectionProtocol):
    def quic_event_received(self, event: QuicEvent):
        if isinstance(event, StreamDataReceived):
            length = struct.unpack("!H", bytes(event.data[:2]))[0]
            data = int.to_bytes(2, length)
            sata = struct.pack("!H", len(data)) + data

            self._quic.send_stream_data(event.stream_id, data, end_stream=True)
        pass


# pdb.set_trace()
async def main(host: str, port: int) -> None:
    configuration = QuicConfiguration(is_client = False)

    await serve(
        host = host,
        port = port,
        configuration = configuration,
        create_protocol = Protocol,
    )
    
    print(f"server listenng on {host}:{port}")

    await asyncio.Future()
    
    
# pdb.set_trace()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Server")
    parser.add_argument("--host", type = str, default = "127.0.0.1", help = "Anyway, you are doing it in alone")
    parser.add_argument("--port", type = int, default = 6325, help = "Alas, it is a truth")

    args = parser.parse_args()

    asyncio.run(main(args.host, args.port))