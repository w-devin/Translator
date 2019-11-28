import os
import sys
import time
import shutil
import random

from googletrans import Translator

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('python main.py INPUT_PATH OUTPUT_PATH')
    exit()

  input_path = sys.argv[1]
  output_path = sys.argv[2]

  if os.path.exists(input_path):
    if os.path.exists(output_path):
      shutil.rmtree(output_path)
    shutil.copytree(input_path, output_path)
  else:
    print('input path not exists, exit')
    exit()

  translator = Translator(service_urls=['translate.google.cn'])

  for path, dir_list, file_list in os.walk(output_path):
    for text_file in file_list:
      with open(os.path.join(path, text_file), 'r') as f:
        lines = f.readlines()

      # Translate
      text = ''
      err_line_count = 0

      for line in lines:
        try:
            line_trans = translator.translate(line).text
            text = '\n'.join([text, line_trans])
            print('one line succeed')
        except Exception as e:
            print('one line err, {}'.format(e))
            text = '\n'.join([text, 'TRANSLATE_ERR'])
            err_line_count += 1

        #time.sleep(random.randint(0, 5))

      with open(os.path.join(path, text_file), 'w+') as f:
        text = f.write(text)

      print('translate succeed: {}, {} lines err'.format(
        os.path.join(path, text_file), err_line_count))
