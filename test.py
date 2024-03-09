import pdb
import asyncio
import argparse
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration

class Protocol(QuicConnectionProtocol):
    pass

# pdb.set_trace()
async def main(host: str, port: int):
    print(host, port)
    configuration = QuicConfiguration(is_client = False)

    await serve(host = host,
                     port = port,
                     configuration = configuration,
                     create_protocol = Protocol,)
    
    print(f"server listenng on {host}:{port}")
    
# pdb.set_trace()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Server")
    parser.add_argument("--host", type = str, default = "127.0.0.1", help = "Anyway, you are doing it in alone")
    parser.add_argument("--port", type = int, default = 6325, help = "Alas, it is a truth")

    args = parser.parse_args()

    asyncio.run(main(args.host, args.port))