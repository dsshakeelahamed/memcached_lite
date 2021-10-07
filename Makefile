run: server test_cases client

server:
	pip install -r requirements.txt
	nohup python3 ./main.py & > server.log
	sleep 2

client:
	python3 ./repl.py

test_cases:
	python3 -m unittest test_cases.py
