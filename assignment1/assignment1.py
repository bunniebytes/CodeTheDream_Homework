# Task 1
def hello():
    return "Hello!"

# Task 2
def greet(name):
    return f"Hello, {name}!"

# Task 3
def calc(num1, num2, operator = "multiply"):
    # add, subtract, multiply, divide, modulo, int_divide (for integer division) and power
    # First check num1 and num2 are valid numbers
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        return "You can't multiply those values!"
    # Check what the operator is and return the correct answer
    match operator:
        case "add":
            return num1 + num2
        case "subtract":
            return num1 - num2
        case "multiply":
            return num1 * num2
        case "divide":
            try:
                return num1 / num2
            except ZeroDivisionError:
                return "You can't divide by 0!"
        case "modulo":
            try:
                return num1 % num2
            except ZeroDivisionError:
                return "You can't divide by 0!"
        case "int_divide":
            try:
                return num1 // num2
            except ZeroDivisionError:
                return "You can't divide by 0!"
        case "power":
            return num1 ** num2
        
# Task 4
def data_type_conversion(value, data_type):
	try:
		match data_type:
			case "int":
				return int(value)
			case "float":
				return float(value)
			case "str":
				return str(value)
	except ValueError:
		return f"You can't convert {value} into a {data_type}."
	
# # Task 5
def grade(*args):
    try:
        average = sum(args)/len(args)
    except TypeError:
        return "Invalid data was provided."
    
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"
    
# Task 6
def repeat(string, count):
    new_string = ""
    for x in range(count):
        new_string += string
    return new_string

# Task 7
def student_scores(position, **kwargs):
    match position:
        case "best":
            highest_score = max(kwargs.values())
            for key, value in kwargs.items():
                if value == highest_score:
                    return key
        case "mean":
            return sum(kwargs.values())/len(kwargs.values())
        
# Task 8
def titleize(string):
    title_words = string.split()
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    for idx, word in enumerate(title_words):
        if idx == 0 or idx == len(title_words) - 1 or word not in little_words:
            word = word.capitalize()
        title_words[idx] = word
    return " ".join(title_words)

# Task 9
def hangman(secret, guess):
	answer = ""
	for letter in secret:
		if letter in guess:
			answer += letter
		else:
			answer += "_"
	return answer

# Task 10
def pig_latin(string):
    word_list = string.split(" ")
    special = "qu"
    vowels = ["a", "e", "i", "o", "u"]
    answer = []
    
    if string[0] in vowels:
        return string + "ay"
    for word in word_list:
        for idx, letter in enumerate(word):
            if letter in vowels:
                match letter:
                    case "u" if word[idx - 1:idx + 1] == special:
                        idx += 1
                translate = word[idx::] + word[:idx:] + "ay"
                answer.append(translate)
                break
    return(" ").join(answer)