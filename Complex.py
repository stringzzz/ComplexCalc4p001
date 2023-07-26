#Class for dealing with Complex number operations

import math

class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
        
    def Mod(self):
        #Modulus
        return math.sqrt(math.pow(self.real, 2) + math.pow(self.imag, 2))
    
    def Arg(self):
        #Argument
        pi_over_two = 3.141592 / 2
        if self.real == 0 and self.imag > 0:
            return pi_over_two
        elif self.real == 0 and self.imag < 0:
            return -pi_over_two
        elif self.real == 0 and self.imag == 0:
            return 0
            
        arg = math.atan(self.imag / self.real)
        if self.real >= 0 and self.imag >= 0:
            return arg
        elif self.real < 0 and self.imag >= 0:
            return arg + 3.141592
        elif self.real < 0 and self.imag < 0:
            return (-(pi_over_two - abs(arg))) - pi_over_two
        else:
            return arg
        
    def Inverse(self):
        #Multiplicative inverse
        temp = Complex(0, 0)
        temp.real = self.real / (math.pow(self.real, 2) + math.pow(self.imag, 2));
        temp.imag = -(self.imag / (math.pow(self.real, 2) + math.pow(self.imag, 2)));
        return temp
    
    def Display(self):
        #Display complex number in form a+bi
        ch = ''
        if self.imag >= 0:
            ch = '+'
        else:
            ch = '-'
        return str("%g" %  self.real) + ch + str("%g" % abs(self.imag)) + "i"
    
    def __add__(self, c_obj):
        #Add 2 Complex number objects with overloaded +
        temp = Complex(0, 0)
        temp.real = self.real + c_obj.real
        temp.imag = self.imag + c_obj.imag
        return temp
    
    def __sub__(self, c_obj):
        #Subtract 1 Complex number object from another with overloaded -
        temp = Complex(0, 0)
        temp.real = self.real - c_obj.real
        temp.imag = self.imag - c_obj.imag
        return temp
    
    def __mul__(self, c_obj):
        #Multiply 2 Complex number objects with overloaded *
        temp = Complex(0, 0)
        temp.real = self.real * c_obj.real - self.imag * c_obj.imag
        temp.imag = self.real * c_obj.imag + self.imag * c_obj.real
        return temp
    
    def __truediv__(self, c_obj):
        #Divide 1 Complex number object by another with overloaded /
        temp = Complex(0, 0)
        temp.real = (self.real * c_obj.real + self.imag * c_obj.imag) / (math.pow(c_obj.real, 2) + math.pow(c_obj.imag, 2))
        temp.imag = (-self.real * c_obj.imag + self.imag * c_obj.real) / (math.pow(c_obj.real, 2) + math.pow(c_obj.imag, 2))
        return temp
        
    def __EQ__(self, c_obj):
        # ==
        return (self.real == c_obj.real and self.imag == c_obj.imag)
    
    def __NE__(self, c_obj):
        # !=
        return not(self == c_obj)
    
    def __neg__(self):
        #Unary negation
        temp = Complex(0, 0)
        temp.real = -self.real
        temp.imag = -self.imag
        return temp
    
    def Pow(self, exp):
        #Complex number raised to a real number exponent
        temp = Complex(0, 0)
        temp.real = math.pow(self.Mod(), exp) * math.cos(exp * self.Arg())
        temp.imag = math.pow(self.Mod(), exp) * math.sin(exp * self.Arg())
        return temp
    
    def cPow(self, c_obj):
        #Complex number raised to a complex number exponent
        temp = Complex(0, 0)
        temp.real = math.pow(self.Mod(), c_obj.real) * math.exp(-c_obj.imag * self.Arg()) * math.cos(c_obj.real * self.Arg() + c_obj.imag * math.log(self.Mod()))
        temp.imag = math.pow(self.Mod(), c_obj.real) * math.exp(-c_obj.imag * self.Arg()) * math.sin(c_obj.real * self.Arg() + c_obj.imag * math.log(self.Mod()))
        return temp
    
    def Base(self, n):
        #n^(Complex number)
        temp = Complex(0, 0)
        temp.real = math.pow(n, self.real) * math.cos(self.imag * math.log(n))
        temp.imag = math.pow(n, self.real) * math.sin(self.imag * math.log(n))
        return temp
    
    def Sin(self):
        #Complex form of sine function
        temp = Complex(0, 0)
        temp.real = (math.sin(self.real) / 2) * (math.exp(-self.imag) + math.exp(self.imag))
        temp.imag = -(math.cos(self.real) / 2) * (math.exp(-self.imag) - math.exp(self.imag))
        return temp
    
    def Cos(self):
        #Complex form of cosine function
        temp = Complex(0, 0)
        temp.real = (math.cos(self.real) / 2) * (math.exp(-self.imag) + math.exp(self.imag))
        temp.imag = (math.sin(self.real) / 2) * (math.exp(-self.imag) - math.exp(self.imag))
        return temp
    
    def Tan(self):
        #Complex form of tangent function, just uses the identity sin(x)/cos(x)
        return self.Sin() / self.Cos()
    
    def Exp(self):
        #e^(Complex number)
        temp = Complex(0, 0)
        temp.real = math.exp(self.real) * math.cos(self.imag)
        temp.imag = math.exp(self.real) * math.sin(self.imag)
        return temp
    
    def Log(self):
        #Principal logarithm of complex number
        temp = Complex(0, 0)
        temp.real = math.log(self.Mod())
        temp.imag = self.Arg()
        return temp
