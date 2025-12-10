# Task 2

def type_convertor(type_of_output):
    def type_to_convert(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return type_to_convert
        
@type_convertor(str)
def return_int():
    return 5

@type_convertor(int)
def return_string():
    return "Not a number"

y = return_int()
print(type(y).__name__) # This should print "str"
try:
   y = return_string()
   print("shouldn't get here!")
except ValueError:
   print("can't convert that string to an integer!") # This is what should happen