import requests
import json

def main():
	url="https://ofj4dj.deta.dev"
	data = {
		'x': 12,
		'y': 3
	}
	res = requests.post(url, json.dumps(data))
	print(res.json())

if __name__ == "__main__":
	main()