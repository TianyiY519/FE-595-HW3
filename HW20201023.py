# import packages
import pandas as pd
from textblob import TextBlob
from collections import Counter
import os
# set path
path=r'C:/Users/Administrator/Documents/WeChat Files/wxid_r7n7a0b6lrad21/FileStorage/File/2020-10/company/'
# 'companies.txt', 'inputs.txt', 'output-1.txt', 'output.txt', 'web_scrape.txt'
txt_files=[]
for file in os.listdir(path):
    if (file.find('txt')!=-1):
        txt_files.append(file)

# companies.txt
f = open(path+'companies.txt')
txt=f.read()
f.close()
txt_split=txt.split(sep='\n')
names1=[txt_split[3*x+1].replace('Name: ','') for x in range(0,50)]
purpose1=[txt_split[3*x+2].replace('Purpose: ','') for x in range(0,50)]

# inputs.txt
f = open(path+'inputs.txt')
txt=f.read()
f.close()
txt_split=txt.split(sep='\n')
names2=[txt_split[2*x].replace('Name: ','') for x in range(0,50)]
purpose2=[txt_split[2*x+1].replace('Purpose: ','') for x in range(0,50)]

# output-1.txt
f = open(path+'output-1.txt')
txt=f.read()
f.close()
txt_split=txt.split(sep=']\n[')
names3=[txt_split[2*x].replace('[\'Name\', \' ','').replace('\'','').replace('Name,  ','') for x in range(0,50)]
purpose3=[txt_split[2*x+1].replace('[\'Purpose\', \' ','').replace('\'','').replace('Purpose,  ','').replace(']\n','') for x in range(0,50)]

# output.txt
f = open(path+'output.txt')
txt=f.read()
f.close()
txt_split=txt.split(sep=']\n[')
names4=[txt_split[2*x].replace('[\'Name\', \' ','').replace('\'','').replace('Name,  ','') for x in range(0,50)]
purpose4=[txt_split[2*x+1].replace('[\'Purpose\', \' ','').replace('\'','').replace('Purpose,  ','').replace(']\n','') for x in range(0,50)]


# web_scrape.txt
f = open(path+'web_scrape.txt')
txt=f.read()
f.close()
txt_split=txt.split(sep='\n')
names5=[txt_split[3*x].replace('Name: ','') for x in range(0,50)]
purpose5=[txt_split[3*x+1].replace('Purpose: ','') for x in range(0,50)]

names1.extend(names2)
names1.extend(names3)
names1.extend(names4)
names1.extend(names5)

purpose1.extend(purpose2)
purpose1.extend(purpose3)
purpose1.extend(purpose4)
purpose1.extend(purpose5)

# sentiment analysis
polarity=[TextBlob(x).sentiment[0] for x in purpose1]
subjectivity=[TextBlob(x).sentiment[1] for x in purpose1]

# creat dataframe
data=pd.DataFrame({'names':names1,'purpose':purpose1,'polarity':polarity,'subjectivity':subjectivity})
data.to_csv(path+'sentiment score.csv')

# best and worst
print(data.sort_values('polarity')[['names','polarity']]) # sort

# common words
char=''
for txt in purpose1:
    char=char+' '+txt

word_freq=Counter(char.lower().split(' '))
word_freq.most_common(10)
word_freq_df=pd.DataFrame([word_freq.keys(),word_freq.values()])
word_freq_df=pd.DataFrame(word_freq_df.values.T, columns=['words','frequency'])
word_freq_df=word_freq_df.sort_values(by='frequency',ascending =False)
word_freq_df.to_csv(path+'word frequency.csv')