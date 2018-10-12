from .exceptions import *
import random


class GuessAttempt(object):
    
    def __init__(self, letter, hit=None, miss=None):
        if hit is miss:
            raise InvalidGuessAttempt()
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit is not None:
            return self.hit
        else:
            return False
        
    
    def is_miss(self):
        if self.miss is not None:
            return self.miss
        else:
            return False


class GuessWord(object):
    
    def __init__(self, word=None):
        if not word:
            raise InvalidWordException()
        self.masked = '*' * len(word)
        self.answer = word
        
    def perform_attempt(self, letter):
        if len(letter) != 1:
            raise InvalidGuessedLetterException()
            
        if letter.lower() in self.answer.lower():
            result = ''
            for ind, char in enumerate(self.answer):
                if char.lower() == letter.lower():
                    result += char.lower()
                else:
                    result += self.masked[ind]
            self.masked = result
            return GuessAttempt(letter, hit=True)
        else:
            return GuessAttempt(letter, miss=True)
        
            
            


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls, words):
        if len(words) < 1:
            raise InvalidListOfWordsException()
        return random.choice(words)
    
    def __init__(self, list_of_words=None, number_of_guesses=5):
        if list_of_words is None:
            self.list_of_words = HangmanGame.WORD_LIST
        else:
            self.list_of_words = list_of_words
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(HangmanGame.select_random_word(self.list_of_words))
        self.game_won = None
        self.finished = False
        
    def is_finished(self):
        return self.finished
    
    def is_won(self):
        return  self.finished and self.game_won
        
    def is_lost(self):
        return self.finished and not self.game_won
    
    def guess(self, letter):
        if self.finished:
            raise GameFinishedException()
        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
            self.previous_guesses.append(letter.lower())
        if attempt.is_hit():
            self.previous_guesses.append(letter.lower())
            
        if "*" not in self.word.masked and self.remaining_misses > 0:
            #if guesses remaining but letters are all unmasked, won
            self.finished = True
            self.game_won = True
            raise GameWonException()
        elif '*' in self.word.masked and self.remaining_misses == 0:
            #if out of guesses and * is still present in the masked word, lost
            self.finished = True
            self.game_won = False
            raise GameLostException()

        return attempt
    
    
