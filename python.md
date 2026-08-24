What is Python?

Python is a high-level, interpreted, dynamically-typed, general-purpose programming language. Let's unpack every one of those words, because each one is interview material.

"High-level" means the language is far removed from machine code (the raw 1s and 0s / CPU instructions the processor actually executes). When you write x = 5, you don't manage memory addresses, register allocation, or binary encoding — the language abstracts all of that away. Contrast with a "low-level" language like C, where you manually manage memory with malloc/free, or Assembly, where you write near-direct CPU instructions.

"Interpreted" — this is the big one

---> In a language like C, source code is compiled directly to native machine code for your specific CPU/OS ahead of time. You run the compiled binary directly.

---> In Java, source code (.java) is compiled to bytecode (.class files) — an intermediate, platform-independent instruction set. The JVM (Java Virtual Machine) then either interprets this bytecode line-by-line OR uses a JIT (Just-In-Time) compiler to convert hot code paths into native machine code at runtime for speed.

---> In standard Python (CPython — the reference implementation you're almost certainly using): your .py source file is first compiled to Python bytecode (a .pyc file, cached usually in a __pycache__ folder) — this is similar in spirit to Java's .class file. Then, this bytecode is run by the Python Virtual Machine (PVM), which interprets it instruction-by-instruction. Unlike modern Java's JIT, standard CPython does not compile hot paths to native machine code by default (this is a major reason Python is slower than Java for CPU-heavy work — though newer CPython versions, 3.11+, added internal optimizations, and there are JIT-based alternatives like PyPy).

So the pipeline for your code is: your_script.py → compiled to bytecode → executed by the PVM interpreter. That's why Python is called "interpreted" even though there IS a compilation step internally — the key difference from Java is there's no separate explicit "build step" you run yourself; python your_script.py does both compilation and execution together, transparently, every time.

"Dynamically-typed" — variable types are checked and resolved at runtime, not compile time. In Java, if you write String s = 5;, the compiler rejects your code before it ever runs — the type error is caught at compile time. In Python, s = 5 followed later by s = "hello" is perfectly legal because the type lives with the object, not the variable name. Type errors in Python (e.g., adding a string to an int) are only discovered when that specific line actually executes — at runtime. This is why Python code can fail in production on a rarely-hit code path that was never type-checked in advance — a real and common category of bugs, and exactly why tools like mypy and type hints (which we'll cover later) exist to catch this earlier, closer to Java's safety net.

"General-purpose" — it's not built for one narrow task (unlike, say, SQL for databases). It's used for web backends (Django, FastAPI, Flask), data science/ML (NumPy, Pandas, PyTorch), automation/scripting, DevOps tooling, embedded systems, and more.