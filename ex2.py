'''
1. Slow Implementation (Linear Search):
   Use a simple list or array to store the nodes and their corresponding distances from the 
   source. When you need to find the node with the smallest distance, you iterate through the 
   entire array to find the minimum distance node. Finding the node with the smallest distance: O(n)

2. Faster Implementation (Priority Queue):
   A priority queue is a data structure that allows efficient access to the min (or max) element 
   in a collection. In the context of Dijkstra's algorithm, a min-heap is commonly used as 
   a priority queue. In a min-heap, the minimum element can be accessed in constant time.
   Finding the node with the smallest distance: O(log n) because accessing the minimum 
   element takes O(1) time, but after removing the min element and you must restore the heap.
'''