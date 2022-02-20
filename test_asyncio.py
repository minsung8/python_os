import time 
import asyncio

def process_async():
    start = time.time()

    exe_calculate_sync('one', 3)
    exe_calculate_sync('two', 2)
    exe_calculate_sync('three', 1)

    end = time.time()

    print(f'total second : {end -time}')

def exe_calculate_sync():
    pass

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(process_async())
    # asyncio.run(process_async())
    pass
