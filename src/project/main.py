import asyncio
from xbcontroller import XbController

# Read known mac address from text file
def get_controller_mac_addr() -> str:
    with open("addr.txt", 'r') as file:
        return file.readline().strip()

async def main():
    controller = XbController(get_controller_mac_addr())

    while(not await controller.establish_connection()):
        continue

if __name__ == "__main__":
    asyncio.run(main())