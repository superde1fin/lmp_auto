#include "shortener.hpp"

Shortener::Shortener(std::string filename){
    input.open(filename);
    output.open("short_" + filename);
    }

int Shortener::shorten_file(int start, int end, int step, int block_size){
    //skip towards the beginning of the shortened section
    int counter;
    for(counter = 1; counter < start; counter++){
        getline(input, line);
        }

    //Scan through lines and only write those which make up blocks devisible by step
    end -= start;
    counter = 0;
    while(getline(input, line) && counter < end){
        if(!(counter/block_size%step)){
            output << line << endl;
            }
        counter++;
        }

    //Write all of the lines at the end
    output << line << endl;
    while(getline(input, line)){
        output << line << endl;
        }
    return 0;
    }

int Shortener::shorten_file(int start, int end, int step, string delim){
    //skip towards the beginning of the shortened section
    int counter;
    for(counter = 1; counter < start; counter++){
        getline(input, line);
        }

    //Record all the lines after start and before first delimetor
    bool done = false;
    while(!done){
        if(!getline(input, line)){
            done = true;
            }else{output << line << endl;}
        if(line == delim){
            done = true;
            }
        }


    //Scan through lines and only write those which make up blocks devisible by step
    int block_counter = 0;
    while(getline(input, line) && counter < end){
        if(line == delim){
            block_counter++;
            }
        if(!(block_counter%step)){
            output << line << endl;
            }
        counter++;
        }

    //Write all of the lines at the end
    output << line << endl;
    while(getline(input, line)){
        output << line << endl;
        }
    return 0;
    }

Shortener::~Shortener(){}
