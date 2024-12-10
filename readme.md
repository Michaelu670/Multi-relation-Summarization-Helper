# k-median & greedy+ helper

A. [k-median](#k-median)
1. [How to use](#how-to-use)
2. [How to turn into k-median+](#how-to-turn-into-k-median)
3. [Result and Takeaway](#result-and-takeaway)
4. [Other notes](#other-notes)

B. [greedy+](#greedy)
1. [Result and Takeaway](#result-and-takeaway-1)

## k-median

### How to use
1. Load your adjacency matrix to a `numpy.ndarray`, preferrably in a new file (see [dsurollback.py](dsurollback.py) for example)

2. Change [kmedian.py](kmedian.py) last part

3. Run kmedian.py


### How to turn into k-median+
Precompute and load the aggregated adjacency matrix


### Result and Takeaway
For dsurollback-concat:

Clusters: 
```py
# aggregate method: SUM
# k=3
[
    [1, 4, 5, 8, 9, 10, 11, 12], 
    [2, 3], 
    [6, 7]
]
```

Good grouping, but no good ways to create superedges
(Maybe) better for larger k, before switching to greedy

```py
# aggregate method: SUM
# k=8
[
    [1], 
    [2, 3], 
    [4], 
    [5, 9, 10, 12], 
    [6], 
    [7], 
    [8], 
    [11]]
```

Not so good at k being too large

```py
# aggregate method: SUM
# k=5
[
    [1], 
    [2, 3], 
    [4], 
    [5, 8, 9, 10, 11, 12], 
    [6, 7]
]
```

much better, but why node 5 with the rest?

```py
# aggregate method: SUM
# k=6
[
    [1], 
    [2, 3], 
    [4], 
    [5, 8, 9, 10, 11, 12], 
    [6], 
    [7]
]
```
not reliable to increment, but k-median provide good baseline to work

```py
# aggregate method: CONCAT
# k=6
[
    [1, 5, 8, 9, 11, 12], 
    [2, 3], 
    [4], 
    [6], 
    [7], 
    [10]
]
```
using concat that was mentioned as the one with 'quality guarantee' does not imply better result. This is subjectively, but clearly, worse than the previous result

### Other notes
may improve by using other metric


## greedy+

### Result and Takeaway
```py
# k=3
[
    [1, 4, 5, 8, 9, 10, 11, 12], 
    [2, 3], 
    [6, 7]
]
```
same as k-median+ (SUM)

```py
# k=6
[
    [1, 4, 5, 8, 9], 
    [2, 3], 
    [6, 7], 
    [10], 
    [11], 
    [12]
]
```
better than k-median in terms of preserving logically similar nodes (2-3 & 6-7), but worse at grouping the rest.

promising pre-result for hybrid approach

```py
# k=10
[
    [1], 
    [2, 3], 
    [4], 
    [5], 
    [6, 7], 
    [8], 
    [9], 
    [10], 
    [11], 
    [12]
]
```
to iterate on previous point, really good at detecting promising supernodes early, but not as good when used too extensive