#!/usr/bin/python
# ASCII solitare
# Copyright (c) 2014-2015 by Matthew Bustad <mybustad@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#

import sys
import curses
import random
import time

def main():
  copyright = """
  
   ASCII solitare, Copyright (C) 2016 Matthew Bustad <mybustad@gmail.com>
  
   This software may be used and distributed according to the terms of the
   GNU General Public License version 2 or any later version.
  
  """
  print "%s" % copyright
  print " Press ? for help."
  print ""
  time.sleep(1)
  
  d = 0	# debug flag
  
  if d : file = open('.sollog', 'w')
  
  Suites = ["c","s","D","H"] # club, spade, Diamond, Hearts
  Rank = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
  # Ace, two,...,nine, ten, jack, queen, king
  
  stdscr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(1)
  
  # Start of class definitions
  
  class Sol(object):
    """Master class"""
    def __init__(self):
      self.hand = []		# empty hand
      self.owner = ''		# where did this card come from
    def show(self):
      """Display all cards"""
      if self.hand :		# hand not empty
         for I in range( len(self.hand),0, -1 ):
           stdscr.addstr( 4 + I, 9, `self.hand[I - 1]`)
      else:
        stdscr.addstr( 5, 9,"[]")
    def space(self): pass   # placeholder functions for subclasses
    def right(self): pass 
    def left(self): pass 
    def movedown(self): pass 
    def cleari(self): pass		# clear index for tab stacks
    def moveup(self): pass
    def getx(self): return 0
    def gety(self): return 0
  
  class Card(object):
    """Card object"""
    def __init__(self, suite, rank):
      self.suite = suite
      self.rank = rank
      self.hide = True
  
    def flip(self):
      """turn card face up"""
      self.hide = 0
    def isnext(self,c):
      """is card the same suite and next card down"""
      if self.suite == c.suite and self.rank + 1 == c.rank :
        return True
      else:
        return False
    def isup(self):
      """is the card face up?"""
      return not self.hide
    def isace(self):
      """are this an Ace card"""
      if self.rank == 0 :
        return True
      else:
        return False
    def isking(self):
      """is this a King card"""
      if self.rank == 12 :
        return True	# King!
      else:
        return False	# Minion!
    def stackdown(self,c):
      """test if card can be above in stacks"""
      if self.isalt(c) and ( self.rank == c.rank + 1 ):
        return True
      else:
        return False
    def isalt(self,c):
      """true if ALTernate color"""
      if self.suite < 2 and c.suite > 1 :
        return True
      elif self.suite > 1 and c.suite < 2 :
        return True
      else :
        return False
    def back(self):
      """Hide face of card"""
      self.hide = True
    def __repr__(self):
      """How am I printed"""
      if self.hide:
        result = "##"  # hidden
      else:
        result = Rank[self.rank] + Suites[self.suite] 
      return result
  
  class Aces(Sol):
    """Four foundation Stacks on right side"""
    def __init__(self,id):	# constructor
      self.cards = []		# empty show area
      self.id = id		# 0..3
    def show(self):
      """print stacks"""
      stdscr.addstr( 1, 44 + self.id * 4, "__") # header
      for I in range(13):
        if len(self.cards) > I :
          stdscr.addstr( 2 + I, 44 + self.id * 4, `self.cards[I]`)
    def gety(self):
      """horizonal location"""
      return 44 + self.id * 4
    def getx(self):
      """verical position"""
      return 2 + len(self.cards)
    def right(self):
      """move curser right"""
      if sol.hand and  0 <= self.id < 3 :
          setcur(ace[self.id + 1])
      else :
        setcur(stock)  # now in stock area
    def left(self):
      """move curser left"""
      if sol.hand and  0 < self.id <= 3 :
        setcur(ace[self.id - 1])
      else :
        setcur(s[6])
    def space(self):
      """put or pull card"""
      if sol.hand :
        if self.cards :
          if self.cards[-1].isnext(sol.hand[0]) :
            self.cards.append(sol.hand.pop())
            sol.hand = []
        elif sol.hand[0].isace():
          self.cards.append(sol.hand[0])
          sol.hand = []
        
  class Tab(Sol):
    """Thirteen Tableau Stacks"""
    def __init__(self,id):
      self.cards = []		# empty show area
      self.id = id		# column 1..7
      self.index = 1		# where we are in the stack
    def dealdown(self,c):
      """deal card faced down"""
      self.cards.append(c)
    def space(self):
      """put or pull card"""
      if sol.hand :		# card in hand
        if sol.owner == self :	# my card in hand
          sol.hand.reverse()
          while sol.hand:
            self.cards.append(sol.hand.pop())
          sol.hand = []
        else:			# some others card
          if self.cards :		# I still have cards
            if self.cards[-1].stackdown(sol.hand[0]):	# cards in alt suite
              sol.hand.reverse()
              while sol.hand :
                self.cards.append(sol.hand.pop())
              sol.hand = []
          else :			# only take a king
            if sol.hand[0].isking():
              sol.hand.reverse()
              while sol.hand :
                self.cards.append(sol.hand.pop())
              sol.hand = []
      else:
        if self.cards :
          if self.cards[-1].isup() :	# bottom cards is not hidden
            for I in range(len(self.cards) - self.index + 2):
              sol.hand.append(self.cards.pop() )
            sol.owner = self
            sol.hand.reverse()
          else :
            self.cards[-1].flip()
    def dealup(self,c):
      """deal card faced up"""
      c.flip()
      self.cards.append(c)
    def left(self):
      if  0 < self.id <= 6 :
        setcur(s[self.id - 1])
      else :
        if len(sol.hand) > 1 :
          setcur(s[6])
        elif waste.up or (sol.hand and waste == sol.owner) :
          setcur(waste)
        else :
          setcur(stock)  # now in stock area
    def right(self):
      if  0 <= self.id < 6 :
        setcur(s[self.id + 1])
      elif len(sol.hand) == 1 :		# only one card in hand
        setcur(ace[0])
      elif len(sol.hand) > 1 :
        setcur(s[0])
      else :
        setcur(stock)  # now in stock area
    def show(self):
      stdscr.addstr( 1, 14 + self.id * 4, "__")
      for I in range(26):
        if len(self.cards) > I :
          stdscr.addstr( 2 + I, 14 + self.id * 4, `self.cards[I]`)
    def gety(self):
      return 14 + self.id * 4
    def movedown(self):
      if self.index < 1 + len(self.cards) :
        self.index = self.index + 1
    def moveup(self):
      if self.index > 2 and not sol.hand :		# Not at the top
        if self.cards[self.index - 3].isup():
          self.index = self.index - 1
    def getx(self):
      return self.index
    def cleari(self):
      if sol.hand :		# Card in hand
        self.index = 2 + len(self.cards)
      else :
        if self.cards :
          self.index = 1 + len(self.cards)
        else:
          self.index = 2
  
  class Waste(Sol): # showing cards
    """Three card deal"""
    def __init__(self):		# constructor
      self.up = []		# empty show area
      self.up0 = ''		# 2nd up card
      self.up1 = ''		# 3rd up card
    def right(self):
      setcur(s[0])
    def space(self):		# space bar hit
      if sol.hand :		# take back card?
        if sol.owner == self :	# my card in hand
          self.putt(sol.hand[0])
          sol.hand = []
      else :
        if self.up1 :
          sol.hand.append(self.up1)
          self.up1 = ''
          sol.owner = self
        elif self.up0:
          sol.hand.append(self.up0)
          self.up0 = ''
          sol.owner = self
        elif self.up:
          sol.hand.append( self.up.pop() )
          sol.owner = self
    def gety(self):
      global cur 
      if self.up :		# cards are here
        return 5
      elif sol.hand :		# no cards here and  cards in hand
        return 5
      else :			# no cards here and no cards in hand
        setcur(s[0])		# move to right object when it exists
        return cur.gety()
    def getx(self):
      global cur 
      if sol.hand :		# Card in hand
        if self.up1 :		# Should never happen
          return 4
        elif self.up0 :
          return 4
        elif self.up :
          return 3
        else :			# no cards here
          return 2
      else :			# no card in hand
        if self.up1 :		# Should never happen
          return 4
        elif self.up0 :
          return 3
        elif self.up :
          return 2
        else :			# no cards here
          setcur(s[0])		# move to Right object when it exists
          return cur.getx()
    def left(self):
      setcur(stock)  # now in stock area
    def show(self):
      if self.up :
        stdscr.addstr( 2, 5, `self.up[-1]`)
      else:
        stdscr.addstr( 2, 5,"[]")
      if self.up0 :
        stdscr.addstr( 3, 5, `self.up0`)
      else:
        stdscr.addstr( 3, 5,"[]")
      if self.up1 :
        stdscr.addstr( 4, 5, `self.up1`)
      else:
        stdscr.addstr( 4, 5,"[]")
    def putt(self, c):		# Move into stack
      if self.up1 :		# 10S
        self.up.append(self.up0)
        self.up0 = self.up1
        self.up1 = c
        self.up1.flip()		# show card face
      else:			# _??
        if self.up0 :		# _0S
          self.up1 = c
          self.up1.flip()		# show card face
        else:			# __?
          if self.up :		# __S
            self.up0 = c
            self.up0.flip()		# show card face
          else :			# ___ All empty
            self.up.append(c)
            c.flip()		# show card face
    def pull(self):		# return all of the cards
      results = []		# to hold deck
      if self.up1 :		# push lower card
        results.append(self.up1)
        self.up1 = ''
      if self.up0 :		# push upper card
        results.append(self.up0)
        self.up0 = ''
      self.up.reverse()
      results = results + self.up
      self.up = []		# clear self.up deck
      for x in results :		# put cards on their back
        x.back()
      return(results)
    def debug(self):
      if self.up1 :
        stdscr.move(17, 1)
        stdscr.addstr("%s"% Rank[self.up1.rank] )
        stdscr.move(18, 1)
        stdscr.addstr("%s"% Suites[self.up1.suite] )
        stdscr.move(19, 1)
        stdscr.addstr("%s"% self.up1.hide )
      if self.up0 :
        stdscr.move(17, 2)
        stdscr.addstr("%s"% Rank[self.up0.rank] )
        stdscr.move(18, 2)
        stdscr.addstr("%s"% Suites[self.up0.suite] )
        stdscr.move(19, 2)
        stdscr.addstr("%s"% self.up0.hide )
      for J in range(len(self.up)):
        I = len(self.up) - 1 - J
        stdscr.move(17, 4 + I)
        stdscr.addstr("%s"% Rank[self.up[J].rank] )
        stdscr.move(18, 4 + I)
        stdscr.addstr("%s"% Suites[self.up[J].suite] )
        stdscr.move(19, 4 + I)
        stdscr.addstr("%s"% self.up[J].hide )
  
  
  class Stock(Sol): # pull desk of cards
    def __init__(self):		# constructor
      self.data = []		# empty deck
    def put(self, card):
      self.data.append(card)
    def getx(self):
      return 2
    def gety(self):
      return 1
    def left(self):
      if sol.hand :
        setcur(ace[3])
      else :
        setcur(s[6])
    def right(self):
      setcur(waste)
    def show(self):
      if self.data : # cards in Stock
        stdscr.addstr( 2, 1, `self.data[-1]`)
      else:
        stdscr.addstr( 2, 1,"[]")
    def space(self):		# space bar hit
      if sol.hand :		# no-opp if card is in hand
        pass
      else :
        # pull three cards, if they exist and push onto waste
        if self.data :
          waste.putt(self.data.pop() )
          if self.data :
            waste.putt(self.data.pop() )
            if self.data :
              waste.putt(self.data.pop() )
        else:		# empty stack
          # pull back from waste
          self.data = waste.pull()
    def debug(self):
      for I in range(len(self.data)):
        stdscr.move(21, 1 + I)
        stdscr.addstr("%s"% Rank[self.data[I].rank] )
        stdscr.move(22, 1 + I)
        stdscr.addstr("%s"% Suites[self.data[I].suite] )
        stdscr.move(23, 1 + I)
        stdscr.addstr("%s"% self.data[I].hide )
  
  # End of class definitions
  
  def dbug():
    file.write('-----\nsol=')
    for i in range(len(stock.data)):
      file.write(Rank[stock.data[i].rank])
      file.write(Suites[stock.data[i].suite])
      file.write(' ')
    file.write('\nwaste=')
    for i in range(len(waste.up)):
      file.write(Rank[waste.up[i].rank])
      file.write(Suites[waste.up[i].suite])
      file.write(' ')
    file.write('-')
    if waste.up0 :
      file.write(Rank[waste.up0.rank])
      file.write(Suites[waste.up0.suite])
      file.write(' ')
    if waste.up1 :
      file.write(Rank[waste.up1.rank])
      file.write(Suites[waste.up1.suite])
    file.write('\n')
    for j in range(7):
      file.write('s[%s]' % j)
      for i in range(len(s[j].cards)):
        file.write(Rank[s[j].cards[i].rank])
        file.write(Suites[s[j].cards[i].suite])
        file.write(' ')
      file.write('\n')
    for j in range(4):
      file.write('a[%s]' % j)
      for i in range(len(ace[j].cards)):
        file.write(Rank[ace[j].cards[i].rank])
        file.write(Suites[ace[j].cards[i].suite])
        file.write(' ')
      file.write('\n')
    file.flush()
  
  def setcur(c):
    global cur
    cur.cleari()			# clear where we are leaving
    cur = c
    cur.cleari()			# clear new location
  
  def management():		# boss button
    stdscr.clear()
    stdscr.move(1, 0)
    stdscr.addstr("( 1158 /root )")
    stdscr.move(2, 0)
    stdscr.addstr("#")
    stdscr.move(2, 2)
    c = stdscr.getch()
  
  def help():		# show help 
    stdscr.clear()
    stdscr.move(1, 0)
    stdscr.addstr("Key - Function")
    stdscr.move(2, 0)
    stdscr.addstr(" l  - move right")
    stdscr.move(3, 0)
    stdscr.addstr(" h  - move left")
    stdscr.move(4, 0)
    stdscr.addstr(" j  - move down")
    stdscr.move(5, 0)
    stdscr.addstr(" j  - move up")
    stdscr.move(6, 0)
    stdscr.addstr(" p  - pick or place")
    stdscr.move(7, 0)
    stdscr.addstr(" n  - new game")
    stdscr.move(8, 0)
    stdscr.addstr(" m  - boss button")
    stdscr.move(9, 0)
    stdscr.addstr(" q  - quit")
    stdscr.move(11, 1)
    stdscr.addstr(" press a key to go back")
    c = stdscr.getch()
  
  def win():		# Win page
    """win test"""
    if stock.data:
      if d : file.write('failed stock\n')
      return False        # No win yet
    if d : file.write('passwd stock\n')
    if waste.up :
      if d : file.write('failed waste\n')
      return False	# No win yet
    for J in range(7):
      if s[J].cards :
        if not s[J].cards[0].isup():
          if d : file.write('failed s[%s]\n' % J)
          return False	# No win yet
      if d : file.write('passed empty s[%s]\n' % J)
  
    stdscr.move(20, 4)
    stdscr.addstr("You Won! Press 'n' for a new game or 'q' to quit")
    c = stdscr.getch()
    if c == ord('n'):
      setup()
      return True		# new game
    else:
      stdscr.clear()
      stdscr.refresh()
      if d : file.close()
      curses.nocbreak(); stdscr.keypad(0); curses.echo()
      curses.endwin()
      sys.exit()
  
  
  def setup():
    global stock, waste, sol, ace, s, cur
    stock = Stock()
    waste = Waste()
    sol = Sol()
    ace = []
    for I in range(4):
     ace.append(Aces(I) )
    s = []
    for I in range(7):
     s.append(Tab(I) )
    
    for I in range(4):
      for J in range(13):
        stock.put( Card(I,J) )
    
    random.seed()
    random.shuffle(stock.data)
     
    for I in range(7):			# deal down cards to Tableau
      for J in range(I):
        s[I].dealdown( stock.data.pop() )
    
    for I in range(7):			# deal faced up cards to Tableau
      s[I].dealup( stock.data.pop() )
    
    stdscr.refresh()
    cur = stock  # now in stock area
  
  setup()
  
  while True:
    if d : dbug()
    stdscr.clear()
    for I in range(4):
      ace[I].show()
    stock.show()
    if d : stock.debug()
    waste.show()
    if d : waste.debug()
    sol.show()
    for I in range(7):
      s[I].show()
    stdscr.move(20, 44)
    stdscr.addstr("   ")
    stdscr.move(cur.getx(), cur.gety() )
    stdscr.refresh()
  
    if win() :
      setup()
    else:
      c = stdscr.getch()
      if c == ord('p'): cur.space()
      elif c == ord('q'): break # Exit the while()
      elif c == curses.KEY_RIGHT: cur.right()
      elif c == ord('l'): cur.right()
      elif c == curses.KEY_LEFT: cur.left()
      elif c == ord('h'): cur.left()
      elif c == ord('k'): cur.moveup()
      elif c == curses.KEY_UP: cur.moveup()
      elif c == ord('j'): cur.movedown()
      elif c == curses.KEY_DOWN: cur.movedown()
      elif c == ord('n'): setup()
      elif c == ord(' '): management()
      elif c == ord('m'): management()
      elif c == ord('?'): help()
  
  stdscr.clear()
  stdscr.refresh()
  
  if d : file.close()
  curses.nocbreak(); stdscr.keypad(0); curses.echo()
  curses.endwin()
  
   
if __name__ == '__main__':
  main()
