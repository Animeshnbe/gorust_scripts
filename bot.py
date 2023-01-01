import re
import random

R_EATING = "I don't like eating anything because I'm a bot obviously!"
R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"


def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "That sounds funny",
                "What does that mean?"][
        random.randrange(4)]
    return response

def msg_prob(user_input,recognised_words,single_resp=False,required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_input:
        if word in recognised_words:
            message_certainty += 1

    for word in required_words:
        if word not in user_input:
            has_required_words = False
            break

    percent = float(message_certainty)/float(len(recognised_words))

    if has_required_words or single_resp:
        return int(percent*100)
    else:
        return 0

def check_all(msg):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_resp=False,required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = msg_prob(msg, list_of_words, single_resp, required_words)

    response('Hello!', ['hello', 'hi', 'sup', 'hey', 'hiya', 'hola', 'heyo'], single_resp=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('I was made in a lab in Hyderabad', ['where','are','you','from'], required_words=['where','from'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    print(highest_prob_list)

    return unknown() if highest_prob_list[best_match] < 1 else best_match

def get_resp(user_input):
    msg = re.split(r'\s+|[,;?!.-=\']\s*', user_input.lower())
    if msg in ["bye", "goodbye"]:
        return "Bye"
    response = check_all(msg)
    return response

while True:
    print('Canbot: ' + get_resp(input('You: ')))