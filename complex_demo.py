class Complex:
    def __init__(self, real_no, imaginary_no):
        self.real_no = real_no
        self.imaginary_no = imaginary_no

    def sumNumber(self):
        print(self.real_no, "i +", self.imaginary_no, "j")

    def __add__(self, other):
        return Complex(self.real_no + other.real_no, self.imaginary_no + other.imaginary_no)


if __name__ == "__main__":
    c = Complex(2, 3)
    c.sumNumber()

    c1 = Complex(4, 6)
    c1.sumNumber()

    c2 = c + c1
    c2.sumNumber()
