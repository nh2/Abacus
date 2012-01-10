Abacus Alignment Plugin
================

I'm pretty anal about aligning things in my code, but the alignment plugins I tried were more-or-less one-trick-ponies, and I didn't like any of their tricks, so I made my own.

In Abacus, you can slide the midline separator toward either either the left or the right columns by giving each possible token a `gravity` property like so:

``` json
{
    "abacus_alignment_separators": [    { "token": "\\:", "gravity": "left" }, 
                                        { "token": "\\=", "gravity": "right"}    ]
}
```

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

While the code the intern wrote can go from this:

``` Python
someVar = "blah"
someOtherVar = "blah as well"
heyLookIKnowPolishNotation = "Humpty Dance"
```

To this:

``` Python
someVar                       = "blah"
someOtherVar                  = "blah as well"
heyLookIKnowPolishNotation    = "Humpty Dance"
```

All with the same config.

Note that the `token` properties should be valid Python regexes, and since the config file is in JSON, that means double slashes everywhere. Awful, I know.


Usage
============

Make a selection, then `command + control + ]`.

There's no Linux or Windows keymappings because I don't use these operating systems (at least not their GUIs) and have no idea what's appropriate for them. If you have suggestions, I'm all ears. 

Caveats
============

I wrote this in one night and haven't tested it with complex selections or multi-character separators at all. The regex performing the tokenization is ridiculously simple and will probably need to be replaced with a real parser. I don't care if you like tabs or Windows line endings and don't bother with handling them. If it blows up on you, you can uninstall it. 