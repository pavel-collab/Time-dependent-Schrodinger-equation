#include <iostream>
#include <vector>
#include "lib.hpp"

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

    bool IsSquare() const 
    { 
        return height_ == width_; 
    };

    std::vector<T> data() const 
    { 
        return values_; 
    };

    Matrix(unsigned w, unsigned h): width_{w}, height_{h} 
    {
        values_.resize(w * h);
    };

    Matrix(unsigned w, unsigned h, T* vals): width_{w}, height_{h} 
    {
        unsigned total = w * h;
        values_.resize(total);

        for(unsigned i = 0; i < total; ++i)
            values_[i] = vals[i];
    };

    //TODO убрать пустой деструктор. Компилятор и так добавить деструктор по умоланию.
    ~Matrix() {};


    Matrix operator+=(const Matrix& Other) 
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

    Matrix operator+(const Matrix& Other) const 
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

    Matrix operator-=(const Matrix& Other) 
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

    Matrix operator-(const Matrix& Other) const 
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

    Matrix operator*(const Matrix& Other) const 
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

    Matrix operator*=(const T& Num) 
    {
        unsigned total = this->width_ * this->height_;

        for(int i = 0; i < total; ++i) 
        {
            this->values_[i] *= Num;
        }

        return *this;
    }

    Matrix operator/=(const T& Num) 
    {
        unsigned total = this->width_ * this->height_;

        for(int i = 0; i < total; ++i) 
        {
            this->values_[i] /= Num;
        }

        return *this;
    }

    Matrix operator/(const T& Num) 
    {
        Matrix NewMat{*this};
        unsigned total = this->width_ * this->height_;

        for(int i = 0; i < total; ++i) 
        {
            NewMat.values_[i] /= Num;
        }

        return NewMat;
    }

    Matrix identity() 
    {
        for(int i = 0; i < this->width_; ++i)
            for(int j = 0; j < this->height_; ++j) 
            {
                this->values_[j + i * this->height_] = (T)(i == j);
            }

        return *this;
    }

};

//TODO передача матрицы по ссылке
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
    SqrMatrix(unsigned d): Matrix<T>(d, d), dimension_{d} {};

    SqrMatrix(unsigned d, T* vals): Matrix<T>(d, d, vals), dimension_{d} {};

    Matrix<T> exp() const 
    {
        Matrix<T> NewMat{this->dimension_, this->dimension_};
        NewMat.identity();

        Matrix<T> CurrPow{NewMat};
        Matrix<T> PowStep{*this};

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

        for(int i = 1; i < 20; ++i) {
            float fctr = static_cast<float>(fact(i));
            CurrPow = CurrPow * PowStep;
            NewMat += CurrPow / fctr;
        }

        if(Sum > 0)
            for(int i = 0; i < p; ++i)
                NewMat = NewMat * NewMat;

        return NewMat;
    };
};
