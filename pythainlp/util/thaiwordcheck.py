# -*- coding: utf-8 -*-
"""
Check if it's an "authentic Thai word"

Adapted from
https://github.com/wannaphongcom/open-thai-nlp-document/blob/master/check_thai_word.md

References
- ทีมงานทรูปลูกปัญญา 2015. ลักษณะของคำไทยแท้ http://www.trueplookpanya.com/learning/detail/30589-043067
- วารุณี บำรุงรส 2010. คำไทยแท้ https://www.gotoknow.org/posts/377619
"""
import re
import warnings

_THANTHAKHAT_CHAR = "\u0e4c"  # Thanthakhat (cancellation of sound)

# Non-authentic Thai characters
_TH_NON_THAI_CHARS = {
    "ฆ",
    "ณ",
    "ฌ",
    "ฎ",
    "ฏ",
    "ฐ",
    "ฑ",
    "ฒ",
    "ธ",
    "ศ",
    "ษ",
    "ฬ",
}

 # Known authentic Thai words (exceptions)
_TH_TRUE_THAI_WORD = {
    "ฆ่า",
    "เฆี่ยน",
    "ศึก",
    "ศอก",
    "เศิก",
    "เศร้า",
    "ธ",
    "ณ",
    "ฯพณฯ",
    "ใหญ่",
    "หญ้า",
    "ควาย",
    "ความ",
    "กริ่งเกรง",
    "ผลิ",
}

# Authentic Thai final consonants
_TH_TRUE_FINALS = {"ก", "ด", "บ", "น", "ง", "ม", "ย", "ว"}

# Diphthong prefixes (can starts authentic Thai word)
_TH_PREFIX_DIPHTHONG = {"กะ", "กระ", "ปะ", "ประ"}

# Thai alpabets filter
_TH_CONSONANTS_PATTERN = re.compile(r"[ก-ฬฮ]", re.U)


def is_authentic_thai(word: str) -> bool:
    """
    Check if a word is an "authentic Thai word" (Thai: "คำไทยแท้")

    :param str word: word
    :return: True or False
    :rtype: bool

    :Example:

    English word::

        from pythainlp.util import is_authentic_thai

        is_authentic_thai("Avocado")
        # output: False

    Authentic Thai word::

        is_authentic_thai("มะม่วง")
        # output: True
        is_authentic_thai("ตะวัน")
        # output: True

    Non authentic Thai word:

        is_authentic_thai("สามารถ")
        # output: False
        is_authentic_thai("อิสริยาภรณ์")
        # output: False
    """
    # Known authentic Thai words (exceptions)
    if word in _TH_TRUE_THAI_WORD:
        return True

    # If a word contains Thanthakhat, it is not an authentic Thai
    if _THANTHAKHAT_CHAR in word:
        return False

    # If a word contains non-Thai char, it is not an authentic Thai
    for ch in word:
        if ch in _TH_NON_THAI_CHARS:
            return False

    chs = re.findall(_TH_CONSONANTS_PATTERN, word)  # get only Thai alphabets
    if not chs:  # If do not contain any Thai alphabets -> cannot be Thai
        return False

    # If a word does not end with true final, it is not an authentic Thai
    if (len(chs) == 1) or (chs[len(chs) - 1] in _TH_TRUE_FINALS):
        return True

    # Note: This will not work, as it check the whole word, not the prefix.
    # Prefix-sentitive tokenization is required in order to able to check this.
    if word in _TH_PREFIX_DIPHTHONG:
        return True

    return False


def thaicheck(word: str) -> bool:
    warnings.warn(
        "thaicheck is deprecated, use is_authentic_thai instead",
        DeprecationWarning
    )
    return is_authentic_thai(word)
