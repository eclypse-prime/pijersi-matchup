import asyncio
from os import PathLike
from typing import Union

class Engine:
    """A class encapsulating a UGI engine process with methods to send commands and receive stdout."""

    def __init__(self, path: Union[str, bytes, PathLike], name = ''):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.__async_start_process(path))
        self.name = name

    def send_command(self, command: str, expect: str = '', timeout: float = 60) -> list[str]:
        return self.loop.run_until_complete(self.__async_send_command(command, expect, timeout))

    async def __async_start_process(self, path: Union[str, bytes, PathLike]) -> None:
        self.process = await asyncio.subprocess.create_subprocess_exec(path, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)

    async def __async_send_command(self, command: str, expect: str = '', timeout: float = 60) -> list[str]:
        result = []
        self.process.stdin.write((command + '\n').encode('utf-8'))
        if expect != '':
            expect_detected = False
            while not expect_detected:
                out = await self.process.stdout.read(2048)
                lines: str = out.decode().strip().split('\n')
                for line in lines:
                    if line != '':
                        result.append(line)
                        if expect in line:
                            expect_detected = True
                            break
        return result

    def __del__(self):
        self.process.kill()