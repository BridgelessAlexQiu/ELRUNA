Parameters:
1. .edges file of G1
2. .edges file of G2 (please make sure $|V_1| \leq |V_2|$)
3. larger diameter
4. [optional] (0/1) flag indicates which alignment method to use
  - 0: (default) seed alignment
  - 1: naive alignment
  
**Run the alignment algorithm:**
```
cd code/c
g++ -std=c++11 -O3 main.cpp -o main
./main name_of_the_first_network name_of_the_second_network diameter [0/1]
```

**Example:**
