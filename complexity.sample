#include <stdio.h>

void print_matrix(char s[], double m[], size_t rows, size_t cols)
{
    size_t len = rows * cols;
    printf("%s = \n", s);
    for (size_t i = 0 ; i < len ; i++)
    {
        if ( i >  0 && i % cols == 0)
        {printf("\n");}
        if (m[(i % cols) + (i / cols)*cols]>=10)
        {
            printf("  %.0f   ", m[(i % cols) + (i / cols)*cols]);
        }
        else 
        {
            printf("   %.0f   ", m[(i % cols) + (i / cols)*cols]);
        }
    }
    printf("\n");
}

int test_fan_out(int x , int b ) 
{
    return x + b; 
}

void transpose(double m[], size_t rows, size_t cols, double r[])
{
    size_t len = rows * cols;
    // 1 2 3 4 5 6  -> 1 3 5 2 4 6 : 0,1 5> 1,0 
    for (size_t i = 0 ; i < len ; i++)
    {
        r[i] = m[(i / rows)+ (i % rows)*cols];
    }
}

void add(double m1[], double m2[], size_t rows, size_t cols, double r[])
{
    size_t len = rows * cols;
    for (size_t i = 0 ; i < len ; i++)
    {
        size_t index = (i % cols) + (i / cols)*cols;
        r[index] = m1[index] + m2[index];
    }
}

void mul(double m1[], double m2[], size_t r1, size_t c1, size_t c2, double r[])
{
    for (size_t i = 0; i < r1; i++)
    {
        for (size_t j = 0; j < c2; j++)
        {
            for (size_t k = 0; k < c1; k++)
            {
                r[i*r1+j] += m1[i*c1+k] * m2[k*c2+j];
            }          
        }
        
    }
    
}

