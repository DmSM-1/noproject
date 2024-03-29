import asyncio
import logging
import sys
import logging
import datetime
import subprocess
import struct


from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent, StreamDataReceived, ConnectionTerminated


try: 
    import uvloop
except ImportError:
    uvloop = None


class colors:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    DEFAULT = '\033[0m'


class SSP(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = []
    
    def quic_send(self, stream_id, message,)->None:
        data = message.encode("utf-8")
        data = struct.pack("!H", len(data))+data
        self._quic.send_stream_data(stream_id, data, end_stream=True)
        self.transmit()

    def quic_event_received(self, event: QuicEvent):
        if isinstance(event,  StreamDataReceived):
            recv_mes = event.data[2:].decode('utf-8')
            print(colors.GREEN +\
                f"|{datetime.datetime.now().strftime(' %H:%M:%S')}|"+\
                colors.DEFAULT+f" {recv_mes}")
            
            self.messages.append(recv_mes)
            self.quic_send(event.stream_id ,recv_mes)
        

    # async def quic_send(self, message)->None:
    # stream_id = self._quic.get_next_available_stream_id()
    # data = message.encode("utf-8")
    # data = struct.pack("!H", len(data))+data
    # self._quic.send_stream_data(stream_id, data, end_stream=False)
    # self.transmit()


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

    config.load_cert_chain("ssl/cert.pem", 
                           "ssl/key.pem", 
                           password="kitten",
    )

    logging.debug("uvloop was assigned")
    if uvloop is not None:
        uvloop.install()
        
    logging.debug("main task was added")
    subprocess.call("clear", shell = True)

    helo = f"Server: host={host}, port={port}"
    print(colors.RED+helo+colors.DEFAULT)
    print(colors.BLUE+"~"*len(helo)+colors.DEFAULT)
    print(colors.RED+"| time    | text"+colors.DEFAULT)

    asyncio.run(
        main(
            host=host,
            port=port,
            config=config,
            retry=False,
        )
    )