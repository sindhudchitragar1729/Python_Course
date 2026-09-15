x = 5
y = x
x = 10
print(y)   # 5, not 10

# Why doesn't y change? Because y = x did NOT copy data into a box called y. 
# It made y point to the same integer object that x was pointing to at that moment. 
# Then x = 10 doesn't modify that integer object (integers are immutable — more on this below) — 
# it creates a brand-new integer object 10 and rebinds the name x to point to it. y still points to the old 5 object, untouched.


# Mutability — the concept that actually matters more than "variables" itself

# This is where Python fundamentally splits from simple "pointer" thinking, 
# and it's the #1 source of subtle bugs for people transitioning from Java.

# Immutable objects (cannot be changed after creation): int, float, str, bool, tuple, frozenset. 
# Any "modification" actually creates a brand new object.

# Mutable objects (can be changed in-place, same object, same memory address): list, dict, set, and custom class instances by default.

#Immutable example
s = "hello"
s = s + " world"   #creates a new string object, rebinds s to it. Old hello object is now unused(garbage collected)

#Mutable examples
lst = [1,2,3]
lst2 = lst        # lst2 points to the SAME list object as lst

lst.append(4)     # modifies the list object IN PLACE — no new object created

print(lst2)        # [1, 2, 3, 4]  <- lst2 sees the change! Because it's the same object.

# How It Works Internally

# Every object in CPython has three things, always:

# Type — what kind of object it is (int, str, list, custom class...) — determines what operations are valid on it.
# Value — the actual data.
# Identity — essentially, its memory address. Unique and constant for the object's lifetime. You can check it with the built-in id() function.

x = 5
y =5
print(id(x), id(y))   # often the SAME address!

"""Wait — why would two separate variables holding "5" have the same identity? 
This is CPython's integer caching / interning optimization: small integers from -5 to 256 
are pre-created once at interpreter startup and reused everywhere, because they're used so 
frequently (loop counters, small constants) that recreating them constantly would waste time/memory. 
This is a genuine CPython implementation detail, not a language guarantee — don't rely on it for logic, 
but expect it as an interview trivia question ("why does 5 is 5 return True but 1000 is 1000 sometimes return False?")."""

a = 1000
b = 1000

print(a is b)  # False (usually/ maybe , may not be) — not cached, two separate objects, "is" compares identity
print(a==b)     # True — "==" compares VALUE, not identity

"""This distinction — is vs == — is critical and heavily tested in interviews. 
== calls the object's __eq__ method to compare values. is compares raw memory 
identity (id(a) == id(b)). You almost always want == for value comparison. 
is is correctly used only for singleton checks, most commonly 
if x is None: (never if x == None: — that's considered bad style, because a custom 
object could override __eq__ to make x == None behave unexpectedly, 
but is None is always a safe, unambiguous identity check since there's only ever one 
None object in the entire running program)."""



#---Reference counting & garbage collection (brief preview):


"""every object keeps an internal count of how many names/references point to it. 
When that count hits zero (nothing references it anymore), CPython immediately deallocates the memory. 
This is why in the earlier example, when x got rebound to a new 10 object, the old 5 object's refcount 
dropped — if nothing else referenced it, it was freed right then, deterministically 
(unlike Java's JVM garbage collector, which runs periodically/unpredictably in the background).

Difficulties / Where This Trips People Up (real production bugs)

 1) The classic mutable default argument trap — this WILL come up in interviews and WILL 
    bite you in real code if you don't know it:"""

def add_item(item, cart=[]):
  cart.append(item)
  return cart

print(add_item("apple"))      # ['apple']
print(add_item("banana"))      # ['apple', 'banana']  <- BUG! Expected ['banana']

"""Why? The default value [] is created once, at function definition time, 
not each call — and since lists are mutable, every call that doesn't pass its own 
cart shares and mutates that same list object. 
The fix: def add_item(item, cart=None): if cart is None: cart = []."  """

def add_item2(item, cart = None):
  if cart is None:
    cart = []
  cart.append(item)
  return cart

print(add_item2("Bus"))
print(add_item2("Train"))

"""
2)  Passing mutable objects into functions and unexpectedly mutating the caller's data:
"""
def process_order(items):
  items.append("processing_fee")   # mutates the CALLER's list!
  return items

order = ["laptop", "mouse"]
process_order(order)
print(order)               # ['laptop', 'mouse', 'processing_fee'] — caller's list changed unexpectedly

"""
This is a very real bug class in production code — functions silently 
mutating data the caller didn't expect to change. Disciplined codebases avoid 
this by either not mutating input arguments (return new data instead) or being very 
explicit in documentation/naming when a function does mutate in place 
(Python convention: methods that mutate in place, like list.sort(), return None 
and are named as verbs, signaling "this changes things, doesn't return a new object" — versus sorted() which returns a new list).
"""

"""
Assignment:

1)  Why does is sometimes give surprising/inconsistent results when comparing integers, 
    but == never does? What's the correct one to use for value comparison, and the one correct use case for is?

2)  Write a short function merge_configs(base_config, override_config) that takes two dictionaries 
    and returns a new dictionary combining them (override values take precedence) — without mutating 
    either input dictionary. This directly tests whether you can apply the mutability lesson to avoid 
    the exact bug class described above. (You don't need dict methods you haven't learned yet in depth — 
    a simple loop-based approach is fine; we'll cover the elegant dict merging syntax when we formally do dictionaries.)    

"""
def merge_configs(base_config, override_config):
  res = {}

  for key in base_config:
    res[key] = base_config[key]

  for key in override_config:
    res[key] = override_config[key]
  return res

base = {"theme": "light", "font" : "Arial", "size": 12}
override = {"theme": "dark", "size": 14}

merged = merge_configs(base, override)
print(merged)
print(base)
print(override)
  