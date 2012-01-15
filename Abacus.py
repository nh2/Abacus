import sublime, sublime_plugin, re, sys
from string import Template

class AbacusCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        candidates      = []
        separators      = self.view.settings().get("abacus_alignment_separators")

        #Run through the separators accumulating alignment candidates
        #starting with the longest ones i.e. '==' before '='.
        longest_first = sorted(separators, key=lambda sep: -len(sep["token"]))

        #Favor those that lean right so assignments with slice notation in them
        #get handled sanely
        for separator in [righty for righty in longest_first if righty["gravity"] == "right"]:
            self.find_candidates_for_separator(separator, candidates)

        for separator in [lefty for lefty in longest_first if lefty["gravity"] == "left"]:
            self.find_candidates_for_separator(separator, candidates)
        
        #After accumulation is done, figure out what the minimum required
        #indentation and column width is going to have to be to make every
        #candidate happy. Avoid selecting discontiguous regions requiring
        #differing levels of indentation.
        indent, left_col_width  = self.calc_left_col_width(candidates)
        indentor                = Template("$indentation$left_col")
        lg_aligner              = Template("$left_col$separator")
        rg_aligner              = Template("$left_col$gutter$separator_padding$separator")

        #Perform actual alignments based on gravitational pull of separators
        for candidate in candidates:
            sep_width   = len(candidate["separator"])
            #Normalize indentation
            left_col    = indentor.substitute(  indentation = " " * indent, 
                                                left_col    = candidate["left_col"] )
            right_col   = candidate["right_col"].strip()
            #Marry the separator to the proper column
            if candidate["gravity"] == "left":
                #Separator sits flush left
                left_col = lg_aligner.substitute(   left_col    = left_col, 
                                                    separator   = candidate["separator"] )
            elif candidate["gravity"] == "right":
                gutter_width = left_col_width + indent - len(left_col) - len(candidate["separator"])
                #Push the separator ONE separator's width over the tab boundary
                left_col = rg_aligner.substitute(   left_col            = left_col,
                                                    gutter              = " " * gutter_width,
                                                    separator_padding   = " " * sep_width,
                                                    separator           = candidate["separator"] )
                #Most sane people will want a space between the operator and the value.
                right_col = " %s" % right_col
            #Snap the left side together
            left_col                    = left_col.ljust(indent + left_col_width)
            candidate["replacement"]    = "%s%s\n" % (left_col, right_col)
            
            #Replace each line in its entirety
            full_line = self.region_from_line_number(candidate["line"])
            #sys.stdout.write(candidate["replacement"])
            self.view.replace(edit, full_line, candidate["replacement"])
            
        #Scroll and muck with the selection
        self.view.sel().clear()
        for region in [self.region_from_line_number(changed["line"]) for changed in candidates]:
            start_of_right_col  = region.begin() + indent + left_col_width
            insertion_point     = sublime.Region(start_of_right_col, start_of_right_col)
            self.view.sel().add(insertion_point)
            #self.view.show_at_center(insertion_point)

    def find_candidates_for_separator(self, separator, candidates):
        token                   = separator["token"]
        selection               = self.view.sel()
        new_candidates          = []
        for region in selection:
            for line in self.view.lines(region):
                line_no         = self.view.rowcol(line.begin())[0]
            
                #Never match a line more than once
                if len([match for match in candidates if match["line"] == line_no]):
                    continue

                #Is it even conceivable that this line might
                #be alignable? 
                line_content    = self.view.substr(line)

                if line_content.find(token) != -1:
                    #Collapse any string literals that might
                    #also contain our separator token so that
                    #we can reliably find the location of the 
                    #real McCoy.
                    collapsed           = line_content
                    token_pos           = None

                    for match in re.finditer(r"(\"[^\"]*(?<!\\)\"|'[^']*(?<!\\)')", line_content):
                        quoted_string   = match.group(0)
                        collapsed       = collapsed.replace(quoted_string, "\0" * len(quoted_string))

                    #Split on the first/last occurrence of the token
                    if separator["gravity"] == "right":
                        partitioned = collapsed.rpartition(token)
                    elif separator["gravity"] == "left":
                        partitioned = collapsed.partition(token)
                    
                    #Did that give us valid columns?
                    if len(partitioned[0]) and len(partitioned[1]):
                        #Then there's our boundary line
                        token_pos       = len(partitioned[0])
                        left_col        = self.detab(line_content[:token_pos]).rstrip()
                        right_col       = self.detab(line_content[token_pos + len(token):])
                        sep             = line_content[token_pos:token_pos + len(token)]
                        initial_indent  = re.match("\s+", left_col)
                        if initial_indent: initial_indent = len(initial_indent.group(0))
                        candidate       = { "line":             line_no,
                                            "original":         line_content,
                                            "separator":        sep,
                                            "gravity":          separator["gravity"],
                                            "initial_indent":   initial_indent,
                                            "left_col":         left_col.lstrip(),
                                            "right_col":        right_col.rstrip() }
                        new_candidates.append(candidate)
        #Poke more stuff in the accumulator
        candidates.extend(new_candidates)

    def calc_left_col_width(self, candidates):
        width           = 0
        indent          = 0
        sep_width       = 0

        for candidate in candidates:
            indent      = max([candidate["initial_indent"], indent])
            sep_width   = max([len(candidate["separator"]), sep_width])
            width       = max([len(candidate["left_col"]), width])
        
        width += sep_width

        #Bump up to the next multiple of tab_width
        width += (self.tab_width - width % self.tab_width)

        #Make sure we start on a tab boundary
        if indent and indent % self.tab_width:
            if indent > self.tab_width:
                indent -= indent % self.tab_width
            else:
                indent = self.tab_width
            
        return indent, width
    
    @property
    def tab_width(self):
        return int(self.view.settings().get('tab_size', 4))

    def detab(self, input):
        return input.expandtabs(self.tab_width)
        
    def region_from_line_number(self, line_number):
        return self.view.full_line(self.view.text_point(line_number, 0))
