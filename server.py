import socket
from _thread import *
import random
import sys
import time


answer = ''
points = [0,0,0] # A list to keep track of the participant's points
numlist = []
k = 0
server = socket.socket()
host = '127.0.0.1'
port = 8080
list_of_clients = []  # A list to keep track of the clients
try:
    server.bind((host, port))
except socket.error as e:
    print(str(e)) #An error is thrown instead of crashing if the host is already occupied

print('Waitiing for a Connection..')
server.listen(3)

lines = ['Who is the Prime minister of India? \n a.Narendra Modi b.Amit Shah c.Lk Advani d.Rahul Gandhi',
        'Who is the Pesident of India?\n a.Narendra Modi b.Pranah Mukherjee c.Ram Nath Kovind d.Venkaiah Naidu',
        'What is the value of 3*4?\n a.12 b.16 c. 20 d.7',
        'When was IIITB established?\n a.1998 b.1997 c.1996 d.1999',
        'What is the value 0f 5/5?\n a.1 b.2 c.0 d.3',
        'Who is the president of The USA?\n a.Hillary Clinton b.Barack Obama c.Donald Trump d.Joe Biden',
        'Which is the smallest state of India?\n a.Goa b.Kerala c.Meghalaya d.Mizoram',
        'What is the capital of Mizoram?\n a.Kohima b.Shillong c.Imphal d.Aizwal',
        'In which country did the coronavirus originate?\n a.China b.Japan c.South Korea d.North Korea',
        'Which planet is closest to the sun?\n a.Mercury b.Venus c.Pluto d.Mars',
        'Who is the captain of Indian cricket Team?\n a.Ms Dhoni b.Virat Kohli c.Rohit Sharma d.K l Rahul',
        'Who is the author of Vande Maataram\n a.Rabindranath Tagore b.Sri Aurobindo c.Jawaharlal Nehru d.Bankim Chandra Chatherjee',
        'What is the national animal of India\n a.Deer b.Lion c.Tiger d.Antelope',
        'Who is the Vice President of India\n a.Ram Nath Kovind b.Venkaiah Naidu c.Nirmal Sitharaman d.Rajnath Singh',
        'Of Which country is Kangaroo the national animal?\n a.New Zealand b.Australia c.Antarctica d.Japan',
        'What is the largest planet in the Solar System?\n a.Jupiter b.Saturn c.Uranus d.Earth',
        'Which of these is not a leap year?\n a.1900 b.1940 c.1980 d.2000',
        'Which is the largest continent in the world?\n a.Europe b.Asia c.Africa d.North America',
        'Which is the tallest mountain in the world?\n a.Mount k2 b.KanchenJunga c.Mount Everest d.Nanga Parbhat',
        'In which continent is the Amazon rain forest located?\n a.South America b.North America c.Australlia d.Africa',
        'Which is the smallest country in terms of area?\n a.Maldives b.Vatican City c.an Marino d.Nauru',
        'How many rings are present in the olympics logo?\n a.3 b.4 c.6 d.5'
        ] #list of questions
answers = ['a','c','a','d','a','c','a','d','a','a','b','d','c','b','b','a','a','b','c','a','b','d']#list of answers
threadcount = 0
numlist = random.sample(range(0,len(lines)),len(lines)-1)# TO generate random questions without repition
def quiz():
    global k
    global lines
    global answer
    global threadcount
    global numlist
    num = numlist[k]
    k += 1
    if(k == len(lines)-1):
        send_all("it's a tie\n")
        for i in range(0,threadcount):
            list_of_clients[i].send(('You have scored ' + str(points[i]) + " points\n").encode())
            list_of_clients[i].send(('GAME OVER !!\n').encode())
            threadcount = 0
        
    else:#If the question list exhausts before everyone wins it will be  atie
        for client in list_of_clients:
            client.send(('server: '+ lines[num]+'\n').encode())
            answer = answers[num]

def clientthread(conn):
    global answer
    global points
    global threadcount
    conn.send("Hello!! Welcome to the quiz\n\n The rules of the quiz are simple:\n\n1.You will be given questions with 4 options.\n2.You will have 10 seconds to click the buzzer.\n3.The one to click the buzzer first gets tWelcomeo answer the question\n4.There is no passing of the question\n5.Press any button to click the buzzer\n6.Scoing rules:\n  a.1 point for correct answer\n  b.-0.5 in all other cases\n \nThe person to reach five points first wins\n\n".encode())
    threadcount += 1
    while True:
        # time.sleep(10)
        try:
            message = conn.recv(2048)#recieving the message from the clien
        except:
            pass
        try:
            if message:
                for i in range(0,len(list_of_clients)):#To keep track of which client is responding
                    if(list_of_clients[i] == conn):
                        break
                send_all("player " + str(i+1) +" has clicked the buzer\n")
                conn.send(("Please enter your answer: ").encode())
                data = conn.recv(2048).decode()
                if(answer in data):  #Adds a point if the answer is correct
                    points[i] += 1
                    send_all('player ' + str(i+1) + ' got one point\n')
                else:                #Deducts half a point if the answer is wrong
                    points[i] -= 0.5
                    send_all('player ' + str(i+1) + ' lost half point\n')
                
                if(points[i] >= 5.0):      # The player and wins and the game closes if anyone's points are more than 5
                    for client in list_of_clients:
                        client.send(('Player ' + str(i+1) + ' wins\n\n').encode()) 

                    for i in range(0,threadcount):
                        list_of_clients[i].send(('You have scored ' + str(points[i]) + " points\n").encode())
                        list_of_clients[i].send(('GAME OVER !!\n').encode())
                    threadcount = 0                    # New set of clients van play with the server being on
                else:
                    for i in range(0,threadcount):
                        list_of_clients[i].send(('Your score is ' + str(points[i]) + "\n\n").encode())
                    quiz()        
        except:
            exit()
        
       
def send_all(input):           # A function to send a message to all the participants
    for client in list_of_clients:
        client.send(input.encode())          

while True:
    conn,addr = server.accept()  #Accepting the connection from the client
    list_of_clients.append(conn)   #Adding the clients into the list of clients list
    print ("connected to "+ str(addr))
    start_new_thread(clientthread,(conn,))
    time.sleep(2)
    if(threadcount == 3):     #The quiz will start if the number of clients reach 3
        quiz()
