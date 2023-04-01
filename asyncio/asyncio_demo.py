#series of examples of using asyncio
import asyncio
import time
import queue

#using asyncio code can be written to run concurrently
#blocking operations appear to be running in the background even though it all runs on a single thread

#this method prints 1,2,3 but with a 500ms delay between each print
#in total it will take about 1 second to complete and will block
def print123_synchronous():
    print(1)
    time.sleep(0.5)
    print(2)
    time.sleep(0.5)
    print(3)
print("running synchronously")
print123_synchronous()

#if you wanted to run two instances of print123_synchronous in parallel you could run 
#each on a separate thread
#alternatively you can rewrite the function to use asyncio and get concurrent execution on a single thread
#the use of the async keyword makes this a coroutine (cooperating routine)
#a couroutine can contain await statements.
#the way it effectively works is that the function pauses at await points. The statement to the right of the await is
#evaluated, returning a future. once this is complete the coroutine is resumed.
#in this way the CPU is never blocking for 0.5 second as in the synchronous example, but can get on doing other tasks
#the statement to the right of the await must be an awaitable object
async def print123_async():
    print(1)
    #the await will cause the function to return immediately here
    await asyncio.sleep(0.5)
    print(2)
    await asyncio.sleep(0.5)
    print(3)
        
#calling the method no longer executes it but instead returns a couroutine object
#this object manages the execution of the method in parts. It keeps track of state and allows it to be paused/resumed at
#await points
coroutine_object = print123_async()

#the coroutine can be run by passing it to asyncio.run. This will wait for its completion
#the output will be identical to running it synchronously
print("running asynchronously")
asyncio.run(coroutine_object)

#behind the scenes asyncio.run creates a task wrapping the couroutine object
#an event loop is used to process all active tasks
#in this way multiple tasks can be run concurrently
#async.gather can be used to await the completion of multiple coroutines
async def parallel():
    #this will run both print10 tasks in parallel
    await asyncio.gather(print123_async(), print123_async())
#output will be 1,1,2,2,3,3 - both couroutines executing concurrently
print("running 2 tasks concurrently")
asyncio.run(parallel())

#because async.gather is awaitable it is possible to chain 
#async.gather isn't a coroutine - it returns a Future, but this is another type of awaitable object
async def parallel2():
    #this will run two parallel tasks in parallel
    await asyncio.gather(parallel(), parallel())
#output will be 1,1,2,2,3,3 - both couroutines executing concurrently
print("running 2 tasks concurrently that each run 2 tasks concurrently (4 tasks concurrently)")
asyncio.run(parallel2())

#a major advantage of using asyncio to run tasks concurrently rather than separate threads is that the execution
#is automatically threadsafe
#for example here is a producer writing numbers to a queue and consumer pulling the numbers out and printing them
#there is no need for any threadsafe handling for accessing the queue
print("running async producer/consumer")
#an asynchronous queue is used. This provides methods that are awaitable.
q = asyncio.Queue()
#the producer adds 0 to 9 to the queue with a delay between each add
async def producer(q):
    for i in range(6):
        await q.put(i)
        await asyncio.sleep(0.5)

#the consumer removes and prints items from the queue as fast as they are produced
async def consumer(q):
    for i in range(6):
        a = await q.get()
        print(a)

async def m():
    #this will run two parallel tasks in parallel
    await asyncio.gather(producer(q), consumer(q))
asyncio.run(m())

#the above example used asynchronous queue which handily provides the awaitable put and get
#if you need to use a non async supporting object its possible to make a blocking method awaitable by
#running just that method on another thread. Of course then you have to worry about thread-safety.
#here is an example that does using the non-asynchronous python queue. In this case the python queue is threadsafe anyway.
print("running async producer/consumer using blocking queue")
q = queue.Queue()
async def producer2(q):
    for i in range(6):
        q.put(i)
        await asyncio.sleep(0.5)

async def consumer2(q):
    for i in range(6):
        #run get on a separate thread wrapped in a coroutine that can be awaited
        a = await asyncio.to_thread(q.get)
        print(a)     
async def m2():
    await asyncio.gather(producer2(q), consumer2(q))
asyncio.run(m2())

#the event loop that drives asyncio can be obtained from within a coroutine and used
#to insert tasks or callbacks. In this case below a callback is scheduled to be run on the next
#iteration of the event loop
#there's also call_at and call_later functions that can be used to schedule the call
print("event loops")
def callback(argument):
    print("callback " + argument)

async def test1():
    print("a")
    await asyncio.sleep(1)
    print("b")
    event_loop = asyncio.get_running_loop()
    event_loop.call_soon(callback, "arg")
    await asyncio.sleep(2)
    print("c")

asyncio.run(test1())
#output will be
#a
#b
#callback arg
#c

#an async generator can be created where each value obtains can be awaited
#simulate an async receive, just return the input after a 1 second delay
print("async generator")
async def recv_data(data):
    await asyncio.sleep(1)
    return data
async def generator_coroutine():
    for i in range(4):
        data = await recv_data(i)
        yield data
async def caller():
    async_generator=generator_coroutine()
    async for data in async_generator:
        print(data)
asyncio.run(caller())