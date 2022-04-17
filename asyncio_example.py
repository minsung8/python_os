import asyncio

async def fetch_data():

    print('start fetch data')

    await asyncio.sleep(2)

    print('end fetch data')

async def print_numbers():
    for i in range(1, 11):
        print(i)
        await asyncio.sleep(0.5)

async def main():
    
    task1 = asyncio.create_task(print_numbers())
    task2 = asyncio.create_task(fetch_data())

    await task1

asyncio.run(main())
