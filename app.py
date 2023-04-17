from flask import Flask
from flask import render_template, request, redirect
import data_handler
from datetime import datetime 


app = Flask(__name__)


# @app.route('/')
# @app.route('/list')
# def route_list():
#     all_questions = data_handler.get_all_questions()
#     return render_template("list.html", all_questions = all_questions)

@app.route('/')
@app.route('/list')
def route_list():
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    order_by = "date" if order_by == None else order_by
    order_direction = "desc" if order_direction == None else order_direction
    all_questions = data_handler.get_all_questions()
    sorted_questions = data_handler.sort_questions(all_questions, order_by, order_direction)
    return render_template("list.html", questions = sorted_questions, sort_options = [order_by, order_direction])


@app.route('/question/<id>')
def route_question(id):
    question = data_handler.get_question(id)
    answers = data_handler.get_answers(id)
    data_handler.count_view(id)
    return render_template("question.html", question = question, answers = answers)

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
    next_id = data_handler.get_next_id("question")
    current_date = str(datetime.now())[0:19]
    
    if 'file' not in request.files:
        image = ""
    else:
        file = request.files['file']
        image = data_handler.save_file(file, next_id, "question")

    if request.method == 'POST':
        your_question = [next_id, current_date, "0", "0", request.form.get('title'), request.form.get('message'), image ]
        data_handler.add_question(your_question)
        redirect_dir = "/question/" + str(next_id) 
        return redirect(redirect_dir)
    return render_template("ask-question.html")


@app.route('/question/<id>/new-answer')
def route_answer(id):
    return render_template("new-answer.html", id=id)


@app.route('/new-answer', methods=["POST", "GET"])
def new_answer():
    next_id = data_handler.get_next_id("answer")
    current_date = str(datetime.now())[0:19]

    if 'file' not in request.files:
        image = ""
    else:
        file = request.files['file']
        image = data_handler.save_file(file, next_id, "answer")

    if request.method == 'POST':
        your_answer = [next_id, current_date, "0", str(request.form.get('id')), request.form.get('new-answer'), image ]
        redirect_dir = "/question/" + str(request.form.get('id'))
        data_handler.add_answer(your_answer)
        return redirect(redirect_dir)
    return render_template("new-answer.html")

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
    data_handler.remove_question(id)
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
        current_date = str(datetime.now())[0:19]
    
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


if __name__ == '__main__':
    app.run()

# for run the python's flask server
# use> python -m flask run
# for automatic changes and debugger use> "python -m flask --debug run"