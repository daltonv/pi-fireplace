"""MPV integration boundary.

Your task: design and implement a small client for MPV's JSON IPC socket.

Questions to explore:
- How do you locate/configure the socket?
- What if MPV isn't running or the socket disappears?
- Do you want synchronous or asynchronous IPC?
- How will you validate property values and handle failures?

This module deliberately contains no implementation.
"""

import asyncio
import json
from pathlib import Path


class MpvClient:
    def __init__(self, socket_path: Path):
        self.socket_path = socket_path

    async def command(self, *args: object):
        reader, writer = await asyncio.open_unix_connection(str(self.socket_path))

        # TODO: add request_id field for better async handeling
        command = {"command": list(args)}

        writer.write(json.dumps(command).encode() + b"\n")
        await writer.drain()

        data = await reader.read(1024)  # Read up to 1024 bytes
        data_obj = json.loads(data)

        writer.close()
        await writer.wait_closed()

        print(data_obj)

        if data_obj["error"] != "success":
            raise RuntimeError(f"MPV command failed: {data_obj['error']}")

        return data_obj.get("data")

    async def get_property(self, name: str):
        data = await self.command("get_property", name)
        return data

    async def set_property(self, name: str, value: object):
        await self.command("set_property", name, value)

    async def pause(self):
        await self.set_property("pause", True)

    async def resume(self):
        await self.set_property("pause", False)
