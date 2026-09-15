Concept 3: Strings

A string in Python (str) is a sequence of Unicode code points. Let's unpack that precisely, because "string" hides a lot of machinery that interviewers love to probe.

What is a "character," really? At the lowest level, computers only store numbers. To represent text, we need a mapping from numbers to human-readable characters — that's what an encoding is. The most important standard today is Unicode, which assigns every character in (almost) every human writing system a unique number called a code point — e.g., 'A' is code point U+0041 (65 in decimal), 'क' (Devanagari ka) is U+0915, an emoji like '😀' is U+1F600.

Python 3's str type is a sequence of these Unicode code points — not raw bytes. This is a deliberate, important design decision, and it's actually one of the biggest differences between Python 2 and Python 3 (Python 2's str was raw bytes by default, causing constant real-world bugs with non-English text — this was significant enough that it was a primary driver of the Python 2 → 3 migration that the entire industry had to go through around 2015-2020).

s = "Hello"
print(len(s))    # 5 — number of Unicode code points, not bytes

Encoding vs the string itself: a str object in memory is not bytes yet — it's Python's internal representation of code points. When you need to send text over a network, save it to a file, or store it in a database, you must encode it into a specific byte representation — most commonly UTF-8, the dominant encoding on the modern web, which represents each code point using 1 to 4 bytes (ASCII characters like 'A' take 1 byte; characters like 'क' or emoji take more).

s = "cafe"
b = s.encode("utf-8")  # converts str -> bytes
print(b)                    # b'caf\xc3\xa9'  <- 'é' became 2 bytes (0xc3 0xa9) in UTF-8
print(len(s))                # 4 (4 code points: c, a, f, é)
print(len(b))                 # 5 (5 bytes, because é needs 2 bytes in UTF-8)

back = b.decode("utf-8")    # converts bytes -> str


This str vs bytes distinction is one of the single most common real-world Python bugs, especially in web backends: UnicodeDecodeError or TypeError: a bytes-like object is required, not 'str' happen constantly when code mixes the two without explicit encode/decode. Every time you read a file, receive an HTTP request body, or read from a socket, you're getting bytes — and you must decode it to get a str your Python logic can work with normally (slicing, .upper(), etc. all operate on code points, not raw bytes).