
/**
 * @brief basic defines
 * some random text
 * @def some def
 */
#define ODD 21
#define EVEN 22

/**
 * @struct type
 * @brief default struct for this check
 */
typedef struct type_t{
    int i;
    double db;
}type;

/**
 * @brief Check if number is odd
 * @attention 1. Check if is intiger
 * @param a number to check
 * @return True if odd, false if even
 */
bool IsOdd(int a){
    return a%2;
}

