import os, os.path

from pymongo import MongoClient
from lxml import etree

from kesh.schema import *

schemas = {'questions':QuestionSchema,
           'answers':AnswerSchema,
           'comments':CommentSchema,
           'post_history':PostHistorySchema,
           'post_links':PostLinkSchema,
           'users':UserSchema,
           'votes':VoteSchema,
           'tags':TagSchema}