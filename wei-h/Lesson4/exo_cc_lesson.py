# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:03:53 2014

@author: wei he
"""
import re




credit_cards = 'Thanks for paying with 1111-2222-3333-4444 and with 5555-6666-7777-8888'

cred = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}-')


# input credit_card
# cred.findall(credit_cards)
# $ la fin de chaine


