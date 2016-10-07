# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com

import json
import random
import traceback
from sqlalchemy.orm.exc import NoResultFound

import tornado.web
from ..db.user_answer import Answer

from config import *
from tornado.httpclient import HTTPRequest,HTTPClient,HTTPError
import tornado.web
import tornado.gen
import urllib,json

class LoginHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def get(self):
		self.render('login.html')

	def post(self):

		#验证用户身份
		retjson={
				'code':200,
				'text':"登录成功,请开始答题"
				}
		studentnum = self.get_argument('studentnum',default=None)
		password = self.get_argument('password',default=None)

		if studentnum in ban:
			retjson['code'] = 300
			retjson['text'] = u'阿偶不让你们参加(｡◕ˇε ˇ◕｡)'

		result = self.newAuthApi(studentnum,password)

		print 'resultcode:',result['code']


		if result['code']==200:
			#随机生成一个题目列表
			qarray = self.get_random(0,50)
			qlist = ''
			for i in range(0,50):
				qlist += str(qarray[i])+','
			try:
				answer = self.db.query(Answer).filter(Answer.username == studentnum).one()
				retjson['code'] = 401
				retjson['text'] = u'已经完成答题'
			except NoResultFound:
				answer = Answer(username=studentnum,questionList=qlist)
				self.db.add(answer)
				self.db.commit()
				self.set_secure_cookie("user",studentnum,expires_days=2)
			except:
				traceback.print_exc()
				retjson['code'] = 500
				retjson['text'] = u'数据库链接异常，请联系后台管理员'
		elif result['code'] == 400:
			retjson['code'] = 400
			retjson['text'] = u'密码错误或网络故障，请稍后再试'
		else:
			retjson['code'] = 500
			retjson['text'] = u'系统错误，请联系后台管理员'
		print retjson
		self.write(json.dumps(retjson))


	def authApi(self,username,password):
		data = {
				'user':username,
				'password':password,
				'appid':'34cc6df78cfa7cd457284e4fc377559e'
			}
		result = {'code':200,'content':''}
		try:
			client = HTTPClient()
			request = HTTPRequest(
				CHECK_URL,
				method='POST',
				body=urllib.urlencode(data),
				request_timeout=TIME_OUT)
			response = client.fetch(request)
			if '401' in response.body:
				result['code'] = 400
		except Exception,e:
			traceback.print_exc()
		return result

	def newAuthApi(self,username,password):
		data = {
				'username':username,
				'password':password
			}
		result = {'code':200,'content':''}
		try:
			client = HTTPClient()
			request = HTTPRequest(
				CHECK_URL,
				method='POST',
				body=urllib.urlencode(data),
				validate_cert=False,
				request_timeout=TIME_OUT)
			response = client.fetch(request)
			header = response.headers
			if 'Ssocookie' in header.keys():
				headertemp = json.loads(header['Ssocookie'])
				cookie = headertemp[0]['cookieName']+"="+headertemp[0]['cookieValue']
				cookie += ";"+header['Set-Cookie'].split(";")[0]
				result['content'] = cookie
			else:
				result['code'] = 400
		except HTTPError as e:
			result['code'] = 400
		except Exception,e:
			result['code'] = 500
		return result


	def get_random(self,first,len):
			rand = []
			for i in range(first,len):
				rand.append(i)
			for i in range(first,len):
				temp1 = random.randint(first,len-1)
				temp2 = random.randint(first,len-1)
				c = rand[temp1]
				rand[temp1] = rand[temp2]
				rand[temp2] = c
			return rand




