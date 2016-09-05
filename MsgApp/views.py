from flask import render_template, request, session, redirect, url_for, flash

from MsgApp import app, db, datetime, LOG_FILE
from MsgApp.models import UserData


def get_or_create_user(session, model, **kwargs):
    """ If a row with the given kwargs already exists in the db, return the
        instance. Otherwise creates a new row and returns it's instance.
        NOTE: Only checks 'name' and 'phone' in our case.
    """
    instance = session.query(model).filter_by(name=kwargs['name'],
                                              phone=kwargs['phone']).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html',
                               name=session.get('name', ''),
                               phone=session.get('phone', '')
                               )

    params = {}
    params['name'] = request.form['name']
    params['phone'] = request.form['phone']
    params['start_time'] = datetime.datetime.utcnow()  # USE UTC time!
    params['tz_offset'] = request.form['tz_offset']
    print(params['tz_offset'])
    session.update(params)
    try:
        instance, is_new = get_or_create_user(db.session, UserData, **params)
    except:
        flash("Name and phone number don't match. Try again.")
        return render_template('index.html',
                               name=session.get('name', ''),
                               phone=session.get('phone', '')
                               )

    if is_new:
        print('You need to start the scheduler here!')

    return redirect(url_for('info',
                            name=session.get('name')
                            )
                    )


@app.route("/user/info/<name>", methods=['GET', 'POST'])
def info(name):
    if request.method == 'GET':
        instance = db.session.query(UserData).filter_by(name=name).first()
        if not instance:
            flash("The given name does not exist! Please sign up again.")
            return render_template('info.html')

        start = instance.start_time
        lstart = instance.get_local_start_time()
        return render_template('info.html',
                               name=name,
                               phone=instance.phone,
                               start=lstart.strftime("%Y-%m-%d, %H:%M:%S"),
                               td=(datetime.datetime.utcnow() - start)
                               )

    elif request.method == 'POST':
        if request.form['submit'] == 'Delete Reminder':
            instance = db.session.query(UserData).filter_by(name=name).first()
            UserData.query.filter_by(name=name).delete()
            db.session.commit()
            print('Remove the tasks scheluded for this one!')
            return redirect(url_for('index'))

        elif request.form['submit'] == 'View Logs':
            return redirect(url_for('logs', name=name))


@app.route("/user/logs/<name>", methods=['GET'])
def logs(name):
    logs = []
    try:
        with open(LOG_FILE.format(name), 'r') as logfile:
            logs = logfile.readlines()
    except IOError:
        flash('Error: No log file exists for this user!')
    return render_template('logs.html',
                           name=name,
                           logs=logs)
