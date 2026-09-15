Concept 1: Variables & Memory Model in Python

In Java (and C), when you declare int x = 5;, the compiler allocates a box of memory labeled x, and puts the value 5 directly inside that box. The variable is the storage location.

Python does not work this way at all, and this is the single most important mental model shift you need coming from Java.

In Python, every value is an object living somewhere in memory (on the heap), and a variable is just a name — a label, a reference, a pointer — that points to that object. The variable itself holds no data; it's an entry in a dictionary-like structure (called a namespace) that maps the string "x" to the memory address of an object.

x = 5

What actually happens:

Python creates an integer object with value 5 somewhere in memory.
Python takes the name x and creates a binding: x → (address of that int object).

This is why Python documentation and experienced Python developers say "assignment binds a name to an object", never "assignment stores a value in a variable." That phrasing is precise and matters.

