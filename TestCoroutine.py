import datetime
import logging
import os
import asyncio
from os import path as fs
import random

from log.MyLog import log


async def openFile():
    dir = r"G:\WorkSpaceXXX"
    path = r"G:\WorkSpaceXXX\text.txt"
    pic = r"C:\Users\Administrator\Pictures\781556526281276530.png"
    print(f"curdir={path} cwd={os.getcwd()}")
    acc = os.access(path=path, mode=os.R_OK)
    exist = fs.exists(path)
    listFiles(dir)

    print(f"acc={acc} exist={exist}")
    f = open(path, mode="r+",)
    f.seek(0)
    line = f.readlines()
    print(f"pre read lines list={line}")
    # f.mode='w+'
    f.seek(10)
    f.truncate()
    f.seek(0)

    print(f"after truncate={f.read()}")
    for i in range(10):
        f.write(f"write string {i}\n")
    # 读取整个文件
    f.seek(0)
    line = f.read()
    print(f"content:\n{line} ")
    f.close()
    d = await generateData()
    print(f"load read end {d}")

    # copyPngFile(pic)
    return


def listFiles(dir):
    dirs = os.listdir(dir)
    # for fl in dirs:
    #     print(f"file={fl}")
    print(f"file size={len(dirs)}")


def copyPngFile(pic):
    p = open(pic, "rb")
    cp = open(fs.join("cp.png"), "wb")

    data = 1
    while (data):
        data = p.readline()  # 单行字符串读取
        print(data)
        cp.write(data)
        if not data:
            break
    p.close()
    cp.close()


async def generateData():

    d = "yiedlData"
    print(d)
    await asyncio.sleep(1)
    return d


async def worker(index):
    '''多任务并发的任务'''
    randomTime = random.uniform(0.1, 2.0)
    print(f"index={index} start sleep.. {randomTime}")
    await asyncio.sleep(randomTime)
    print(f"index={index} finished")

    return index


async def concurrentCall():
    '''多任务并发的demo调用'''
    workers = [worker(i) for i in range(10)]
    result = await asyncio.gather(*workers)
    for item in result:
        print(f"result={item}")
    return result


async def main():
   

    # openFile()
    await concurrentCall()
    log("succes")
    return


# 协程入口
asyncio.run(main())
