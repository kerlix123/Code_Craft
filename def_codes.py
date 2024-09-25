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
