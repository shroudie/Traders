from flask import request, jsonify, Blueprint, current_app, session, render_template

import traders_back.utils as utils
import traders_back.manage as manage
import datetime


chart = Blueprint('chart', __name__)
virtual_time = datetime.datetime(2018,1,1,18,0,0)


@chart.route('/chart_api')
def chart_api():
	return "candle api"

@chart.route('/charts')
def chart_page():
	return render_template('live_trading.html')
	
@chart.route('/available_exchange_rates')
def get_available_exchange_rates():
	q =\
	"""
	SELECT DISTINCT currency_from From ExchangeRates 
	"""
	return jsonify(utils.getter_db(q)['result'])
	

@chart.route('/chart_point', methods=['GET', 'POST'])
def chart_points():
	req = utils.get_req_data()
	fr = req['currency_from']
	to = req['currency_to']
	q =\
	"""
	SELECT * FROM ExchangeRates 
	WHERE TIME>%s
	AND currency_from=%s and currency_to=%s
	LIMIT 1
	"""
	
	if not "virtual_time" in session:
		session['virtual_time'] = virtual_time

	ret = utils.getter_db(q, (session['virtual_time'], fr, to))['result'][0]
	session['virtual_time'] = ret['time']
	return jsonify(ret)

"""
	Chart points every couple minutes, 5 mins by default
"""
@chart.route('/chart_history', methods=['POST'])
def char_history():
	req = utils.get_req_data()
	fr = req['currency_from']
	to = req['currency_to']
	granularity = int(req['granularity'])
	if not "virtual_time" in session:
		session['virtual_time'] = virtual_time
	q =\
	"""
	SELECT E.* FROM ExchangeRates E 
	NATURAL JOIN (
		SELECT max(E.id) as id, max(E.time) FROM ExchangeRates E
		WHERE currency_from=%s AND currency_to=%s
		AND (time<%s and time>%s)
		GROUP BY hour(time), floor(minute(time)/%s)
	) T
	"""
	return jsonify(utils.getter_db(q, (fr, to, session['virtual_time'], virtual_time, granularity))['result'])
	

@chart.route('/candle_history', methods=['POST'])
def candle_history():
	req = utils.get_req_data()
	fr = req['currency_from']
	to = req['currency_to']
	end = datetime.datetime.strptime(req['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
	granularity = int(req['granularity'])
	times = [end]
	while True:
		tmp = times[0] - datetime.timedelta(minutes=granularity)
		if tmp > virtual_time:
			times = [tmp] + times
		else:
			break
	ret = []
	for time in times:
		ret.append(find_candle(fr, to, time, granularity))
	return jsonify(ret)
		
	
@chart.route('/candle_point', methods=['POST'])
def candle_point():
	req = utils.get_req_data()
	fr = req['currency_from']
	to = req['currency_to']
	end = datetime.datetime.strptime(req['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
	granularity = int(req['granularity'])
	return jsonify(find_candle(fr, to, end, granularity))

def find_candle(fr, to, end, granularity):
	start = end - datetime.timedelta(minutes=granularity)
	q =\
	"""
	SELECT * FROM ExchangeRates 
	WHERE currency_from=%s AND currency_to=%s
	AND (time<%s and time>%s)
	"""
	data = utils.getter_db(q, (fr, to, end, start))['result']
	ret = {
		'open':None,
		'close':None,
		'high':None,
		'low':None
	}
	high = 0
	low = 10**5
	if len(data) > 0:
		ret['open'] = data[0]['ask']
		ret['high'] = data[0]['ask']
		ret['low'] = data[0]['ask']
		ret['close'] = data[-1]['ask']

		for row in data:
			if row['ask'] > ret['high']:
				ret['high'] = row['ask']
			if row['ask'] < ret['low']:
				ret['low'] = row['ask']
	return ret

@chart.route('/chart_clear')
def chart_clear():
	session.clear()
	return ""

@chart.route('/virtual_time')
def get_virtual_time():
	if not "virtual_time" in session:
		session['virtual_time'] = virtual_time
	return jsonify(session['virtual_time'])
	
