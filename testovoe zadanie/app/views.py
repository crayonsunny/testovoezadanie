# -*- coding: utf-8 -*-

import os
import shutil
from flask import Flask, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, models
from forms import LoginForm, RegistrationForm, RenewalForm, DeleteForm, IndexForm
from models import User, ROLE_USER, ROLE_ADMIN
from config import MONGODB_SETTINGS, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from mongoengine import connect
from werkzeug.utils import secure_filename



@lm.user_loader
def load_user(login):
    us = models.User.objects.filter(login=login)  #spisok userov
    if not us:
        return None
    for u in us:
        return u

def allowed_file(filename):
        if filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
            return True

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    user = g.user         
    form = IndexForm()
    log = user.login
    path = os.path.join('E:\\fss\\', log)
    dirflist = os.listdir(path)
    logvbd = models.User.objects.filter(login=log)
    for s in logvbd:
        s.dirsp = []
        s.flsp = []
        for dirf in dirflist:
            p = os.path.join('E:\\fss\\', log, dirf)
            if os.path.isdir(p):
                s.dirsp.append(dirf)
            else:
                s.flsp.append(dirf)
        s.save()
    if request.method == "POST":
         if 'file' not in request.files:
             flash('No file part')
             return redirect(url_for("index"))
         file = request.files['file']
         if file.filename == '':
             flash('No selected file')
             return redirect(url_for("index"))
         if file and allowed_file(file.filename):
             filename = secure_filename(file.filename)
             name = file.filename
             file.save(os.path.join(UPLOAD_FOLDER, log, name))
             size = os.stat(os.path.join(UPLOAD_FOLDER, log, name)).st_size
             logvbd = models.User.objects.filter(login=log)
             for s in logvbd:
                 kk = models.Fl(flnm = name, flsz = size, flpth = os.path.join(UPLOAD_FOLDER, log, name))
                 s.fls = kk
                 s.save()    
             flash('File has been successfully uploaded')
             return redirect(url_for("index"))
    return render_template("index.html",
        user = user)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
      return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
               
        session['remember_me'] = form.remember_me.data
        log = form.login.data       #zapiseuvaem vvedeneui login v lo
        pd = form.pswd.data         #zapiseuvaem vvedeneui login v lo
        def uidb(l, p):             #user in db
            connect ('pick')        #vozvrat true esli log+pd est' v bd i false v inom sluchae         
            logvbd = models.User.objects.filter(login=l)  #spisok iz 1 el
            if logvbd:              #proveryat' vvod na pustotu ne nado t.k. v formah est' validatory
                for s in logvbd:    #s budet document (zapisiyu) s nuzhneum loginom
                    pdvbd = s.pswd  #veutaskivaem parol etogo logina iz bd
                if pdvbd == p:      #parol na etot login sovpadaet s tem chto vvel user
                    return s
        user = uidb(log, pd)
        remember_me = False
        if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
        if user:                    #v bd est' user s takimi loginom i parolem - avtorizuem i delaem redirect
            login_user(user, remember = remember_me)
            return redirect(request.args.get('next') or url_for("index"))
        else: flash('Sorry, we do not have user with such login-password combination :(')
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/registration', methods = ['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
       flash('Login = "' + form.login.data + '", email = "' +
           form.email.data + '", password = "' +
           form.newpswd.data + '", confirmed password = "' +
           form.confirm.data + '", accept_tos=' + str(form.accept_tos.data))
       log = form.login.data
       eml = form.email.data
       pd = form.newpswd.data
       connect('pick')
       provlog = models.User.objects.filter(login=log)
       provemail = models.User.objects.filter(email=eml)
       if not provlog and not provemail:
           v = models.User(login=log, pswd=pd, email=eml)
           v.save()
           user = v
           remember_me = False
           if 'remember_me' in session:
                    remember_me = session['remember_me']
                    session.pop('remember_me', None)
           login_user(user, remember = remember_me)
           path = os.path.join('E:\\fss\\',log)
           os.mkdir(path)
           return redirect(request.args.get('next') or url_for("index"))
       if provemail and not provlog: flash('Sorry, this email address is already in use')
       if provlog and not provemail: flash('Sorry, this login is already in use')
       if provemail and provlog: flash('Sorry, such login and email address are already in use')
    return render_template('reg.html',
        title = 'Registration',
        form = form)

@app.route('/renew', methods = ['GET', 'POST'])
@login_required
def renew():
    form = RenewalForm()
    if form.validate_on_submit():
        flash('New Login = "' + form.renewlogin.data + '", new email = "' +
              form.renewemail.data + '", new password = "' +
              form.renewpswd.data + '", new confirmed password = "' +
              form.renewconfirm.data + '". Renewal succeed!')
        oldlog = form.oldlogin.data
        rnwlog = form.renewlogin.data
        rnweml = form.renewemail.data
        rnwpd = form.renewpswd.data
        connect('pick')
        spisok = models.User.objects.filter(login=oldlog)       #spisok iz 1 el
        for s in spisok:                                        #s budet document (zapisiyu) s nuzhneum loginom
          if rnwlog:
              s.login = rnwlog
              path = os.path.join('E:\\fss\\',oldlog)
              npath = os.path.join('E:\\fss\\',rnwlog)
              os.rename(path, npath)
          if rnwpd:
              s.pswd = rnwpd
          if rnweml:
              s.email = rnweml
          s.save()
          user = s
        remember_me = False
        if 'remember_me' in session:
           remember_me = session['remember_me']
           session.pop('remember_me', None)
        login_user(user, remember = remember_me) 
        return redirect('/index')
        
    return render_template('renewal.html', 
        title = 'Personal data renewal',
        form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/deleteacc', methods = ['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        log = form.login.data                                   #zapiseuvaem vvedeneui login v lo
        pd = form.pswd.data                                     #zapiseuvaem vvedeneui login v lo
        def uidb(l, p):                                         #user in db - vozvrat true esli log+pd est' v bd i false v inom sluchae
            connect ('pick')
            logvbd = models.User.objects.filter(login=l)        #spisok iz 1 el
            if logvbd and g.user.login==l:
                for s in logvbd:                                #s budet document (zapisiyu) s nuzhneum loginom
                    pdvbd = s.pswd                              #veutaskivaem parol etogo logina iz bd
                if pdvbd == p:                                  #parol na etot login sovpadaet s tem chto vvel user
                    s.delete()
                    return True
        usdel = uidb(log, pd)
        if usdel:
            logout_user()
            path = os.path.join('E:\\fss\\',log)
            shutil.rmtree(path)                                 #udalyaem papku i vse vlozhennoe
            redirect(url_for("index"))
            flash('Your account has been successfully deleted!')
        else: flash('Sorry, we do not have user with such login-password combination :(')
    return render_template('deleteacc.html', 
        title = 'Delete account',
        form = form)






