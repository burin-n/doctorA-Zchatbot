from mongoengine import Document, StringField, DateTimeField, BooleanField, DecimalField, FloatField

class User(Document):    
    name = StringField(max_length=50, default=None)
    age = DecimalField(default=None)
    gender = StringField(choices = ['Male', 'Female'])
    height = FloatField(default=None)
    weight = FloatField(default=None)
    pressure = StringField(default=None) 
    hospital = StringField(max_length=50,default=None)
    hn_number = StringField(max_length=50,default=None)
    birthday = DateTimeField(default=None)
    problems = StringField(max_length=500,default=None)
    doctor = StringField(max_length=50,default=None)
    date = DateTimeField(default=None)
    line_id = StringField(max_length=100, require=True)
    last_msg_time = DateTimeField(default=None)
    last_msg = StringField(max_length=300,default=None)
    last_response = DecimalField(default='')
    is_confirm = BooleanField(default=False)
    meta = {
        'indexes' : [ 'line_id' ]
    }
