#from typing import List, Dict

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
    order_direction = 'DESC' if order_direction != 'ASC' else order_direction
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message
        FROM question
        ORDER BY {order_by} {order_direction}
       """
    cursor.execute(query)
    return cursor.fetchall()

@database.connection_handler
def get_latest_questions(cursor, number_of_questions:int):
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY submission_time DESC LIMIT {number_of_questions} OFFSET 0 
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
def get_comments_question(cursor, question_id):
    query = f"""
        SELECT id, question_id, message, submission_time, edited_number
        FROM comment
        WHERE question_id = {question_id}
        ORDER by id DESC
       """
    cursor.execute(query)
    return cursor.fetchall()

@database.connection_handler
def get_comments_answer(cursor):
    query = f"""
    SELECT comment.answer_id, comment.id, comment.message, comment.submission_time
    FROM comment
    INNER JOIN answer ON answer.id = comment.answer_id;
       """
    cursor.execute(query)
    return cursor.fetchall()

@database.connection_handler
def get_comment(cursor, comment_id):
    query = f"""
    SELECT id, question_id, message, submission_time, edited_number
        FROM comment
        WHERE question_id = {comment_id}    
    """
    cursor.execute(query)
    return cursor.fetchone()


@database.connection_handler
def add_question(cursor, current_date:str, your_question:dict, image:str):
    try:
        query = f"""
            INSERT INTO question (submission_time, title, message, image) 
            VALUES ('{current_date}', '{your_question["title"]}','{your_question["message"]}', '{image}')
        """
        cursor.execute(query)
    except:
        raise ValueError("Wrong values types provided for database input.")


def save_question_image(file):
    if file.filename != "":
        file_name = util.get_unique_file_name()
        file_name_with_extension =  file_name + ".jpg"
        file.save(os.path.join(UPLOAD_FOLDER_FOR_QUESTIONS, file_name_with_extension))
        return UPLOAD_FOLDER_FOR_QUESTIONS + file_name_with_extension
    else:
        return "no-image"

def save_answer_image(file):
    if file.filename != "":
        file_name = util.get_unique_file_name()
        file_name_with_extension =  file_name + ".jpg"
        file.save(os.path.join(UPLOAD_FOLDER_FOR_ANSWERS, file_name_with_extension))
        return UPLOAD_FOLDER_FOR_ANSWERS + file_name_with_extension
    else:
        return "no-image"

@database.connection_handler
def add_answer(cursor, current_date:str, your_answer:dict, image:str):
    try:
        query = f"""
            INSERT INTO answer (submission_time, question_id, message, image) 
            VALUES ('{current_date}', '{your_answer["question_id"]}', '{your_answer["message"]}', '{image}')
        """
        cursor.execute(query)
    except:
        raise ValueError("Wrong values types provided for database input.")


@database.connection_handler
def add_comment_question(cursor, question_comment, id:int):
    current_date = str(datetime.now())[0:19]
    query = f"""
        INSERT INTO comment (question_id, message, submission_time) 
        VALUES ({id}, '{question_comment}', '{current_date}')
    """
    cursor.execute(query)


@database.connection_handler
def add_comment_answer(cursor, question_comment, answer_id:int):
    current_date = str(datetime.now())[0:19]
    query = f"""
        INSERT INTO comment (answer_id, message, submission_time) 
        VALUES ({answer_id}, '{question_comment}', '{current_date}')
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
def get_question_image_path(cursor, id:int):
    query = f"""
        SELECT image FROM question
        WHERE id = {id}
    """
    cursor.execute(query)
    return cursor.fetchone()

@database.connection_handler
def remove_question(cursor, id:int, file_path:str):
    os.path.exists(file_path) and os.remove(file_path)
    query = f"""
        DELETE FROM question
        WHERE id = {id}
    """
    cursor.execute(query)
    #TODO remove answer connected with question

def remove_comment(cursor, comment_id):
    query = f"""
    DELETE FROM comment
    WHERE ID = {comment_id}
    """
    cursor.execute(query)

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

@database.connection_handler
def search_for_questions(cursor, search_argument):
    query = f"""
        SELECT * FROM question 
        WHERE id IN (SELECT DISTINCT question_id
                        FROM answer 
                        WHERE message LIKE '%{search_argument}%')
        OR title LIKE '%{search_argument}%' 
        OR message LIKE '%{search_argument}%'
    """
    cursor.execute(query)
    return cursor.fetchall()


@database.connection_handler
def get_tags_list(cursor):
    query = "SELECT * FROM tag"
    cursor.execute(query)
    return cursor.fetchall()


@database.connection_handler
def get_question_tags(cursor, question_id):
    query = f"""
        SELECT * FROM tag 
        WHERE id IN (SELECT tag_id FROM question_tag WHERE question_id = {question_id})"""
    cursor.execute(query)
    return cursor.fetchall()


@database.connection_handler
def add_new_tag(cursor, new_tag):
    query = f"INSERT INTO tag (name) VALUES ('{new_tag}')"
    cursor.execute(query)
 

@database.connection_handler
def get_tag_id(cursor, tag):
    query = f"SELECT id FROM tag WHERE name = '{tag}'"
    cursor.execute(query)
    return cursor.fetchone()


@database.connection_handler
def add_tag_to_question(cursor, question_id, tag_id):
    query = f"INSERT INTO question_tag (question_id, tag_id) VALUES ({question_id}, {tag_id})"
    cursor.execute(query)

@database.connection_handler
def delete_tag(cursor, tag_id, question_id):
    query = f"DELETE from question_tag WHERE question_id = {question_id} AND tag_id = {tag_id}"
    cursor.execute(query)