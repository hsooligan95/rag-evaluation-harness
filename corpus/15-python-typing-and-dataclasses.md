Source: Python documentation - typing and dataclasses (docs.python.org/3/library/typing.html, docs.python.org/3/library/dataclasses.html)
License: see corpus/ATTRIBUTION.md

# Python Typing and Dataclasses

Python's typing module lets developers annotate the expected types of variables, function parameters, and return values. Annotations do not change runtime behavior by themselves, but they document intent and let type checkers and editors catch mistakes early.

A TypedDict describes a dictionary with a fixed set of keys and typed values. It is a natural fit for graph state, because state is passed around as a dictionary whose keys every node must agree on.

Dataclasses generate the boilerplate for classes that mainly hold data, such as an index record for a document chunk. Declaring fields with types gives a readable record type without hand-written constructor code.

Clear types are a collaboration tool in agent code. When state keys, retrieval results, and check results are typed, a reader can follow data through the graph without guessing what each step produces.
