

TODO:
- unit test for linerange.text()

pyBooks
=======

Lesson learned:
- code reuse is good IF
  - the code is written well (e.g. tests, comments, DRY)
  - the code was doing a significant amount of work (size up the value gained)
- in my case neither were true

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
Relationship of resource and reference
{{{
  - in tagz, i want to have a set of top references
  - i want ot be able to ask them questiona bout their resource type
    too....
  - problem is that if i make all of the simple refs also simple books,
    then i can't reuse them in bible
- whatever factory loads it is what determines what it is, because
  it creates all the objects
  - i could store the resource on the top reference
  - i guess i'dl ike to dynamically inherit
  - but the best we can do is to compose it on the top level
  - resource() on any ref could call to the top parent and then 
    retrieve the resource

Just realized that my paths are not restful!!!  That the different layers contain overlapping information... So I can't just write a generic algorithm to create the fullpath.. .  it should be    VER/Book/Chap/Verse1-Verse2
This means:
1. in tagz i could parse the path and then pass that to reference()
What i am trying to do is create a generic way of pathing...

In the case of P&P, the top level is a book,.. the resource is 

In the case of the bible, the top level is a Version, and it has a name accordingly.

the top level reference should be enough to 

I have created a 2 level lookup system:
  resource / reference (that the resource knows)

  So the path of hte top level thing is just its nmae.
  The path of anyhthing else is its ref + the top level


The issue is that I am treating the top ref specially.  All other levesl of refs get 1 level, and it gets 1 too.
I give it a pretty name which equals the resource name, which doesn't make sense unless it and the resource are one in teh smae (which is doable)

The reference should handle their own paths however, because they are the ones who know how to parse them.
OPTIONS:
1. simple approach: in tagz, treat the top level specially
2. have path for the top level actually return "".
3. resource handles its own paths, and the top reference is the root path.  This would require that the top level have its own namespace so that it could be uniquely identified against resources.

For now I think doing the simple thing is fine. Generalize later if needed. Path is bette than pretty though.
Let the resource's name be the top reference's name. Library will store it that way. The top level resource should have a path of "/"

TODO:
- in library get name from resource instead of passing it in
  - make sure all resources have their name internal
-   
}}}

Todo
----
- unit tests for
  - path
  - root
  - resource
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

