year=[]
for i in range(1947,2026):
    if(i%4==0 and i%100!=0) or (i%400==0):
        year.append(i)
    print(year)