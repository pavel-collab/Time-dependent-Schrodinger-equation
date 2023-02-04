#include <iostream>     
#include <complex>
#include <vector>
#include "lib.hpp"   

int main()
{    
    int N = 4;
    double* val1 = new double[N];

    for (int i = 0; i < N; ++i)
    {
        val1[i] = i;
    }

    SqrMatrix<double> Mat1(N/2, val1);

    for (int i = 0; i < N; ++i)
    {
        std::cout << Mat1.data()[i] << std::endl;
    }


    Matrix<double> res1 = Mat1.exp();

    std::cout << res1 << std::endl;

    std::complex<double>* val2 = new std::complex<double>[N];

    for (int i = 0; i < N; ++i)
    {
        std::complex<double> z(i, i+1);
        val2[i] = z;
    }

    SqrMatrix<std::complex<double>> Mat2(N/2, val2);
    Matrix<std::complex<double>> res2 = Mat2.exp();
    std::cout << res2 << std::endl;

    delete val1;
    delete val2;
    return 0;
}