# importing libraries
import time
import math
 
# decorator to calculate duration
# taken by any function.
# class tester:
#     def __init__(self,num):
#         self.num = num

#     def calculate_time(*args, **kwargs):
        
#         # added arguments inside the inner1,
#         # if function takes any arguments,
#         # can be added like this.
#         def inner1(func):
    
#             # storing time before function execution
#             begin = time.time()
            
#             func(*args, **kwargs)
    
#             # storing time after function execution
#             end = time.time()
#             print("Total time taken in : ", func.__name__, end - begin)
    
#         return inner1
    
#     # this can be added to any function present,
#     # in this case to calculate a factorial
#     @calculate_time(self = self)
#     def factorial(self):
    
#         # sleep 2 seconds because it takes very less time
#         # so that you can see the actual difference
#         time.sleep(2)
#         print(math.factorial(self.num))
 
# # calling the function.
# test = tester(10)
# test.factorial()

# # Final print
# print("It works!")
# states = {"a":"b", "b":"c", "c":"d", "d":"end"}
# class Foo:
#     def __init__(self):
#         self.init = True

#     # skip some staff
#     def will_change_state(f):
#         def wrapper(*args):
#             ret =  f(*args)
#             args[0].change_state()
#             return ret
#         return wrapper

#     def change_state(self):
#         self.state = states[self.state]

#     @will_change_state
#     def func1(self):
#         pass

#     @will_change_state
#     def func2(self):
#         pass

# if __name__ == "__main__":
#     print("testing")
#     Foo.func1()
#     print("tested")
#     pass