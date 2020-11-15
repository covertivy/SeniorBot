BOT_FILE = SeniorBot.py
NECESSARY_FILES = ${BOT_FILE} botconfig.cfg BotData.py

all: SeniorBot.exe

SeniorBot.exe: ${NECESSARY_FILES}
	pyinstaller -F ${BOT_FILE}
	mv ./dist/SeniorBot.exe ./SeniorBot.exe
	make clean

pip: requirements.txt
	pip install -r $^

clean:
	rm -rf ./build/ ./dist/ SeniorBot.spec
