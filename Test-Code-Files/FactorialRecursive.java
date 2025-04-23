public class FactorialRecursive {

    public static int factorial(int n) {
        // Base case: factorial of 0 is 1
        if (n == 0) {
            return 1;
        } else {
            // Recursive step: n! = n * (n-1)!
            return n * factorial(n - 1);
        }
    }

    public static void main(String[] args) {
        int num = 5;  // Example: Calculate factorial of 5
        int result = factorial(num);
        System.out.println("Factorial of " + num + " is: " + result);


        //Demonstrating potential issues with large numbers
        num = 20;
        result = factorial(num);
        System.out.println("Factorial of " + num + " is: " + result);

        num = 25; //Factorial of 25 is a very large number that will exceed int's maximum.
        result = factorial(num);
        System.out.println("Factorial of " + num + " is: " + result); //Observe the negative result.  This is overflow.


        //Handling potential overflow with BigInteger (for very large numbers)
        java.math.BigInteger bigNum = java.math.BigInteger.valueOf(25);
        java.math.BigInteger bigResult = factorialBig(bigNum);
        System.out.println("Factorial of " + bigNum + " is: " + bigResult);

    }

    //Factorial using BigInteger to handle larger numbers and avoid overflow.
    public static java.math.BigInteger factorialBig(java.math.BigInteger n) {
        java.math.BigInteger one = java.math.BigInteger.ONE;
        if (n.equals(java.math.BigInteger.ZERO)) {
            return one;
        } else {
            return n.multiply(factorialBig(n.subtract(one)));
        }
    }
}