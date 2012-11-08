# coding=utf8

"""
Generates images of notes using lilypond
"""

import pipes

# maps needed notes into it's lilypond notation
notes = {
    'до': 'c',
    'ре': 'd',
    'ми': 'e',
    'фа': 'f',
    'соль': 'g',
    'ля': 'a',
    'си': 'b',
}


def generate (name, octave, note):
    note = note + "'"*octave
    t = pipes.Template ()
    t.append ("lilypond -o res/%s-%d --png - 2>/dev/null" % (name, octave), "-.")
    f = t.open ("/dev/null", 'w')
    f.write ("""\\version "2.14.2"
\\header { 
  tagline = ""  %% removed 
}
#(set-default-paper-size "a10")
{
        \\override Staff.TimeSignature #'stencil = ##f 
        %s
}
""" % note)



for name, s in notes.iteritems ():
    for octave in range(3):
        print "%s, октава %d" % (name, octave)
        generate (name, octave, s)
