
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

- Book.children -> [Chapter]
- Chapter.children -> Lines
- Lines.children -> [Line]

So Lines is what breaks the pattern.  
  - Do I need that?
    1. when you convert the reference 1:3-4, it's so you can have a single
       reference for that range. This is kinda nice and handy.
       We could use this for refs, but skip it for children of chapter.
    2. The implementation  of Line is very simple given Lines.
    3. it's used for children of a chapter but we could change that.
    4. Then should we add Chapters also? and Books? if needed
  - Are lists okay? I think so if they provide a field which gives the id like chapter did.
