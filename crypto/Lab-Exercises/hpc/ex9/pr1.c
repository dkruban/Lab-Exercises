#include <stdio.h>
#include <omp.h>

double f(double x) { return x * x; }

int main() {
    double a, b;
    int n;

    printf("Enter lower limit (a): ");
    scanf("%lf", &a);
    printf("Enter upper limit (b): ");
    scanf("%lf", &b);
    printf("Enter number of sub-intervals (n): ");
    scanf("%d", &n);

    double h = (b - a) / n;
    double res_red = (f(a) + f(b)) / 2.0;
    double res_crit = (f(a) + f(b)) / 2.0;

    #pragma omp parallel for reduction(+:res_red)
    for (int i = 1; i < n; i++) {
        res_red += f(a + i * h);
    }
    res_red *= h;

    #pragma omp parallel
    {
        double local = 0.0;
        #pragma omp for
        for (int i = 1; i < n; i++) {
            local += f(a + i * h);
        }
        #pragma omp critical
        res_crit += local;
    }
    res_crit *= h;

    printf("Reduction: %f\nCritical: %f\n", res_red, res_crit);
    return 0;
}

