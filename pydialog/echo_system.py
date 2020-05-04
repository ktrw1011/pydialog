import abc

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram_bot

class BaseSystem(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    def initial_message(self, input):
        raise NotImplementedError

    @abc.abstractclassmethod
    def reply(self, input):
        raise NotImplementedError

class EchoSystem(BaseSystem):
    def __init__(self):
        pass
 
    def initial_message(self, input):
        # 最初はNoneになっている(ユーザーからの発話を得るには？)
        text = input["utt"]
        sessionId = input["sessionId"]

        return {'utt': f'{text}\nこんにちは{sessionId}。対話を始めましょう。', 'end':False}
 
    def reply(self, input):
        return {"utt": input['utt'], "end": False}

if __name__ == "__main__":
    system = EchoSystem()
    bot = telegram_bot.TelegramBot(system)
    bot.run()