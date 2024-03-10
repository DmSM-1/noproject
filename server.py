import argparse
import asyncio
import logging
import struct
import sys
import pdb
from typing import Dict, Optional

from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived
from aioquic.quic.logger import QuicFileLogger
from aioquic.tls import SessionTicket


class SSP(QuicConnectionProtocol):
    pass


async def main(
        host:   str,
        port:   int,
        config: QuicConfiguration,
        retry:  bool,
)->None:
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

    host = "127.0.0.1" if argv[0] != "d" else argv[0]
    host = 8000 if not argv[1] else argv[1]

    
        


    
