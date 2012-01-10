Abacus Alignment Plugin
================

I'm pretty anal about aligning things in my code, but the alignment plugins I tried were more-or-less one-trick-ponies, and I didn't like any of their tricks, so I made my own.

In Abacus, you can slide the midline separator toward either either the left or the right columns by giving each possible token a `gravity` property like so:

``` json
{
    "abacus_alignment_separators": [    { "token": ":", "gravity": "left" }, 
                                        { "token": "=", "gravity": "right"}    ]
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

While the CoffeeScript the intern wrote can go from this:

``` CoffeeScript
events:
    #"keyup input:text, input:password":                "userChangedNameboundField"
    "change input:text, input:password": "userChangedNameboundField"
    "change select[name='settings.timezone']": "userChangedNameboundField"

woah="Shock G and Humpty Hump are actually Tyler Durden"
noFrigginWayBrah ="Guy Fawkes masks don't make you a hacker"
number_of_stupid_mustaches =    9
```

To this:

``` CoffeeScript
events:
    #"keyup input:text, input:password":        "userChangedNameboundField"
    "change input:text, input:password":        "userChangedNameboundField"
    "change select[name='settings.timezone']":  "userChangedNameboundField"

    woah                                        = "Shock G and Humpty Hump are actually Tyler Durden"
    noFrigginWayBrah                            = "Guy Fawkes masks don't make you a hacker"
    number_of_stupid_mustaches                  = 9
```

All with the same config.

Now how much would you pay?

Usage
============

Make a selection, then `command + control + ]`.

There's no Linux or Windows keymappings because I don't use these operating systems (at least not their GUIs) and have no idea what's appropriate for them. If you have suggestions, I'm all ears. 

Caveats
============

I don't care if you like tabs or Windows line endings and don't bother with handling them. Need to get smarter about matching against longer separator tokens first.