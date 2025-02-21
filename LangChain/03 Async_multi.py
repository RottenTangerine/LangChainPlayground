from utils.LLM import model
import asyncio


async def async_stream1():  # 必须要套在一个async方法内
    chunks = []
    async for chunk in model.astream("天空是什么颜色的"):
        chunks.append(chunk)

        if len(chunks) == 2:
            print(chunks[1])
        print(chunk.content, end="|", flush=True)


async def async_stream2():  # 必须要套在一个async方法内
    chunks = []
    async for chunk in model.astream("讲个笑话"):
        chunks.append(chunk)

        if len(chunks) == 2:
            print(chunks[1])
        print(chunk.content, end="|", flush=True)


async def main():
    # 同步调用
    # await async_stream1()
    # await async_stream2()

    # 异步调用
    await asyncio.gather(async_stream1(), async_stream2())


if __name__ == "__main__":
    asyncio.run(main())