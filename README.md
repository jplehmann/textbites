
pyBooks
=======


Questions
---------
- how to use same set of tests, with a different implementation without rewriting the tests
  - answer: use a getter in each test to obtain the implementatation
  - I'm thinking you'd want a parent testsets which calls getImplUnderTest() which is provided
    by either subclass. Then run the subclass tests

Todo
----
- Tests
  - assert parent types in test
  - create an API test


- What if we used the non-view approach?
- Could possibly simplify by not using array in the resource, to help with off by one
  - and/or we could use arrays with a dummy element
- Should I move this into pybible or a common project?

- Consider whether Line and Lines are confusing, or inconsistent?
- is it bad that chapter refs returns an array which is 0 indexed?
  - possibly should return Chapters() reference
  1) I think the problem is that Chapter.children() does not return an array 
    but everything else does.
    Book -> Chapter -> Lines -> Line
  2) returning arrays may also be bad

