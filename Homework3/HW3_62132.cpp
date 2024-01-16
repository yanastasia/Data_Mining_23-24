#include <iostream>
#include <math.h>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

//coordinates - x and y axes
int* x;
int* y;

int n;

double distance(int x1, int y1, int x2, int y2)
{
	return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

struct Individual
{
	vector<int> genes;
	double result = 0;

	void findResult()
	{
		for (int i = 0; i < genes.size() - 1; i++)
		{
			int a = genes[i];
			int b = genes[i + 1];
			result += distance(x[a], y[a], x[b], y[b]);
		}
	}

	friend bool operator>(Individual& i1, Individual& i2)
	{
		return i1.result > i2.result;
	}
};

struct Compare
{
	bool operator()(Individual& lhs, Individual& rhs)
	{
		return lhs > rhs;
	}
};

priority_queue<Individual, vector<Individual>, Compare> q;
priority_queue<Individual, vector<Individual>, Compare> nextQ;

Individual findBest()
{
	return q.top();
}

void printIndividual(Individual individual) {
	/*cout << "Genes ";
	for (int i = 0; i < individual.genes.size(); i++)
	{
		cout << individual.genes[i] << " ";
	}*/
	cout << "Current best result: " << individual.result << endl;
}

void mutate(Individual& i)
{
	int randGene1 = rand() % n;
	int randGene2 = rand() % n;

	swap(i.genes[randGene1], i.genes[randGene2]);
}

void fillRestOfChildWithParent(Individual& child, Individual& parent, int stopper)
{
	bool found;
	int iter = 0;
	int nextGen;

	for (int i = stopper + 1; i < n; i++) {
		found = true;
		while (found)
		{
			nextGen = parent.genes[iter];
			found = false;
			for (int j = 0; j < child.genes.size(); j++)
			{
				if (child.genes[j] == nextGen)
				{
					found = true;
					iter++;
					break;
				}
			}
		}
		child.genes.push_back(nextGen);
	}
}

void cross(Individual p1, Individual p2) {
	Individual c1, c2;

	int stopper = rand() % n;

	for (int i = 0; i <= stopper; i++) {
		c1.genes.push_back(p1.genes[i]);
		c2.genes.push_back(p2.genes[i]);
	}

	fillRestOfChildWithParent(c1, p2, stopper);
	fillRestOfChildWithParent(c2, p1, stopper);

	mutate(c1);
	mutate(c2);
	
	c1.findResult();
	c2.findResult();

	/*
	cout << "Parents" << endl;

	printIndividual(p1);
	printIndividual(p2);

	cout << "Children" << endl;

	printIndividual(c1);
	printIndividual(c2);
	*/
	nextQ.push(c1);
	nextQ.push(c2);
}

void reproduce()
{
	Individual i1, i2;
	int initSize = q.size();

	while (q.size() > initSize / 2)
	{
		i1 = q.top();
		q.pop();
		i2 = q.top();
		q.pop();
		cross(i1, i2);

		nextQ.push(i1);
		nextQ.push(i2);
	}

	//clear the queue
	while (!q.empty()) {
		q.pop();
	}
}

void generateRandomCoordinates()
{
	for (int i = 0; i < n; i++)
	{
		x[i] = rand() % 10;
		y[i] = rand() % 10;
		//cout << "x: " << x[i] << " y: " << y[i] << endl;
	}
}

void initNextGen() {
	q = nextQ;

	while (!nextQ.empty())
	{
		nextQ.pop();
	}
}

int main()
{
	cin >> n;

	x = new int[n];
	y = new int[n];

	generateRandomCoordinates();

	vector<Individual> parents;

	int numberPop = 10;	

	for (int i = 0; i < numberPop; i++)
	{
		Individual individ;
		parents.push_back(individ);
		for (int j = 0; j < n; j++)
		{
			parents[i].genes.push_back(j);
		}
		std::random_shuffle(parents[i].genes.begin(), parents[i].genes.end());
		parents[i].findResult();
		q.push(parents[i]);
	}

	int iter = 0;

	Individual best;

	while (iter <= 50000) {
		if (iter == 10 || iter == 100 || iter == 1000 || iter == 5000 || iter == 50000)
		{
			cout << iter<< ": ";
			best = findBest();
			printIndividual(best);
		}

		reproduce();
		initNextGen();
		iter++;
	}

	delete[] x, y;

	return 0;
}