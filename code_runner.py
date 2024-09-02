import io
import sys

def exec_code(code):
    buffer = io.StringIO()
    sys.stdout = buffer
    variables = {}
    exec(code, variables, variables)
    sys.stdout = sys.__stdout__
    output = buffer.getvalue().splitlines()
    buffer.close()
    return {"out": output, "vars": variables}

def cbd_maker(code):
    cbd = []
    j = 0
    while j < len(code):
        if code[j] in [' ', '\t', '\n', ',']:
            j += 1
        elif code[j].isalnum():
            sb = ""
            while j < len(code) and code[j].isalnum():
                sb += code[j]
                j += 1
            cbd.append(sb)
        elif code[j] == '"':
            j += 1
            sb = '"'
            while code[j] != '"':
                sb += code[j]
                j += 1
            j += 1
            sb += '"'
            cbd.append(sb)
        else:
            sb = code[j]
            cbd.append(sb)
            j += 1
    return cbd

def grade_code(p1_code, p1_coms, p2_code, p2_coms):
    grades = [0, 0]
    
    l = [len(p1_code), len(p1_code.split("\n")), len(p1_coms), len(p2_code), len(p2_code.split("\n")), len(p2_coms)]

    if l[0] < l[3]:
        grades[0] += 1
    elif l[0] > l[3]:
        grades[1] += 1

    if l[1] < l[4]:
        grades[0] += 1
    elif l[1] > l[4]:
        grades[1] += 1

    if l[2] < l[5]:
        grades[0] += 1
    elif l[2] > l[5]:
        grades[1] += 1

    return grades