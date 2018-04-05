// This program gives change with the biggest coins possible

#include <stdio.h>
#include <math.h>

int main(void){
    //these floats are set by the total cost and payment
    double paid;
    double cost;

    printf("how much did the customer spend?\n");

    scanf("%lf", &cost);

    printf("and how much did they pay with?\n");

    scanf("%lf", &paid);

    //this could be done as a function e.g. takes in '0.25' and owed and returns int quarters and remainder.

    //"Why did you make a function?" In this personal context, the cost of time was a priority since I already know how to do functions.

    double owed = paid - cost;

    int payQuarters = owed / 0.25;

    double remainderQ = owed - (payQuarters * 0.25);

    int payTens = remainderQ / 0.10;

    double remainderT = remainderQ - (payTens * 0.10);

    int payFives = remainderT / 0.05;

    double remainderF = remainderT - (payFives * 0.05);

    int payPennies = remainderF / 0.01;

    printf("Please give back \n%d quarters, \n%d tens, \n%d fives and \n%d cents", payQuarters, payTens, payFives, payPennies);

}
