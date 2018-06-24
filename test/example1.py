#!/usr/bin/env python3
import sys
import termapp


class MyTerminal(termapp.TermApp):
	
	def __init__(self):
		super().__init__(create_header=True, create_footer=False)
		self.prompt.autocompletionAddWords(['hello', 'howareyou?'])


	def onCommand(self, command_text):
		self.currentPageAppendText(command_text, "normal_color")
		return True


	def onKeyPress(self, key):
		if key == "f2":
			self.switchToNextPage()
		if key == "f3":
			self.switchToPrevPage()
		if key == "f4":
			self.chapters.createNewPage()
		if key == "f9":
			self.prompt.startFlashing(self.loop)
		if key == "f8":
			self.prompt.stopFlashing()
		if key == "f5":
			self.header.setText("Hello!")
		if key == "f6":
			self.footer.setText("Goodbye!")
		return True


my_term = MyTerminal()
if my_term.start():
	my_term.run()
sys.exit(0)

