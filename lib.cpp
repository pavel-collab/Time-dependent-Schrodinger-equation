#include <complex>
#include "lib.hpp"

/*
По сути мне даже не надо писать C обертки для C++ классов и методов,
потому что я не буду использовать эти классы и методы в Python коде.
Я могу просто написать C функцию foo() временной эволюции psi функции,
используя C++ фнукционал и потом объявить функцию foo(), как
extern "C".
*/

// получаем матрицу для взятия второй производной
void diags(double* arr, int N)
{
    for (int i = 0; i < N; ++i)
    {
        for (int j = 0; j < N; ++j)
        {
            if (j == i)
                arr[i*N+j] = -2;
            else if ((i != 0) and ((j == i-1)) || (j == i+1))
                arr[i*N+j] = 1;
            else
                arr[i*N+j] = 0;
        }
    }
}

// получаем матрицу для значений потенциальной энергии
void spdiags(double* arr, int N, double* vals)
{
    for (int i = 0; i < N; ++i)
    {
        for (int j = 0; j < N; j++)
        {
            if (i == j)
                arr[i*N+j] = vals[i];
            else
                arr[i*N+j] = 0;
        }
    }
}

double* PsiTimeEvolution(long N, double dx, double* psi, double* V)
{
    double* H = new double[N*N];

    double* L = new double[N*N];
    double* U = new double[N*N];

    diags(L, N);
    spdiags(U, N, V);

    for (long i = 0; i < N; ++i)
    {
        for (long j = 0; j < N; ++j)
        {
            long idx = i*N + j;
            H[idx] = (-1/(2*dx*dx)) * L[idx] + U[idx];
        }
    }

    delete L;
    delete U;

    // на этой стадии у нас есть матрица гамильтониана в виде одномерного массива
}