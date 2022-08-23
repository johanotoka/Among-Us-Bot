import json
import random

from aiohttp import TraceConnectionQueuedEndParams

file =  open('example code/taskList.json')

data = json.load(file)

#for i in range(7):
#   print(data["Short Task"]["tasks"][f"{random.randint(1,7)}"])

#TODO make sure there are no duplicate tasks when generating random tasks - Fayaz.
#   return value: p0 = [1,2,3,8,10,20] where p(n) is p[layer and n is the player number.
#   tc p0 t5

def get_task():
    tasks=[]
    task_no=[]
    

    
    for i in range(3):  
        x=random.randint(1,7)
        y= random.randint(8,17)
        z=random.randint(18,24)
        task_no.extend([x,y,z])
        tasks.append(data["Short Task"]["tasks"][f"{x}"])
        tasks.append(data["Medium Task"]["tasks"][f"{y}"])
        tasks.append(data["Long Task"]["tasks"][f"{z}"])
    # print("task log ", set(task_no))
    # print(set(tasks))
    return(set(tasks),set(task_no))
    

# pp,cc=get_task()
# print(dict(zip(pp,cc)))

"""

Player - 

Random tasks 
Completed task


Task JSON


"""