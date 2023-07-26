#For using these variables globally in the Complex Calculator
#There may be a better solution to making this work, but
#at least this works for now

class ComplexCalc4GlobalVars():
    def __init__(self):
        self.realNo1 = ""
        self.imagNo1 = ""
        self.realNo2 = 0
        self.imagNo2 = 0
        self.oper = ""
        self.expression = ""
        self.tail = False    
        self.resultSet = False
        self.resultRealNo = ""
        self.resultImagNo = ""
        
        self.varStore = False
        self.skin = 0
        self.wreal = 0
        self.wimag = 0
        self.xreal = 0
        self.ximag = 0
        self.yreal = 0
        self.yimag = 0
        self.zreal = 0
        self.zimag = 0
