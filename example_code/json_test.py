from itertools import count
import json
import random

from aiohttp import TraceConnectionQueuedEndParams

file =  open('example_code/taskList.json')

data = json.load(file)

#for i in range(7):
#   print(data["Short Task"]["tasks"][f"{random.randint(1,7)}"])

#TODO make sure there are no duplicate tasks when generating random tasks - Fayaz.
#   return value: p0 = [1,2,3,8,10,20] where p(n) is p[layer and n is the player number.
#   tc p0 t5

def get_task():
    tasks=[]
    task_no=set()
    

    
    for i in range(3):  
        x=random.randint(1,7)
        y= random.randint(8,17)
        z=random.randint(18,24)
        task_no.update([x,y,z])
    
    for i in task_no:
        tasks.append(data["tasks"][f"{i}"])
       
    # print("task log ", set(task_no))
    # print(set(tasks))
    print("tasks = ", tasks, "\n ",task_no)
    return(tasks,task_no)


def get_task_dict():
    return data['tasks']     

# pp,cc=get_task()
# get_task_dict()
# print(dict(zip(pp,cc)))


print(get_task_dict())
"""

Player - 

Random tasks 
Completed task


Task JSON


"""