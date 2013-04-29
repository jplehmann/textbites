Textbites
=========
Textbites is a Python library for representing textual resources. It provides a interface for browsing and searching along with several implementations and many unit tests.

Textbites is used in [Nutritious][1], a Django-based web application for browsing and tagging textual content, inspired by Delicious.

[1]: http://github.com/jplehmann/nutritious


Details
-------
Textbites' API includes classes: Resource and Reference.

*Resources* are containers of textual content which provide a top-most reference to that resource as well a "reference locator" service which parses a string reference and returns the associated reference object.  A resource could contain additional meta-data such as the type of resource.

*References* represent an iterator-like pointer into the resource. They provide methods to:

* Retrieve the text at that location.
* Retrieve a human-readable version of the reference string.
* Navigate by traversing to the parent or child references.
* Search over the textual content at that location returning matching references.

Implementations
---------------

* SimpleBooks
  * Book, Chapter, ChapterRange, Line, LineRange
* ViewBooks
* Bible
  * Bible (TODO: rename to ???)
* Quotes


Future
------
Currently, all implementations are static, in-memory resources.



