class Complex:
    def __init__(self,real_no,imaginary_no):
        self.real_no=real_no
        self.imaginary_no=imaginary_no
    def sumNumber(self):
        print(self.real_no,"i +",self.imaginary_no,"j")

    def __add__(c,c1):
        newReal=c.real_no+c1.real_no
        newimginary=c.imaginary_no+c1.imaginary_no
        return Complex(newReal,newimginary) 


c=Complex(2,3)
c.sumNumber()

c1=Complex(4,6)
c1.sumNumber()

c2=c+c1
c2.sumNumber()