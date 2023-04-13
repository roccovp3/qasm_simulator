// ECE 312 PA0
// Rocco Perciavalle
// rvp425
// Slip days used: 0
// Fall 2022


double computeSquare(double x) {
	//TODO: Your code here
	return x*x;
}

int gcd(int y, int z) {
    //positives only
    if(y < 0) y = y*-1;
    if(z < 0) z = z*-1;

    int j;
    j = (y > z) ? y : z; //if y is greater than z, start for loop counting dowm from y and vice versa

    for(int i = j; i > 0; i--){
        if((z % i == 0) && (y % i == 0)){
            return i;
        }
    }
	return 0;
}

//Given function to be used in findSumPrimes
//Returns 1 if num is prime and 0 if num is not prime
int isPrime(int num) {

    if (num <= 1) return 0;
    if (num % 2 == 0 && num > 2) return 0;
    for(int i = 3; i< num / 2; i+= 2)
    {
        if( num % i == 0 ){
            return 0;
        }
    }
    return 1;
}

int findSumPrimes(int x) {
    int result = 0;
    for(int i = x; i > 0; i--){
        if(isPrime(i)){
            result = result + i;
        }
    }
    return result;
}

