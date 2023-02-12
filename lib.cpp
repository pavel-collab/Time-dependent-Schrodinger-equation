#include <complex>
#include <algorithm>
#include "lib.hpp"

/*
По сути мне даже не надо писать C обертки для C++ классов и методов,
потому что я не буду использовать эти классы и методы в Python коде.
Я могу просто написать C функцию foo() временной эволюции psi функции,
используя C++ фнукционал и потом объявить функцию foo(), как
extern "C".
*/

//TODO посмотреть, нет ли готовых функций для сложения массивов. 
// может быть можно использовать готовые плюсовые контейнеры или библиотеки
double* PsiTimeEvolution(long N, double dx, double* real_psi, double* imag_psi, double* V)
{
    std::cout << "checkpoint 1" << std::endl;
    std::complex<double>* H = new std::complex<double>[N*N];

    double* L = new double[N*N];
    double* U = new double[N*N];

    diags(L, N);
    spdiags(U, N, V);

    std::cout << "checkpoint 2" << std::endl;

    for (long i = 0; i < N; ++i)
    {
        for (long j = 0; j < N; ++j)
        {
            long idx = i*N + j;
            std::complex<double> z(0, -((-1/(2*dx*dx)) * L[idx] + U[idx]));
            H[idx] = z;
        }
    }

    delete L;
    delete U;

    std::cout << "checkpoint 3" << std::endl;

    // на этой стадии у нас есть комплексная матрица гамильтониана в виде одномерного массива

    SqrMatrix<std::complex<double>> Hamiltonian(N, H);
    std::cout << Hamiltonian << std::endl;

    std::cout << "checkpoint Matrix exp" << std::endl;

    Matrix<std::complex<double>> newU = Hamiltonian.exp();
    std::cout << newU << std::endl;

    delete H;

    std::cout << "checkpoint 4" << std::endl;

    std::vector<std::complex<double>> vals;
    vals = newU.data();

    std::cout << "checkpoint 5" << std::endl;

    for (int i = 0; i < N*N; ++i)
    {
        std::complex<double> z(0, 0);
        if (vals[i].real()*vals[i].real() + vals[i].imag()*vals[i].imag() < 0.000001)
            newU.SetValue(z, i);
    }

    std::cout << newU << std::endl;

    std::cout << "checkpoint 6" << std::endl;

    std::complex<double>* dst = new std::complex<double>[N];

    for (int i = 0; i < N ; ++i)
    {
        std::complex<double> z(real_psi[i], imag_psi[i]);
        dst[i] = z;
    }

    std::complex<double>* res = new std::complex<double>[N];

    std::cout << "checkpoint 7" << std::endl;

    std::complex<double>* v = new std::complex<double>[N*N];
    for (long i = 0; i < N*N; ++i)
    {
        v[i] = newU.data()[i];
    } 

    SqrMatrix<std::complex<double>> a{N, v};
    a.Transpose();
    std::cout << a << std::endl;
    for (int i = 0; i < N; ++i)
    {
        std::complex<double> sum(0, 0);
        for (int j = 0; j < N; ++j)
        {
            sum += a.data()[i*N+j] * dst[j];
        }

        res[i] = sum;
    }

    delete v;

    std::cout << "checkpoint 8" << std::endl;

    for (int i = 0; i < N; ++i)
    {
        real_psi[i] = res[i].real();
        imag_psi[i] = res[i].imag();
    }

    std::cout << "checkpoint 9" << std::endl;

    delete dst;
    delete res;

    return real_psi;
}