import csv, os

DATA_FILE_PATH_ANSWER = 'data/answer.csv'
DATA_FILE_PATH_QUESTION = 'data/question.csv'
UPLOAD_FOLDER_FOR_QUESTIONS = 'static/images/questions/'
UPLOAD_FOLDER_FOR_ANSWERS = 'static/images/answers/'
ALLOWED_EXTENSIONS = {'jpg'}


def import_data_file(filename):
    questions = list()
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            questions.append(row)
    return questions


def get_all_questions():
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    # questions.sort(key = lambda inner:inner[1], reverse=True)
    return questions


def get_question(id):
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    for question in questions:
        if question[0] == id:
            return question
        

def get_answer(id):
    answers = import_data_file(DATA_FILE_PATH_ANSWER)
    for answer in answers:
        if answer[0] == id:
            return answer
        
def get_answers(question_id):
    all_answers = import_data_file(DATA_FILE_PATH_ANSWER)
    selected_answers = list()
    for answer in all_answers:
        if answer[3] == question_id:
            selected_answers.append(answer)
    return selected_answers


def get_next_id(selector):
    if selector == "answer":
        data_file = import_data_file(DATA_FILE_PATH_ANSWER )
    elif selector == "question":
        data_file = import_data_file(DATA_FILE_PATH_QUESTION)
    try:
        id = int(data_file[-1][0]) + 1
    except:
        id = 1
    return str(id)


def add_question(question):
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    questions.append(question)
    save_data(DATA_FILE_PATH_QUESTION, questions)
    

def save_data(filename, questions, separator = ","):
   with open(filename, "w") as file:
        for record in questions:
            row = separator.join(record)
            file.write(row + "\n")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, current_id, selector):

    if selector == "question":
        upload_folder = UPLOAD_FOLDER_FOR_QUESTIONS
    elif selector == "answer":
        upload_folder = UPLOAD_FOLDER_FOR_ANSWERS

    if file and allowed_file(file.filename) and file.filename != "":
        saved_name = current_id + ".jpg"
        file.save(os.path.join(upload_folder, saved_name))
        return "/" + upload_folder + current_id + ".jpg"
    else:
        return ""
    
def add_answer(answer):
    answers = import_data_file(DATA_FILE_PATH_ANSWER)
    answers.append(answer)
    save_data(DATA_FILE_PATH_ANSWER, answers)

def add_vote_question(id):
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    for question in questions:
        if question[0] == id:
            votes = question[3]
            votes = int(votes)
            votes += 1
            question[3] = str(votes)
            save_data(DATA_FILE_PATH_QUESTION, questions)

def substract_vote_question(id):
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    for question in questions:
        if question[0] == id:
            votes = question[3]
            votes = int(votes)
            votes -= 1
            question[3] = str(votes)
            save_data(DATA_FILE_PATH_QUESTION, questions)

def add_vote_answer(answer_id):
    answers = import_data_file(DATA_FILE_PATH_ANSWER)
    for answer in answers:
        if answer[0] == answer_id:
            votes_answer = answer[2]
            votes_answer = int(votes_answer)
            votes_answer += 1
            answer[2] = str(votes_answer)
            save_data(DATA_FILE_PATH_ANSWER, answers)
            return answers

def substract_vote_answer(answer_id):
    answers = import_data_file(DATA_FILE_PATH_ANSWER)
    for answer in answers:
        if answer[0] == answer_id:
            votes_answer = answer[2]
            votes_answer = int(votes_answer)
            votes_answer -= 1
            answer[2] = str(votes_answer)
            save_data(DATA_FILE_PATH_ANSWER, answers)
            return answers
        
def remove_question(id):
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    answers = import_data_file(DATA_FILE_PATH_ANSWER)
    questions_filtered = list()
    answers_filtered = list()
    for question in questions:
        if question[0] == str(id):
            file_path = "static/images/questions/" + str(id) + ".jpg" 
            os.path.exists(file_path) and os.remove(file_path)
            continue
        else:
            questions_filtered.append(question)
    for answer in answers:
        if answer[3] == str(id):
            file_path = "static/images/answers/" + str(answer[0]) + ".jpg" 
            os.path.exists(file_path) and os.remove(file_path)
            continue
        else:
            answers_filtered.append(answer)
    save_data(DATA_FILE_PATH_QUESTION, questions_filtered)
    save_data(DATA_FILE_PATH_ANSWER, answers_filtered)

def remove_answer(id):
    answers = import_data_file(DATA_FILE_PATH_ANSWER)
    answers_filtered = list()
    question_id = 0
    for answer in answers:
        if answer[0] == str(id):
            file_path = "static/images/answers/" + str(id) + ".jpg" 
            os.path.exists(file_path) and os.remove(file_path)
            question_id = answer[3]
            continue
        else:
            answers_filtered.append(answer)

    save_data(DATA_FILE_PATH_ANSWER, answers_filtered)
    return question_id

def update_question(question_id, question_date, question_title, question_message, question_image):
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    updated_question = [question_date, question_title, question_message]
    updated_image = question_image
    for question in questions:
        if question[0] == str(question_id):
            question[1], question[4], question[5] = updated_question
            if updated_image != "":
                question[6] = updated_image
    save_data(DATA_FILE_PATH_QUESTION, questions)

def count_view(id):
    questions = import_data_file(DATA_FILE_PATH_QUESTION)
    for question in questions:
        if question[0] == id:
            votes = question[2]
            votes = int(votes)
            votes += 1
            question[2] = str(votes)
            save_data(DATA_FILE_PATH_QUESTION, questions)    

def sort_questions(questions, order_by, order_direction):
    reverse = True if order_direction == "desc" else False
    if order_by == 'title':
        questions.sort(key = lambda inner:inner[4], reverse = reverse)
    elif order_by == 'date':
        questions.sort(key = lambda inner:inner[1], reverse = reverse)
    elif order_by == 'views':
        questions.sort(key = lambda inner:int(inner[2]), reverse = reverse)
    elif order_by == 'votes':
        questions.sort(key = lambda inner:int(inner[3]), reverse = reverse)
    elif order_by == 'message':
        questions.sort(key = lambda inner:inner[5], reverse = reverse)
    else:
        questions = questions     
    return questions    