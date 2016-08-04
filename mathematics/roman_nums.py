from bisect import bisect_left

N = 13  # up to 3999
DEC = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
ROM = ['I', 'IV', 'V', 'IX', 'X', 'XL', 'L', 'XC', 'C', 'CD', 'D', 'CM', 'M']

def dec_to_roman(x):
    assert 0 <= x <= 3999
    r = []
    while x > 0:
        i = bisect_left(DEC, x)
        if i == N or x < DEC[i]:
            i -= 1
        r.append(ROM[i])
        x -= DEC[i]
    return ''.join(r)

def roman_to_dec(xs):
    d = dict(zip(ROM, DEC))
    r = 0
    while len(xs) > 0:
        if xs[:2] in d:
            r += d[xs[:2]]
            xs = xs[2:]
        else:
            r += d[xs[0]]
            xs = xs[1:]
    return r

if __name__ == '__main__':
    for d, r in [(0, ''), (1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'), (6, 'VI'), (7, 'VII'), (8, 'VIII'),
                 (9, 'IX'), (10, 'X'), (11, 'XI'), (12, 'XII'), (13, 'XIII'), (14, 'XIV'), (15, 'XV'), (16, 'XVI'),
                 (17, 'XVII'), (18, 'XVIII'), (19, 'XIX'), (20, 'XX'), (21, 'XXI'), (22, 'XXII'), (23, 'XXIII'),
                 (24, 'XXIV'), (25, 'XXV'), (26, 'XXVI'), (27, 'XXVII'), (28, 'XXVIII'), (29, 'XXIX'), (30, 'XXX'),
                 (31, 'XXXI'), (32, 'XXXII'), (33, 'XXXIII'), (34, 'XXXIV'), (35, 'XXXV'), (36, 'XXXVI'), (37, 'XXXVII'),
                 (38, 'XXXVIII'), (39, 'XXXIX'), (40, 'XL'), (41, 'XLI'), (42, 'XLII'), (43, 'XLIII'), (44, 'XLIV'),
                 (45, 'XLV'), (46, 'XLVI'), (47, 'XLVII'), (48, 'XLVIII'), (49, 'XLIX'), (50, 'L'), (51, 'LI'),
                 (52, 'LII'), (53, 'LIII'), (54, 'LIV'), (55, 'LV'), (56, 'LVI'), (57, 'LVII'), (58, 'LVIII'),
                 (59, 'LIX'), (60, 'LX'), (61, 'LXI'), (62, 'LXII'), (63, 'LXIII'), (64, 'LXIV'), (65, 'LXV'),
                 (66, 'LXVI'), (67, 'LXVII'), (68, 'LXVIII'), (69, 'LXIX'), (70, 'LXX'), (71, 'LXXI'), (72, 'LXXII'),
                 (73, 'LXXIII'), (74, 'LXXIV'), (75, 'LXXV'), (76, 'LXXVI'), (77, 'LXXVII'), (78, 'LXXVIII'),
                 (79, 'LXXIX'), (80, 'LXXX'), (81, 'LXXXI'), (82, 'LXXXII'), (83, 'LXXXIII'), (84, 'LXXXIV'),
                 (85, 'LXXXV'), (86, 'LXXXVI'), (87, 'LXXXVII'), (88, 'LXXXVIII'), (89, 'LXXXIX'), (90, 'XC'),
                 (91, 'XCI'), (92, 'XCII'), (93, 'XCIII'), (94, 'XCIV'), (95, 'XCV'), (96, 'XCVI'), (97, 'XCVII'),
                 (98, 'XCVIII'), (99, 'XCIX'), (100, 'C'), (200, 'CC'), (300, 'CCC'), (400, 'CD'), (500, 'D'),
                 (600, 'DC'), (700, 'DCC'), (800, 'DCCC'), (900, 'CM'), (1000, 'M'), (1100, 'MC'), (1200, 'MCC'),
                 (1300, 'MCCC'), (1400, 'MCD'), (1500, 'MD'), (1600, 'MDC'), (1700, 'MDCC'), (1800, 'MDCCC'),
                 (1900, 'MCM'), (1990, 'MCMXC'), (1991, 'MCMXCI'), (1992, 'MCMXCII'), (1993, 'MCMXCIII'),
                 (1994, 'MCMXCIV'), (1995, 'MCMXCV'), (1996, 'MCMXCVI'), (1997, 'MCMXCVII'), (1998, 'MCMXCVIII'),
                 (1999, 'MCMXCIX'), (2000, 'MM'), (2001, 'MMI'), (2002, 'MMII'), (2003, 'MMIII'), (2004, 'MMIV'),
                 (2005, 'MMV'), (2006, 'MMVI'), (2007, 'MMVII'), (2008, 'MMVIII'), (2009, 'MMIX'), (2010, 'MMX'),
                 (2011, 'MMXI'), (2012, 'MMXII'), (2013, 'MMXIII'), (2014, 'MMXIV'), (2015, 'MMXV'), (2016, 'MMXVI'),
                 (2017, 'MMXVII'), (2018, 'MMXVIII'), (2019, 'MMXIX'), (2020, 'MMXX'), (3549, 'MMMDXLIX')]:
        assert dec_to_roman(d) == r
        assert roman_to_dec(r) == d
