def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid calculation."
