#!/usr/bin/env python3
"""Build and inject Sino-Vietnamese (Hán - Việt) pronunciations into all HSK vocabulary files.

Sources:
1. OpenCC STCharacters (Simplified to Traditional mapping)
2. ph0ngp/hanviet-pinyin-wordlist (Hanzi to Sino-Vietnamese with pinyin mapping)
3. ryanphung/chinese-hanviet-api (Compound Sino-Vietnamese wordlist)
4. Curated manual overrides for polyphonic & high-frequency particles
"""

import ast
import csv
import glob
import io
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = ROOT / 'database/vocabs'
HSK30_DIR = VOCAB_DIR / 'hsk3_0'
TOPICS_DIR = VOCAB_DIR / 'topics'

# 1. Fetch & parse OpenCC STCharacters
print('Downloading OpenCC STCharacters...')
url_opencc = 'https://raw.githubusercontent.com/BYVoid/OpenCC/master/data/dictionary/STCharacters.txt'
req = urllib.request.Request(url_opencc, headers={'User-Agent': 'Mozilla/5.0'})
s2t = {}
with urllib.request.urlopen(req, timeout=30) as r:
    for line in r.read().decode('utf-8').splitlines():
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            s2t[parts[0]] = parts[1].split()

# 2. Fetch & parse hanviet.csv
print('Downloading hanviet.csv...')
url_hv = 'https://raw.githubusercontent.com/ph0ngp/hanviet-pinyin-wordlist/master/hanviet.csv'
req_hv = urllib.request.Request(url_hv, headers={'User-Agent': 'Mozilla/5.0'})
char_map = {}
with urllib.request.urlopen(req_hv, timeout=30) as r:
    reader = csv.reader(io.StringIO(r.read().decode('utf-8')))
    header = next(reader)
    for row in reader:
        if not row:
            continue
        ch = row[0]
        try:
            hv_list = ast.literal_eval(row[1])
        except Exception:
            hv_list = [row[1]]
        py = row[2] if len(row) > 2 else ''
        if ch not in char_map:
            char_map[ch] = {}
        if hv_list:
            char_map[ch][py] = hv_list[0]
            if '' not in char_map[ch]:
                char_map[ch][''] = hv_list[0]

# 3. Fetch & parse ryanphung compound database
print('Downloading ryanphung compound database...')
url_ryan = 'https://raw.githubusercontent.com/ryanphung/chinese-hanviet-api/master/db.json'
req_r = urllib.request.Request(url_ryan, headers={'User-Agent': 'Mozilla/5.0'})
ryan_dict = {}
with urllib.request.urlopen(req_r, timeout=30) as r:
    data = json.loads(r.read().decode('utf-8'))
    for item in data.get('words', []):
        w = item.get('word')
        hv = item.get('hanviet')
        if w and hv:
            # Capitalize each word in title case
            clean_hv = ' '.join(p.capitalize() for p in hv.strip().split())
            ryan_dict[w] = clean_hv

# 4. Manual overrides for high-frequency characters & grammatical particles
manual_chars = {
    '离': {'li2': 'ly', '': 'ly'},
    '着': {'zhe0': 'trước', 'zhe5': 'trước', 'zhao2': 'trước', 'zhuo2': 'trước', '': 'trước'},
    '痹': {'bi4': 'tý', '': 'tý'},
    '爸': {'ba4': 'ba', '': 'ba'},
    '妈': {'ma1': 'ma', '': 'ma'},
    '吗': {'ma0': 'ma', 'ma5': 'ma', '': 'ma'},
    '呢': {'ne0': 'ni', 'ne5': 'ni', '': 'ni'},
    '哪': {'na3': 'nả', '': 'nả'},
    '那': {'na4': 'na', '': 'na'},
    '这': {'zhe4': 'giá', '': 'giá'},
    '什': {'shen2': 'thập', '': 'thập'},
    '么': {'me0': 'ma', 'me5': 'ma', '': 'ma'},
    '几': {'ji3': 'kỷ', 'ji1': 'kỷ', '': 'kỷ'},
    '读': {'du2': 'độc', 'dou4': 'đậu', '': 'độc'},
    '打': {'da3': 'đả', 'da2': 'tá', '': 'đả'},
    '觉': {'jue2': 'giác', 'jiao4': 'giác', '': 'giác'},
    '没': {'mei2': 'một', 'mo4': 'mạt', '': 'một'},
    '说': {'shuo1': 'thuyết', '': 'thuyết'},
    '系': {'xi4': 'hệ', '': 'hệ'},
    '行': {'xing2': 'hành', 'hang2': 'hàng', '': 'hành'},
    '长': {'chang2': 'trường', 'zhang3': 'trưởng', '': 'trường'},
    '得': {'de0': 'đắc', 'de5': 'đắc', 'de2': 'đắc', 'dei3': 'đắc', '': 'đắc'},
    '便': {'bian4': 'tiện', 'pian2': 'tiện', '': 'tiện'},
    '重': {'zhong4': 'trọng', 'chong2': 'trùng', '': 'trọng'},
    '了': {'le0': 'liễu', 'le5': 'liễu', 'liao3': 'liễu', '': 'liễu'},
    '的': {'de0': 'đích', 'de5': 'đích', 'di2': 'đích', '': 'đích'},
    '地': {'de0': 'địa', 'de5': 'địa', 'di4': 'địa', '': 'địa'},
}
for c, d in manual_chars.items():
    if c not in char_map:
        char_map[c] = {}
    char_map[c].update(d)

# Curated overrides for multi-character words where standard Vietnamese usage is specific
curated_words = {
    '打电话': 'Đả Điện Thoại',
    '打篮球': 'Đả Lam Cầu',
    '打车': 'Đả Xa',
    '打听': 'Đả Thính',
    '打算': 'Đả Toán',
    '学校': 'Học Hiệu',
    '学生': 'Học Sinh',
    '大学生': 'Đại Học Sinh',
    '什么': 'Thập Ma',
    '怎么': 'Chẩm Ma',
    '怎么样': 'Chẩm Ma Dạng',
    '为什么': 'Vi Thập Ma',
    '我们': 'Ngã Môn',
    '你们': 'Nhĩ Môn',
    '他们': 'Tha Môn',
    '她们': 'Tha Môn',
    '它们': 'Tha Môn',
    '没关系': 'Một Quan Hệ',
    '没有': 'Một Hữu',
    '不要': 'Bất Yếu',
    '不知道': 'Bất Tri Đạo',
    '对不起': 'Đối Bất Khởi',
    '买东西': 'Mãi Đông Tây',
    '睡觉': 'Thụy Giác',
    '觉得': 'Giác Đắc',
    '认识': 'Nhận Thức',
    '知道': 'Tri Đạo',
    '先生': 'Tiên Sinh',
    '小姐': 'Tiểu Tỷ',
    '衣服': 'Y Phục',
    '医生': 'Y Sinh',
    '医院': 'Y Viện',
    '星期': 'Tinh Kỳ',
    '明天': 'Minh Thiên',
    '昨天': 'Tạc Thiên',
    '今天': 'Kim Thiên',
    '现在': 'Hiện Tại',
    '时候': 'Thời Hậu',
    '时间': 'Thời Gian',
    '小时': 'Tiểu Thời',
    '分钟': 'Phân Chung',
    '多少': 'Đa Thiểu',
    '高兴': 'Cao Hứng',
    '漂亮': 'Phiêu Lượng',
    '出租车': 'Xuất Tô Xa',
    '自行车': 'Tự Hành Xa',
    '火车站': 'Hỏa Xa Trạm',
    '公共汽车': 'Công Cộng Khí Xa',
    '机场': 'Cơ Trường',
    '铅笔': 'Duyên Bút',
    '毛笔': 'Mao Bút',
    '方便': 'Phương Tiện',
    '便宜': 'Tiện Nghi',
    '银行': 'Ngân Hàng',
    '决定': 'Quyết Định',
    '满意': 'Mãn Ý',
    '运动': 'Vận Động',
    '环境': 'Hoàn Cảnh',
    '介绍': 'Giới Thiệu',
    '可以': 'Khả Dĩ',
    '关系': 'Quan Hệ',
    '中国': 'Trung Quốc',
    '北京': 'Bắc Kinh',
    '汉语': 'Hán Ngữ',
    '中文': 'Trung Văn',
}


def get_char_hanviet(ch: str) -> str:
    if ch in char_map:
        return char_map[ch].get('', '')
    if ch in s2t:
        for tc in s2t[ch]:
            if tc in char_map:
                return char_map[tc].get('', '')
    return ''


def get_word_hanviet(hanzi: str) -> str:
    if hanzi in curated_words:
        return curated_words[hanzi]
    if hanzi in ryan_dict:
        return ryan_dict[hanzi]

    parts = []
    for ch in hanzi:
        if '\u4e00' <= ch <= '\u9fff':
            hv = get_char_hanviet(ch)
            parts.append(hv.capitalize() if hv else ch)
        else:
            parts.append(ch)
    return ' '.join(parts).strip()


def enrich_file(file_path: Path):
    with file_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f'Skipping non-list file: {file_path.name}')
        return

    updated_count = 0
    for item in data:
        if not isinstance(item, dict):
            continue
        hanzi = item.get('hanzi') or item.get('word')
        if not hanzi:
            continue
        hv = get_word_hanviet(hanzi)
        if hv:
            # Reconstruct dict with hanviet placed right after pinyin
            new_item = {}
            for k, v in item.items():
                new_item[k] = v
                if k == 'pinyin':
                    new_item['hanviet'] = hv
            if 'hanviet' not in new_item:
                new_item['hanviet'] = hv
            item.clear()
            item.update(new_item)
            updated_count += 1

    with file_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'Updated {updated_count}/{len(data)} entries in {file_path.name}')


def main():
    print('Enriching HSK 2.0 files...')
    for p in sorted(VOCAB_DIR.glob('hsk[1-6]_vocabularies.json')):
        enrich_file(p)

    print('\nEnriching HSK 3.0 files...')
    for p in sorted(HSK30_DIR.glob('level*.json')):
        enrich_file(p)

    print('\nEnriching Topics files...')
    for p in sorted(TOPICS_DIR.glob('*.json')):
        enrich_file(p)

    # Export a compact client-side character map for runtime lookup / fallbacks
    print('\nBuilding client-side hanviet character dictionary...')
    client_dict = {}
    for ch, d in char_map.items():
        val = d.get('', '')
        if val:
            client_dict[ch] = val.capitalize()
    # Add simplified variants
    for sch, tchs in s2t.items():
        if sch not in client_dict:
            for tc in tchs:
                if tc in client_dict:
                    client_dict[sch] = client_dict[tc]
                    break

    # Add curated words as compound entries
    compounds = dict(ryan_dict)
    compounds.update(curated_words)

    js_file = ROOT / 'assets/js/hanviet-dict.js'
    with js_file.open('w', encoding='utf-8') as f:
        f.write('// Auto-generated Sino-Vietnamese (Hán - Việt) dictionary & lookup helper.\n')
        f.write('const HANVIET_COMPOUNDS = ')
        json.dump(compounds, f, ensure_ascii=False, indent=None)
        f.write(';\n\n')
        f.write('const HANVIET_CHARS = ')
        json.dump(client_dict, f, ensure_ascii=False, indent=None)
        f.write(';\n\n')
        f.write('''function getWordHanViet(wordOrHanzi) {
  if (!wordOrHanzi) return '';
  if (typeof wordOrHanzi === 'object') {
    if (wordOrHanzi.hanviet) return wordOrHanzi.hanviet;
    wordOrHanzi = wordOrHanzi.hanzi || wordOrHanzi.word || '';
  }
  const str = String(wordOrHanzi).trim();
  if (!str) return '';
  if (typeof HANVIET_COMPOUNDS !== 'undefined' && HANVIET_COMPOUNDS[str]) {
    return HANVIET_COMPOUNDS[str];
  }
  const parts = [];
  for (const ch of str) {
    if (ch >= '\\u4e00' && ch <= '\\u9fff') {
      const hv = (typeof HANVIET_CHARS !== 'undefined' && HANVIET_CHARS[ch]) || ch;
      parts.push(hv);
    } else {
      parts.push(ch);
    }
  }
  return parts.join(' ').replace(/\\s+/g, ' ').trim();
}

if (typeof window !== 'undefined') {
  window.getWordHanViet = getWordHanViet;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { getWordHanViet };
}
''')
    print(f'Wrote client-side script to {js_file.name} (Chars: {len(client_dict)}, Compounds: {len(compounds)})')
    print('Done!')


if __name__ == '__main__':
    main()
