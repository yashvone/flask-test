from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def api_root():
    file = open("assets/assets.txt", "r")
    assets = file.read().split(' ')[:-1]; file.close()
    file = open("assets/workers.txt", "r")
    workers = file.read().split(' ')[:-1]; file.close()
    file = open("assets/tasks.txt", "r")
    tasks = file.read().split(' ')[:-1]; file.close()
    return render_template('index.html', assets = assets, tasks = tasks, workers = workers)

@app.route('/add-asset',methods=['POST'])
def api_add_asset():
    i = request.form['assetid']
    file = open("assets/assets.txt", "r+")
    check = file.read().split(' ')[:-1]
    if i not in check:
        file.write(i + ' ')
        file.close()
    return render_template('output.html', data = check+[i], detail = 'Asset added!')

@app.route('/add-task',methods=['POST'])
def api_add_task():
    i = request.form['taskid']
    file = open("assets/tasks.txt", "r+")
    check = file.read().split(' ')[:-1]
    if i not in check:
        file.write(i + ' ')
        file.close()
    return render_template('output.html', data = check+[i], detail = 'Task added!')

@app.route('/add-worker',methods=['POST'])
def api_add_worker():
    i = request.form['workerid']
    file = open("assets/workers.txt", "r+")[:-1]
    check = file.read().split(' ')
    if i not in check:
        file.write(i + ' ')
        file.close()
    return render_template('output.html', data = check+[i], detail = 'Worker added!')

@app.route('/assets/all')
def api_list_assets():
    file = open("assets/assets.txt", "r")
    check = file.read().split(' ')[:-1]
    return render_template('output.html', data = check, detail = 'Following is a list of all added assets!')

@app.route('/allocate-task',methods=['POST'])
def api_allocate():
    task = request.form['taskid']
    asset = request.form['assetid']
    worker = request.form['workerid']
    completeby = request.form['taskToBePerformedBy']
    file = open("assets/allocated.json",'r')
    allocated = json.loads(file.read()); file.close()
    allocated[worker] = allocated.get(worker, []) + [[task,asset,completeby]]
    file = open("assets/allocated.json",'w')
    file.write(json.dumps(allocated)); file.close()
    return render_template('output.html', data = allocated[worker], detail = 'Allocated the task!')

@app.route('/get-tasks-for-worker',methods=['POST'])
def api_get_tasks():
    i = request.form['workerid']
    file = open("assets/allocated.json",'r+')
    allocated = json.loads(file.read()); file.close()
    if not i in allocated:
        data = ['no tasks found for this worker!']
    else:
        data = allocated[i]
    return render_template('output.html', data = data, detail = 'Following tasks are assigned to the given worker in format [task, asset, timeToBeCompletedBy]!')
if __name__ == '__main__':
    app.run(debug=False)