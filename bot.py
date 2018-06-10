from models.users import User
import nltk
from nltk import word_tokenize
from nltk import pos_tag
english_vocab = set(w.lower() for w in nltk.corpus.words.words())
from random import randint
from collections import defaultdict
import datetime

class Bot:
    def __init__(self):
        self.q_name = ["What's your name?"]
        self.q_age = ["How old are you?"]
        self.q_gender = ["What's your gender?", "You're male or female?"]
        self.q_height = ["What's your height?"]
        self.q_weight = ["How much do you weight?"]
        self.q_pressure = ["Can I have your pressure?"]
        self.q_hospital = ["Which hospital do you prefer?"]
        self.q_birthday = ["What's your birthday?"]

        self.p_edit = ['no', 'nope', 'none']
        self.CONFIRM = "information is confirmed"

        self.fields = ['name','gender','height','weight','pressure',
                'birthday','hospital']
        self.dateformat = ['birthday', 'date']

        self.units = defaultdict(lambda : '')
        s = [ ('weight', 'kg.'), ('height', 'm.'), ('pressure', 'mmHg'), 
                ('age', 'years old') ] 
        for k,v in s:
            self.units[k] = v
        


    def isFloat(self,n):
        try:
            float(n)
            return True
        except ValueError:
            return False


    def isInt(self,n):
        try:
            int(n)
            return True
        except ValueError:
            return False


    def findUser(self,userId):
        user = User.objects( line_id = userId )
        if( len(user) == 0 ):
            user = User(line_id = userId).save()
            return user
        return user[0]


    def a_name(self,user_input):
        name = user_input
        return True, name


    def a_age(self,user_input):
        for v in word_tokenize(user_input):
            if( self.isInt(v) ):
                age = int(v)
                return True, age 
        return False, None


    def a_gender(self,user_input):
        to_word = defaultdict( lambda : 'invalid')
        s = [ ('m','male'), ('f', 'female'), ('male','male'), ('female','female')]
        for k,v in s:
            to_word[k] = v

        gender = to_word[user_input]
        if(gender == 'invalid'):
            return False, None
        return True, gender 


    def a_height(self,user_input):
        if self.isFloat(user_input):
            return True, float(user_input) 
        else:
            return False, None 


    def a_weight(self,user_input):
        if self.isFloat(user_input):
            return True, float(user_input)
        else: 
            return False, None


    def a_pressure(self,user_input):
        return True, user_input


    def a_hospital(self,user_input):
        return True, user_input


    def a_birthday(self,user_input):
        d,m,y = user_input.split('/')
        m_map = { 'jan' : 1, 'feb' : 2, 'mar' : 3 , 'apr' : 4, 'may':5,'june':6 ,
                'july':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
        try:
            d = int(d)
            if(not self.isInt(m)):
                m = m_map[m]
            else:
                m = int(m)
            y = int(y)
            return True, datetime.date(y,m,d)
        except Exception as E:
            print(str(E))
            return False, None

    def a_edit(self,user_input):
        if(user_input in self.p_edit):
            return True, self.CONFIRM
        elif(user_input in self.fields):
            return True, None
        else:
            return False, None


    def a_done(self,user_input):
        if(user_input == 'yes'):
            return True, False
        else:
            return False, None


    def validate_answer(self,q,user_input,user):
        success = False
        
        if(q == 'edit') :
            success, result = self.a_edit(user_input)
            if(success):
                if(result == self.CONFIRM):
                    user.is_confirm = True
                    user.save()
                else:
                    user[user_input] = result
                return True
            return False

        if(q == 'name'):
            success, result = self.a_name(user_input)
        elif(q == 'age'):
            success, result = self.a_age(user_input)
        elif(q == 'gender'):
            success, result = self.a_gender(user_input)
        elif(q == 'height'):
            success, result = self.a_height(user_input)
        elif(q == 'weight'):
            success, result = self.a_weight(user_input)
        elif(q == 'pressure'): 
            success, result = self.a_pressure(user_input)
        elif(q == 'birthday'):
            success, result = self.a_birthday(user_input)
        elif(q == 'hospital'):
            success, result = self.a_hospital(user_input)
        elif(q == 'done'):
            success, result = self.a_done(user_input)
            q = 'is_confirm'
     
        if(success):
            user[q] = result
            user.save()
            return True
        return False


    def gen_question(self,key):
        if( key == 'name' ):
            return self.q_name[randint(0,len(self.q_name)-1)]
        elif( key == 'age' ):
            return self.q_age[randint(0,len(self.q_age)-1)] 
        elif( key == 'gender' ):
            return self.q_gender[randint(0,len(self.q_gender)-1)]
        elif( key == 'height'):
            return self.q_height[randint(0,len(self.q_height)-1)] + " (in cm.)"
        elif( key == 'weight' ):
            return self.q_weight[randint(0,len(self.q_weight)-1)] + " (in kg.)"
        elif( key == 'pressure' ):
            return self.q_pressure[randint(0,len(self.q_pressure)-1)]
        elif( key == 'birthday' ):
            return self.q_birthday[randint(0,len(self.q_birthday)-1)]+ " (day/month/year)"
        elif( key == 'hospital'):
            return self.q_hospital[randint(0,len(self.q_hospital)-1)]
        else:
            return None 


    def get_question(self,user):
        for key in self.fields:
            value = user[key]
            if(value == None):
                user.last_response = key
                user.save()
                return self.gen_question(key)
        return None        


    def get_all_information(self,user):
        text = ''
        for key in self.fields:
            if( key in self.dateformat):
                text += "{}: {}\n".format(key, user[key].strftime("%d/%m/%Y"))
            else:
                text += "{}: {} {}\n".format(key, user[key], self.units[key])
        return text


    # this method should be called
    def response(self,userId, message):
        if(not message['type'] == 'text'):
            return '' 

        user = self.findUser(userId)
        last_response = user.last_response
        user_input = message['text'].lower().strip()
        
        try:
            res = self.validate_answer(last_response, user_input, user)
        except Exception as E:
            print (E)

        question = self.get_question(user)
        
        if( question == None ):
            if(user.is_confirm == True):
                # add confirm expire for next conversation here
                user.last_response = 'done'
                user.save()
                return ["Your information is fully received.",
                        "Do you want to change anything?"]

            reply = []
            reply.append("This is your information.")
            reply.append(self.get_all_information(user))
            reply.append("Is there anything you want to edit?")
            user.last_response = 'edit'
            user.save()
            return reply
        else:
            return [question]
