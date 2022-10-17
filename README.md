# slow

Search with backtracking:
1. For each possible rotation of each respective pi-polyomino (called configuration)
2. For a fixed polyomino
3. For each position of the upper corner for the polyomino
4. Decide whether it can be completed to fit the table:
    - True, if it is the last one;
    - Otherwise, back to step 2 with the next polyomino. 
    
Time: ~ $O(4^{n_p}nT^2)$; Space: $O(nT)$, though easily reducable to $O(T)$ (omitted for simplicity). </br>
Here $n_p$ -- the number of pi-polyomino; $n$ -- total number of polyominos; $T=T_1T_2$.

There are $4^{n_p}$ possible configurations (sets of distinct...)

# not that slow

- 1. For each pi-polyomino starting from the smallest one (in area) to the biggest one
  2. For the "gap" produced by the pi-polyomino, "fit" as much other polyominos (includeing pi-polyominos) as possible in a greedy manner.
- Now we can treat pi-polyominos as the rest of the rectangles. The problem then is to decide whether a finite set of rectangles can be packed into a bigger rectangle. 
