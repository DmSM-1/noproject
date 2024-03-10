import argparse
import asyncio
import logging
import struct
import sys
import pdb
import os
import logging
import ssl


from aioquic.asyncio.client import connect
from aioquic.asyncio import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated


class Protocol(QuicConnectionProtocol):
    pass


async def main(
        config: QuicConfiguration,
        host: str,
        port: int,
        message: str,
        local_port: int,
)->None:
    async with connect(
        host,
        port,
        configuration=config,
        local_port=local_port,
        wait_connected= True,
    ) as client:
        pass
    

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 4:
        print(f"Wrong input values: {argv}")
        exit()

    host = "127.0.0.1" if argv[1] == "d" else argv[1]
    port = 8000        if argv[2] == "d" else int(argv[2])
    uport= 2000        if argv[3] == "d" else int(argv[3])

    config = QuicConfiguration(
        is_client=True,
        max_datagram_frame_size=65536,
    )
    config.verify_mode = ssl.CERT_NONE
        
    logging.debug("main task was added")
    asyncio.run(
        main(
            host=host,
            port=port,
            config=config,
            message="1",
            local_port=uport,
        )
    )


