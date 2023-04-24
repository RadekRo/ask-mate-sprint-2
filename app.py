from flask import Flask
from flask import render_template, request, redirect
from datetime import datetime 

import data_handler
import util

app = Flask(__name__)


@app.route('/')
def index():
    latest_questions = data_handler.get_latest_questions(5)
    return render_template('index.html', latest_questions = latest_questions)

@app.route('/list')
def route_list():
    order_by = request.args.get('order_by') 
    order_direction = request.args.get('order_direction')
    questions = data_handler.get_all_questions(order_by, order_direction)
    return render_template("list.html", questions = questions, order_by = order_by, order_direction = order_direction)


@app.route('/question/<id>')
def route_question(id):
    question = data_handler.get_question(id)
    answers = data_handler.get_answers(id)
    comments_question = data_handler.get_comments_question(id)
    tags = data_handler.get_question_tags(id)
    data_handler.count_view(id)
    return render_template("question.html", question = question, answers = answers, comments_question = comments_question, tags = tags)


@app.route('/answer/<answer_id>/answer_add_vote', methods=["POST", "GET"])
def route_answer_add_vote(answer_id):
    data_handler.add_vote_answer(answer_id)
    id = request.form.get("id")
    redirect_dir = "/question/" + str(id) 
    return redirect(redirect_dir)
    

@app.route('/answer/<answer_id>/answer_substract_vote', methods=["POST", "GET"])
def route_answer_substract_vote(answer_id):
    data_handler.substract_vote_answer(answer_id)
    id = request.form.get("id")
    redirect_dir = "/question/" + str(id) 
    return redirect(redirect_dir)
    

@app.route('/ask-question', methods=["POST","GET"])
def ask_question():
    
    if request.method == 'GET':
        return render_template('ask-question.html')
    
    file_name = request.files['file']
    image = data_handler.save_question_image(file_name)
    your_question = dict(request.form)
    current_date = util.get_current_date()
    data_handler.add_question(current_date, your_question, image)
    return redirect('/list')


@app.route('/question/<id>/new-answer')
def route_answer(id):
    return render_template("new-answer.html", id=id)


@app.route('/question/<id>/new-comment')
def route_comment(id):
    return render_template("new-comment.html", id=id)


@app.route('/question/<id>/<answer_id>/new-comment_answer')
def route_comment_answer(id, answer_id):
    comments_answer = data_handler.get_comments_answer(answer_id)
    return render_template("new-comment_answer.html", id=id, answer_id=answer_id, comments_answer = comments_answer)


@app.route('/new-answer', methods=["POST", "GET"])
def new_answer():

    if request.method == 'GET':
        return render_template("new-answer.html")

    file_name = request.files['file']
    image = data_handler.save_answer_image(file_name)
    your_answer = dict(request.form)
    current_date = util.get_current_date()
    data_handler.add_answer(current_date, your_answer, image)
    redirect_dir = "/question/" + your_answer['question_id']
    return redirect(redirect_dir)

@app.route('/question/<id>/vote_add', methods=["POST", "GET"])
def route_vote_add(id):
    data_handler.add_vote_question(id)
    redirect_dir = "/?order_by=" + request.form.get('order_by') + "&order_direction=" + request.form.get('order_direction')
    return redirect(redirect_dir)

@app.route('/question/<id>/vote_substract', methods=["POST", "GET"])
def route_vote_substract(id):
    data_handler.substract_vote_question(id)
    redirect_dir = "/?order_by=" + request.form.get('order_by') + "&order_direction=" + request.form.get('order_direction')
    return redirect(redirect_dir)

@app.route('/question/<id>/delete')
def delete_question(id):
    file_path = data_handler.get_question_image_path(id)
    data_handler.remove_question(id, file_path['image'])
    return redirect("/")

@app.route('/answer/<id>/delete')
def delete_answer(id):
    question_id = data_handler.remove_answer(id)
    redirect_dir = "/question/" + question_id
    return redirect(redirect_dir)

@app.route('/question/<id>/edit')
def edit_question(id):
    question = data_handler.get_question(id)
    return render_template("edit-question.html", id = id, question = question)

@app.route('/question/update', methods=["GET", "POST"])
def update_question():

    if request.method == 'POST':
        question_id = request.form.get('id')    
        current_date = util.get_current_date()
    
        if 'file' not in request.files:
            image = ""
        else:
            file = request.files['file']
            image = data_handler.save_file(file, question_id, "question")
        updated_date = current_date
        updated_title = request.form.get('title')
        updated_message = request.form.get('message')
        updated_image = image

    data_handler.update_question(question_id, updated_date, updated_title, updated_message, updated_image)

    redirect_dir = "/question/" + str(question_id)
    return redirect(redirect_dir)

@app.route('/question/<id>/new-comment', methods=["POST", "GET"])
def add_comment_question(id):

    if request.method == 'GET':
        return render_template('new-comment.html')
    question_comment = request.form.get('message')
    data_handler.add_comment_question(question_comment, id)
    redirect_dir = "/question/" + id
    return redirect(redirect_dir)

@app.route('/question/<id>/<answer_id>/new-comment_answer', methods=["POST", "GET"])
def add_comment_answer(id, answer_id):

    if request.method == 'GET':
        return render_template('new-comment_answer.html')
    answer_comment = request.form.get('message')
    data_handler.add_comment_answer(answer_comment, id, answer_id)
    redirect_dir = "/question/" + id
    return redirect(redirect_dir)

@app.route('/search', methods=['GET'])
def search_questions():
    search_argument = request.args.get('q')
    filtered_questions = data_handler.search_for_questions(search_argument)
    search_result_number = len(filtered_questions)
    return render_template("search.html", filtered_questions = filtered_questions, search_result_number = search_result_number)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == "POST":
        
        question_id = request.form.get('question_id')
        new_tag = request.form.get('new_tag')
        
        if new_tag != "":
            data_handler.add_new_tag(new_tag.lower()) 
            tag = new_tag
        else:
            tag = request.form.get('tag')
        
        tag_id = data_handler.get_tag_id(tag)['id']
        data_handler.add_tag_to_question(question_id, tag_id)
        return redirect("/question/" + str(question_id))
    
    existing_tags = data_handler.get_tags_list()
    return render_template("add-tag.html", question_id = question_id, existing_tags = existing_tags)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(tag_id, question_id):
    data_handler.delete_tag(tag_id, question_id)
    return redirect('/question/' + question_id)

if __name__ == '__main__':
    app.run()

# for run the app
# use> python app.py
