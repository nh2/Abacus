import sublime, sublime_plugin, re

class AbacusCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        candidates      = []
        length_delta    = 0
        separators      = self.view.settings().get("abacus_alignment_separators")
        for separator in separators:
            candidates.extend(self.find_candidates_for_separator(separator))
        
        indent, left_col_width  = self.calc_left_col_width(candidates)

        for candidate in candidates:
            #Normalize indentation
            left_col    = "%s%s" % (" " * indent, candidate["left_col"])
            right_col   = candidate["right_col"].strip()
            #Marry the separator to the proper column
            if candidate["gravity"] == "left":
                #Separator sits flush left
                left_col = "%s%s" % (left_col, candidate["separator"])
            elif candidate["gravity"] == "right":
                sep_space = left_col_width + indent - len(left_col) - len(candidate["separator"])
                #Push the separator over the tab boundary
                left_col = "%s%s %s" % (left_col, " " * sep_space, candidate["separator"])
                right_col = " %s" % right_col
            #Snap the left side together
            left_col = left_col.ljust(indent + left_col_width)
            candidate["replacement"] = "%s%s" % (left_col, right_col)
            #We're adding and removing shit left and right, so
            #all existing regions need to shift.
            candidate["region"] = sublime.Region(candidate["region"].begin() + length_delta, candidate["region"].end() + length_delta)
            #And the next one will move even more
            length_delta += len(candidate["replacement"]) - len(candidate["original"])            
            #print repr(candidate["replacement"]), candidate["region"]
            self.view.replace(edit, candidate["region"], candidate["replacement"])
        #Scroll and muck with the selection
        self.view.sel().clear()
        for region in [changed["region"] for changed in candidates]:
            self.view.show_at_center(region)

    def find_candidates_for_separator(self, separator):
        token       = separator["token"]
        tokenizer   = re.compile("([^%s]+)(%s)(.+)" % (token, token))
        selection   = self.view.sel()
        alignment_candidates = []
        for region in selection:
            for line in self.view.lines(region):
                line_content        = self.view.substr(line)
                tokenized           = tokenizer.match(line_content)
                if tokenized:
                    left_col        = self.detab(tokenized.group(1))
                    right_col       = self.detab(tokenized.group(3))
                    sep             = tokenized.group(2)
                    initial_indent  = re.match("\s+", left_col)
                    if initial_indent: initial_indent = len(initial_indent.group(0))
                    candidate       = { "region":           line,
                                        "original":         line_content,
                                        "separator":        sep,
                                        "gravity":          separator["gravity"],
                                        "initial_indent":   initial_indent,
                                        "left_col":         left_col.lstrip(),
                                        "right_col":        right_col.rstrip() }
                    alignment_candidates.append(candidate)
        return alignment_candidates

    def calc_left_col_width(self, candidates):
        width       = 0
        indent      = 0
        sep_width   = 0

        for candidate in candidates:
            indent      = max([candidate["initial_indent"], indent, self.tab_width])
            sep_width   = max([len(candidate["separator"]), sep_width])
            width       = max([len(candidate["left_col"]), width])

        width += sep_width

        #If we're going to fall exactly on a tab boundary
        #tab out one more so the right column isn't butted
        #up against us.
        if width % self.tab_width == 0:
            width += self.tab_width
        
        width += width % self.tab_width

        #Make sure we fall on a tab boundary
        indent -= indent % self.tab_width
            
        return indent, width
    
    @property
    def tab_width(self):
        return int(self.view.settings().get('tab_size', 4))

    def detab(self, input):
        return input.expandtabs(self.tab_width)
