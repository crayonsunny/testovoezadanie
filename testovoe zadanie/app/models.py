from app import db
import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

class Fl(db.EmbeddedDocument):
    flnm = db.StringField(max_length=64)                            #file name
    flsz = db.IntField()                                            #file size
    flpth = db.StringField()                                        #put' k file na mashine servera
    flpthcl = db.StringField()                                      #put' k file v sheme clientskogo interfeisa
    create_at = db.DateTimeField(default=datetime.datetime.now)     #data sozdaniya file-a

class User(db.Document):
    login = db.StringField(max_length=64, unique = True)
    pswd = db.StringField(min_length=6, max_length=64)
    email = db.EmailField(max_length=100, unique = True)
    role = db.IntField(default = ROLE_USER)                             #rol' usera, osobo ne ispolzuetsya, zodano dlya razvitia
    fls = db.EmbeddedDocumentField(Fl)                                  #vstroennie documenty s opisaniem filov
    confirmed_at = db.DateTimeField(default=datetime.datetime.now)      #data registracii usera
    dirsp = db.ListField()                                              #spisok papok usera
    flsp = db.ListField()                                               #spisok fileov usera
    meta = {'collection': 'user'}
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.login)  
        

   
