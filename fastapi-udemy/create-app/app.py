import streamlit as st
import requests
import datetime
import json
import pandas as pd


page = st.sidebar.selectbox('choose your page', ['users', 'rooms', 'bookings'])

if page == 'users':
				st.title('ユーザー登録画面')
				with st.form(key='user'):
					# user_id: int = random.randint(0, 100)
					username: str = st.text_input('ユーザー名', max_chars=12)
					data = {
						# 'user_id': user_id,
						'username': username
					}
					submit_button = st.form_submit_button(label='リクエスト送信')

				if submit_button:
					st.write('## レスポンス結果')
					url="http://127.0.0.1:8000/users"
					res = requests.post(
									url, 
									data=json.dumps(data)
					)
					if res.status_code ==	200:
									st.success('ユーザー登録完了')
					st.json(res.json())

elif page == 'rooms':
			st.title('会議室登録画面')
			with st.form(key='room'):
							room_name: str = st.text_input('客室名', max_chars=12)
							capacity: int = st.number_input('定員', step=1)
							data = {
								'room_name': room_name,
								'capacity': capacity
							}
							submit_button = st.form_submit_button(label='会議室登録')

							if submit_button:
											url="http://127.0.0.1:8000/rooms"
											res = requests.post(url, data=json.dumps(data))
											if res.status_code ==	200:
															st.success('会議室登録完了')
											st.json(res.json())

elif page == 'bookings':
	st.title('会議室予約画面')
	# ユーザー一覧
	url_users = 'http://127.0.0.1:8000/users'
	res = requests.get(url_users)
	users = res.json()
	# ユーザー名をキー、ユーザーIDをバリュー
	users_dict = {}
	for user in users:
		users_dict[user['username']] = user['user_id']
	# 会議室一覧の取得
	url_rooms = 'http://127.0.0.1:8000/rooms'
	res = requests.get(url_rooms)
	rooms = res.json()
	rooms_dict = {}
	for room in rooms:
		rooms_dict[room['room_name']] = {
			'room_id': room['room_id'],
			'capacity': room['capacity']
			}

	st.write("### 会議室一覧")
	df_rooms = pd.DataFrame(rooms)
	df_rooms.columns = ["会議室名", "予約人数", "会議室ID"]


	with st.form(key='booking'):
		username: str = st.selectbox('予約者名', users_dict.keys())
		room_name: str = st.selectbox('会議室名', rooms_dict.keys())
		booked_num: int = st.number_input('予約人数', step=1, min_value=1)
		date = st.date_input('日付: ',min_value=datetime.date.today())
		start_time = st.time_input('開始時刻: ',value=datetime.time(hour=9, minute=0))
		end_time = st.time_input('終了時刻: ',value=datetime.time(hour=20, minute=0))
		submit_button = st.form_submit_button(label='予約登録')

	if submit_button:
		user_id: int = users_dict[username]
		room_id: int = rooms_dict[room_name]['room_id']
		capacity: int = rooms_dict[room_name]['capacity']

		data = {
			'room_id': room_id,
			'user_id': user_id,
			'booked_num': booked_num,
			'start_datetime': datetime.datetime(
				year=date.year,
				month=date.month,
				day=date.day,
				hour=start_time.hour,
				minute=start_time.minute
			).isoformat(),
			'end_datetime': datetime.datetime(
				year=date.year,
				month=date.month,
				day=date.day,
				hour=end_time.hour,
				minute=end_time.minute
			).isoformat()
			}
		
		if booked_num <= capacity:
			# 会議室予約
			url="http://127.0.0.1:8000/bookings"
			res = requests.post(url, data=json.dumps(data))
			if res.status_code == 200:
				st.write('予約完了')
			st.json(res.json())
		
		else:
			st.error(f'{room_name}の店員は、〜')