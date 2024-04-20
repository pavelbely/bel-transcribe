
import re
import json
from pathlib import Path

maps_json = Path(__file__).with_name('maps.json')
with open('maps.json') as json_data:
    maps = json.load(json_data)
    json_data.close()

def get_replacer(pattern, replacement):
  def replacer(match):
    g = match.group()
    replaced_str= re.sub(pattern, replacement, g, flags=re.IGNORECASE)
    if g.islower(): return replaced_str.lower()
    if g.istitle(): return replaced_str.title()
    if g.isupper(): return replaced_str.upper()
    return replaced_str
  return replacer

def replace_text_with_replacements(input_text, replacements, is_full_word = False):
  result = input_text
  for key in replacements.keys():
    pattern = None
    if is_full_word:
      pattern = rf'\b({key})\b'
    else:
      pattern = rf'({key})'
    result = re.sub(pattern, get_replacer(pattern, replacements.get(key)), result, flags=re.IGNORECASE)
  return result

def replace(input_file, output_file):
  infile_path = Path(__file__).with_name(input_file)
  outfile_path = Path(__file__).with_name(output_file)
  with open(infile_path, 'r', encoding='utf-8') as infile, open(outfile_path, 'w', encoding='utf-8') as outfile:
      lines = infile.readlines()
      for line in lines:
          line = replace_text_with_replacements(line, maps['letter_map'])
          line = replace_text_with_replacements(line, maps['syllable_map'])
          line = replace_text_with_replacements(line, maps['syllable_group_map'])
          line = replace_text_with_replacements(line, maps['word_map'], True)
          outfile.write(line)
  print(f"Word replacements complete. Modified file saved to {output_file}")

replace('input.srt', 'output.srt')