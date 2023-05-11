import copy
from typing import Dict, Generator, List, Tuple, Union

import numpy as np
import pagexml.model.physical_document_model as pdm
import pagexml.helper.pagexml_helper as pagexml_helper
import pagexml.analysis.layout_stats as layout_helper
from pagexml.analysis.text_stats import WordBreakDetector

import republic.helper.paragraph_helper as para_helper
import republic.model.republic_document_model as rdm


def running_id_generator(base_id: str, suffix: str, count: int = 0):
    """Returns an ID generator based on running numbers."""

    def generate_id():
        nonlocal count
        count += 1
        return f'{base_id}{suffix}{count}'

    return generate_id


def is_paragraph_boundary(prev_line: Union[None, pdm.PageXMLTextLine],
                          curr_line: pdm.PageXMLTextLine,
                          next_line: Union[None, pdm.PageXMLTextLine]) -> bool:
    if prev_line and pdm.in_same_column(curr_line, prev_line):
        if curr_line.is_next_to(prev_line):
            # print("SAME HEIGHT", prev_line['text'], '\t', line['text'])
            return False
        elif curr_line.coords.left > prev_line.coords.left + 20:
            # this line is left indented w.r.t. the previous line
            # so is the start of a new paragraph
            return True
        elif curr_line.coords.left - prev_line.coords.left < 20:
            if curr_line.coords.right > prev_line.coords.right + 40:
                # this line starts at the same horizontal level as the previous line
                # but the previous line ends early, so is the end of a paragraph.
                return True
            else:
                return False
    elif next_line and pdm.in_same_column(curr_line, next_line):
        if curr_line.coords.left > next_line.coords.left + 20:
            return True
    return False


class ParagraphLines:

    def __init__(self, lines: Union[pdm.PageXMLTextLine, List[pdm.PageXMLTextLine]]):
        self.lines = []
        self.lefts: np.array = np.array([])
        self.rights: np.array = np.array([])
        self.widths: np.array = np.array([])
        self.heights: np.array = np.array([])
        self.top = None
        self.bottom = None
        self.avg_distances = np.empty(0)
        self.num_chars = 0
        self.avg_char_width = 0
        self.add_lines(lines)

    @property
    def json(self):
        return {
            'lefts': self.lefts,
            'rights': self.rights,
            'widths': self.widths,
            'heights': self.heights,
            'top': self.top,
            'bottom': self.bottom,
            'avg_distances': self.avg_distances,
            'num_chars': self.num_chars,
            'avg_char_width': self.avg_char_width,
            'lines': [line.text for line in self.lines],
        }

    @property
    def last(self):
        if len(self.lines) > 0:
            return self.lines[-1]
        else:
            return None

    def _set_left_right(self):
        coords_list = [line.baseline if line.baseline else line.coords for line in self.lines]
        self.lefts = np.array([coords.left for coords in coords_list])
        self.rights = np.array([coords.right for coords in coords_list])
        self.widths = np.array([coords.width for coords in coords_list])
        self.heights = np.array([coords.height for coords in coords_list])

    def _set_top_bottom(self):
        coords_list = [line.baseline if line.baseline else line.coords for line in self.lines]
        self.top = min([coords.top for coords in coords_list])
        self.bottom = max([coords.bottom for coords in coords_list])

    def add_lines(self, lines: Union[pdm.PageXMLTextLine, List[pdm.PageXMLTextLine]]):
        print('\tADDING LINES', lines)
        if isinstance(lines, pdm.PageXMLTextLine):
            lines = [lines]
        if len(self.lines) == 0:
            new_interval_lines = lines
        else:
            new_interval_lines = [self.lines[-1]] + lines
        for line in lines:
            if line.text is None:
                continue
            self.num_chars += len(line.text)
        self.lines.extend(lines)
        self._set_top_bottom()
        self._set_left_right()
        print(f'\tWIDTHS: {self.widths}\t\tSUM OF WIDTHS: {self.widths.sum()}\n')
        self.avg_char_width = self.widths.sum() / self.num_chars
        if len(new_interval_lines) >= 2:
            new_distances = layout_helper.get_line_distances(new_interval_lines)
            avg_distances = [point_distances.mean() for point_distances in new_distances]
            if len(self.avg_distances) > 0:
                avg_distances = [dist for dist in self.avg_distances] + avg_distances
            # print(avg_distances)
            self.avg_distances = np.array(avg_distances)

    def get_horizontal_overlap(self, element: pdm.PageXMLDoc):
        min_left, max_left = sorted([self.lefts.mean(), element.coords.left])
        min_right, max_right = sorted([self.rights.mean(), element.coords.right])
        return min_right - max_left, (min_right - max_left) / (max_right - min_left)


def get_relative_position(curr_line: pdm.PageXMLTextLine, para_lines: ParagraphLines):
    if len(para_lines.lines) == 0:
        raise ValueError(f'cannot get position relative to empty {para_lines.__class__.__name__}')
    if curr_line.metadata['scan_id'] != para_lines.lines[-1].metadata['scan_id']:
        left_indent, right_indent, vertical_distance, overlap_abs, overlap_ratio = -1, -1, -1, -1, -1
    else:
        line_coords = curr_line.baseline if curr_line.baseline else curr_line.coords
        line_bottom = line_coords.bottom
        overlap_abs, overlap_ratio = para_lines.get_horizontal_overlap(curr_line)
        left_indent = line_coords.left - para_lines.lefts.mean()
        right_indent = para_lines.rights.mean() - line_coords.right
        vertical_distance = line_bottom - para_lines.bottom
        # print('get_relative_position - line_bottom:', line_bottom)
        # print('get_relative_position - para_lines.bottom:', para_lines.bottom)
        # print('get_relative_position - vertical_distance:', vertical_distance)
    relative_position = {
        'left_indent': left_indent,
        'right_indent': right_indent,
        'vertical_distance': vertical_distance,
        'overlap_abs': overlap_abs,
        'overlap_ratio': overlap_ratio
    }
    return relative_position


def split_paragraphs(lines: List[pdm.PageXMLTextLine]):
    # find vertical gap
    # find left indentations
    # find right indentations
    # find horizontal overlap between pair of lines
    if lines[0].baseline:
        lefts = [line.baseline.left for line in lines]
    else:
        lefts = [line.coords.left for line in lines]
    if len(lines) <= 1:
        return lines
    paras = []
    para_lines = None
    for ci, curr_line in enumerate(lines):
        if curr_line.text is None:
            continue
        print('----------------------------------------------------------------------------')
        print('split_paragraphs - iterating lines - curr_line:', curr_line.text)
        coords = curr_line.coords
        baseline = curr_line.baseline
        # print(f'\t{coords.left: >4}-{coords.right: <4}\t{coords.top: >4}-{coords.bottom}')
        # print(f'\t{baseline.left: >4}-{baseline.right: <4}\t{baseline.top: >4}-{baseline.bottom}')
        # if para_lines:
        #     print(f'start of iteration, para_lines has {len(para_lines.lines)} lines')
        if para_lines is None or para_lines.last is None:
            print('\tSTART: empty para_lines')
            para_lines = ParagraphLines([curr_line])
            continue
        elif pdm.in_same_column(curr_line, para_lines.last) is False:
            print('\tSPLIT: different column, appending para_lines')
            paras.append(para_lines)
            yield para_lines
            para_lines = ParagraphLines([curr_line])
            continue
        else:
            rel_pos = get_relative_position(curr_line, para_lines)
            print('\n\tRELATIVE POSITION', rel_pos)
            print('\tpara_lines.avg_char_width:', para_lines.avg_char_width)
            # print('\tpara_lines - lines:', para_lines.lines)
            if rel_pos['vertical_distance'] > curr_line.coords.height * 2:
                # vertical distance to prev line is twice the height of current line
                # so this is probably the start of a new para
                print('\tSPLIT: vertical distance more than twice line height')
                paras.append(para_lines)
                yield para_lines
                para_lines = ParagraphLines([curr_line])
                continue
            if len(para_lines.lines) >= 2:
                if rel_pos['vertical_distance'] > para_lines.avg_distances.mean() * 1.5:
                    print('\tSPLIT: vertical distance more than 1.5 avg vertical distance')
                    paras.append(para_lines)
                    yield para_lines
                    para_lines = ParagraphLines([curr_line])
                    continue
            if rel_pos['overlap_ratio'] > 0.85:
                # curr_line and para are left- and right-aligned
                print('\tAPPEND: line and para are left- and right-aligned')
                para_lines.add_lines(curr_line)
                continue
            elif abs(rel_pos['left_indent']) < para_lines.avg_char_width * 3:
                # print('left_indent:', rel_pos['left_indent'], abs(rel_pos['left_indent']), para_lines.avg_char_width)
                # print(para_lines.json)
                if rel_pos['right_indent'] > para_lines.avg_char_width * 3:
                    # line and para are left-aligned but line is right-indented
                    print('\tAPPEND AND SPLIT: line and para are left-aligned but line is right-indented')
                    para_lines.add_lines(curr_line)
                    paras.append(para_lines)
                    yield para_lines
                    para_lines = None
                else:
                    # line is left-aligned with para but longer
                    print('\tAPPEND: line is left-aligned with para but longer')
                    para_lines.add_lines(curr_line)
            elif abs(rel_pos['right_indent']) < para_lines.avg_char_width * 2:
                # line and para are right-aligned
                if rel_pos['left_indent'] > 0:
                    # curr line is right-aligned with para, but is left-indented
                    print('\tAPPEND: curr line is right-aligned with para, but is left-indented')
                    para_lines.add_lines(curr_line)
                else:
                    # curr line is negatively left-indented, new para
                    print('\tSPLIT: curr line is negatively left-indented, new para')
                    paras.append(para_lines)
                    yield para_lines
                    para_lines = ParagraphLines([curr_line])
            else:
                # line and para are not aligned
                print('\tSPLIT: line and para are not aligned')
                paras.append(para_lines)
                yield para_lines
                para_lines = ParagraphLines([curr_line])
    if len(para_lines.lines) > 0:
        paras.append(para_lines)
        yield para_lines
    return paras


def is_resolution_gap(prev_line: pdm.PageXMLTextLine, line: pdm.PageXMLTextLine, resolution_gap: int) -> bool:
    # print('resolution_gap:', resolution_gap)
    # print('prev_line.coords.bottom:', prev_line.coords.bottom if prev_line else None)
    # print('line.coords.bottom:', line.coords.bottom)
    if not prev_line:
        return False
    # Resolution start line has big capital with low bottom.
    # If gap between box bottoms is small, this is no resolution gap.
    if -20 < line.coords.bottom - prev_line.coords.bottom < resolution_gap:
        # print('is_resolution_gap: False', line.coords.bottom - prev_line.coords.bottom)
        return False
    # If this line starts with a big capital, this is a resolution gap.
    if layout_helper.line_starts_with_big_capital(line):
        # print('is_resolution_gap: True, line starts with capital')
        return True
    # If the previous line has no big capital starting a resolution,
    # and it has a large vertical gap with the current line,
    # this is resolution gap.
    if not layout_helper.line_starts_with_big_capital(prev_line) and line.coords.top - prev_line.coords.top > 70:
        # print('is_resolution_gap: True', line.coords.bottom - prev_line.coords.bottom)
        return True
    else:
        # print('is_resolution_gap: False', line.coords.bottom - prev_line.coords.bottom)
        return False


class ParagraphGenerator:

    def __init__(self, line_break_detector: WordBreakDetector = None,
                 word_break_chars: str = None, use_left_indent: bool = False,
                 use_right_indent: bool = False,
                 resolution_gap: int = None):
        self.lbd = line_break_detector
        self.word_break_chars = word_break_chars
        self.use_left_indent = use_left_indent
        self.use_right_indent = use_right_indent
        self.resolution_gap = resolution_gap

    def get_paragraphs(self, doc: Union[pdm.PageXMLTextRegion, rdm.RepublicDoc],
                       prev_line: Union[None, dict] = None) -> Generator[rdm.RepublicParagraph, None, None]:
        if self.use_left_indent:
            paragraphs = self.get_paragraphs_with_left_indent(doc, prev_line=prev_line)
        elif self.use_right_indent:
            paragraphs = self.get_paragraphs_with_right_indent(doc, prev_line=prev_line)
        else:
            paragraphs = self.get_paragraphs_with_vertical_space(doc, prev_line=prev_line)
        for paragraph in paragraphs:
            paragraph.metadata['doc_id'] = doc.id
            yield paragraph

    def make_paragraph(self, doc: Union[pdm.PageXMLTextRegion, rdm.RepublicDoc],
                       doc_text_offset: int, paragraph_id: str,
                       para_lines: List[pdm.PageXMLTextLine]) -> rdm.RepublicParagraph:
        metadata = copy.deepcopy(doc.metadata)
        metadata['id'] = paragraph_id
        metadata['type'] = "paragraph"
        text_region_ids = []
        for line in para_lines:
            if line.metadata["parent_id"] not in text_region_ids:
                text_region_ids.append(line.metadata["parent_id"])
                if line.metadata['page_id'] not in metadata['page_ids']:
                    metadata['page_ids'].append(line.metadata['page_id'])
        text, line_ranges = self.make_paragraph_text(para_lines)
        paragraph = rdm.RepublicParagraph(lines=para_lines, metadata=metadata,
                                          text=text, line_ranges=line_ranges)
        paragraph.metadata["start_offset"] = doc_text_offset
        return paragraph

    def make_paragraph_text(self, lines: List[pdm.PageXMLTextLine]) -> Tuple[str, List[Dict[str, any]]]:
        text, line_ranges = pagexml_helper.make_text_region_text(lines, word_break_chars=self.word_break_chars)
        return text, line_ranges

    def get_paragraphs_with_left_indent(self, doc: Union[pdm.PageXMLTextRegion, rdm.RepublicDoc],
                                        prev_line: Union[None, pdm.PageXMLTextLine] = None,
                                        text_page_num_map: Dict[str, int] = None,
                                        page_num_map: Dict[str, int] = None) -> List[rdm.RepublicParagraph]:
        paragraphs: List[rdm.RepublicParagraph] = []
        generate_paragraph_id = running_id_generator(base_id=doc.id, suffix='-para-')
        para_lines = []
        doc_text_offset = 0
        lines = [line for line in doc.get_lines()]
        for li, line in enumerate(lines):
            if text_page_num_map is not None and line.metadata["parent_id"] in text_page_num_map:
                line.metadata["text_page_num"] = text_page_num_map[line.metadata["parent_id"]]
            line.metadata["page_num"] = page_num_map[line.metadata["parent_id"]]
            next_line = lines[li + 1] if len(lines) > (li + 1) else None
            if is_paragraph_boundary(prev_line, line, next_line):
                if len(para_lines) > 0:
                    paragraph = self.make_paragraph(doc, doc_text_offset, generate_paragraph_id(),
                                                    para_lines)
                    doc_text_offset += len(paragraph.text)
                    paragraphs.append(paragraph)
                para_lines = []
            para_lines.append(line)
            if not line.text or len(line.text) == 1:
                continue
            if prev_line and line.is_next_to(prev_line):
                continue
            prev_line = line
        if len(para_lines) > 0:
            paragraph = self.make_paragraph(doc, doc_text_offset, generate_paragraph_id(),
                                            para_lines)
            doc_text_offset += len(paragraph.text)
            paragraphs.append(paragraph)
        return paragraphs

    def get_paragraphs_with_right_indent(self, doc: Union[pdm.PageXMLTextRegion, rdm.RepublicDoc],
                                         prev_line: Union[None, dict] = None,
                                         text_page_num_map: Dict[str, int] = None,
                                         page_num_map: Dict[str, int] = None):
        lines = [line for line in doc.get_lines()]

    def get_paragraphs_with_vertical_space(self, doc: Union[pdm.PageXMLTextRegion, rdm.RepublicDoc],
                                           prev_line: Union[None, dict] = None,
                                           text_page_num_map: Dict[str, int] = None,
                                           page_num_map: Dict[str, int] = None) -> List[rdm.RepublicParagraph]:
        para_lines = []
        paragraphs = []
        doc_text_offset = 0
        generate_paragraph_id = running_id_generator(base_id=doc.metadata["id"], suffix="-para-")
        if self.resolution_gap is not None:
            resolution_gap = self.resolution_gap
            lines = [line for line in doc.get_lines()]
        elif isinstance(doc, rdm.Session) and doc.date.date.year < 1705:
            resolution_gap = 120
            margin_trs = []
            body_trs = []
            for tr in doc.text_regions:
                left_margin = 800 if tr.metadata['page_num'] % 2 == 0 else 3100
                if tr.coords.x < left_margin and tr.coords.width < 1000:
                    margin_trs.append(tr)
                else:
                    body_trs.append(tr)
            lines = [line for tr in body_trs for line in tr.lines]
        else:
            resolution_gap = 80
            lines = [line for line in doc.get_lines()]
        print('getting paragraphs with vertical space')
        print('number of lines:', len(lines))
        for li, line in enumerate(lines):
            if text_page_num_map is not None and line.metadata["parent_id"] in text_page_num_map:
                line.metadata["text_page_num"] = text_page_num_map[line.metadata["parent_id"]]
            if page_num_map is not None:
                line.metadata["page_num"] = page_num_map[line.metadata["parent_id"]]
            if prev_line:
                print(prev_line.coords.top, prev_line.coords.bottom, line.coords.top, line.coords.bottom, line.text)
            if is_resolution_gap(prev_line, line, resolution_gap):
                if len(para_lines) > 0:
                    paragraph = self.make_paragraph(doc, doc_text_offset,
                                                    generate_paragraph_id(), para_lines)
                    doc_text_offset += len(paragraph.text)
                    print('\tappending paragraph:', paragraph.id)
                    print('\t', paragraph.text)
                    print()
                    paragraphs.append(paragraph)
                para_lines = []
            para_lines.append(line)
            if not line.text or len(line.text) == 1:
                continue
            if prev_line and line.is_next_to(prev_line):
                continue
            prev_line = line
        if len(para_lines) > 0:
            paragraph = self.make_paragraph(doc, doc_text_offset, generate_paragraph_id(),
                                            para_lines)
            doc_text_offset += len(paragraph.text)
            paragraphs.append(paragraph)
        return paragraphs


