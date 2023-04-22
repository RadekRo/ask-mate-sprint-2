from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime 

import database
import os
import util

UPLOAD_FOLDER_FOR_QUESTIONS = 'static/images/questions/'
UPLOAD_FOLDER_FOR_ANSWERS = 'static/images/answers/'
QUESTION_SORT_OPTIONS = ['submission_time', 'view_number', 'vote_number', 'title', 'message']


@database.connection_handler
def get_all_questions(cursor, order_by, order_direction):
    order_by = 'submission_time' if order_by not in QUESTION_SORT_OPTIONS else order_by
    order_direction = 'DESC' if order_direction not in QUESTION_SORT_OPTIONS else order_direction
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY {order_by} {order_direction}
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
        ORDER by id DESC
       """
    cursor.execute(query)
    return cursor.fetchall()

@database.connection_handler
def get_comments(cursor, question_id):
    query = f"""
        SELECT id, question_id, answer_id, message, submission_time, edited_number
        FROM comment
        WHERE question_id = {question_id}
        ORDER by id DESC
       """
    cursor.execute(query)
    return cursor.fetchall()


@database.connection_handler
def add_question(cursor, current_date:str, your_question:dict, image:str):
    try:
        query = f"""
            INSERT INTO question (submission_time, title, message, image) 
            VALUES ('{current_date}', '{your_question["title"]}','{your_question["message"]}', '{image}')
        """
        cursor.execute(query)
    except:
        raise ValueError("Wrong values types provided for sql query.")


def save_question_image(file):

    if file.filename != "":
        file_name = util.get_unique_file_name()
        file_name_with_extension =  file_name + ".jpg"
        file.save(os.path.join(UPLOAD_FOLDER_FOR_QUESTIONS, file_name_with_extension))
        return "/" + UPLOAD_FOLDER_FOR_QUESTIONS + file_name_with_extension
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

@database.connection_handler
def add_comment_question(cursor, question_comment, id:int):
    current_date = str(datetime.now())[0:19]
    query = f"""
        INSERT INTO comment (question_id, message, submission_time) 
        VALUES ({id}, '{question_comment}', '{current_date}')
    """
    cursor.execute(query)

@database.connection_handler
def add_comment_answer(cursor, question_comment, id:int, answer_id:int):
    current_date = str(datetime.now())[0:19]
    query = f"""
        INSERT INTO comment (question_id, answer_id, message, submission_time) 
        VALUES ({id}, {answer_id}, '{question_comment}', '{current_date}')
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