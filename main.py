import os
import random
import sqlite3
global main_db, sql
main_db = sqlite3.connect("main.db")
sql = main_db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT,
    money BIGINT
);""")

main_db.commit()

# колода
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

# инициализация счета
wins = 0
losses = 0


def registration():
    global user_login
    user_login = input("Login: ")
    user_password = input("Password: ")
    global balance
    balance = 40
    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}' ")
    sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, balance))
    main_db.commit()
    print("Registration completed successfully! ")



def start():
    user_login = input("Login: ")
    user_password = input("Password: ")

    if sql.fetchone() is None:
        print("There is no such account. Please register at Black Jack")
        registration()
        print("Your balance =" + str(balance) +"$")
        game()
        enter()
    else:
        game()
        enter()

    sql.execute(f"SELECT balance FROM users WHERE login = '{user_login}'")
    sql.execute(f'SELECT login FROM users WHERE login = "{user_login}"')

def moneyup(balance):
    print("You win :( , your balance =" + str(balance + 10) +"$")

def moneybjup(balance):
    print("You win :( , your balance = " + str(balance + 20) +"$")

def moneybjdown(balance):
    print("You lose :) , your balance = " + str(balance - 20) +"$")

def moneydown(balance):
    print("You lose :) , your balance = " + str(balance - 10) +"$")

def enter():
    for i in sql.execute('SELECT login, cash FROM users'):
        print(i)

def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        if card == 10:card = "J"
        if card == 10:card = "Q"
        if card == 10:card = "K"
        if card == 11:card = "A"
        hand.append(card)
    return hand

# метод сыграть еще раз
def play_again():
    again = input("Do you want to play again? (Yes/No) : ").lower()

    if again == "yes" or again == "Yes":
        dealer_hand = []
        player_hand = []
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        game()
    elif again == "No" or again == "no":
        print("Bye!")
        exit()
    else:
        print("Print correct answer")
        play_again()

# метод подсчета очков старших карт
def total(hand):
    total = 0

    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif card == "A":
            if total >= 11: total += 1
            else: total += 11
        else: total += card

    return total

# метод взять карту из колоды
def hit(hand):
    card = deck.pop()

    if card == 10:card = "J"
    if card == 10:card = "Q"
    if card == 10:card = "K"
    if card == 11:card = "A"

    hand.append(card)

    return hand

# метод очистки терминала
def clear():

    if os.name == 'nt':
        os.system('CLS')
    if os.name == 'posix':
        os.system('clear')

# метод вывода результата
def print_results(dealer_hand, player_hand):
    clear()

    print("\n    WELCOME TO BLACKJACK!\n")
    print("-"*30+"\n")
    print("    \033[1;32;40mWINS:  \033[1;37;40m%s   \033[1;31;40mLOSSES:  \033[1;37;40m%s\n" % (wins, losses))
    print("-"*30+"\n")
    print("The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)))
    print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))

# метод blackjack останавливает игру и выводит сообщение о победе/поражении игрока, набравшего 21 очко
def blackjack(dealer_hand, player_hand):
    global wins
    global losses

    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Congratulations! You got a Blackjack!\n")
        wins += 1
        moneybjup(balance)
        play_again()
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Sorry, you lose. The dealer got a blackjack.\n")
        losses += 1
        moneybjdown(balance)
        play_again()

# метод score обновляет глобальные переменные wins и losses
def score(dealer_hand, player_hand):
        global wins
        global losses

        if total(player_hand) == 21:
            print_results(dealer_hand, player_hand)
            print("Congratulations! You got a Blackjack!\n")
            wins += 1
            moneybjup(balance)
        elif total(dealer_hand) == 21:
            print_results(dealer_hand, player_hand)
            print("Sorry, you lose. The dealer got a blackjack.\n")
            losses += 1
            moneybjdown(balance)
        elif total(player_hand) > 21:
            print_results(dealer_hand, player_hand)
            print("Sorry. You busted. You lose.\n")
            losses += 1
            moneydown(balance)
        elif total(dealer_hand) > 21:
            print_results(dealer_hand, player_hand)
            print("Dealer busts. You win!\n")
            wins += 1
            moneyup(balance)
        elif total(player_hand) < total(dealer_hand):
            print_results(dealer_hand, player_hand)
            print("Sorry. Your score isn't higher than the dealer. You lose.\n")
            losses += 1
            moneydown(balance)
        elif total(player_hand) > total(dealer_hand):
            print_results(dealer_hand, player_hand)
            print("Congratulations. Your score is higher than the dealer. You win\n")
            wins += 1
            moneyup(balance)
# метод реализации самой игры
def game():
    global wins
    global losses
    choice = 0
    clear()

    print("\n    WELCOME TO BLACKJACK!\n")
    print("-"*30+"\n")
    print("    \033[1;32;40mWINS:  \033[1;37;40m%s   \033[1;31;40mLOSSES:  \033[1;37;40m%s\n" % (wins, losses))
    print("-"*30+"\n")

    dealer_hand = deal(deck)
    player_hand = deal(deck)

    print ("The dealer is showing a " + str(dealer_hand[0]))
    print ("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
    blackjack(dealer_hand, player_hand)
    quit = False

    while not quit:
        choice = input("Do you want to [H]it, [S]tand, or [Q]uit: ").lower()
        if choice == "H" or choice == "h":
            hit(player_hand)
            print(player_hand)
            print("Hand total: " + str(total(player_hand)))
            if total(player_hand) > 21:
                print('You busted')
                print("Dealer hand total: " + str(total(dealer_hand)))
                losses += 1
                moneydown(balance)
                play_again()
            elif total(player_hand) == 21:
                blackjack(dealer_hand, player_hand)
        elif choice =="S" or choice == "s":
            while total(dealer_hand) < 17:
                hit(dealer_hand)
                print(dealer_hand)
                if total(dealer_hand) > 21:
                    print("Dealer hand total: " + str(total(dealer_hand)))
                    print('Dealer busts, you win!')
                    wins += 1
                    moneyup(balance)
                    play_again()
            score(dealer_hand,player_hand)
            play_again()
        elif choice == "Q" or choice == "q":
            print("Bye!")
            quit = True

            exit()

start()

