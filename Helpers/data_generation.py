import pandas as pd
import random
import pandas as pd
import numpy as np
import random
import re

sample_size = 53333
df_raw = pd.read_csv('../Data/Arabic_names.csv')



Mname=[]
with open('../Data/mnames.txt','r',encoding="utf8") as f:
    Mname=f.readlines()

Fname=[]
with open('../Data/fnames.txt','r',encoding="utf8") as f:
    Fname=f.readlines()


Mname=[name.replace('\n','') for name in Mname]
Fname=[name.replace('\n','') for name in Fname]




all_names = list(df_raw['Name'].values)
male =df_raw[df_raw['Gender']=='M']['Name'].values
female = df_raw[df_raw['Gender']=='F']['Name'].values
all_char = list(set(re.findall(r'[\u0600-\u06FF]',str(all_names)))) +['']

choice  =[False,True,False,True,False,False]
def generate_negative_sample():
    
    names = []
    negative = 0
    for i in range(0,3):
        edit = random.choice(choice)
        idx = random.randint(0, len(all_names)-1)
        name = all_names[idx]
    
        if edit:
            negative +=1
            char = random.randint(0, len(name)-1)
            noise_char = random.choice(all_char)
            name = list(name)
            name[char] = noise_char
            name = "".join(name)
        names.append(name)     
    if negative:
        return " ".join(names)
    else:
        return " "
 
def generate_positive_sample():
    
    gender = random.choice(['male','female'])
    name = []
    if gender == 'male':
        first = random.choice(male)
    else:
        first = random.choice(female)
    second = random.choice(male)
    last = random.choice(male)
    return first + ' ' + second + ' ' + last






def generate_Fake_name():
    rand = random.randint(0,20)
    if rand%2==0:
        random1 = random.randint(0,len(Fname)-1)
        Name1 = Fname[random1]
    else:
        random1 = random.randint(0,len(Mname)-1)
        Name1 = Mname[random1]
    
    cl=Mname
    if rand%5==0:
        cl = Mname
    else:
        cl= Fname
    random2 = random.randint(0,len(Fname)-1)
    Name2 = cl[random2]

    random3 = random.randint(0,len(cl)-1)
    Name3 = cl[random3]

    return Name1+" "+Name2+" "+Name3


real_names = []
fake_names = []

for i in range(sample_size):
    real_names.append(generate_positive_sample())
    real_names.append(generate_positive_sample())


    fake_names.append(generate_Fake_name())
    fake_names.append(generate_negative_sample())

real_names=list(set(real_names))
fake_names=list(set(fake_names))

data = {'name':real_names + fake_names,
        'status':list(np.ones(len(real_names))) + list(np.zeros(len(fake_names)))}

df_1 = pd.DataFrame(data)
df_1 = df_1.sample(frac = 1)

df_1.to_csv('../Data/test.csv')