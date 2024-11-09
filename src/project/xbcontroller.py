import asyncio
import aioble

class XbController:
    def __init__(self, addr: str):
        self._addr = addr
        self._device = aioble.Device(aioble.ADDR_PUBLIC, addr)

    async def establish_connection(self) -> bool:
        try:
            await self._device.connect(timeout_ms=2000) # type: ignore
            return True
        except asyncio.TimeoutError:
            return False