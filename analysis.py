from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract
import re

import init

def convert_pdfs(file_name):
    # leave off the extension for file_name
    directory = init.img_path.format(file_name + '/')
    if not os.path.exists(directory):
        os.makedirs(directory)

    pages = convert_from_path(init.pdf_path.format(file_name+'.pdf'), 500)

    for i in range(len(pages)):
        pages[i].save(init.img_path.format(file_name+'/'+str(i)+'.jpg'), 'jpeg')

def perform_ocr(file_path):
    return pytesseract.image_to_string(Image.open(file_path), config='--psm 6')

def get_important_lines(string):
    # string is ocr string from tesseract
    lines = string.split('\n')
    include_first_words = set([str(i) for i in range(0, len(lines))] + \
                          ['Skating', 'Transitions', 'Performance', 'Composition', 'Interpretation'])
    lines = [line for line in lines if re.split('[^0-9a-zA-Z]', line)[0] in include_first_words]
    return lines

def parse_lines(lines):
    start_line_re = '^[0-9]{1,2} [A-Za-z]+ [A-Z]{3} [0-9]{1,2} ([0-9]{1,3}\.[0-9]{2} ){3}[0-9]\.[0-9]{2}$'

def parse_technical_line(line):
    line_elements = [_ for _ in line[2:].split(' ') if _] # gets rid of any empty strings
    goes = [int(g) for g in line_elements if is_goe(g)] # extracts the goes from the judges

    pts = [float(s) for s in line_elements if is_score(s)] # extracts the judges scores
    element_pts = pts[0]
    goe_pts = pts[1]
    total_pts = pts[2]

    element = line_elements[0] if len(line_elements[0])>2 else line_elements[1]

    print('GOEs', goes)
    print('points', element_pts, goe_pts, total_pts)
    print('element', element)

def parse_pcs(line):
    split_line = line.split(' ')
    label = split_line[0]
    print(split_line)
    scores = [float(format_pcs_score(s)) for s in split_line if is_pc_score(s)]

    avg = scores[-1]
    judges_scores = scores[1:-1]
    factor = scores[0]

    print(label, avg, judges_scores, factor)

def is_goe(s):
    try:
        return int(s) in range(-5, 6)
    except:
        return False

def format_pcs_score(s):
    if ',' in s:
        s = '.'.join(s.split(','))
    elif ',' not in s and '.' not in s and (int(s)%25 == 0):
        s = s[0]+'.'+s[1:]
    return s

def is_pc_score(s):
    return re.match('^[0-9](\.|,)?[0-9]{2}$', s)

def is_score(s):
    return re.match('^[0-9]{1,3}\.[0-9]{2}$', s)

# def is_element(s):
    # return re.match('^[A-Za-z0-4]{3,}')

if __name__ == '__main__':
    # string = perform_ocr(init.img_path.format('llt19_seniorfs/0.jpg'))
    # lines = get_important_lines(string)
    # print(lines)
    # lines = ['1  AB2 3.00 1.02 5 3 3 3 4 4 3 4.02', '2 = 13+pi3 7.00 2.24 3 1 3 3 3 4 4 9.24', '3. AC2 3.00 1.08 4 3 4 3 3 4 4 4.08', '4 GL3 6.50 2.34 4 3 3 4 4 3 4 8.84', '5 = 13+pi3 7.00 2.24 4 3 3 3 3 3 4 9.24', '6 ME3+fm3 6.00 2.64 4 5 4 4 4 5 5 8.64', '7 Crt 4.50 1.62 4 3 4 2 4 3 4 6.12', '8 TE4 6.50 1.95 3 4 3 3 3 3 3 8.45', '9 Pad 6.00 2.16 4 4 3 3 3 5 4 8.16', '10 AW2 3.00 1.14 4 4 4 3 4 3 5 4.14']
    # for line in lines:
        # parse_technical_line(line)

    lines = ['Skating Skills 1.60 925 925 9,00 875 9,00 9,00 9,25 9.10', 'Transitions 1.60 9,00 9,00 9,00 850 900 9,25 8,75 8.95', 'Performance 1.60 925 975 9,25 9,00 9,00 9,50 9,25 9.25', 'Composition 1.60 950 950 9,00 875 9,00 9,25 9,50 9.25', 'Interpretation of the Music/Timing 1.60 925 950 9,25 9,25 9,00 9,25 9,50 9.30']
    for line in lines:
        parse_pcs(line)