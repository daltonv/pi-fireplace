import pytest
import asyncio
from pathlib import Path
from pi_fireplace.services.mpv import MpvClient


@pytest.fixture(scope="session")
async def mpv_process(tmp_path_factory: pytest.TempPathFactory):
    socket_path = tmp_path_factory.mktemp("mpv") / "fireplace-mpv.sock"
    process = await asyncio.create_subprocess_exec(
        "mpv",
        "--no-terminal",
        "--no-config",
        "--idle=yes",
        "--vo=null",
        "--ao=null",
        f"--input-ipc-server={socket_path}",
    )

    try:
        # Wait for mpv to accept connections before starting tests.
        async with asyncio.timeout(5):
            while True:
                if process.returncode is not None:
                    raise RuntimeError("mpv exited before its socket was ready")
                try:
                    _, writer = await asyncio.open_unix_connection(socket_path)
                except (FileNotFoundError, ConnectionRefusedError):
                    await asyncio.sleep(0.05)
                else:
                    writer.close()
                    await writer.wait_closed()
                    break

        yield socket_path
    finally:
        if process.returncode is None:
            process.terminate()
        await process.wait()


@pytest.fixture(scope="module")
def mpv_client(mpv_process: Path):
    return MpvClient(mpv_process)


async def test_bad_command(mpv_client: MpvClient):
    with pytest.raises(RuntimeError):
        await mpv_client.command("bad_command")


async def test_pause(mpv_client: MpvClient):
    await mpv_client.set_property("pause", False)

    await mpv_client.pause()

    assert await mpv_client.get_property("pause") is True
