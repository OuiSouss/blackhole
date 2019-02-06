from funct_base import *
import unittest
from pymongo import MongoClient

class BaseTest(unittest.TestCase):
	
	def setUp():
		client = MongoClient('localhost:27017')
		global dbr
		global dbi
		dbr = client.Route
		dbi = client.Security

	def test_insert():
    		#TODO
	def test_read():
		#TODO
	def test_activate():
  		#TODO
	def test_desactivate():
		#TODO
	def test_update():
		#TODO
	def test_delete():
		#TODO
	def test_register():
		#TODO
	def test_connect():
		#TODO
	def test_login():
   		#TODO
