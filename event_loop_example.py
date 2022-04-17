import asyncio
 
async def coroutine1():
    print("Hello coroutine1!")
    return "return coroutine1"
 
async def coroutine2():
    print("Hello coroutine2!")
    return "return coroutine2"
 
async def coroutine3():
    print("Hello coroutine3!")
    await asyncio.sleep(5)
    return "return coroutine3"
 
async def main():
    # 코루틴 실행 결과(리턴값)가 coroutine_list 변수에 list로 담긴다.
    coroutine_list = await asyncio.gather(coroutine1(), coroutine2(), coroutine3())
    print(coroutine_list)
 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
