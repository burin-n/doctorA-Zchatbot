import nltk
from nltk import word_tokenize
from nltk import pos_tag
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

# What are your name and your surname (Both must be started with capital letter!) ?
# เอาคำแรกที่เป็น NNX หลัง name and surname

def replymessage(user_input_message, nq):
	if nq == 1:
		global english_vocab

		user_input = user_input_message.lower()
		tokenized_user_input_message = word_tokenize(user_input_message)
		tagged_user_input_message = pos_tag(word_tokenize(user_input_message))

		user_name = ''
		user_surname = ''
		isNameNotFound = False
		isSurnameNotFound = False

		reply_message = ''

		if 'name' not in user_input and 'surname' not in user_input and len(tokenized_user_input_message) == 2:
			user_name = tokenized_user_input_message[0]
			user_surname = tokenized_user_input_message[1]
			return 'Your name is ' + user_name + ' and Your surname is ' + user_surname
		
		else:
			if 'name' in user_input or 'Name' in user_input:
				try:
					index_name = tokenized_user_input_message.index('name') + 1
				except ValueError:
					try:
						index_name = tokenized_user_input_message.index('Name') + 1
					except ValueError:
						if len(reply_message) == 0:
							reply_message += ('Sorry, I did not get what your name is')
						else:
							reply_message += (' Sorry, I did not get what your name is')
						isNameNotFound = True				

				if isNameNotFound == False:
					while(True):
						try:
							user_name = tokenized_user_input_message[index_name]
							if 'NN' in tagged_user_input_message[index_name][1]:
								if len(reply_message) == 0:
									reply_message += ('Your name is ' + user_name + '.')
								else:
									reply_message += (' Your name is ' + user_name + '.')
								break
							else:
								index_name += 1

						except IndexError:
							if len(reply_message) == 0:
								reply_message += ('Sorry, I did not get what your name is')
							else:
								reply_message += (' Sorry, I did not get what your name is')
			
			else:
				if len(reply_message) == 0:
					reply_message += ('Sorry, I did not get what your name is')
				else:
					reply_message += (' Sorry, I did not get what your name is')


			if 'surname' in user_input or 'Surname' in user_input:
				try:
					index_surname = tokenized_user_input_message.index('surname') + 1
				except ValueError:
					try:
						index_surname = tokenized_user_input_message.index('Surname') + 1
					except ValueError:
						if len(reply_message) == 0:
							reply_message += ('Sorry, I did not get what your surname is')
						else:
							reply_message += (' Sorry, I did not get what your surname is')
						isSurnameNotFound = True
				
				if isSurnameNotFound == False:
					while (True):
						try:
							user_surname = tokenized_user_input_message[index_surname]
							if 'NN' in tagged_user_input_message[index_surname][1]:
								if len(reply_message) == 0:
									reply_message += ('Your surname is ' + user_surname + '.')
								else:
									reply_message += (' Your surname is ' + user_surname + '.')
								break

							else:
								index_surname += 1

						except IndexError:
							if len(reply_message) == 0:
								reply_message += ('Sorry, I did not get what your surname is')
							else:
								reply_message += (' Sorry, I did not get what your surname is')

			else:	
				if len(reply_message) == 0:
					reply_message += ('Sorry, I did not get what your surname is')
				else:
					reply_message += (' Sorry, I did not get what your surname is')

			return reply_message

# Test
print(replymessage(input('What are your name and your surname (Both must be started with a capital letter!) ? '), 1))