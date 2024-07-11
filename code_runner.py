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