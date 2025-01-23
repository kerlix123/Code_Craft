import io
import sys
import shutil, os, tempfile, subprocess
from func_timeout import func_timeout, FunctionTimedOut

timeout = 5

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Code execution exceeded time limit")

def exec_code(code, timeout=5):
    buffer = io.StringIO()
    sys.stdout = buffer
    variables = {}
    result = {"out": [], "vars": variables, "error": None}

    def execute():
        exec(code, variables, variables)

    try:
        func_timeout(timeout, execute)
    except FunctionTimedOut:
        result["error"] = f"Execution timed out after {timeout} seconds"
        if "coms" in variables:
            variables["coms"].clear()
    except Exception as e:
        result["error"] = str(e)
    finally:
        sys.stdout = sys.__stdout__
        result["out"] = buffer.getvalue().splitlines()
        buffer.close()

    return result

def exec_c_code(code, l, timeout=10):
    # Validate language and determine compiler
    if l == "C":
        compiler = "gcc"
    elif l == "C++":
        compiler = "g++"
    else:
        return {"out": [], "error": "Invalid language specified. Choose 'C' or 'C++'."}

    # Check if compiler is available
    if shutil.which(compiler) is None:
        return {"out": [], "error": f"You need to have {compiler.upper()} installed to use {l}!"}

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create file paths
        ext = 'c' if l == "C" else 'cpp'
        c_file = os.path.join(tmpdirname, f"temp.{ext}")
        executable_file = os.path.join(tmpdirname, "temp_executable")

        # Write code to file
        with open(c_file, "w") as f:
            f.write(code)

        # Compile with optimization flags: -O0, -pipe uses in-memory pipes
        compile_flags = [compiler, '-O0', "-pipe", c_file, "-o", executable_file]
        compile_process = subprocess.run(
            compile_flags,
            stdout=subprocess.DEVNULL,  # Discard stdout
            stderr=subprocess.PIPE
        )

        if compile_process.returncode != 0:
            return {"out": [], "error": compile_process.stderr.decode()}

        # Execute the compiled binary
        try:
            run_process = subprocess.run(
                [executable_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout
            )
            return {
                "out": run_process.stdout.decode().splitlines(),
                "error": run_process.stderr.decode() if run_process.stderr else None
            }
        except subprocess.TimeoutExpired:
            return {"out": [], "error": "Error: Code execution exceeded time limit"}

def cbd_maker(code):
    cbd = []
    j = 0
    code_length = len(code)
    while j < code_length:
        if code[j] in [' ', '\t', '\n', ',']:
            j += 1
        elif code[j].isalnum():
            sb = ""
            while j < code_length and code[j].isalnum():
                sb += code[j]
                j += 1
            cbd.append(sb)
        elif code[j] == '"':
            j += 1
            sb = '"'
            while j < code_length and code[j] != '"':
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

def code_length(code):
    return sum(1 for el in code if el not in {'\n', '\t', ' '})

def time_diff(times):
    return (200*abs(times[0]-times[1]))/(times[0]+times[1])

def differences(code_1, code_2):
    diff = 0
    c1pt, c2pt = 0, 0
    len_1, len_2 = len(code_1), len(code_2)
    while c1pt < len_1 and c2pt < len_2:
        if code_1[c1pt] == " ":
            c1pt += 1
            continue
        elif code_2[c2pt] == " ":
            c2pt += 1
            continue
        elif code_1[c1pt] == "\n" and c1pt < len_1 and code_2[c2pt] != "\n":
            while code_2[c2pt] != "\n":
                diff += 1
                c2pt += 1
        elif code_2[c2pt] == "\n" and c2pt < len_2 and code_1[c1pt] != "\n":
            while code_1[c1pt] != "\n":
                diff += 1
                c1pt += 1
        elif code_1[c1pt] != code_2[c2pt]:
            diff += 1
        c1pt += 1
        c2pt += 1
    if c2pt < len_2:
        c2pt += 1
        while c2pt < len_2:
            if code_2[c2pt] == "\n":
                c2pt += 1
            else:
                diff += 1
                c2pt += 1
    elif c1pt < len_1:
        c1pt += 1
        while c1pt < len_1:
            if code_1[c1pt] == "\n":
                c1pt += 1
            else:
                diff += 1
                c1pt += 1

    return diff

def grade_code(p1_code, p2_code, times, calls):
    max_time_diff = 10
    max_diffs = 20
    grades = [0, 0]
    if time_diff(times) < max_time_diff:
        grades[0] += 1
        grades[1] += 1
    elif times[0] > times[1]:
        grades[1] += 1
    elif times[1] > times[0]:
        grades[0] += 1

    if differences(p1_code, p2_code) < max_diffs:
        grades[0] += 1
        grades[1] += 1

    len_1 = code_length(p1_code)
    len_2 = code_length(p2_code)
    if len_1 == len_2:
        grades[0] += 1
        grades[1] += 1
    elif len_1 < len_2:
        grades[0] += 1
    else:
        grades[1] += 1

    if calls[0] == calls[1]:
        grades[0] += 1
        grades[1] += 1
    elif calls[0] < calls[1]:
        grades[0] += 1
    else:
        grades[1] += 1
    
    return grades