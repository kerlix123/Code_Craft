def_code_python = f"""coms = []
class Mob:
    global coms
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def go_up(self, n):
        self.y += n
        coms.append(("up", n))
    def go_down(self, n):
        self.y -= n
        coms.append(("down", n))
    def go_right(self, n):
        self.x += n
        coms.append(("right", n))
    def go_left(self, n):
        self.x -= n
        coms.append(("left", n))
mob = Mob(0, 0)
""" 

def_code_c = f"""#include <stdio.h>
struct Mob {{
    int x;
    int y;
}};
void go_up(struct Mob *mob, int n) {{
    mob->y += n;
    printf("up %d\\n", n);
}}
void go_down(struct Mob *mob, int n) {{
    mob->y -= n;
    printf("down %d\\n", n);
}}
void go_right(struct Mob *mob, int n) {{
    mob->x += n;
    printf("right %d\\n", n);
}}
void go_left(struct Mob *mob, int n) {{
    mob->x -= n;
    printf("left %d\\n", n);
}}
int main() {'{'}
    struct Mob mob = {{0, 0}};
"""

def_code_cpp = f"""#include <iostream>
#include <string>
using namespace std;
class Mob {{
    public:
        int x;
        int y;
        Mob(int a, int b) {{
            x = a;
            y = b;
        }}
        void go_up(int n) {{
            y += n;
            cout << "up " << n << endl;
        }}
        void go_down(int n) {{
            y -= n;
            cout << "down " << n << endl;
        }}
        void go_right(int n) {{
            x += n;
            cout << "right " << n << endl;
        }}
        void go_left(int n) {{
            cout << "left " << n << endl;
            x -= n;
        }}
}};
int main() {'{'}
    Mob mob(0, 0);
"""

new_level_curr = {
    "steve_xy": [
        0,
        0
    ],
    "input_text_Python": "class Mob:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def go_up(self, n):\n        self.y += n\n    def go_down(self, n):\n        self.y -= n\n    def go_right(self, n):\n        self.x += n\n    def go_left(self, n):\n        self.x -= n\n\nmob = Mob(0, 0)",
    "input_text_C": "#include <stdio.h>\nstruct Mob {\n    int x;\n    int y;\n};\nvoid go_up(struct Mob *mob, int n) {\n    mob->y += n;\n}\nvoid go_down(struct Mob *mob, int n) {\n    mob->y -= n;\n}\nvoid go_right(struct Mob *mob, int n) {\n    mob->x += n;\n}\nvoid go_left(struct Mob *mob, int n) {\n    mob->x -= n;\n}\nint main() {\n    struct Mob mob = {0, 0};\n\n    return 0;\n}",
    "input_text_C++": "#include <iostream>\n#include <string>\nusing namespace std;\nclass Mob {\n    public:\n        int x;\n        int y;\n        Mob(int a, int b) {\n            x = a;\n            y = b;\n        }\n        void go_up(int n) {\n            y += n;\n        }\n        void go_down(int n) {\n            y -= n;\n        }\n        void go_right(int n) {\n            x += n;\n        }\n        void go_left(int n) {\n            x -= n;\n        }\n};\nint main() {\n    Mob mob(0, 0);\n\n    return 0;\n}",
    "path_block": "",
    "blocks": [
        [
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png"
        ],
        [
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png"
        ],
        [
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png"
        ],
        [
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png"
        ],
        [
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png"
        ],
        [
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png"
        ],
        [
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png",
            "plus.png"
        ]
    ]
}