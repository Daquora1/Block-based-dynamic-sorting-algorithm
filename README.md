# Block-based-dynamic-sorting-algorithm

Got it 👍
Below is **clean, copy-pasteable plain text**, no fancy formatting, no markdown tricks.
At the very end, I include **the full Python code**, also copy-paste ready.

---

Block-based dynamic sorting algorithm

Problem to be solved
Speeding up insertion-based sorting for large datasets.

Classical sorting algorithms (such as bubble sort or insertion sort) work well on small or partially sorted datasets, but they become increasingly expensive on larger, chaotic inputs. This cost may appear in execution time, memory usage, or CPU load, since these algorithms perform many unnecessary comparisons and element movements.

My goal was to design an algorithm that maintains sorted order dynamically during insertion, while limiting the cost of local operations and avoiding global re-sorting whenever possible.

---

Initial idea: grouping elements

My first idea was to split the elements into groups (blocks).
Consider the following example with k = 12 elements:

2, 8, 1, 12, 3, 11, 10, 6, 4, 9, 5, 7

The algorithm starts and successfully sorts the first few elements, producing the sequence:

1, 2, 8

These elements are stored in a group, along with the minimum and maximum values of the group. The algorithm then continues.

The next element is 12. The algorithm checks whether 12 is greater than the maximum of the first group. Since it is, the algorithm moves on.

The next element is 3. The algorithm checks whether 3 falls within the range of the first group — that is, whether it is greater than or equal to the minimum and less than or equal to the maximum. Since this condition is satisfied, the algorithm jumps back and performs another insertion sort within that group.

As a result, the sequence becomes:

[1, 2, 3], 8, 12, 11, 10, 6, 4, 9, 5, 7

Next, the algorithm examines the value 11 relative to the first group. Since 11 is greater than the group’s maximum, the algorithm creates a new group by inserting it among the remaining elements using insertion sort.

This process continues, creating groups of arbitrary size.

---

Grouping logic

The algorithm follows these rules:

* If the current element is greater than the maximum of a given group, that group is skipped.
* If the element is equal to the group’s maximum, it is assigned to that group.
* If the element is smaller than the group’s minimum, the algorithm checks the next group (if it exists).
* If the element is equal to the group’s minimum, it is assigned to that group.

Whenever a new group is created, the algorithm re-evaluates the ordering of groups based on their ranges. For example, a group with range [1, 4] should come before a group with range [8, 12].

By “jumping back,” I mean that within a given subset, a standard sorting method is used to recompute the local minimum and maximum.

I consider this approach useful because grouping allows longer sorting processes to be performed with fewer swaps. However, the logic is significantly more complex, which likely increases CPU usage. For small datasets, it may be less efficient than simpler methods.

---

Further block subdivision

Another possibility is to subdivide the blocks themselves into smaller blocks.
Consider the following sorted set:

[0, 3, 4, 5, 6, 8, 10, 11]

This can be split into blocks like:

[[0, 3], [4, 5], [6, 8], [10, 11]]

Suppose a new element arrives: n = 9.
The algorithm examines the midpoint blocks and determines whether the value is smaller or larger. If smaller, it searches left; if larger, it searches right. This process repeats until it becomes clear between which two blocks the value belongs.

Managing many small blocks is simpler than managing a few large ones. However, this introduces another problem: the new element may fall exactly between two blocks. For example, n = 9 falls between [6, 8] and [10, 11].

In such cases, creating a new block is preferable, as it avoids reorganizing existing blocks.

If n equals a block’s minimum or maximum, it can be inserted directly, since neither boundary changes. This reduces three major issues at once:

* The search space is reduced.
* Constant re-sorting is avoided.
* Insertions often do not change minimum or maximum values.

---

Identified problems

Fragmentation
Many values may fall between two blocks. This is manageable because blocks can be expanded when necessary, so fragmentation alone is not critical.

Block merging
If two blocks are clearly consecutive, such as [5, 6] and [8, 9], and a new element n = 7 arrives, it is unnecessary to create a separate block. Since the value fits directly between them, merging the blocks is more efficient.

This allows the algorithm to progress incrementally and avoids a costly merge at the end. Later insertions (for example, n = 6) can easily be handled within the merged block without changing its minimum or maximum.

This improves three things:

* Eliminates large, delayed merges.
* Reduces the number of blocks.
* Produces stable minimum and maximum values.

---

Using the last inserted element

Another improvement is to store the last inserted element within each block and compare new values relative to it. Since elements are ordered, this provides directional guidance.

Example:

[1, 2, 3, 4, 10, 13], [14, 14, 17]

A new element arrives: n = 12.

n is greater than the minimum of the first block.
n is not smaller than the maximum of the first block.
n is smaller than the minimum of the second block.

Therefore, the element must belong to the first block.

The last inserted value in that block was 4.
Since n > 4, the algorithm searches to the right.

The exact insertion position is still unknown, which leads to the next idea.

---

Bidirectional linear search

The most suitable solution is a bidirectional linear search. This method has a clear upper bound: it continues until the condition

a[i] ≤ n ≤ a[i + 1]

is satisfied.

Because the dataset has already been split into small blocks, this search is fast and efficient at this level, and the correct position can be found easily.

---

Block size limitation

At this point, only one major issue remains: determining the block size.

There must be an upper limit on block size, but this limit should scale with the total number of elements k.

Let X denote the maximum block size, which depends on k.

The idea is that for every 128–256 element increase in k, the maximum block size increases by 32. For example:

64 elements: max block size = 32
128 elements: max block size = 32
169 elements: max block size = 32
224 elements: max block size = 32
256 elements: max block size = 64

---

Alternative approach based on divisibility

Another approach is to define block limits based on the divisibility of k.
If k is divisible by 3, 4, 8, 16, 32, or 64, the algorithm maintains proportional block sizes.

For example, 64 is not divisible by 3, but it is divisible by 16, so at most four blocks of size 16 may exist, or alternatively sixteen blocks of size 4.

---

Final block size formula

X = 32 * floor(log2(k) / 2 + 1)
X = min(X, 128)

Where:
k = number of inserted elements (dataset size)
X = maximum block size

Why this works:

As the dataset grows, the block size may also grow — but more slowly than k.
The log2(k) term describes how many times k can be halved before reaching 1. Since two logarithmic steps are required for X to increase, X only grows when k is quadrupled.

This provides a stable upper bound.

At this point, the algorithm is essentially complete in its current form.

---

Comparison with insertion sort

The O-notation describes how an algorithm’s runtime grows as the input size increases.

n = total number of elements
X = maximum block size

Classical insertion sort:

Best case: O(n)
Average case: O(n²)
Worst case: O(n²)

Block-based dynamic sorting algorithm:

Best case: O(n)
Average case: O(n² / X)
Worst case: O(n²)
