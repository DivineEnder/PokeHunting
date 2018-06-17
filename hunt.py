# @Author: DivineEnder
# @Date:   2018-06-17 00:58:11
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2018-06-17 04:00:54

import webbrowser as wb
import pokebase as pokedb

class Move():
	def __init__(self, name, max_pp = None, cur_pp = None):
		self.name = name
		self.db_move = pokedb.move(name)
		self.max_pp = self.db_move.pp if max_pp is None else max_pp
		self.cur_pp = self.max_pp if cur_pp is None else cur_pp

	def is_useable(self):
		return self.cur_pp == 0

	def decPP(self, amount = 1):
		if self.cur_pp - amount > 0:
			self.cur_pp = self.cur_pp - amount
		else:
			print("Cannot decrease PP of %s by %d because move currently has %d/%d pp" % (self.name, amount, self.cur_pp, self.max_pp))

	def incPP(self, amount = 1):
		if self.cur_pp + amount <= self.max_pp:
			self.cur_pp = self.cur_pp + amount
		else:
			print("Cannot increase PP of %s by %d because move currently has %d/%d pp" % (self.name, amount, self.cur_pp, self.max_pp))

	def display(self):
		print("_" * 30)
		print("| {:<18} {:<2}/{:<2}   |".format(
				self.name,
				self.cur_pp,
				self.max_pp
			)
		)
		print("\\" + ("_" * 28) + "/")

class Pokemon():
	def __init__(self, name):
		self.name = name
		self.moves = []
		self.db_pokemon = pokedb.pokemon(name)

	def addMove(self, name):
		if len(self.moves) >= 4:
			print("Error when trying to add %s. %s already knows %d moves" % (name, self.name, len(self.moves)))
			return False
			# raise EnvironmentError("When trying to add move, too many moves. Pokemon has %d moves already" % len(self.moves))
		elif name in map(lambda move: move.name, self.moves):
			print("Error when trying to add %s. %s already knows %s" % (name, self.name, name))
			return False
		# if not name in map(lambda move: move["name"], self.db_pokemon.moves):
		# 	raise EnvironmentError("Could not find that move in pokemon's moveset. You sure that is the right move?")
		else:
			self.moves.append(Move(name))
			print("Added %s to %s's moveset" % (name, self.name))
			return True

	def deleteMove(self, name):
		self.moves = [move for move in self.moves if not move.name == name]

	def indexOfMove(self, name):
		for i in range(0, len(self.moves)):
			if self.moves[i].name == name:
				return i

		return None

	def useMoveByIndex(self, index, times = 1):
		if not index is None:
			self.moves[index].decPP(times)
			return True

		return False

	def useMove(self, name, times = 1):
		mv_index = self.indexOfMove(name)
		if mv_index is None:
			self.addMove(name)


		return self.useMoveByIndex(-1, times)

	def unuseMoveByIndex(self, index, times = 1):
		if not index is None:
			self.moves[index].incPP(times)
			return True

		return False

	def unuseMove(self, move, times = 1):
		return self.unuseMoveByIndex(self.indexOfMove(move), times)

	def useNextMove(self, times = 1):
		for move in self.moves:
			if move.is_useable:
				move.decPP(times)
				return True

		return False

	def display(self, counter):
		print("\n----{:-<20}|{:03d}|-".format(self.name.upper(), counter))
		for move in self.moves:
			move.display()
		print()

pokemon = Pokemon(input("Enter name of pokemon you are catching: "))
# wb.open(pokemon.db_pokemon.sprites.front_shiny)

exitConditions = ["done", "exit", "q"]
inputMove = ""
counter = 0
while True:
	pokemon.display(counter)
	inputMove = input("Enter move used this turn and a plus if a pokemon appeared (ex. 'leer+'): ")
	if inputMove in exitConditions:
		break

	if inputMove == "":
		counter = counter + 1
		pokemon.useNextMove()
	elif inputMove.startswith("+"):
		counter = counter + 1
		inputMove.replace("+", "")
	elif inputMove.startswith("-"):
		counter = counter - 1
		inputMove.replace("-", "")

	if inputMove:
		try:
			if inputMove[-1] == "--":
				inputMove = inputMove.replace("--", "")
				pokemon.deleteMove(inputMove)
			elif inputMove[-1] == "+":
				inputMove = inputMove.replace("+", "")

				try:
					pokemon.unuseMoveByIndex(int(inputMove) - 1)
				except ValueError as ve:
					pokemon.unuseMove(inputMove)
			else:
				if inputMove.startswith("-"):
					inputMove = inputMove.replace("-", "")

				try:
					pokemon.useMoveByIndex(int(inputMove) - 1)
				except ValueError as ve:
					pokemon.useMove(inputMove)
		except Exception as e:
			print("Something went wrong.")
			print(e)
