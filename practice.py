import requests
import json
import random
import html
import pprint
url = "https://opentdb.com/api.php?amount=1"
end_game = ""
r= requests.get(url)
while end_game != "exit":
    if r.status_code != 200:
        end_game = input("Error fetching data from the API, please 'Enter' to try again later or quit")
    else:
        valid_answer = False 
        answer_number = 1   
        data= json.loads(r.text)
        question= data['results'][0]["question"]
        answers = data['results'][0]["incorrect_answers"]
        correct_answer = data['results'][0]["correct_answer"]
        answers.append(correct_answer)



        print(html.unescape(question) + "\n")
        random.shuffle(answers)
        for answer in answers:
            print(str(answer_number)  + ". " + html.unescape(answer))
            answer_number += 1
        while valid_answer == False:   
         user_answer=input("/nType the number of your answer and press 'Enter' to continue or type 'exit' to quit: ")
         try:
             user_answer = int(user_answer)
             if user_answer > len(answers) or user_answer < 0:
                    print("The input must be a number from '1 to 4' ")
             else:       
                    valid_answer = True
         except:
             print("The input must be a number from '1 to 4' ")    
             user_answer = answers[int(user_answer)-1]
  
        # print(json.dumps(data, indent=2))
        # print(data)

  
        if user_answer == correct_answer:
            print("Correct!")
        else:
            print("Incorrect! The correct answer was: " + html.unescape(correct_answer))
        end_game = input("Type 'exit' to quit or press 'Enter' to play again: ").lower()
print("Thanks for playing!")      
        


    

