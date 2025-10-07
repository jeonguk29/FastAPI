import asyncio

async def func1():
    print("func1: Start")
    await asyncio.sleep(2)  # 비동기로 2초간 대기
    print("func1: End")

async def func2():
    print("func2: Start")
    await asyncio.sleep(1)  # 비동기로 1초간 대기
    print("func2: End")

async def main():
    await asyncio.gather(func1(), func2())  # func1과 func2를 동시에 실행
    # 위 코드의 비동기 작업이 완료 될때까지 기다리고 아래 코드가 있다면 실행
    print("비동기 작업 끝")
if __name__ == "__main__":
    asyncio.run(main())