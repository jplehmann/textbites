
pyBooks
=======

Things that made it a whipping:

- sharing tests meant sharing test fixture data
  - so i had to be able to load that 'translation' instead, which is a good change
  - I had assumed a fixed set of book names, and went back and made that
    dynamic

- sharing tests but different assumptiosn among impls
  - simple and books didn't account for book names so they all used Chapter only.
  - and expected to be able to create using a referene without a book name

TODO:
- ditch pybible
- fold extensions from bible back into simple


- in the end, the pybible doesn't add much so I shouldn't have used it.. more effort to load into the other data structures then copy them over!!



Questions
---------

Todo
----
x pybible behind pybooks interface
  x load into simple books impl
  x parse references
x bible -- use main tests
  x make it load its own data not text fixture data
  x implement search for Bible
- would like bible search 


Done
----
x logging for Bible to keep it quiet
x simple books
  x issue: interface doesn't have search over a range of chapters, and
    this is a pretty important feature
x Tests
  x assert parent types in test
  x create an API test
x children returns [Line]
x Create a second implementation with a 'simpler' non-view approach
  x ViewImpl
  x ContainerImpl
- load a whole book from JSON



