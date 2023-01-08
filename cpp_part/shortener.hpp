#include <string>
#include <fstream>
#include <iostream>
#include <memory>

using namespace std;

class Shortener{
    public:
        Shortener(string);
        int shorten_file(int, int, int, int);
        int shorten_file(int, int, int, string);
        ~Shortener();
    private:
        ifstream input;
        ofstream output;
        string line;
};
