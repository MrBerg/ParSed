ParSed
======

an experimental stream editor for transforming text
made to implement http://xkcd.com/1288/ CC BY-NC 2.5
XKCD's word list included

Right now ParSed supports using multiple filter files simultaneously
It is also possible to use more than one input and output file, but then there has to be equally many listed, as ParSed simultaneously works through both lists one element at a time 

To emulate sed
The basic sed command is 'sed s/foo/bar/g inputtext >outputfile' which changes every occurence of 'foo' from the inputtext into 'bar' and prints the output to outputfile
to emulate this, create a filter file with one row reading 'foo:=bar'
and run 'python main.py inputtext -f filterfile >outputfile'
or 'python main.py inputtext -f filterfile -o outputfile'

no regexes right now

ParSed is recursive to a degree whereas sed is not. For example if the change is foo:=ufoo and the input is foobar

Because it is supposed to work on streams, it should be able to work on one passthrough,
meaning that it should check the text character by character and that a change shouldn't affect text before the match

Included is the esmre library licensed under LGPL2.1, for building a string index
https://code.google.com/p/esmre/
and a getch()-like unbuffered character reading class licensed under the Python Software Foundation License
 http://code.activestate.com/recipes/134892/ 
To install: 
-Make sure that Python 2.7 is installed
-Follow the instructions in esmre-0.3.1/INSTALL


8 hours so far
