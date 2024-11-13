// Basic arithmetic operations
int sum(int v1, int v2) {
    return v1 + v2;
}

int multiply(int v1, int v2) {
    return v1 * v2;
}

float divide(float v1, float v2) {
    if (v2 != 0) {
        return v1 / v2;
    }
    return 0;
}
