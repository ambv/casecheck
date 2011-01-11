casecheck
---------

This is a basic tool that lists all paths that would clash if the filesystem was
not case-sensitive. A check like that would be most useful if you'd want to
convert your filesystem to a case-insensitive variant. Note that this tool
doesn't do the actual filesystem conversion, it only checks for potential
problems if you would try doing it.

Python 3.2 is required.

Why convert to a case-insensitive file system
---------------------------------------------

This applies to Mac OS X where HFS+ can be formatted both in a case-sensitive
and a case-insensitive manner. The former option appeals Unix-junkies like me,
whereas the latter is the default. That means occasionally strange things happen
when someone develops an application in a sloppy manner in regard to cases in
paths.  List of problems include:

* Pro Applications Update 2008-05 hangs in Software Update forever

* MacVim cannot open two files at once which would share a path on an
  case-insensitive system

* iTunes occasionally screws up album grouping when there are a few variants
  only differing in case

I've not used that myself but I also heard about problems with installing:

* Adobe CS3 applications

* World of Warcraft

On the other hand, occasionally you may also find tools created on other Unix
variants (incl. Linux) which use the possibility of keeping multiple entries in
a directory that only differ in case. All in all, however, it looks like using
the default setting will probably cause less trouble.
