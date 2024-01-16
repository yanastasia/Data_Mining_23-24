#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <math.h>

using namespace std;

vector<string> dataset;

int democrats[3][16];
int republicans[3][16];

double numDem = 0;
double numRep = 0;

const int initPosRep = 11;
const int initPosDem = 9;

int testsize;

void updateTables(string line, int diff)
{
    bool isRep = line[0] == 'r';

    isRep ? numRep+=diff : numDem+=diff;

    int initPos = isRep ? initPosRep : initPosDem;
    int counter = 0;
    for (int i = initPos; i<line.size(); i+=2)
    {
       switch (line[i])
       {
            case 'y':
               isRep ? republicans[0][counter]+=diff : democrats[0][counter]+=diff;
               break;
            case 'n':
               isRep ? republicans[1][counter]+=diff : democrats[1][counter]+=diff;
               break;
            case '?':
               isRep ? republicans[2][counter]+=diff : democrats[2][counter]+=diff;
               break;
       }
       counter++;
    }
}

void printSubjects()
{
    for (int i = 0; i<3; i++)
    {
        for (int j = 0; j<16; j++)
        {
            cout<<"D "<<i<<" "<<j<<" "<< democrats [i][j]<<endl;
            cout<<"R "<<i<<" "<<j<<" "<< republicans [i][j]<<endl;
        }
    }
}

int processTestLine(string line)
{
    bool isRep = line[0] == 'r';
    int initPos = isRep ? initPosRep : initPosDem;
    double probRepLog = 0;
    double probDemLog = 0;

    int indexAttribute = 0;

    for (int i = initPos; i<line.size(); i+=2)
    {
        switch (line[i])
            {
            case 'y':
               probRepLog += log ((republicans[0][indexAttribute] + 1) / (numRep + 2));
               probDemLog += log((democrats[0][indexAttribute] + 1) / (numDem + 2));
               break;
            case 'n':
               probRepLog += log((republicans[1][indexAttribute] + 1) / (numRep + 2));
               probDemLog += log((democrats[1][indexAttribute] + 1) / (numDem + 2));
               break;
            case '?':
               probRepLog += log((republicans[2][indexAttribute] + 1) / (numRep + 2));
               probDemLog += log((democrats[2][indexAttribute] + 1) / (numDem + 2));
               break;
            }
        indexAttribute++;
    }

    probRepLog += log((numRep + 1) / (numRep + numDem + 2));
    probDemLog += log((numDem + 1) / (numRep + numDem + 2));

    return isRep ? (probRepLog >= probDemLog) : (probRepLog <= probDemLog);
}

double calculateAccuracy(int testinit)
{
    string curLine;
    double rightPredictions = 0;

    for (int i = 0; i < testsize; i++)
    {
        rightPredictions += processTestLine(dataset[testinit+i]);
    }

    return rightPredictions * 100/testsize;
}

int main()
{
    ifstream filein("house-votes-84.data", ios::in);
    string line;

    while (getline(filein, line)) {
        dataset.push_back(line);
        updateTables(line, 1);
    }

    filein.close();

   // 10-fold cross-validation
    testsize = dataset.size()/10;
    int testinit;
    double sumperc = 0;
    double accuracy;

    for (int j = 0; j < 10; j++)
    {
        testinit = j * testsize;

        for (int i = testinit; i < testinit + testsize; i++)
        {
            if (testinit != 0)
            {
                updateTables(dataset[i-testsize], 1);
            }

            updateTables(dataset[i], -1);
        }

        accuracy = calculateAccuracy(testinit);
        cout << accuracy << "%"<<endl;
        sumperc += accuracy;
    }

    cout <<"---------"<<endl;
    cout << sumperc/10 << "%"<<endl;
}
