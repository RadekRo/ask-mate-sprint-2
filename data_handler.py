from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime 

import database
import csv, os

# DATA_FILE_PATH_ANSWER = 'data/answer.csv'
# DATA_FILE_PATH_QUESTION = 'data/question.csv'
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


@database.connection_handler
def get_all_questions(cursor):
    query = """
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY id
       """
    cursor.execute(query)
    return cursor.fetchall()

       
@database.connection_handler
def get_question(cursor, id):
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE id = {id}
       """
    cursor.execute(query)
    return cursor.fetchone()
        

@database.connection_handler
def get_answer(cursor, id):
    query = f"""
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id = {id}
       """
    cursor.execute(query)
    return cursor.fetchall()
        

@database.connection_handler
def get_answers(cursor, question_id):
    query = f"""
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id = {question_id}  
       """
    cursor.execute(query)
    return cursor.fetchall()


@database.connection_handler
def add_question(cursor, your_question:dict):
    current_date = str(datetime.now())[0:19]
    query = f"""
        INSERT INTO question (submission_time, title, message) 
        VALUES ('{current_date}', '{your_question["title"]}','{your_question["message"]}')
    """
    cursor.execute(query)

    
# def save_data(filename, questions, separator = ","):
#    with open(filename, "w") as file:
#         for record in questions:
#             row = separator.join(record)
#             file.write(row + "\n")


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
    
# def add_answer(answer):
#     answers = import_data_file(DATA_FILE_PATH_ANSWER)
#     answers.append(answer)
#     save_data(DATA_FILE_PATH_ANSWER, answers)

@database.connection_handler
def add_answer(cursor, your_answer:dict):
    current_date = str(datetime.now())[0:19]
    query = f"""
        INSERT INTO answer (submission_time, question_id, message) 
        VALUES ('{current_date}', '{your_answer["id"]}', '{your_answer["message"]}')
    """
    cursor.execute(query)


database.connection_handler
def add_vote_question(cursor, id:int):
    query = f"""
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = {id}
    """
    cursor.execute(query)


database.connection_handler
def add_vote_question(cursor, id:int):
    query = f"""
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = {id}
    """
    cursor.execute(query)


@database.connection_handler
def add_vote_answer(cursor, id:int):
    query = f"""
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = {id}
    """
    cursor.execute(query)


@database.connection_handler
def substract_vote_answer(cursor, id:int):
    query = f"""
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = {id}
    """
    cursor.execute(query)

# def remove_question(id):
#     questions = import_data_file(DATA_FILE_PATH_QUESTION)
#     answers = import_data_file(DATA_FILE_PATH_ANSWER)
#     questions_filtered = list()
#     answers_filtered = list()
#     for question in questions:
#         if question[0] == str(id):
#             file_path = "static/images/questions/" + str(id) + ".jpg" 
#             os.path.exists(file_path) and os.remove(file_path)
#             continue
#         else:
#             questions_filtered.append(question)
#     for answer in answers:
#         if answer[3] == str(id):
#             file_path = "static/images/answers/" + str(answer[0]) + ".jpg" 
#             os.path.exists(file_path) and os.remove(file_path)
#             continue
#         else:
#             answers_filtered.append(answer)
#     save_data(DATA_FILE_PATH_QUESTION, questions_filtered)
#     save_data(DATA_FILE_PATH_ANSWER, answers_filtered)

@database.connection_handler
def remove_question(cursor, id:int):
    file_path = "static/images/questions/" + str(id) + ".jpg" 
    os.path.exists(file_path) and os.remove(file_path)
    query = f"""
        DELETE FROM question
        WHERE id = {id}
    """
    cursor.execute(query)
    #TODO remove answer connected with question

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


@database.connection_handler
def count_view(cursor, id:int):
    query = f"""
        UPDATE question 
        SET view_number = view_number + 1
        WHERE id = {id}
    """
    cursor.execute(query)


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