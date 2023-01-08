#include "shortener.hpp"

Shortener::Shortener(string filename){
    Shortener::input.open(filename);
    Shortener::output.open("short_" + filename);
    }

int Shortener::shorten_file(int start, int end, int step, int block_size){
    //skip towards the beginning of the shortened section
    int counter;
    for(counter = 1; counter < start; counter++){
        getline(input, Shortener::line);
        }

    //Scan through lines and only write those which make up blocks devisible by step
    end -= start;
    counter = 0;
    while(getline(input, Shortener::line) && counter < end){
        if(!(counter/block_size%step)){
            Shortener::output << Shortener::line << endl;
            }
        counter++;
        }

    //Write all of the lines at the end
    Shortener::output << Shortener::line << endl;
    while(getline(input, Shortener::line)){
        Shortener::output << Shortener::line << endl;
        }
    return 0;
    }

int Shortener::shorten_file(int start, int end, int step, string delim){
    //skip towards the beginning of the shortened section
    int counter;
    for(counter = 1; counter < start; counter++){
        getline(input, Shortener::line);
        }

    //Record all the lines after start and before first delimetor
    bool done = false;
    while(!done){
        if(!getline(input, Shortener::line)){
            done = true;
            }else{Shortener::output << Shortener::line << endl;}
        if(Shortener::line == delim){
            done = true;
            }
        }


    //Scan through lines and only write those which make up blocks devisible by step
    int block_counter = 0;
    while(getline(input, Shortener::line) && counter < end){
        if(Shortener::line == delim){
            block_counter++;
            }
        if(!(block_counter%step)){
            Shortener::output << Shortener::line << endl;
            }
        counter++;
        }

    //Write all of the lines at the end
    Shortener::output << Shortener::line << endl;
    while(getline(input, Shortener::line)){
        Shortener::output << Shortener::line << endl;
        }
    return 0;
    }

Shortener::~Shortener(){}
