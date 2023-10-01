import json
from difflib import get_close_matches

#load the knowledge from a json file

def load_knowledge(file_path:str)->dict:
    with open(file_path,'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge(file_path:str, data:dict):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)


def find_best_match(user_question:str,questions:list[str]) -> str | None:
    matches:list =get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question:str, knowledgebase:dict) -> str | None:
    for q in knowledgebase["questions"]:
        if q[question] == question:
            return q["answer"]
    

def chat_bot():
    knowledgebase:dict = load_knowledge('knowledgebase.json')

    while True:
        user_input: str = input('you: ')
        if user_input.lower()=='quit':
            break
        best_match:  str | None = find_best_match(user_input,[q["question"] for q in knowledgebase["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledgebase)
            print(f'Bot:{answer}')
        else:
            print('Bot: I don\'t know the answer ,Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip:')

            if new_answer.lower()!= 'skip':
                knowledgebase["questions"].append({"question":user_input, "answer":new_answer})
                save_knowledge('knowledgebase.json',knowledgebase)
                print('Bot :Thank you ! i learned a new response')

if __name__=='__main__':
    chat_bot()