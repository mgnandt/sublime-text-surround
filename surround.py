import sublime, sublime_plugin

MATCHING_CHARS = {
  '{' : ['{', '}'],
  '}' : ['{', '}'],
  '[' : ['[', ']'],
  ']' : ['[', ']'],
  '(' : ['(', ')'],
  ')' : ['(', ')'],
  '<' : ['<', '>'],
  '>' : ['<', '>']
}

class AddSurroundCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.window().show_input_panel('Surround with [char]:', '', self.after_input, None, None)
  
  def after_input(self, text):
    if text:
      surround_chars = self.get_matching_char_pair(text[0])
      self.apply_surround_chars(surround_chars)
    
  def get_matching_char_pair(self, text):
    if text in MATCHING_CHARS:
      return MATCHING_CHARS[text]
    return [text, text]
  
  def apply_surround_chars(self, surround_chars):
    selected_regions = self.view.sel()
    for region in selected_regions:
      word = self.get_word_to_surround(region)
      self.insert_around_word(word, surround_chars)
  
  def get_word_to_surround(self, region):
    if region.empty():
      return self.view.word(region.a)
    return region

  def insert_around_word(self, word, surround_chars):
    edit_sequence = self.view.begin_edit()
    self.view.insert(edit_sequence, word.begin(), surround_chars[0])
    self.view.insert(edit_sequence, word.end() + 1, surround_chars[1])
    self.view.end_edit(edit_sequence)

class DeleteSurroundCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.window().show_input_panel('Delete surrounding [char]:', '', self.after_input, None, None)
  
  def after_input(self, text):
    if text:
      surround_chars = self.get_matching_char_pair(text[0])
      self.apply_surround_chars(surround_chars)
  
  def get_matching_char_pair(self, text):
    if text in MATCHING_CHARS:
      return MATCHING_CHARS[text]
    return [text, text]

  def apply_surround_chars(self, surround_chars):
    selected_regions = self.view.sel()
    for region in selected_regions:
      regions_to_delete = self.get_closest_surrounding_regions(surround_chars, region)
      if regions_to_delete:
        self.delete_surrounding_regions(regions_to_delete)

  def get_word_to_surround(self, region):
    if region.empty():
      return self.view.word(region.a)
    return region
  
  def get_closest_surrounding_regions(self, surround_chars, region):
    line_region = self.get_line_region_of_region(region)
    if not line_region:
      return None

    line = self.view.substr(line_region)
    begin, end = self.get_region_in_relation_to_line(region, line_region)
    if begin == 0 or end == len(line) - 1:
      return None

    start = self.find_surrounding_char_on_line_before(surround_chars[0], line, begin)
    if start < 0:
      return None

    stop = self.find_surrounding_char_on_line_after(surround_chars[1], line, end)
    if stop < 0:
      return None
    
    start += line_region.begin()
    stop += line_region.begin()
    
    return (sublime.Region(start, start + 1), sublime.Region(stop - 1, stop))
  
  def get_line_region_of_region(self, region):
    line_regions = self.view.lines(region)
    if not len(line_regions) == 1:
      return None
    return line_regions[0]

  def get_region_in_relation_to_line(self, region, line_region):
    return region.begin() - line_region.begin(), region.end() - line_region.begin()

  def find_surrounding_char_on_line_before(self, surround_char, line, begin):
    return line.rfind(surround_char, 0, begin)
  
  def find_surrounding_char_on_line_after(self, surround_char, line, end):
    return line.find(surround_char, end)

  def delete_surrounding_regions(self, regions):
    edit_sequence = self.view.begin_edit()
    self.view.erase(edit_sequence, regions[0])
    self.view.erase(edit_sequence, regions[1])
    self.view.end_edit(edit_sequence)

class ReplaceSurroundCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.window().show_input_panel('Replace surrounding [char] with [char]:', '', self.after_input, None, None)
  
  def after_input(self, text):
    if not text or len(text) < 2:
      return
    surround_chars = self.get_matching_char_pair(text[0])
    replace_chars = self.get_matching_char_pair(text[1])
    self.apply_surround_chars(surround_chars, replace_chars)

  def get_matching_char_pair(self, text):
    if text in MATCHING_CHARS:
      return MATCHING_CHARS[text]
    return [text, text]
  
  def apply_surround_chars(self, surround_chars, replace_chars):
    selected_regions = self.view.sel()
    for region in selected_regions:
      regions_to_replace = self.get_closest_surrounding_regions(surround_chars, region)
      if regions_to_replace:
        self.replace_surrounding_regions(regions_to_replace, replace_chars)
  
  def get_word_to_surround(self, region):
    if region.empty():
      return self.view.word(region.a)
    return region
  
  def get_closest_surrounding_regions(self, surround_chars, region):
    line_region = self.get_line_region_of_region(region)
    if not line_region:
      return None

    line = self.view.substr(line_region)
    begin, end = self.get_region_in_relation_to_line(region, line_region)
    if begin == 0 or end == len(line) - 1:
      return None

    start = self.find_surrounding_char_on_line_before(surround_chars[0], line, begin)
    if start < 0:
      return None

    stop = self.find_surrounding_char_on_line_after(surround_chars[1], line, end)
    if stop < 0:
      return None
    
    start += line_region.begin()
    stop += line_region.begin()
    
    return (sublime.Region(start, start + 1), sublime.Region(stop, stop + 1))
  
  def get_line_region_of_region(self, region):
    line_regions = self.view.lines(region)
    if not len(line_regions) == 1:
      return None
    return line_regions[0]

  def get_region_in_relation_to_line(self, region, line_region):
    return region.begin() - line_region.begin(), region.end() - line_region.begin()

  def find_surrounding_char_on_line_before(self, surround_char, line, begin):
    return line.rfind(surround_char, 0, begin)
  
  def find_surrounding_char_on_line_after(self, surround_char, line, end):
    return line.find(surround_char, end)

  def replace_surrounding_regions(self, regions, replace_chars):
    edit_sequence = self.view.begin_edit()
    self.view.replace(edit_sequence, regions[0], replace_chars[0])
    self.view.replace(edit_sequence, regions[1], replace_chars[1])
    self.view.end_edit(edit_sequence)
