import queue
tsq = queue.PriorityQueue()
tsq.put_nowait(((0, 1.1),{'task_name': 'aaa'})) 
tsq.put_nowait(((0, 1.0), {'task_name', 'bbbb'})) 

print(tsq.get())