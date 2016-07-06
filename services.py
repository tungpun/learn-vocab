#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import random

lhost = '0.0.0.0'
lport = 2006

def wrap_word(end, vie):
    word = {
        'eng': end,
        'vie': vie
    }
    return word

def extract_lines(lines):
    words = []
    for line in lines:
        eng = line.split(';')[0]
        vie = line.split(';')[1]
        words.append(wrap_word(eng, vie))
    return words


def build_database(unit):
    filename = 'unit' + str(unit) + '.txt'
    with open(filename, 'rb') as f:
        lines = f.readlines()
        words = extract_lines(lines)
    return words


def get_a_word(words):
    while (True):
        w = words[random.randint(0, len(words)-1)]
        if len(w['vie'].strip()) >= 5:
            return w

if __name__ == '__main__':
    all_count = 0
    right_count = 0
    while (True):
        l = listen(lport, lhost)
        c = l.wait_for_connection()
        c.send("Enter unit number: ")
        unit  = int(c.recvline().strip())
        words = build_database(unit)
        random.shuffle(words)
        i = 0
        while (True):
            #word = get_a_word(words)
            word = words[i % len(words)]
            try:
                c.send("VIE: " + word['vie'].strip() + " ?\nENG: ")
                all_count += 1
                answer = c.recvuntil('\n').strip()
                if answer == word['eng']:
                    c.sendline("Correct")
                    i += 1
                    right_count += 1
                else:
                    c.sendline("ANS: " + word['eng'].strip() + " <= Right\nIncorrect")
                c.sendline("Result: " + str(right_count) + "/" + str(all_count) + "\n")
            except Exception, e:
                c.close()
                break            
