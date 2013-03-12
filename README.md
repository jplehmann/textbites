
pyBooks
=======


Questions
---------

Done
----
x Tests
  x assert parent types in test
  x create an API test

Todo
----
- Create a second implementation with a 'simpler' non-view approach

- Consider whether Line and Lines are confusing, or inconsistent?
  1) I think the problem is that Chapter.children() does not return an array 
    but everything else does.
    Book -> Chapter -> Lines -> Line
  - Also is it bad that chapter refs returns an array which is 0 indexed?
    - possibly should return Chapters() reference
    2) returning arrays may also be bad

- Could possibly simplify by not using array in the resource, to help with off by one
  - and/or we could use arrays with a dummy element

