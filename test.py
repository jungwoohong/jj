import asyncio
from datetime import datetime
from random import randint

async def run_job() -> None:
    delay = randint(5, 15)
    print(f'{datetime.now()} sleep for {delay} seconds')
    #await asyncio.sleep(delay)  # 5~15초 동안 잠자기
    print(f'{datetime.now()} finished ({delay} sec)')

async def main() -> None:
    
	asyncio.create_task(run_job())
	#await asyncio.sleep(10)

asyncio.run(run_job())