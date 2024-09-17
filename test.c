#include <stdio.h>
struct Mob {
    int x;
    int y;
};
void go_up(struct Mob *mob, int n) {
    mob->y += n;
}
void go_down(struct Mob *mob, int n) {
    mob->y -= n;
}
void go_right(struct Mob *mob, int n) {
    mob->x += n;
}
void go_left(struct Mob *mob, int n) {
    mob->x -= n;
}
int main() {
    struct Mob mob = {0, 0};
    go_down(&mob, 6);
    return 0;
}
