import argparse
import asyncio
import logging
import struct
import sys
import pdb
import os
import logging
from typing import Dict, Optional


from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated


try: 
    import uvloop
except ImportError:
    uvloop = None


# logging.basicConfig(level=logging.DEBUG)


class SSP(QuicConnectionProtocol):
    def quic_event_received(self, event: QuicEvent):
        print("e")
        # if isinstance(event, StreamDataReceived):
        #     print("Data received:", event.data.decode())
        # elif isinstance(event, ConnectionTerminated):
        #     print("Client disconnected:", event.addr)


async def main(
        host:   str,
        port:   int,
        config: QuicConfiguration,
        retry:  bool,
)->None:
    logging.debug("start main")
    await serve(
        host,
        port,
        configuration   = config,
        create_protocol = SSP,
        retry           = retry,
    )
    await asyncio.Future()


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 3:
        print(f"Wrong input values: {argv}")
        exit()

    host = "127.0.0.1" if argv[1] == "d" else argv[1]
    port = 8000        if argv[2] == "d" else int(argv[2])

    config = QuicConfiguration(
        is_client=False,
        max_datagram_frame_size=65536,
    )

    # os.path.isfile("ssl/cert.pem")
    config.load_cert_chain("cert.pem", 
                           "key.pem", 
                           password="kitten",
    )


    logging.debug("uvloop was assigned")
    if uvloop is not None:
        uvloop.install()
        
    logging.debug("main task was added")
    asyncio.run(
        main(
            host=host,
            port=port,
            config=config,
            retry=False,
        )
    )


    
