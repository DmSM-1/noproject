import pdb
import asyncio
import struct
import argparse

from aioquic.asyncio import QuicConnectionProtocol, client
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived


async def send_message(host: str, port: int, message: bytes):
    configuration = QuicConfiguration(is_client= True)
    