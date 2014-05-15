ParSed
======

an experimental stream editor for transforming text
made to implement http://xkcd.com/1288/ (CC BY-NC 2.5)
A list of replacements from http://xkcd.com/1288/ included.

Installation
---------
-Make sure that Python 2.7 is installed
-Download this repository
-Download the esmre library (licensed under LGPL2.1), for building a string index
https://code.google.com/p/esmre/
-Follow the instructions in esmre-0.3.1/INSTALL
-that's all. If you need help using ParSed, there's always 'python parsed.py -h'!

Tech
-------
ParSed uses filter files to transform multiple strings.
 A filter file contains a list of changes to happen to the text, one per line. For instance, the filter file containing
"foo:=bar
bat:=cat"
changes all occurrences of foo to bar and bat to cat. Right now ParSed supports using multiple filter files simultaneously. If the filter files contain multiple changes for the same string, the last change is used.

It is also possible to use more than one input and output file, but if less output files than input files are listed, ParSed prints everything to the first output file.

ParSed is recursive to a degree whereas sed is not. For example if the changes are "foo:=bar" and "bar:=bat" and the input is "foobar" the output is "bazbat".
You can make it even more recursive by using the -r MAX_NUMBER_OF_RECURSIONS. This feature is still experimental.

Because it is supposed to work on streams, it should be able to work on one passthrough,
meaning that it should check the text character by character and that a change shouldn't affect text before the match

Emulating sed
-------------
The basic sed command is 'sed s/foo/bar/g inputtext >outputfile' which changes every occurence of 'foo' from the inputtext into 'bar' and prints the output to outputfile
to emulate this, create a filter file with one row reading 'foo:=bar'
and run 'python parsed.py -i inputfile -f filterfile -o outputfile'. You can also leave out the output file if you want to see the output on stdout.



Known bugs:
-----------
-Pathological recursions like loop:=loopdeloop don't work as intended
-The number of recursions depends on the amount of characters left to read (at least it doesn't get stuck in an eternal loop...)
