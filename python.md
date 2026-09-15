What is Python?

Python is a high-level, interpreted, dynamically-typed, general-purpose programming language. Let's unpack every one of those words, because each one is interview material.

"High-level" means the language is far removed from machine code (the raw 1s and 0s / CPU instructions the processor actually executes). When you write x = 5, you don't manage memory addresses, register allocation, or binary encoding — the language abstracts all of that away. Contrast with a "low-level" language like C, where you manually manage memory with malloc/free, or Assembly, where you write near-direct CPU instructions.

"Interpreted" — this is the big one

---> In a language like C, source code is compiled directly to native machine code for your specific CPU/OS ahead of time. You run the compiled binary directly.

---> In Java, source code (.java) is compiled to bytecode (.class files) — an intermediate, platform-independent instruction set. The JVM (Java Virtual Machine) then either interprets this bytecode line-by-line OR uses a JIT (Just-In-Time) compiler to convert hot code paths into native machine code at runtime for speed.

---> In standard Python (CPython — the reference implementation you're almost certainly using): your .py source file is first compiled to Python bytecode (a .pyc file, cached usually in a **pycache** folder) — this is similar in spirit to Java's .class file. Then, this bytecode is run by the Python Virtual Machine (PVM), which interprets it instruction-by-instruction. Unlike modern Java's JIT, standard CPython does not compile hot paths to native machine code by default (this is a major reason Python is slower than Java for CPU-heavy work — though newer CPython versions, 3.11+, added internal optimizations, and there are JIT-based alternatives like PyPy).

So the pipeline for your code is: your_script.py → compiled to bytecode → executed by the PVM interpreter. That's why Python is called "interpreted" even though there IS a compilation step internally — the key difference from Java is there's no separate explicit "build step" you run yourself; python your_script.py does both compilation and execution together, transparently, every time.

"Dynamically-typed" — variable types are checked and resolved at runtime, not compile time. In Java, if you write String s = 5;, the compiler rejects your code before it ever runs — the type error is caught at compile time. In Python, s = 5 followed later by s = "hello" is perfectly legal because the type lives with the object, not the variable name. Type errors in Python (e.g., adding a string to an int) are only discovered when that specific line actually executes — at runtime. This is why Python code can fail in production on a rarely-hit code path that was never type-checked in advance — a real and common category of bugs, and exactly why tools like mypy and type hints (which we'll cover later) exist to catch this earlier, closer to Java's safety net.

"General-purpose" — it's not built for one narrow task (unlike, say, SQL for databases). It's used for web backends (Django, FastAPI, Flask), data science/ML (NumPy, Pandas, PyTorch), automation/scripting, DevOps tooling, embedded systems, and more.

People confuse "interpreted" with "not compiled at all" — it IS compiled, just to bytecode, and just automatically, not to native machine code.
Performance assumption mismatch: people assume Python is "slow" universally, but the truth is nuanced (I/O-bound code is fine; CPU-bound raw-loop code is where it lags — and that's precisely why NumPy/Pandas exist, written in C underneath, called from Python).

How It Works Internally (CPython execution pipeline).

your_script.py (source code, human-readable text)
↓ [Lexer: breaks text into tokens — keywords, identifiers, operators]
↓ [Parser: builds an Abstract Syntax Tree (AST) — a tree representing code structure]
↓ [Compiler: converts the AST into bytecode — low-level instructions like LOAD_FAST, BINARY_ADD]
**pycache**/your_script.cpython-311.pyc (cached bytecode file)
↓
Python Virtual Machine (PVM) — a big loop that reads bytecode instructions
one at a time and executes them against the interpreter's internal state
↓
Program output / behavior

You can literally see this yourself:

<import dis
def add(a, b):
return a + b

dis.dis(add)

This prints the actual bytecode instructions generated for that function. Try this — it's genuinely useful for understanding what your code costs.

Is Python single-threaded or multi-threaded? (You asked specifically — here's the real answer)
|

> > Python the language does support multi-threading (via the threading module), but CPython (the standard implementation) has something called the GIL — Global Interpreter Lock — which prevents true CPU-level parallelism for pure Python bytecode across threads.

> > Here's the mechanism: CPython's memory management (reference counting for garbage collection — we'll cover this in detail when we do memory management) is not thread-safe by design. If two threads modified an object's reference count simultaneously without protection, you'd get race conditions corrupting memory. Rather than making every single object's operations individually thread-safe (which is what Java does, at a performance cost), CPython took a simpler approach: only one thread can execute Python bytecode at any given instant, enforced by a single global lock — the GIL. Threads take turns holding this lock, switching every few milliseconds or on I/O operations.

Practical consequence:

> > For I/O-bound work (network calls, file reads, database queries, waiting on a web API) — threading in Python works great, because a thread releases the GIL while waiting on I/O, letting other threads run. This is why Python web servers handle many concurrent requests fine.

> > For CPU-bound work (heavy number crunching, image processing in pure Python loops) — threading gives you zero speedup, because only one thread ever runs Python bytecode at a time regardless of your CPU's core count. For true parallel CPU work, Python offers multiprocessing instead (separate OS processes, each with its own Python interpreter and own GIL, sidestepping the lock entirely — at the cost of higher memory and inter-process communication overhead).

