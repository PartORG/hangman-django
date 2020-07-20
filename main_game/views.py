from django.shortcuts import render, redirect
from .models import Game
from .forms import CreateUserForm
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from random import choice
import string

from django.contrib import messages

from django.views.generic import View
from django.utils.decorators import method_decorator

# Create your views here.
class RegisterPageView(View):
	form_class = CreateUserForm
	template_name = 'main_game/register.html'

	@method_decorator(unauthenticated_user)
	def get(self, request):
		form = self.form_class(None)
		context = {'form':form}
		return render(request, 'main_game/register.html', context)

	@method_decorator(unauthenticated_user)
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			return redirect('login')
		context = {'form':form}
		return render(request, 'main_game/register.html', context)


class LoginPageView(View):
	@method_decorator(unauthenticated_user)
	def get(self, request):
		context = {}
		return render(request, 'main_game/login.html', context)

	@method_decorator(unauthenticated_user)
	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username or Password is incorrect!')

		context = {}
		return render(request, 'main_game/login.html', context)


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('login')


class GameView(View):
	def get_word(self):
		with open('wordlist.txt') as file:
			words = file.read().splitlines()

		rand_word = choice(words)
		return rand_word.upper()

	@method_decorator(login_required(login_url='login'))
	def get(self,request):
		word = self.get_word()
		game = Game()
		game.word = word
		game.word_letters_count = len(set(game.word))
		game.save()
		image = "/static/images/Hangman-0.png"
		word_list = [letter if letter in game.used_letters else '-' for letter in game.word]
		context = {'image':image,'game':game, 'hidden_word':word_list}
		return render(request, 'main_game/game.html', context)

	@method_decorator(login_required(login_url='login'))
	def post(self,request):
		game_id = int(request.POST['game_id'])
		game = Game.objects.get(id=game_id)

		word_letters = set(game.word)  # letters in the word
		alphabet = set(string.ascii_uppercase)

		if game.status == 'ongoing':
			user_letter = request.POST.get('letter')
			if user_letter in alphabet - set(game.used_letters):
				game.used_letters += user_letter
				game.save()
				if user_letter in word_letters:
					# word_letters.remove(user_letter)
					game.word_letters_count -= 1
					game.save()
					messages = 'Correct guess!'
				else:
					game.lives -= 1
					game.save()  # takes away a life if wrong
					messages = 'Your letter, ' + user_letter +  ' is not in the word.'

			elif user_letter in game.used_letters:
				messages = 'You have already used that letter. Guess another letter.'
			else:
				messages = 'That is not a valid letter.'

			if game.lives <= 0:
				game.status = 'lose'
				game.save()
				image = "/static/images/Hangman-6.png"	
			else:
				if game.word_letters_count == 0:
					game.status = 'win'
					game.save()
				image = "/static/images/Hangman-"+str(6-game.lives)+".png"

			word_list = [letter if letter in game.used_letters else '-' for letter in game.word]
			# print(game.used_letters)
			context = {'image':image, 'game':game, 'hidden_word':word_list, 'info_message':messages, 'b_disabled':game.used_letters}
			return render(request, 'main_game/game.html', context)
		else:
			# end game
			if game.lives <= 0:
				image = "/static/images/Hangman-6.png"	
			else:
				image = "/static/images/Hangman-"+str(6-game.lives)+".png"
			messages = 'The game is over. To play a new game press "New Game" on navigation bar.'
			word_list = [letter if letter in game.used_letters else '-' for letter in game.word]
			context = {'image':image, 'game':game, 'hidden_word':word_list, 'endgame_message':messages}

			return render(request, 'main_game/game.html', context)