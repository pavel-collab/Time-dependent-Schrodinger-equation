#include <complex>
#include "lib.hpp"

// Matrix<std::complex<double>>* matrix_new(unsigned int width, unsigned int hight, std::complex<double>* vals)
// {
//     return new Matrix(width, hight, vals);
// }

// void matrix_del(Matrix<std::complex<double>>* matrix)
// {
//     delete matrix;
// }

// bool is_square(Matrix<std::complex<double>>* matrix)
// {
//     return matrix->IsSquare();
// }

// Matrix<std::complex<double>> m_identity(Matrix<std::complex<double>>* matrix)
// {
//     return matrix->identity();
// }

SqrMatrix<std::complex<double>>* sqr_matrix_new(unsigned int d, std::complex<double>* vals)
{
    return new SqrMatrix(d, vals);
}

void sqr_matrix_del(SqrMatrix<std::complex<double>>* sqr_matrix)
{
    delete sqr_matrix;
}

Matrix<std::complex<double>> exp(SqrMatrix<std::complex<double>>* matrix)
{
    return matrix->exp();
}