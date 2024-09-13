import io
import sys

import io
import sys

def exec_code(code):
    buffer = io.StringIO()
    sys.stdout = buffer
    variables = {}
    result = {"out": [], "vars": variables, "error": None}
    
    try:
        exec(code, variables, variables)
    except Exception as e:
        result["error"] = str(e)
    
    sys.stdout = sys.__stdout__
    result["out"] = buffer.getvalue().splitlines()
    buffer.close()
    
    return result


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

def grade_code(p1_code, p2_code, times):
    grades = [0, 0]
    p1_s = [el for el in p1_code.split("\n") if el != ""]
    p2_s = [el for el in p2_code.split("\n") if el != ""]
    
    l = [len(''.join(p1_s)), len(p1_s), len(''.join(p2_s)), len(p2_s)]

    if l[0] < l[2]:
        grades[0] += 1
    elif l[0] > l[2]:
        grades[1] += 1

    if l[1] < l[3]:
        grades[0] += 1
    elif l[1] > l[3]:
        grades[1] += 1

    if times[0] < times[1]:
        grades[0] += 1
    else:
        grades[1] += 1

    return grades