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
"""

new_level_curr = {
    "steve_xy": [
        0,
        0
    ],
    "input_text_Python": "mob = Mob(0, 0)",
    "input_text_C": "#include <stdio.h>\n\nint main() {\n    struct Mob mob = {0, 0};\n\n    return 0;\n}",
    "input_text_C++": "#include <iostream>\nusing namespace std;\n\nint main() {\n    Mob mob(0, 0);\n\n    return 0;\n}","path_block": "oak_log_top.png",
    "path_block": "",
    "text_Python": [
        [
            "In this level you will use functions from",
            "the Mob class to move mob around the",
            "map.",
            "",
            "The functions you can use are:",
            "   - mob.go_up(n) - moves mob up by",
            "   n blocks",
            "   - mob.go_down(n) - moves mob",
            "   down by n blocks",
            "   - mob.go_right(n) - moves mob",
            "   right by n blocks",
            "   - mob.go_left(n) - moves mob left",
            "   by n blocks"
        ],
        [
            "Finish is the trapdoor and you can only",
            "go on grass blocks",
            "",
            "To close this book use",
            "Ctrl+E"
        ]
    ],
    "text_C": [
        [
            "In this level you will use functions",
            "to move mob around the map.",
            "",
            "The functions you can use are:",
            "   - go_up(&mob, n) - moves mob up by",
            "   n blocks",
            "   - go_down(&mob, n) - moves mob",
            "   down by n blocks",
            "   - mob.go_right(&mob, n) - moves mob",
            "   right by n blocks",
            "   - mob.go_left(&mob, n) - moves mob left",
            "   by n blocks"
        ],
        [
            "Finish is the trapdoor and you can only",
            "go on grass blocks",
            "",
            "To close this book use",
            "Ctrl+E"
        ]
    ],
    "text_C++": [
        [
            "In this level you will use functions from",
            "the Mob class to move mob around the",
            "map.",
            "",
            "The functions you can use are:",
            "   - mob.go_up(n) - moves mob up by",
            "   n blocks",
            "   - mob.go_down(n) - moves mob",
            "   down by n blocks",
            "   - mob.go_right(n) - moves mob",
            "   right by n blocks",
            "   - mob.go_left(n) - moves mob left",
            "   by n blocks"
        ],
        [
            "Finish is the trapdoor and you can only",
            "go on grass blocks",
            "",
            "To close this book use",
            "Ctrl+E"
        ]
    ],
    "pages": 2,
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