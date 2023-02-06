#include <iostream>     
#include <complex>
#include <vector>
#include "lib.hpp"   

int main()
{    
    int N = 3;
    std::complex<double>* vec = new std::complex<double>[N];

    for (int i = 0; i < N; ++i) {
        std::complex<double> z(i/N, (i+1)/N);
        vec[i] = z;
    }

    double* L = new double[N*N];
    double* U = new double[N*N];

    double* V = new double[N];
    for (int i = 0; i < N; ++i) {
        V[i] = 0;
    }

    diags(L, N);
    spdiags(U, N, V);

    std::complex<double>* H = new std::complex<double>[N*N];

    double dx = 1;
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

    for (int i = 0; i < N*N; ++i){
        std::cout << H[i] << " ";
    }
    std::cout << std::endl;
    std::cout << std::endl;

    SqrMatrix<std::complex<double>> Hamiltonian(N, H);

    Matrix<std::complex<double>> newU = Hamiltonian.exp();

    delete H;


    // artificial normilize
    newU /= 1000000;

    std::cout << newU << std::endl;
    std::cout << std::endl;

    // for (int i = 0; i < N*N; ++i)
    // {
    //     std::complex<double> z(0, 0);
    //     std::cout << newU.data()[i].real()*newU.data()[i].real() + newU.data()[i].imag()*newU.data()[i].imag() << std::endl;
    //     if (newU.data()[i].real()*newU.data()[i].real() + newU.data()[i].imag()*newU.data()[i].imag() < 0.1)
    //         newU.data()[i] = z;
    // }

    // std::cout << newU << std::endl;

    return 0;
}