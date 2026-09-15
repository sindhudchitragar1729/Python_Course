"""
Immutability — and why this is not just theoretical

For strings specifically, immutability means: no method ever changes a 
string in place. Every "modification" produces a brand-new string object.
"""
s = " Bharath"
s.upper()   #return a new String object, but does not change the original string in place

print(s) # still "Bharath" — the original string is unchanged

s = s.upper()  # now we rebind s to the new string object returned by upper()

print(s)  # now prints "BHARATH" — the re-bound string object

"""
This trips up beginners constantly: calling s.replace(...) or s.strip() and 
expecting s itself to change, when in fact you must reassign the result.
"""

# Difficulties / Where This Trips People Up — the string concatenation performance trap

# This is a classic, real, measurable production performance bug, 
# and a very common interview question ("why is this loop slow, and how would you fix it?").

result = " "
for i in range(10000):
  result = result + str(i)  # O(n^2) time complexity — each concatenation creates a new string object, copying the old one

# Why is this quadratic, not linear? Since strings are immutable, result + str(i) doesn't append to the existing string — it must:

# Allocate a brand new block of memory large enough for the combined length.
# Copy every single character of the old result into the new memory block.
# Copy the new characters (str(i)) after it.
# Rebind result to this new object. The old object is now garbage.

# On iteration 5000, step 2 has to copy ~5000×(avg digit length) characters just to preserve 
# what was already there, every single time. Summed across 10,000 iterations, the total copying work grows 
# roughly as 1 + 2 + 3 + ... + n, which is O(n²) — quadratic. For small n this is invisible; for large n 
# (think: building a large CSV export, a big log file, a large HTML response) this becomes a real, measurable slowdown that shows up in production profiling.


""" The fix:  use a list and .join() to build the string in linear time, O(n):"""
result = " "
parts = []
for i in range(10000):
  parts.append(str(i))    # list append is amortized O(1) — no copying of old data

result = "".join(parts)   # single pass, allocates final string ONCE
print(result)  # now linear time, O(n) — no repeated copying of old data

"""
list.append() is efficient because Python's list implementation over-allocates extra capacity internally 
(similar to Java's ArrayList growth strategy — doubling-ish capacity when it needs to grow), 
so most appends don't require reallocation. "".join(parts) then computes the total final length
upfront and copies everything exactly once — genuinely linear work.

This exact pattern — "avoid repeated string concatenation in a loop, use .join() instead" — is one of 
the most common real code review comments in professional Python codebases and one of 
the most common Python-specific interview questions about performance.



"""