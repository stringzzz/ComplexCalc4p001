 #   ComplexCalc 4.001 GUI Calculator for dealing with basic operations on/with complex numbers
 #   Copyright (C) 2023 stringzzz

 #   This program is free software: you can redistribute it and/or modify
 #   it under the terms of the GNU General Public License as published by
 #   the Free Software Foundation, either version 3 of the License, or
 #   (at your option) any later version.

 #   This program is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.

 #   You should have received a copy of the GNU General Public License
 #   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#Complex Calculator Version 4.001
#by stringzzz
#Ghostwarez Co.
#Version 4.001 'complete' date: 07-26-2023 12:07:30
#Version 4.003: Added option to change skins for the calculator by editing calcMemory.txt file (Enter 0-3 on top line)
#Version 4.003: 'complete' date: 08-02-2023 18:58:30


#Almost complete overhaul of Version 3

#Keyboard shortcuts:
#
#m: Mod
#a: Arg
#e: e^
#l: Log
#s: Sin
#c: Cos
#t: Tan
#p: Power (a^b)
#_ (Space): Clear screen
#v: Input to variable
#w, x, y, z: Use variable
#(ENTER): Compute
#After computation, press any operation or function to use the result of the previous computation

from tkinter import *
import re

#Use Complex class from Complex.py for all the complex number operations
from Complex import Complex

#Use class for global variables
from ComplexCalc4GlobalVars import ComplexCalc4GlobalVars
gv = ComplexCalc4GlobalVars()

in_file = open("/home/stringzzz/aPythonPrograms/ComplexCalc4/calcMemory.txt", 'r')
if in_file.readable():
    file_list = in_file.readlines()
    gv.skin = int(file_list[0].strip())
    gv.wreal = file_list[1].strip()
    gv.wimag = file_list[2].strip()
    gv.xreal = file_list[3].strip()
    gv.ximag = file_list[4].strip()
    gv.yreal = file_list[5].strip()
    gv.yimag = file_list[6].strip()
    gv.zreal = file_list[7].strip()
    gv.zimag = file_list[8].strip()
in_file.close()


#Root widget
root = Tk()

#Functions for the calculator
def checkPat(pat):
#This function os a total mess. It made an improvement on the previous version's mess, but could stand for being a lot cleaner.
#There may be a much better method overall to dealing with this problem of catching the different patterns entirely.
#An improvement is an improvement, though.
	if re.search(r"^(-?\d+\.?\d*(\+|-)\d+\.?\d*i)(\+|-|\*|/)(-?\d+\.?\d*(\+|-)\d+\.?\d*i)$", pat):
		#Complex/Complex
		m1 = re.match(r"(-?\d+\.?\d*(\+|-)\d+\.?\d*i)(\+|-|\*|/)(-?\d+\.?\d*(\+|-)\d+\.?\d*i)", pat)
		
		m2 = re.match(r"(-?\d+\.?\d*)((\+|-)\d+\.?\d*)i", m1.group(1))
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = m2.group(2)
		
		m3 = re.match(r"(-?\d+\.?\d*)((\+|-)\d+\.?\d*)i", m1.group(4))
		gv.realNo2 = m3.group(1)
		gv.imagNo2 = m3.group(2)
		
		gv.oper = m1.group(3)
		return 1
		
	elif re.search(r"^(-?\d+\.?\d*(\+|-)\d+\.?\d*i)(\+|-|\*|/)(-?\d+\.?\d*)$", pat):
		#Complex/Real
		m1 = re.match(r"(-?\d+\.?\d*(\+|-)\d+\.?\d*i)(\+|-|\*|/)(-?\d+\.?\d*)", pat)
		
		m2 = re.match(r"(-?\d+\.?\d*)((\+|-)\d+\.?\d*)i", m1.group(1))
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = m2.group(2)
		
		m3 = re.match(r"(-?\d+\.?\d*)", m1.group(4))
		gv.realNo2 = m3.group(1)
		gv.imagNo2 = 0
		
		gv.oper = m1.group(3)
		
		return 1
		
	elif re.search(r"^(-?\d+\.?\d*)(\+|-|\*|/)(-?\d+\.?\d*(\+|-)\d+\.?\d*i)$", pat):
		#Real/Complex
		m1 = re.match(r"(-?\d+\.?\d*)(\+|-|\*|/)(-?\d+\.?\d*(\+|-)\d+\.?\d*i)", pat)
		
		m2 = re.match(r"(-?\d+\.?\d*)", m1.group(1))
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = 0
		
		m3 = re.match(r"(-?\d+\.?\d*)((\+|-)\d+\.?\d*)i", m1.group(3))
		gv.realNo2 = m3.group(1)
		gv.imagNo2 = m3.group(2)
		
		gv.oper = m1.group(2)
		
		return 1
		
	elif re.search(r"^(-?\d+\.?\d*)(\+|-|\*|/)(-?\d+\.?\d*)$", pat):
		#Real/Real
		m1 = re.match(r"(-?\d+\.?\d*)(\+|-|\*|/)(-?\d+\.?\d*)", pat)

		m2 = re.match(r"(-?\d+\.?\d*)", m1.group(1))
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = 0
		
		m3 = re.match(r"(-?\d+\.?\d*)", m1.group(3))
		gv.realNo2 = m3.group(1)
		gv.imagNo2 = 0
		
		gv.oper = m1.group(2)
		
		return 1
		
	elif re.search(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*(\+|-)\d+\.?\d*i)\)$", pat):
		#Function/Complex
		m1 = re.match(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*(\+|-)\d+\.?\d*i)\)", pat)
		
		gv.oper = m1.group(1)
		
		m2 = re.match(r".*\((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i\)", pat)
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = m2.group(2)
		
		return 2
		
	elif re.search(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*)\)$", pat):
		#Function/Real
		m1 = re.match(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*)\)$", pat)
		
		gv.oper = m1.group(1)
		
		m2 = re.match(r".*\((-?\d+\.?\d*)\)", pat)
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = 0
		
		return 2
		
	elif re.search(r"^(-?\d+\.?\d*(\+|-)\d+\.?\d*i)(\+|-|\*|/)(-?\d+\.?\d*)i$", pat):
		#Complex/Imag
		m1 = re.match(r"(-?\d+\.?\d*(\+|-)\d+\.?\d*i)(\+|-|\*|/)(-?\d+\.?\d*)i", pat)
		
		m2 = re.match(r"(-?\d+\.?\d*)((\+|-)\d+\.?\d*)i", m1.group(1))
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = m2.group(2)
		
		m3 = re.match(r"(-?\d+\.?\d*)", m1.group(4))
		gv.realNo2 = 0
		gv.imagNo2 = m3.group(1)
		
		gv.oper = m1.group(3)
		
		return 3
		
	elif re.search(r"^(-?\d+\.?\d*)i(\+|-|\*|/)(-?\d+\.?\d*(\+|-)\d+\.?\d*i)$", pat):
		#Imag/Complex
		m1 = re.match(r"(-?\d+\.?\d*)i(\+|-|\*|/)(-?\d+\.?\d*(\+|-)\d+\.?\d*i)", pat)
		
		m2 = re.match(r"(-?\d+\.?\d*)", m1.group(1))
		gv.realNo1 = 0
		gv.imagNo1 = m2.group(1)
		
		m3 = re.match(r"(-?\d+\.?\d*)((\+|-)\d+\.?\d*)i", m1.group(3))
		gv.realNo2 = m3.group(1)
		gv.imagNo2 = m3.group(2)
		
		gv.oper = m1.group(2)
		
		return 3
		
	elif re.search(r"^(-?\d+\.?\d*)i(\+|-|\*|/)(-?\d+\.?\d*)i$", pat):
		#Imag/Imag
		m1 = re.match(r"(-?\d+\.?\d*)i(\+|-|\*|/)(-?\d+\.?\d*)i", pat)

		gv.realNo1 = 0
		gv.imagNo1 = m1.group(1)
		
		gv.realNo2 = 0
		gv.imagNo2 = m1.group(3)
		
		gv.oper = m1.group(2)
		
		return 3
		
	elif re.search(r"^(-?\d+\.?\d*)i(\+|-|\*|/)(-?\d+\.?\d*)$", pat):
		#Imag/Real
		m1 = re.match(r"(-?\d+\.?\d*)i(\+|-|\*|/)(-?\d+\.?\d*)", pat)

		gv.realNo1 = 0
		gv.imagNo1 = m1.group(1)
		
		gv.realNo2 = m1.group(3)
		gv.imagNo2 = 0
		
		gv.oper = m1.group(2)
		
		return 3
	
	elif re.search(r"^(-?\d+\.?\d*)(\+|-|\*|/)(-?\d+\.?\d*)i$", pat):
		#Real/Imag
		m1 = re.match(r"(-?\d+\.?\d*)(\+|-|\*|/)(-?\d+\.?\d*)i", pat)

		gv.realNo1 = m1.group(1)
		gv.imagNo1 = 0
		
		gv.realNo2 = 0
		gv.imagNo2 = m1.group(3)
		
		gv.oper = m1.group(2)
		
		return 3
		
	elif re.search(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*(\+|-)\d+\.?\d*i)\)$", pat):
		#Function/Complex
		m1 = re.match(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*(\+|-)\d+\.?\d*i)\)", pat)
		
		gv.oper = m1.group(1)
		
		m2 = re.match(r".*\((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i\)", pat)
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = m2.group(2)
		
		return 4
		
	elif re.search(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*)\)$", pat):
		#Function/Real
		m1 = re.match(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*)\)$", pat)
		
		gv.oper = m1.group(1)
		
		m2 = re.match(r".*\((-?\d+\.?\d*)\)", pat)
		gv.realNo1 = m2.group(1)
		gv.imagNo1 = 0
		
		return 4
	
	elif re.search(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*)i\)$", pat):
		#Function/Imag
		m1 = re.match(r"^(Mod|Arg|e\^|Log|Sin|Cos|Tan|Inv)\((-?\d+\.?\d*)i\)$", pat)
		
		gv.oper = m1.group(1)
		
		m2 = re.match(r".*\((-?\d+\.?\d*)i\)", pat)
		gv.realNo1 = 0
		gv.imagNo1 = m2.group(1)
		
		return 4
		
	elif re.search(r"^Pow\((-?\d+\.?\d*(\+|-)\d+\.?\d*i)\, (-?\d+\.?\d*(\+|-)\d+\.?\d*i)\)$", pat):
		#Pow:Complex/Complex
		m1 = re.match(r"^Pow\(((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i)\, ((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i)\)$", pat)
		
		gv.oper = 'Pow'
		
		gv.realNo1 = m1.group(2)
		gv.imagNo1 = m1.group(3)
		gv.realNo2 = m1.group(6)
		gv.imagNo2 = m1.group(7)
		
		return 5
		
	elif re.search(r"^Pow\((-?\d+\.?\d*(\+|-)\d+\.?\d*i)\, (-?\d+\.?\d*)\)$", pat):
		#Pow:Complex/Real
		m1 = re.match(r"^Pow\(((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i)\, (-?\d+\.?\d*)\)$", pat)
		
		gv.oper = 'Pow'
		
		gv.realNo1 = m1.group(2)
		gv.imagNo1 = m1.group(3)
		gv.realNo2 = m1.group(5)
		gv.imagNo2 = 0
		
		return 5
		
	elif re.search(r"^Pow\((-?\d+\.?\d*)\, (-?\d+\.?\d*(\+|-)\d+\.?\d*i)\)$", pat):
		#Pow:Real/Complex
		m1 = re.match(r"^Pow\((-?\d+\.?\d*)\, ((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i)\)$", pat)
		
		gv.oper = 'Pow'
		
		gv.realNo1 = m1.group(1)
		gv.imagNo1 = 0
		gv.realNo2 = m1.group(3)
		gv.imagNo2 = m1.group(4)
		
		return 5
		
	elif re.search(r"^Pow\((-?\d+\.?\d*)\, (-?\d+\.?\d*)\)$", pat):
		#Pow:Real/Real
		m1 = re.match(r"^Pow\((-?\d+\.?\d*)\, (-?\d+\.?\d*)\)$", pat)
		gv.oper = 'Pow'
		
		gv.realNo1 = m1.group(1)
		gv.imagNo1 = 0
		gv.realNo2 = m1.group(2)
		gv.imagNo2 = 0
		
		return 5
	
	elif re.search(r"^Pow\((-?\d+\.?\d*(\+|-)\d+\.?\d*i)\, (-?\d+\.?\d*)i\)$", pat):
		#Pow:Complex/Imag
		m1 = re.match(r"^Pow\(((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i)\, (-?\d+\.?\d*)i\)$", pat)
		
		gv.oper = 'Pow'
		
		gv.realNo1 = m1.group(2)
		gv.imagNo1 = m1.group(3)
		gv.realNo2 = 0
		gv.imagNo2 = m1.group(5)
		
		return 5
		
	elif re.search(r"^Pow\((-?\d+\.?\d*)i\, (-?\d+\.?\d*(\+|-)\d+\.?\d*i)\)$", pat):
		#Pow:Imag/Complex
		m1 = re.match(r"^Pow\((-?\d+\.?\d*)i\, ((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i)\)$", pat)
		
		gv.oper = 'Pow'
		
		gv.realNo1 = 0
		gv.imagNo1 = m1.group(1)
		gv.realNo2 = m1.group(3)
		gv.imagNo2 = m1.group(4)
		
		return 5
		
	elif re.search(r"^Pow\((-?\d+\.?\d*)i\, (-?\d+\.?\d*)i\)$", pat):
		#Pow:Imag/Imag
		m1 = re.match(r"^Pow\((-?\d+\.?\d*)i\, (-?\d+\.?\d*)i\)$", pat)
		gv.oper = 'Pow'
		
		gv.realNo1 = 0
		gv.imagNo1 = m1.group(1)
		gv.realNo2 = 0
		gv.imagNo2 = m1.group(2)
		
		return 5
		
	#Single number function operation, return 2
		
	else:
		return 0
		
def use_result():
	gv.realNo1 = gv.resultRealNo
	gv.imagNo1 = gv.resultImagNo
	sign = ""
	if gv.imagNo1 >= 0:
		sign = "+"
	gv.expression = str(gv.realNo1) + sign + str(gv.imagNo1) + 'i'
	current = output_display['text']
	output_display.config(text = str(gv.realNo1) + sign + str(gv.imagNo1) + 'i')
	
	gv.resultSet = False

def get_num(num):
	if not(gv.resultSet):
		gv.expression += str(num)
		current = output_display['text']
		output_display.config(text = current + str(num))

def get_dot():
	if not(gv.resultSet):
		gv.expression += '.'
		current = output_display['text']
		output_display.config(text = current + '.')
    
def get_i():
	if not(gv.resultSet):
		gv.expression += 'i'
		current = output_display['text']
		output_display.config(text = current + 'i')

def get_func(func):
	if gv.resultSet:
		use_result()
	
	if not(gv.expression == ''):
		gv.expression = func + '(' + gv.expression + ')'
		current = output_display['text']
		output_display.config(text = func + "(" + current + ")")
	else:
		gv.tail = True
		gv.expression = func + '('
		current = output_display['text']
		output_display.config(text = func + "(")

def get_pow():
	if gv.resultSet:
		use_result()
		
	if not(gv.expression == ''):
		gv.expression = "Pow(" + gv.expression + ", "
		current = output_display['text']
		output_display.config(text = "Pow(" + current + ", ")
		gv.tail = True
	    
def get_operator(op):
	if gv.resultSet:
		use_result()
		
	gv.expression += op
	current = output_display['text']
	output_display.config(text = current + op)

def get_clear():
    gv.realNo1 = ""
    gv.imagNo1 = ""
    gv.realNo2 = 0
    gv.imagNo2 = 0
    gv.oper = ""
    gv.expression = ""
    gv.tail = False
    gv.resultSet = False
    gv.resultRealNo = ""
    gv.resultImagNo = ""
    gv.varStore = False
    output_display['text'] = ''

def clear_for_result():
    gv.realNo1 = ""
    gv.imagNo1 = ""
    gv.realNo2 = 0
    gv.imagNo2 = 0
    gv.oper = ""
    gv.expression = ""
    gv.tail = False
    gv.resultSet = False
    gv.resultRealNo = ""
    gv.resultImagNo = ""
    gv.varStore = False
    output_display['text'] = ''

def get_var():
	if gv.resultSet:
		use_result()
		
	if re.search(r"^(-?\d+\.?\d*(\+|-)\d+\.?\d*i)$", gv.expression):
		m1 = re.match(r"((-?\d+\.?\d*)((\+|-)\d+\.?\d*)i)", gv.expression)
	
		gv.realNo1 = m1.group(2)
		gv.imagNo1 = m1.group(3)

	current = output_display['text']
	output_display.config(text = current + " --> ")
	gv.varStore = True


def use_var(var):
	if gv.varStore:
		if var == 'w':
			gv.wreal = gv.realNo1
			gv.wimag = gv.imagNo1
		elif var == 'x':
			gv.xreal = gv.realNo1
			gv.ximag = gv.imagNo1
		elif var == 'y':
			gv.yreal = gv.realNo1
			gv.yimag = gv.imagNo1
		elif var == 'z':
			gv.zreal = gv.realNo1
			gv.zimag = gv.imagNo1
		
		current = output_display['text']
		output_display.config(text = current + var + ", " + var + " variable set")
		gv.resultSet = True
		gv.varStore = False
	else:
		if var == 'w':
			gv.realNo1 = float(gv.wreal)
			gv.imagNo1 = float(gv.wimag)
		elif var == 'x':
			gv.realNo1 = float(gv.xreal)
			gv.imagNo1 = float(gv.ximag)
		elif var == 'y':
			gv.realNo1 = float(gv.yreal)
			gv.imagNo1 = float(gv.yimag)
		elif var == 'z':
			gv.realNo1 = float(gv.zreal)
			gv.imagNo1 = float(gv.zimag)	
		sign = ""
		if gv.imagNo1 >= 0:
			sign = "+"
		gv.expression += str(gv.realNo1) + sign + str(gv.imagNo1) + 'i'
		current = output_display['text']
		output_display.config(text = current + str(gv.realNo1) + sign + str(gv.imagNo1) + 'i')

def get_save():
    out_file = open("/home/stringzzz/aPythonPrograms/ComplexCalc4/calcMemory.txt", 'w')
    out_file.write(gv.skin + "\n")
    out_file.write(gv.wreal + "\n")
    out_file.write(gv.wimag + "\n")
    out_file.write(gv.xreal + "\n")
    out_file.write(gv.ximag + "\n")
    out_file.write(gv.yreal + "\n")
    out_file.write(gv.yimag + "\n")
    out_file.write(gv.zreal + "\n")
    out_file.write(gv.zimag)
    out_file.close()
    output_display.config(text = "Variable memory saved")

def get_equals():

	if not(gv.resultSet):
		if gv.tail:
			gv.expression += ')'
			current = output_display['text']
			output_display.config(text = current + ")")
				
		if not(checkPat(gv.expression)):
			current = output_display['text']
			output_display.config(text = current + " = Syntax Error")
		else:	
			c1 = Complex(float(gv.realNo1), float(gv.imagNo1))
			c2 = Complex(float(gv.realNo2), float(gv.imagNo2))
			current = output_display['text']
			output_display.config(text = current + " = ")
			
			if gv.oper == "+":
			    c3 = c1 + c2
			    current = output_display['text']
			    output_display.config(text = current + c3.Display())
			    gv.resultRealNo = c3.real
			    gv.resultImagNo = c3.imag
			elif gv.oper == "-":
			    c3 = c1 - c2
			    current = output_display['text']
			    output_display.config(text = current + c3.Display())
			    gv.resultRealNo = c3.real
			    gv.resultImagNo = c3.imag
			elif gv.oper == "*":
			    c3 = c1 * c2
			    current = output_display['text']
			    output_display.config(text = current + c3.Display())
			    gv.resultRealNo = c3.real
			    gv.resultImagNo = c3.imag
			elif gv.oper == "/":
				if float(gv.realNo2) == 0 and float(gv.imagNo2) == 0:
					current = output_display['text']
					output_display.config(text = current + " = Div by 0 error!")
				else:
					c3 = c1 / c2
					current = output_display['text']
					output_display.config(text = current + c3.Display())
					gv.resultRealNo = c3.real
					gv.resultImagNo = c3.imag
			elif gv.oper == "Mod":
			    c2 = Complex(float(c1.Mod()), 0)
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "Arg":
			    c2 = Complex(float(c1.Arg()), 0)
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "e^":
			    c2 = c1.Exp()
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "Log":
			    c2 = c1.Log()
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "Sin":
			    c2 = c1.Sin()
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "Cos":
			    c2 = c1.Cos()
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "Tan":
			    c2 = c1.Tan()
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "Inv":
			    c2 = c1.Inverse()
			    current = output_display['text']
			    output_display.config(text = current + c2.Display())
			    gv.resultRealNo = c2.real
			    gv.resultImagNo = c2.imag
			elif gv.oper == "Pow":
			    c3 = c1.cPow(c2)
			    current = output_display['text']
			    output_display.config(text = current + c3.Display())
			    gv.resultRealNo = c3.real
			    gv.resultImagNo = c3.imag
		
		gv.resultSet = True
		
	    
def keydown(e):
    #Detect key presses to enter numbers and operations
	if e.char == 'i':
		get_i()
	elif e.char == '+':
		get_operator("+")
	elif e.char == '-':
		get_operator("-")
	elif e.char == '*':
		get_operator("*")
	elif e.char == '/':
		get_operator("/")
	elif e.char == '.':
		get_dot()
	elif e.char == '\r':
		get_equals()
	elif e.char.isdigit() and int(e.char) >= 0 and int(e.char) < 10:
		get_num(int(e.char))
	elif e.char == 's':
		get_func("Sin")
	elif e.char == 'c':
		get_func("Cos")
	elif e.char == 't':
		get_func("Tan")
	elif e.char == 'm':
		get_func("Mod")
	elif e.char == 'a':
		get_func("Arg")
	elif e.char == 'l':
		get_func("Log") 
	elif e.char == 'e':
		get_func("e^")
	elif e.char == 'p':
		get_pow()
	elif e.char == 'w':
		use_var("w")
	elif e.char == 'x':
		use_var("x")
	elif e.char == 'y':
		use_var("y")
	elif e.char == 'z':
		use_var("z")
	elif e.char == 'v':
		get_var()
	elif e.char == ' ':
		get_clear()

root['background'] = "#2020FF"
root.title("ComplexCalc 4 by stringzzz, Ghostwarez Co. 2023")

skin_info = [{'file': "Calc4_bg1_Blue.png", 'screen_color': "#9090FF", 'button_color': "#3030FF"}, 
{'file': "Calc4_bg2_Green.png", 'screen_color': "#90FF90", 'button_color': "#25AA25"},
{'file': "Calc4_bg3_Red.png", 'screen_color': "#FF9090", 'button_color': "#CC2525"},
{'file': "Calc4_bg4_Purple.png", 'screen_color': "#FF90FF", 'button_color': "#992099"}]

bg = PhotoImage(file="/home/stringzzz/aPythonPrograms/ComplexCalc4/" + skin_info[gv.skin]['file'])
label_one = Label(root, image=bg)
label_one.place(x=0, y=0)
output_display = Label(text = "", height = 8, width = 50, font = ("Arial", 12), foreground = "black", background = skin_info[gv.skin]['screen_color'])
root.bind("<KeyPress>", keydown) #Key press event

background_color = skin_info[gv.skin]['button_color']

#Buttons, call to functions when pressed
button_9 = Button(text = "9", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(9))
button_8 = Button(text = "8", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(8))
button_7 = Button(text = "7", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(7))
button_6 = Button(text = "6", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(6))
button_5 = Button(text = "5", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(5))
button_4 = Button(text = "4", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(4))
button_3 = Button(text = "3", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(3))
button_2 = Button(text = "2", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(2))
button_1 = Button(text = "1", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(1))
button_0 = Button(text = "0", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_num(0))
button_dot = Button(text = ".", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = get_dot)
button_i = Button(text = "i", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = get_i)
button_mod = Button(text = "Mod", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("Mod"))
button_arg = Button(text = "Arg", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("Arg"))
button_e = Button(text = "e^", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("e^"))
button_log = Button(text = "Log", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("Log"))
button_sin = Button(text = "Sin", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("Sin"))
button_cos = Button(text = "Cos", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("Cos"))
button_tan = Button(text = "Tan", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("Tan"))
button_pow = Button(text = "Pow", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = get_pow)
button_add = Button(text = "+", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_operator("+"))
button_sub = Button(text = "-", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_operator("-"))
button_times = Button(text = "*", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_operator("*"))
button_divide = Button(text = "/", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_operator("/"))

button_w = Button(text = "w", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: use_var("w"))
button_x = Button(text = "x", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: use_var("x"))
button_y = Button(text = "y", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: use_var("y"))
button_z = Button(text = "z", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: use_var("z"))
button_var = Button(text = "Var", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = get_var)
button_save = Button(text = "Save", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = get_save)

button_clear = Button(text = "Clear", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = get_clear)
button_inverse = Button(text = "Inv", width = 4, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = lambda: get_func("Inv"))
button_equals = Button(text = "=", width = 32, height = 2, font = ("Arial", 17), foreground = "black", background = background_color, command = get_equals)

#Set up buttons and display on grid system
output_display.grid(row = 1, column = 0, columnspan = 6, pady = (60, 60))
button_9.grid(row = 3, column = 0)
button_8.grid(row = 3, column = 1)
button_7.grid(row = 3, column = 2)
button_6.grid(row = 4, column = 0)
button_5.grid(row = 4, column = 1)
button_4.grid(row = 4, column = 2)
button_3.grid(row = 5, column = 0)
button_2.grid(row = 5, column = 1)
button_1.grid(row = 5, column = 2)
button_0.grid(row = 6, column = 0, pady = (0, 60))
button_dot.grid(row = 6, column = 1, pady = (0, 60))
button_i.grid(row = 6, column = 2, pady = (0, 60))
button_mod.grid(row = 3, column = 4)
button_arg.grid(row = 3, column = 5)
button_e.grid(row = 4, column = 4)
button_log.grid(row = 4, column = 5)
button_sin.grid(row = 5, column = 4)
button_cos.grid(row = 5, column = 5)
button_tan.grid(row = 6, column = 4, pady = (0, 60))
button_pow.grid(row = 6, column = 5, pady = (0, 60))
button_add.grid(row = 8, column = 0)
button_sub.grid(row = 8, column = 1)
button_times.grid(row = 8, column = 2)
button_divide.grid(row = 8, column = 3)
button_clear.grid(row = 8, column = 4)
button_inverse.grid(row = 8, column = 5)

button_w.grid(row = 9, column = 0, pady = (0, 60))
button_x.grid(row = 9, column = 1, pady = (0, 60))
button_y.grid(row = 9, column = 2, pady = (0, 60))
button_z.grid(row = 9, column = 3, pady = (0, 60))
button_var.grid(row = 9, column = 4, pady = (0, 60))
button_save.grid(row = 9, column = 5, pady = (0, 60))

button_equals.grid(row = 11, column = 0, columnspan = 6, pady = (0, 60))

root.mainloop()
