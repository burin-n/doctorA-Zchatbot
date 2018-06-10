from models.users import User
import nltk
from nltk import word_tokenize
from nltk import pos_tag
english_vocab = set(w.lower() for w in nltk.corpus.words.words())
from random import randint

CONFIRM = "information is confirmed"


class Bot:
    def __init__(self):
        self.q_name = ["What's your name?"]
        self.q_age = ["How old are you?"]
        self.q_gender = ["What's your gender?", "You're male or female?"]
        self.q_height = ["What's your height?"]
        self.q_weight = ["How much do you weight?"]
        self.q_pressure = ["Can I have your pressure?"]
        self.fields = ['name','age','gender','height','weight','pressure']


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
        user = User.objects( line_id = user_Id )
        if( len(user) == 0 ):
            user = User(line_id = userId).save()
            return user
        return user[0]


    def a_name(self,user_input):
        name = user_input
        return True, name


    def a_age(self,user_input):
        for v in tokenize(user_input):
            if( isInt(v) ):
                age = int(v)
                return True, age 
        return False, None


    def a_gender(self,user_input):
        to_word = { 'm' : 'male', 'f' : 'female' }
        if( len(user_input == 1) ):
            gender = to_word[user_input]
        else:
            gender = user_input
        return True, gender 


    def a_height(self,user_input):
        if isFloat(user_input):
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


    def a_edit(self,user_input):
        if(user_input == 'no'):
            return True, CONFIRM
        elif(user_input in self.fields):
            return True, None
        else:
            return False, None


    def validate_answer(self,q,user_input,user):
        success = False

        if(q == 'edit') :
            success, result = a_edit(user_input)
            if(success):
                if(result == CONFIRM):
                    user.is_confirm = True
                    user.save()
                else:
                    user[user_input] = result
                return True
            return False

        if(q == 'name'):
            success, result = a_name(user_input)
        elif(q == 'age'):
            success, result = a_age(user_input)
        elif(q == 'gender'):
            success, result = a_gender(user_input)
        elif(q == 'height'):
            success, result = a_height(user_input)
        elif(q == 'weight'):
            success, result = a_weight(user_input)
        elif(q == 'pressure'):
            success, result = a_pressure(user_input)
     
        if(success):
            user[q] = result
            user.save()
            return True
        return False


    def gen_question(self,key):
        if( key == 'name' ):
            return self.q_name[randint(0,len(self.q_name)-10)]
        elif( key == 'age' ):
            return self.q_age[randint(0,len(self.q_age)-1)] 
        elif( key == 'gender' ):
            return self.q_gender[randint(0,len(self.q_gender)-1)]
        elif( key == 'height'):
            return self.q_height[randint(0,len(self.q_height)-1)] + "(cm.)"
        elif( key == 'weight' ):
            return self.q_weight[randint(0,len(self.q_weight)-1)] + "(kg.)"
        elif( key == 'pressure' ):
            return self.q_pressure[randint(0,len(self.q_pressure)-1)]
        else:
            return ''


    def get_question(self,user):
        for key in self.fields:
            value = user[key]
            if(value == None):
                user.last_response = key
                return gen_question(key)
        return None        


    def response(self,userId, message):
        if(not message.type == 'text'):
            return '' 

        user = self.findUser(userId)
        last_response = user.last_response
        user_input = message.text.lower().strip()

        res = validate_answer(last_response, user_input, user)

        if(user.is_confirm == True):
            # add confirm expire for next conversation here
            return ["Your information is fully received."]

        question = get_question(user)
        
        if( question == None ):
            reply = []
            reply.append("This is your information.")
            text = ''
            for key in self.fields:
                text += "{}: {}\n".format(key, user[key])
            reply.append(text)
            reply.append("Is there anything you want to edit?")
            user.last_response = 'edit'
            user.save()
            return reply
        else:
            return [question]
