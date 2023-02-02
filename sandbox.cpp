#include <iostream>     
#include <complex>
#include <vector>
#include "lib.hpp"   

int main()
{    
    int N = 4;
    // double* val1 = new double[N];

    // std::cout << "checkoint" << std::endl;

    // for (int i = 0; i < N; ++i)
    // {
    //     val1[i] = i;
    // }

    // std::cout << "checkoint" << std::endl;

    double val1[4] = {1, 2, 3, 4};
    SqrMatrix<double> Mat1(N, val1);

    for (int i = 0; i < N; ++i)
    {
        std::cout << Mat1.data()[i] << std::endl;
    }

    std::cout << "checkoint" << std::endl;

    Matrix<double> res1 = Mat1.exp();

    std::cout << Mat1.exp() << std::endl;
    // for (int i = 0; i < N; ++i)
    // {
    //     std::cout << res1.data()[i] << std::endl;
    // }

    // std::complex<double>* val2 = new std::complex<double>[N];

    // for (int i = 0; i < N; ++i)
    // {
    //     std::complex<double> z(i, i+1);
    //     val2[i] = z;
    // }

    // SqrMatrix<std::complex<double>> Mat2(N, val2);
    // Mat2.exp();
    // for (int i = 0; i < 10; ++i)
    // {
    //     std::cout << Mat2.data()[i].real() << std::endl;
    // }

    // delete val1;
    // delete val2;
    return 0;
}