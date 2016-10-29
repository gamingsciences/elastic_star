# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 08:13:18 2016

@author: ken
"""

'''
elasticdump --input=http://admin:santafe1@33c192f38ba000038f45d61b4fe43cac.us-east-1.aws.found.io:9200/slot_player_stats --output=http://admin:santafe1@localhost:9200/slot_player_stats --type=data --searchBody '{"query": { "match_all": {} }, "stored_fields": ["*"], "_source": true }'
'''
