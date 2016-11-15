import random , json

import UssdHttp as ussd

class PhoneNumberScreen(ussd.screens.BaseScreen):

    def render(self,session,context):
        return "You're phone number is %s" % session.phone_number

class GuessingGame(ussd.screens.BaseScreen):

    TARGET_KEY = '_guessing_needle'
    GUESS_KEY = '_guessing_guess'
    # _has_next = True

    def render(self,session,context):
        if self.TARGET_KEY in session:
            guess , target = self.getattrs(session)
            guesses = len(session) - 1
            if guess < target:
                return 'Sorry, {} is not the number.\nMy number is higher.\n\nGuess count {}'.format(guess,guesses)
            elif guess > target:
                return 'Sorry, {} is not the number.\nMy number is lower.\n\nGuess count {}'.format(guess,guesses)
            elif guess == target:
                return 'Congratulations!\n\nThe number was {}.\n\nYou guessed it in {} tries'.format(guess,guesses)
        else:
            # First call to the game. Set a rangom number and display start message
            session[self.TARGET_KEY] = random.randint(0,100)
            return "I'm thinking of a number between 0 and 100 (inclusive).\n\nCan you guess it?"

    def input(self,input,session,context):
        # TODO: add error checking
        session[self.GUESS_KEY] = int(input)
        return self

    def getattrs(self,session):
        return session[self.GUESS_KEY] , session[self.TARGET_KEY]

    def has_next(self,session):
        guess , target = self.getattrs(session)
        return guess != target

class ConvertFinal(ussd.screens.BaseScreen):

    def render(self,session,context):
        converted = session['amount'] * session['currancy'].value
        return '{0[amount]:.2f} KSH\n=\n{1:.2f} {0[currancy].label}\n\nThansk for using USSD Converter'.format(session,converted)

convert_currancy = ussd.screens.SelectOne(labels=['USD','EUR','ZAR'],values=[0.0098,0.0092,0.14],name='currancy',next_screen=ConvertFinal())
convet_ammount = ussd.screens.FloatQuestion(question="Enter amount in KSH",name="amount",next_screen=convert_currancy)

class RandomWords(ussd.screens.BaseScreen):

    def __init__(self,language):
        self.words = json.load(open('USSDDemo/data/{}.json'.format(language)))

    def render(self,session,context):
        if len(session) == 1:
            response_str =  'Enter a character length.\n\nEnter a negative number to stop.'
        elif 0 < session['chars']:
            response_str = ''
            while True:
                missing = session['chars'] - len(response_str)
                if str(missing) in self.words.keys():
                    response_str += random.choice(self.words[str(missing)])
                    break
                elif len(response_str) > session['chars']:
                    response_str = response_str[:session['chars']]
                    break
                else:
                    response_str += random.choice(self.words[random.choice(self.words.keys())]) + ' '
        else:
            response_str = '\n'.join(['{0}. Chars {1}'.format(i+1,node.input) for i,node in enumerate(session.history[1:-1])])
            response_str += '\n\n -- {} hops --'.format(len(session))
        return response_str

    def input(self,input,session,context):
        session['chars'] = int(input)
        return self

    def has_next(self,session):
        if len(session) == 1:
            return True
        else:
            return 0 < session['chars']


########################################
# Main Demo App Menu
########################################
app = ussd.screens.MenuScreen(
    title="Simple USSD Test",
    items = [
        ('Guess A Number', GuessingGame() ),
        ('Convert KSH', convet_ammount),
        ('Random Swahili Words',RandomWords('swahili') ),
        ('Random Hindi Words', RandomWords('hindi') ),
        ('My Phone Number', PhoneNumberScreen() )
    ]
)
