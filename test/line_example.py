#!/usr/bin/env python3
import sys
import time
import random
import termapp


class TerminalLineExample(termapp.TermApp):
	
	def __init__(self):
		super().__init__(create_header=True, create_footer=True)
		self.quitOnESC = True


	def onStart(self):
		# Register some example word completions
		self.prompt.autocompletionAddWords(['hello', 'howareyou?'])
		# Register some basic commands
		command_list = []
		command_list.append(termapp.CommandDescription(
			name         = "print",
			callback     = self.delayedCommand,
			on_waiting   = self.delayedCommandWaiting,
			deferred     = True
		))
		command_list.append(termapp.CommandDescription(
			name         = "echo",
			alias        = "e",
			callback     = self.echo,
			params_join  = True
		))
		command_list.append(termapp.CommandDescription(
			name         = "opt",
			alias        = "o",
			callback     = self.opt,
			params_have_options = True
		))
		self.commandDispatcher.registerCommandList(command_list)


	def echo(self, command):
		# This is an example of how 
		self.print("echo:  " + command.params)
		return True


	def opt(self, command):
		self.print("command opt: params:%s  options:%s" % (str(command.nparams), str(command.noptions)))
		self.print("  params:  %s" % (" ".join(command.params)))
		self.print("  options: %s" % (" ".join(command.options)))
		return True


	def delayedCommandWaiting(self, command):
		# This waiting callback will be called from the main thread
		# before executing a long command.
		# This is helpful, so we can add a "waiting" line to the
		# screen, and having that line report error or success
		# when a long command finally asynchronously complete.
		line_compl = termapp.LineCompletion(self.loop, "Downloading archives ...", flash_waiting=True)
		self.currentPageAppendLine(line_compl)
		command.callbackSuccess = lambda command: line_compl.setSuccess()
		command.callbackError   = lambda command: line_compl.setError()
		return True


	def delayedCommand(self, command):
		# This is a long command that will take some seconds
		# to execute. While this is busy, display is still
		# responsive, because this command will be executed
		# with the "deferred" flag set, so it will be executed
		# by a secondary thread, and not the main thread.
		# When the command is executed, we can set a success
		# status [default], or an error status. 
		time.sleep(random.randint(2,5))
		command.success = random.randint(0,1)
		return True


	def onStart(self):
		self.print("Press F5, F6, F7, F8, F9, to create example of different kinds of lines.")
		self.print("Press F12 to reset all header notifiers")
		#self.prompt.startFlashing()
		return True


	def onExit(self):
		self.print("Goodbye!")
		self.flush()
		time.sleep(1)
		return True


	def onKeyPress(self, key):
		if key == "f5":
			self.header.createNotifier("Hello!   " + str(random.randint(1,9000)), seconds=3)
		if key == "f6":
			self.header.createNotifier("ERROR!   " + str(random.randint(1,9000)), style="fatal_color")
		if key == "f7":
			line_progress = termapp.LineProgress(self.loop, "f572d396fae9206628714fb2ce00f72e94f2258f", max_value=10000, initial_value=3344, display_value=True, progress_width=12, value_width=8)
			self.currentPageAppendLine(line_progress)
			self.loop.startTimer(user_data=line_progress, callback=lambda timer_entry: timer_entry.userData.setValue(8896), seconds=4, repeats=1)
		if key == "f8":
			line_compl = termapp.LineCompletion(self.loop, "Downloading emails ...", flash_waiting=True)
			self.currentPageAppendLine(line_compl)
			self.loop.startTimer(user_data=line_compl, callback=lambda timer_entry: timer_entry.userData.setError(), seconds=2, repeats=1)
		if key == "f9":
			line_compl = termapp.LineCompletion(self.loop, "Downloading images ...", flash_waiting=True)
			self.currentPageAppendLine(line_compl)
			self.loop.startTimer(user_data=line_compl, callback=lambda timer_entry: timer_entry.userData.setSuccess(), seconds=4, repeats=1)
		if key == "f12":
			self.header.resetNotifiers()
		return True


my_term = TerminalLineExample()
if my_term.start():
	my_term.run()
sys.exit(0)

