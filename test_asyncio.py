import time 
import asyncio

async def exe_calculate_async(name, n):
    for i in range(1, n + 1):
        print(f'{name} => {i} of {n} is calculating...')
        await asyncio.sleep(1)
    print(f'{name} - {n} working done!')

async def process_async():
    start = time.time()

    await asyncio.wait([
        exe_calculate_async('one', 3),
        exe_calculate_async('two', 2),
        exe_calculate_async('three', 1)
    ])

    end = time.time()

    print(f'total second : {end - start}')

# def exe_calculate_sync(name, n):
#     for i in range(1, n + 1):
#         print(f'{name} => {i} of {n} is calculating...')
#         time.sleep(1)
#     print(f'{name} - {n} working done!')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(process_async())
    # asyncio.run(process_async())
    pass
