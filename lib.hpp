#ifndef _LIB_HPP_
#define _LIB_HPP_

#include <iostream>
#include <vector>

extern "C"
{
    /*
    Here we need to write the prototypes of C wrap functions.
    The implementations of this function we should to write in lob.cpp 
    */

   double* PsiTimeEvolution(long N, double dx, double* real_psi, double* imag_psi, double* V);
}

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

unsigned long long fact(unsigned n) {
    if(n == 1 || n == 0)
        return 1;
    else
        return n * fact(n - 1);
}

template<typename T>
class Matrix
{
protected:
    unsigned width_;
    unsigned height_;

    std::vector<T> values_;


public:

    bool IsSquare() const;

    std::vector<T> data() const;

    Matrix(unsigned w, unsigned h);
    Matrix(unsigned w, unsigned h, T* vals);

    Matrix operator+=(const Matrix& Other);
    Matrix operator+(const Matrix& Other) const;
    Matrix operator-=(const Matrix& Other);
    Matrix operator-(const Matrix& Other) const;
    Matrix operator*(const Matrix& Other) const;
    Matrix operator*=(const T& Num);
    Matrix operator/=(const T& Num);
    Matrix operator/(const T& Num);

    Matrix identity();

};

template <typename T>
bool Matrix<T>::IsSquare() const
{ 
    return height_ == width_; 
};

template <typename T>
std::vector<T> Matrix<T>::data() const
{ 
    return values_; 
};

template <typename T>
Matrix<T>::Matrix(unsigned w, unsigned h): width_{w}, height_{h} 
{
    values_.resize(w * h);
};

template <typename T>
Matrix<T>::Matrix(unsigned w, unsigned h, T* vals): width_{w}, height_{h} 
{
    unsigned total = w * h;
    values_.resize(total);

    for(unsigned i = 0; i < total; ++i)
        values_[i] = vals[i];
};

template <typename T>
Matrix<T> Matrix<T>::operator+=(const Matrix<T>& Other) 
{
    if(this->width_ == Other.width_ && this->height_ == Other.height_) 
    {
        unsigned total = this->width_ * this->height_;

        for(int i = 0; i < total; ++i) 
        {
            this->values_[i] += Other.values_[i];
        }
    }
    else 
    {
        std::cerr << "Matrices with dimensions [" << this->width_ << ", " << this->height_ << "] and [" << Other.width_ << ", " << Other.height_ << "] cannot be added" << std::endl;
    }

    return *this;
}

template <typename T>
Matrix<T> Matrix<T>::operator+(const Matrix<T>& Other) const 
{
    if(this->width_ == Other.width_ && this->height_ == Other.height_) 
    {
        Matrix NewMat{this->width_, this->height_};
        unsigned total = this->width_ * this->height_;

        for(int i = 0; i < total; ++i) 
        {
            NewMat.values_[i] = this->values_[i] + Other.values_[i];
        }

        return NewMat;
    }
    else 
    {
        std::cerr << "Matrices with dimensions [" << this->width_ << ", " << this->height_ << "] and [" << Other.width_ << ", " << Other.height_ << "] cannot be added" << std::endl;
    }

    return *this;
}

template <typename T>
Matrix<T> Matrix<T>::operator-=(const Matrix<T>& Other) 
{
    if(this->width_ == Other.width_ && this->height_ == Other.height_) 
    {
        unsigned total = this->width_ * this->height_;

        for(int i = 0; i < total; ++i) 
        {
            this->values_[i] -= Other.values_[i];
        }
    }
    else 
    {
        std::cerr << "Matrices with dimensions [" << this->width_ << ", " << this->height_ << "] and [" << Other.width_ << ", " << Other.height_ << "] cannot be subtracted" << std::endl;
    }

    return *this;
}

template <typename T>
Matrix<T> Matrix<T>::operator-(const Matrix<T>& Other) const 
{
    if(this->width_ == Other.width_ && this->height_ == Other.height_) 
    {
        Matrix NewMat{this->width_, this->height_};
        unsigned total = this->width_ * this->height_;

        for(int i = 0; i < total; ++i) 
        {
            NewMat.values_[i] = this->values_[i] - Other.values_[i];
        }

        return NewMat;
    }
    else 
    {
        std::cerr << "Matrices with dimensions [" << this->width_ << ", " << this->height_ << "] and [" << Other.width_ << ", " << Other.height_ << "] cannot be subtracted" << std::endl;
    }

    return *this;
}

template <typename T>
Matrix<T> Matrix<T>::operator*(const Matrix<T>& Other) const 
{
    if(this->width_ == Other.height_) {
        Matrix NewMat{Other.width_, this->height_};

        for(int i = 0; i < this->height_; ++i)
        {
            for(int j = 0; j < Other.width_; ++j) 
            {
                for(int k = 0; k < this->width_; ++k)
                    NewMat.values_[i + this->height_ * j] += this->values_[i + this->height_ * k] * Other.values_[k + Other.height_ * j];
            }
        }

        return NewMat;
    }
    else 
    {
        std::cerr << "Matrices with dimensions [" << this->width_ << ", " << this->height_ << "] and [" << Other.width_ << ", " << Other.height_ << "] cannot be multiplied" << std::endl;
    }

    return *this;
}

template <typename T>
Matrix<T> Matrix<T>::operator*=(const T& Num) 
{
    unsigned total = this->width_ * this->height_;

    for(int i = 0; i < total; ++i) 
    {
        this->values_[i] *= Num;
    }

    return *this;
}

template <typename T>
Matrix<T> Matrix<T>::operator/=(const T& Num) 
{
    unsigned total = this->width_ * this->height_;

    for(int i = 0; i < total; ++i) 
    {
        this->values_[i] /= Num;
    }

    return *this;
}

template <typename T>
Matrix<T> Matrix<T>::operator/(const T& Num) 
{
    Matrix NewMat{*this};
    unsigned total = this->width_ * this->height_;

    for(int i = 0; i < total; ++i) 
    {
        NewMat.values_[i] /= Num;
    }

    return NewMat;
}

template <typename T>
Matrix<T> Matrix<T>::identity() 
{
    for(int i = 0; i < this->width_; ++i)
        for(int j = 0; j < this->height_; ++j) 
        {
            this->values_[j + i * this->height_] = (T)(i == j);
        }

    return *this;
}

template<typename T>
std::ostream& operator<<(std::ostream& os, const Matrix<T>& Mat) 
{
    std::vector<T> vals = Mat.data();

    for (auto ptr = vals.begin(), end = vals.end(); ptr < end; ++ptr)
        os << *ptr << " ";
      
    return os;
}

template<typename T>
class SqrMatrix : public Matrix<T>
{
private:
    unsigned dimension_;

public:
    SqrMatrix(unsigned d);

    SqrMatrix(unsigned d, T* vals);

    Matrix<T> exp() const;
};

template <typename T>
SqrMatrix<T>::SqrMatrix(unsigned d): Matrix<T>(d, d), dimension_{d} {};

template <typename T>
SqrMatrix<T>::SqrMatrix(unsigned d, T* vals): Matrix<T>(d, d, vals), dimension_{d} {};

template <typename T>
Matrix<T> SqrMatrix<T>::exp() const 
{
    Matrix<T> NewMat{this->dimension_, this->dimension_};
    NewMat.identity();

    Matrix<T> CurrPow{NewMat};
    Matrix<T> PowStep{*this};

    // --------------------------------------------------------------------------------------------
    float Sum = 0.0;
    unsigned total = this->dimension_ * this->dimension_;
    for(int i = 0; i < total; ++i) {
        Sum += fabs(this->values_[i]);
    }

    int p = 0;
    if(Sum > 0) {
        p = ceil(log2f(Sum));
        Sum = exp2(p);
        PowStep /= Sum;
    }
    // --------------------------------------------------------------------------------------------

    for(int i = 1; i < 20; ++i) {
        float fctr = static_cast<float>(fact(i));
        CurrPow = CurrPow * PowStep;
        NewMat += CurrPow / fctr;
    }

    // обратная нормировка
    if(Sum > 0)
        for(int i = 0; i < p; ++i)
            NewMat = NewMat * NewMat;

    return NewMat;
};

#endif