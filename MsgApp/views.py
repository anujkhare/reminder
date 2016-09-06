from flask import render_template, request, session, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from MsgApp import app, db, datetime
from MsgApp.models import UserData, UserLogs


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
    session.update(params)

    try:
        instance, is_new = get_or_create_user(db.session, UserData, **params)
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        flash("Name and phone number don't match. Try again.")
        return render_template('index.html',
                               name=session.get('name', ''),
                               phone=session.get('phone', '')
                               )

    return redirect(url_for('info'))


@app.route("/user/info", methods=['GET', 'POST'])
def info():
    name = session.get('name', None)
    if not name:
        flash('Unable to read session. Enable cookies and sign in again!')
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

    # If user clicked on "Delete" or "View Logs"
    elif request.method == 'POST':
        if request.form['submit'] == 'Delete Reminder':
            instance = db.session.query(UserData).filter_by(name=name).first()
            UserData.query.filter_by(name=name).delete()
            db.session.commit()
            print('Remove the tasks scheluded for this one!')
            return redirect(url_for('index'))

        elif request.form['submit'] == 'View Logs':
            return redirect(url_for('logs'))


@app.route("/user/logs", methods=['GET'])
def logs():
    name = session.get('name', None)
    if not name:
        flash('Unable to read session. Enable cookies and sign in again!')
    logs = []
    logs = db.session.query(UserLogs).filter_by(name=name)
    if not logs.first():
        flash('No logs exist for this user!')
    # try:
    #     with open(LOG_FILE.format(name), 'r') as logfile:
    #         logs = logfile.readlines()
    # except IOError:
    return render_template('logs.html',
                           name=name,
                           logs=logs)
