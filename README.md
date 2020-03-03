

**Parameters:**
1. *.edges* file of G1
2. *.edges* file of G2 (**please make sure $|V_1| \leq |V_2|$**)
3. larger diameter
4. [optional] (0/1) flag indicates which alignment method to use
    - 0: (default) seed alignment
    - 1: naive alignment
 
**Naming convention of network files:**
All network files can be found under the directory `datasets`. Based on the nature of networks (random vs real world), they are stored in separate folders `random_network` and `real_network`, respectively. 

**G1:** Given a network G1, its name has the format: *name_g1.edges*, for example: *erdos_g1.edges*.

**G2:** G2 is created upon G1 by adding *p* faction of additional edges. Names of G2s has the format: *name_p_g2.edges*, for example: *erdos_0.25_g2.edges*.

**Run the alignment algorithm:**
```
cd code/c
g++ -std=c++11 -O3 main.cpp -o main
./main name_of_the_first_network name_of_the_second_network diameter [0/1]
```

**Example (using the seed alignment method):**
```
./main datasets/real_network/erdos/erdos_g1.edges datasets/real_network/erdos/erdos_0.25_g2.edges 14
```


**Example (using the naive alignment method):**
```
./main datasets/real_network/econ/econ_g1.edges datasets/real_network/econ/econ_0.25_g2.edges 8 0
```
