
class Base:
    __money__=0

    def showMoney(self):
        print(f'Base money count:{self.__money__}')
        return
    
    def testStatic():
        print("static method called")
        return
    
    def testclassMethod():
        print("classMedthod called")
        return
    

class Employee(Base):
    __level__=0

    def showMoney(self):
        print(self.__money__)
        return super().showMoney()
    
    def testclassMethod():
        print("Employee class method")
        pass

    def testStatic():
        print("Employee static method")
        pass

b=Base()
b.__money__=100
b.showMoney()

Base.testclassMethod()
Base.testStatic()

e=Employee()
e.__money__=99
Employee.testStatic()
e.showMoney()
Employee.testclassMethod()
b.showMoney()