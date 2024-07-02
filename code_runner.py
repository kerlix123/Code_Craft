def cbd_maker(code, i):
    cbd = []
    j = 0
    while j < len(code[i]):
        if code[i][j] in [' ', '\t', '\n', ',']:
            j += 1
        elif code[i][j].isalnum():
            sb = ""
            while j < len(code[i]) and code[i][j].isalnum():
                sb += code[i][j]
                j += 1
            cbd.append(sb)
        elif code[i][j] == '"':
            j += 1
            sb = '"'
            while code[i][j] != '"':
                if code[i][j] == '$':
                    if code[i][j+1] == '{':
                        sb2 = ""
                        while code[i][j] != '}':
                            sb2 += code[i][j]
                            j += 1
                        sb2 += '}'
                        j += 1
                        sb += sb2
                    else:
                        sb2 = ""
                        while code[i][j] != ' ':
                            sb2 += code[i][j]
                            j += 1
                        sb += sb2
                else:
                    sb += code[i][j]
                    j += 1
            j += 1
            sb += '"'
            cbd.append(sb)
        else:
            sb = code[i][j]
            cbd.append(sb)
            j += 1
    return cbd