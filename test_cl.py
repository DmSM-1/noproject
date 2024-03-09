import pdb
import asyncio
import struct
import argparse

from aioquic.asyncio import QuicConnectionProtocol, connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived


async def send_message(host: str, port: int, message: bytes):
    configuration = QuicConfiguration(is_client= True)

    # pdb.set_trace()
    async with connect(
        host = host,
        port = port,
        configuration = configuration,
    ) as conn:
        # pdb.set_trace()
        stream_id = conn._quic.get_next_available_stream_id()
        stream    = conn._quic._get_or_create_stream_for_send()
        conn._quic.send_stream_data(stream_id, message, end_stream=True)
        pdb.set_trace()
        conn.transmit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Client")
    parser.add_argument("--host", type = str, default = "127.0.0.1", help = "Anyway, you are doing it in alone")
    parser.add_argument("--port", type = int, default = 6325, help = "Alas, it is a truth")

    args = parser.parse_args()

    data = input("Enter message: ")
    data = data.encode("utf-8")
    data = struct.pack("!H", len(data)) + data

    asyncio.run(send_message(args.host, args.port, data))