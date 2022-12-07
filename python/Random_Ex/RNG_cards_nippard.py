import random

cardTypes = ['SPADES','CLUBS','HEARTHS','DIAMONDS']
cardNumbers = [i for i in range(2,11)]
specialCards = ['JACK','QUEEN','KING','ACE']

deck = []
def createDeck():
    i=0
    for cardType in cardTypes:
        deck.append([])
        for cardNumber in cardNumbers:
            deck[i].append('{} of {}'.format(cardNumber,cardType))

        for specialCard in specialCards:
            deck[i].append('{} of {}'.format(specialCard,cardType))
        i+=1


createDeck()

SPADES = [
"Push Ups",
"Pike push ups",
"Dumbbell press",
"Lateral raises"
]
CLUBS = [
"Pull ups",
"Table/Desk inverted row [or dumbbell row]",
"Rear delt flyes",
"Deadlift"
]
HEARTS=[
"Walking lunges",
"Bulgarian split squat (pistol squad with one leg raised behind)",
"Single leg hip thrust",
"Fitness Ball Hamstring Curls"
]
DIAMONDS =[
"Biceps curl ",
"Triceps skullcrushers against a tabletop",
"Dips",
"Chin ups"
]

rngWorkout = []
rngWorkoutCards = []

def randomWorkout():
    i=0
    while i<20:
        randomType = random.randint(0,3)
        randomCard = random.randint(0,12)
        if deck[randomType][randomCard] not in rngWorkoutCards:
            rngWorkoutCards.append(deck[randomType][randomCard])
            i+=1

randomWorkout()

def getExercises():
    spadesIndex=0
    clubsIndex=0
    heartsIndex=0
    diamondsIndex=0
    exercise = 1
    for card in rngWorkoutCards:
        if 'SPADES' in card:
            card= "".join(card.rsplit(' of SPADES'))
            if card.isnumeric():
                reps=10+int(card)
            elif card == 'ACE':
                reps = 0
            else:
                reps = 20
            print('{}.'.format(exercise),SPADES[spadesIndex], 'reps: {}'.format(reps))
            spadesIndex+=1
            if spadesIndex == 4:
                spadesIndex =0
        if 'CLUBS' in card:
            card= "".join(card.rsplit(' of CLUBS'))
            if card.isnumeric():
                reps=10+int(card)
            elif card == 'ACE':
                reps = 0
            else:
                reps = 20
            print('{}.'.format(exercise),CLUBS[clubsIndex], 'reps: {}'.format(reps))
            clubsIndex+=1
            if clubsIndex == 4:
                clubsIndex =0
        if 'HEARTHS' in card:
            card= "".join(card.rsplit(' of HEARTHS'))
            if card.isnumeric():
                reps=10+int(card)
            elif card == 'ACE':
                reps = 0
            else:
                reps = 20
            print('{}.'.format(exercise),HEARTS[heartsIndex], 'reps: {}'.format(reps))
            heartsIndex+=1
            if heartsIndex == 4:
                heartsIndex =0
        if 'DIAMONDS' in card:
            card= "".join(card.rsplit(' of DIAMONDS'))
            if card.isnumeric():
                reps=10+int(card)
            elif card == 'ACE':
                reps = 0
            else:
                reps = 20
            print('{}.'.format(exercise),DIAMONDS[diamondsIndex], 'reps: {}'.format(reps))
            diamondsIndex+=1
            if diamondsIndex == 4:
                diamondsIndex =0
        exercise+=1

getExercises()
input("\npress enter close to exit") 