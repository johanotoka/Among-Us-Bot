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
    

    #We want 4 short tasks, 1 medium and 1 long
    while (len(task_no) < 4):
        x=random.randint(1,7)
        if (x not in task_no):
            task_no.update([x])
    
    #for i in range(4):  
    #    x=random.randint(1,7)
    #    task_no.update([x])
    
    y= random.randint(8,11)
    z=random.randint(12,15)
    task_no.update([y,z])

    for i in task_no:
        tasks.append(data["tasks"][f"{i}"])

    #Two common tasks   
    tasks.append(data["tasks"]["16"])
    tasks.append(data["tasks"]["17"])
    task_no.update([16,17])

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