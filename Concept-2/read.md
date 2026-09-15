Concept 2: Numbers in Python — int, float, complex, Decimal, Fraction

In Java, numeric types are a fixed, small menu baked into the language: int (32-bit), long (64-bit), float, double, each with hard-coded size limits and overflow behavior. Python's numeric model is different in a way that matters a lot for correctness-critical code.

int in Python has arbitrary precision. There is no 32-bit or 64-bit ceiling. Python integers grow automatically to however many digits you need, limited only by your machine's available memory.

x = 2 ** 100
print(x)   # 1267650600228229401496703205376

In Java, int would silently overflow (wrap around) at this size, or you'd need BigInteger explicitly. In Python, this is just... a normal int, automatically. Internally, CPython represents integers as an array of "digits" in a large base (not base-10, base-2^30 internally on most systems) plus a sign, and grows this array as needed — similar in spirit to Java's BigInteger, except it's the default and only integer type, not a special opt-in class.

you never have to think about integer overflow in Python the way you do in Java/C — but you DO need to understand this has a performance cost. Arbitrary-precision arithmetic is slower than fixed-width CPU-native integer arithmetic, because the CPU can't just do a single native ADD instruction for huge numbers — CPython has to do multi-"digit" arithmetic in software, digit by digit, similar to how you'd do long multiplication by hand. For small integers (which is the overwhelming majority of real code), CPython optimizes this well, but it's real overhead to be aware of in numerically-intensive code — which is part of why NumPy uses fixed-width C-native integer types (int32, int64) internally instead of Python's arbitrary-precision ints, trading unlimited size for raw speed.


Difficulties / Where This Trips People Up:

-->Using float for money and only discovering the bug in production reconciliation reports, not in dev testing (because the errors are small and don't show up on every transaction).

-->Constructing Decimal from a float literal instead of a string, defeating the entire purpose of using Decimal.

-->Assuming Python ints behave like Java ints (fixed-width, can overflow) — leading to either unnecessary defensive overflow-checking code, or the opposite mistake: assuming all numeric types in Python are similarly unbounded (floats are NOT arbitrary precision — they're still fixed 64-bit IEEE-754).

-->Integer division confusion: / always returns a float in Python 3 (even 4 / 2 gives 2.0, not 2), unlike Java where int / int gives int. This trips up people doing index math expecting an int and getting a float, causing TypeError: list indices must be integers errors later.

How It Works Internally — the / vs // operator dispatch

When you write a + b, Python doesn't have hardcoded behavior per type. It calls a special/dunder method on the object: a.__add__(b). Every type defines its own version of these operations. int.__add__, float.__add__, Decimal.__add__ are all different implementations, chosen dynamically at runtime based on the actual type of a. This is called operator overloading, and it's why Decimal("1") + 1 fails (TypeError) — Decimal.__add__ doesn't know how to combine itself with a plain int implicitly the way float does; you must be explicit: Decimal("1") + Decimal("1"). We'll cover dunder methods properly and in depth when we reach OOP — this is a preview of why they matter.