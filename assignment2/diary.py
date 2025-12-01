# Task 1
import traceback
diary_path = "diary.txt"
new_line = "\n"
    # Keeps track if we are on first entry or not
first_entry = True
# Is diary entry active?
active_entry = True
try:
    with open(diary_path, "a") as diary:
        while active_entry:
            # First entry
            if first_entry:
                entry = input("What happened today? ")
                diary.write(entry + new_line)
                first_entry = False
            # Each additional entry
            else:
                entry = input("What else? ")
                diary.write(entry + new_line)
            if entry.lower() == "done for now":
                diary.write(new_line)
                active_entry = False
                print("Your diary has been closed")
except Exception as e:
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")