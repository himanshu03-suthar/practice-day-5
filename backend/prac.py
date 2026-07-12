class Subjects:
    def __init__(self,maths,science,sanskrit,accounts):
        self.maths=maths
        self.science=science
        self.sanskrit=sanskrit
        self.accounts=accounts
        self.percentage=str((self.maths+self.science+self.sanskrit+self.accounts)/4)+"%"

s=Subjects(18,19,15,11)
s.percentage
print(s.percentage)