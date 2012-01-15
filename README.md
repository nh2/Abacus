Abacus Alignment Plugin for Sublime Text 2
================

I'm pretty anal about aligning things in my code, but the alignment plugins I tried were more-or-less one-trick-ponies, and I didn't like any of their tricks, so I made my own.

Abacus focuses on aligning assignments in as language-agnostic a manner as possible. It works best when there's one assignment per line; if you like shoving all your CSS or JSON declarations on a single line, then you are an enemy of readability and this plugin will make every effort to hinder and harm your creature on Earth as far as it is able.

Abacus' one trick is that it allows you to slide the midline separator token--the thing that defines where the left column ends and the right column begins--toward either either the left or the right by giving each possible token a `gravity` property like so:

``` json
{
    "abacus_alignment_separators": 
    [    
        { "token": ":",     "gravity": "left"  },
        { "token": "=",     "gravity": "right" },
        { "token": "+=",    "gravity": "right" },
        { "token": "-=",    "gravity": "right" },
        { "token": "*=",    "gravity": "right" },
        { "token": "/=",    "gravity": "right" },
        { "token": "?=",    "gravity": "right" },
        { "token": "||=",   "gravity": "right" },
        { "token": "%=",    "gravity": "right" },
        { "token": "==",    "gravity": "right" }
    ]
}
```

*Note that the above is a great example of multiple assignments per line. This plugin will only pay attention to the first one and treat the remainder as part of a single right column.

This way that nasty-ass glob of CSS you inherited from the offshore contractor can go from this:

``` css
a 
{
color:#00f;
    text-decoration:none;
}
```

To this:

``` css
a 
{
    color:              #00f;
    text-decoration:    none;
}
```

While the CoffeeScript the intern wrote can go from this:

``` CoffeeScript
events:
    #"keyup input:text, input:password":                "userChangedNameboundField"
    "change input:text, input:password": "userChangedNameboundField"
    "change select[name='settings.timezone']": "userChangedNameboundField"

woah="Shock G and Humpty Hump are actually Tyler Durden"
noFrigginWayBrah ="Guy Fawkes masks make you a hacker"
number_of_stupid_mustaches =    9
```

To this:

``` CoffeeScript
events:
    #"keyup input:text, input:password":        "userChangedNameboundField"
    "change input:text, input:password":        "userChangedNameboundField"
    "change select[name='settings.timezone']":  "userChangedNameboundField"

    woah                                        = "Shock G and Humpty Hump are actually Tyler Durden"
    noFrigginWayBrah                            = "Guy Fawkes masks make you a hacker"
    number_of_stupid_mustaches                  = 9
```

All with the same config.

And it does its best to leave the insertion point flush against the beginning of the right column so you can tab out further if need be. Note that the CoffeeScript example above highlights Abacus' indentation normalization process which can lead to syntactically invalid code in CoffeeScript and Python. In general, if different sections are meant to have different indentation levels, you should select and align them separately. CSS pseudoclasses like ``:before`` and ``:after`` can also throw it for a loop, so keep your selections as focused on the alignable parts as possible. This is not a full-blown beautifier. 

Now how much would you pay?

Usage
============

Make a selection, then `command + control + ]`.

There's no Linux or Windows keymappings because I don't use these operating systems (at least not their GUIs) and have no idea what's appropriate for them. If you have suggestions, I'm all ears. 

Caveats
============

I don't care if you like real tabs or Windows line endings and don't bother with handling them. Seriously, what year is this? 
