import republic_base_page_parser as page_parser

def is_resolution_header(line, hocr_page, DEBUG=False):
    # resolution header has either
    # year ( page_number )
    # date ( page_number )
    # ( page_number ) year
    # ( page_number ) date
    next_line = page_parser.get_next_line(hocr_page["lines"].index(line), hocr_page["lines"])
    if not is_header(line, next_line):
        return False
    if page_parser.get_highest_inter_word_space(line) < 300: # resolution header has widely spaced elements
        return False
    if not page_parser.has_left_aligned_text(line, hocr_page): # there should always be left-aligned text in a resolution header
        if DEBUG:
            print("\tNO LEFT-ALIGNED TEXT:", line)
        return False
    if not page_parser.has_right_aligned_text(line, hocr_page): # there should always be left-aligned text in a resolution header
        if DEBUG:
            print("\tNO RIGHT-ALIGNED TEXT:", line)
        return False
    resolution_score = score_resolution_header(line, hocr_page, DEBUG=DEBUG)
    if resolution_score > 3:
        if DEBUG:
            print("resolution_header_score:", resolution_score, "line: #{}#".format(line["line_text"]))
        return True
    else:
        return False
        #print(json.dumps(line, indent=2))


def score_resolution_header(line, hocr_page, DEBUG=False):
    resolution_score = 0
    if not line:
        return resolution_score
    if len(line["words"]) <= 6: # resolution header has few "words"
        resolution_score += 1
        if DEBUG:
            print("\tResolution test - few words")
    if page_parser.num_line_chars(line) > 8 and page_parser.num_line_chars(line) < 25: # page number + date is not too short, not too long
        resolution_score += 1
        if DEBUG:
            print("\tResolution test - few chars")
    if line["top"] < 250: # A resolution header is near the top of the page
        resolution_score += 1
        if DEBUG:
            print("\tResolution test - near top")
    if line["width"] > 750: # A resolution header is wide
        resolution_score += 1
        if DEBUG:
            print("\tResolution test - wide")
    if page_parser.get_highest_inter_word_space(line) > 450: # A resolution header has a wide empty centre
        resolution_score += 1
        if DEBUG:
            print("\tResolution test - high inter-word space")
    if page_parser.contains_year(line):
        resolution_score += 2
        if DEBUG:
            print("\tResolution test - contains year-like word")
    if resolution_score > 3:
        if DEBUG:
            print("\tResolution test - resolution_header_score:", resolution_score, "line: #{}#".format(line["line_text"]))
        #print(json.dumps(line, indent=2))
    return resolution_score


