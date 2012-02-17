# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime


def index():
    response.menu = [['Home',False,URL('index')],
                     ['Submit',True,URL('submit')],
                     ["Pupp3t's",False,URL('show')]]
    images = db().select(db.image.ALL, orderby=~db.image.pub_date)
    return dict(images=images)

def puppets():
    response.menu = [['Home',False,URL('index')],
                     ['Submit',True,URL('submit')],
                     ["Pupp3t's",False,URL('show')]]
    images = db().select(db.image.ALL, orderby=~db.image.pub_date)
    return dict(images=images)

def submit():
    response.menu = [['Home',False,URL('index')],
                     ['Submit',True,URL('submit')],
                     ["Pupp3t's",False,URL('show')]]
    form = SQLFORM(db.image, submit_button='Submit Puppet', _id = "submission",formstyle="divs")
    if request.cookies.has_key('posLat') and request.cookies.has_key('posLon') and request.cookies.has_key('posAccuracy'):
        latitude = request.cookies['posLat'].value
        longitude = request.cookies['posLon'].value
        accuracy = request.cookies['posAccuracy'].value    
    else:
        latitude = 0
        longitude = 0
        accuracy = 0
    form.vars.latitude = latitude
    form.vars.longitude = longitude
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form, latitude=latitude, longitude=longitude, accuracy=accuracy)
   
def show():
    response.menu = [['Home',False,URL('index')],
                     ['Submit',True,URL('submit')],
                     ["Pupp3t's",False,URL('show')]]
    image = db(db.image.id==request.args(0)).select().first()
    form = SQLFORM(db.comment)
    form.vars.image_id = image.id
    if form.accepts(request.vars, session):
        response.flash = 'your comment is posted'
    comments = db(db.comment.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

'''
@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id[
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
'''
