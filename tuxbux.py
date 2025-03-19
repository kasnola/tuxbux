from time import monotonic

from textual import log, events
from textual.app import App, ComposeResult
from textual.content import Content
from textual.message import Message
from textual.containers import Middle, HorizontalGroup, VerticalGroup, VerticalScroll, Center, Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Button, Rule, Digits, Footer, Header, Static, Label

class Shop(VerticalScroll):
	"""The shop."""

	def compose(self) -> ComposeResult:
		"""Create child purchasables."""
		yield Purchasable(name="Low-end VPS", classes="purchasable", id="tuxminer")
		# 1x vCPU, 768MB RAM
		yield Purchasable(name="Mid-range VPS", classes="purchasable", id="tuxminer2")
		# 4x vCPU, 4096MB RAM
		yield Purchasable(name="High-end VPS", classes="purchasable")
		# 8x vCPU, 8192MB RAM, 1x vGPU
		yield Purchasable(name="Dedicated Server Box", classes="purchasable")
		yield Purchasable(name="Herd of Linux Boxen", classes="purchasable")
		# you paid a graybeard some serious cash to inherit one of his herds
		yield Purchasable(name="Cloud Compute Cluster", classes="purchasable")
		# let's make this like 100x pricier than CCC
		yield Purchasable(name="Quantum Computer", classes="purchasable")

class Purchasable(HorizontalGroup):
	"""A purchasable widget."""

	description = reactive("Sample description")

	def on_mount(self) -> None:
		self.border_title = self.name

	def on_button_pressed(self, event: Button.Pressed) -> None:
		"""Event handler called when a button is pressed."""
		button_id = event.button.id
		self.log("button pressed @ " + str(button_id))

	def compose(self) -> ComposeResult:
		"""Create child widgets of a purchasable."""
		yield Label(self.description, classes="label")
		yield Button("Buy", classes="button buy", id=self.id)

class TuxLogo(Static):
	class Clicked(Message):
		def __init__(self, int: int) -> None:
			self.int = int
			super().__init__()
	
	def on_click(self) -> None:
		self.post_message(self.Clicked(1))

class TuxbuxCounter(Digits):
	counter = reactive(0)

	def watch_tuxbux_counter(self, counter_value: int):
		self.value = "$" + str(counter_value)

class TuxbuxIdleGameApp(App):

	# Heavily inspired by Cookie Clicker
	tuxbuxEarned : int
	tuxbuxAmount = reactive(0)
	tuxbuxDisplay : int
	tuxbuxPerSecond : int # recalculate w/ every new purchase
	tuxbuxPerSecondRaw : int 
	tuxbuxClicks : int

	CSS_PATH = "tuxbux.tcss"
	TITLE = "Tuxbux"
	SUB_TITLE = "An idle game in your terminal"
	WELCOME = """
╻ ╻┏━╸╻  ┏━╸┏━┓┏┳┓┏━╸     ╻ ╻┏━┓┏━╸┏━┓
┃╻┃┣╸ ┃  ┃  ┃ ┃┃┃┃┣╸      ┃ ┃┗━┓┣╸ ┣┳┛
┗┻┛┗━╸┗━╸┗━╸┗━┛╹ ╹┗━╸ ┛   ┗━┛┗━┛┗━╸╹┗╸
"""
	SHOPHEADER = """
█▀        ▄▄▄▄  ▄    ▄  ▄▄▄▄  ▄▄▄▄▄        ▀█
█        █▀   ▀ █    █ ▄▀  ▀▄ █   ▀█        █
█        ▀█▄▄▄  █▄▄▄▄█ █    █ █▄▄▄█▀        █
█   ▀▀▀      ▀█ █    █ █    █ █       ▀▀▀   █
█        ▀▄▄▄█▀ █    █  █▄▄█  █             █
▀▀                                         ▀▀
"""
	# credits to Mik & ascii-art.de; http://www.ascii-art.de/ascii/jkl/linux.txt
	TUX_ASCII = """
                 .88888888:.
                88888888.88888.
              .8888888888888888.
              888888888888888888
              88' _`88'_  `88888
              88 88 88 88  88888
              88_88_::_88_:88888
              88:::,::,:::::8888
              88`:::::::::'`8888
             .88  `::::'    8:88.
            8888            `8:888.
          .8888'             `888888.
         .8888:..  .::.  ...:'8888888:.
        .8888.'     :'     `'::`88:88888
       .8888        '         `.888:8888.
      888:8         .           888:88888
    .888:88        .:           888:88888:
    8888888.       ::           88:888888
    `.::.888.      ::          .88888888
   .::::::.888.    ::         :::`8888'.:.
  ::::::::::.888   '         .::::::::::::
  ::::::::::::.8    '      .:8::::::::::::.
 .::::::::::::::.        .:888:::::::::::::
 :::::::::::::::88:.__..:88888:::::::::::'
  `'.:::::::::::88888888888.88:::::::::'
        `':::_:' -- '' -'-' `':_::::'`
                  Click me!        
"""
	BINDINGS = [
		("d", "toggle_dark", "Toggle dark mode"),
		("a", "add_purchasable", "Add a purchasable"),
		("r", "remove_purchasable", "Remove a purchasable"),
	]

	def compose(self) -> ComposeResult:
		"""Create child widgets for the app."""
		yield Header()
		yield Footer()
		with VerticalGroup(classes="box counterpane"):
			yield Label(self.WELCOME, classes="welcome label") # TODO this should be a randomly generated name I think, like Hacker Dwarf's Machine
			yield Rule(line_style="thick", classes="welcome rule")
			yield TuxbuxCounter("$999,999", classes="counter digits", id="tuxbux_counter") # turn into millions when you get there
			yield Rule(line_style="dashed", classes="counter rule")
			with Container(classes="welcome", id="icons"):
				yield TuxLogo(self.TUX_ASCII, id="tux_icon")
		yield Static("Hax0r Display", classes="box display")
		with VerticalGroup(classes="box shop"):
			yield Label(self.SHOPHEADER, id="label")
			yield Rule(line_style="thick", id="rule")
			yield Shop(id="shop")

	purchasable_index = 2

	def action_add_purchasable(self) -> None:
		purchasable_name = "Product " + str(self.purchasable_index).zfill(2)
		new_purchasable = Purchasable(name=purchasable_name,classes="purchasable")
		self.query_one("#shop").mount(new_purchasable)
		new_purchasable.scroll_visible()
		self.purchasable_index += 1

	def action_remove_purchasable(self) -> None:
		purchasables = self.query("Purchasable")
		if purchasables:
			purchasables.last().remove()
			self.purchasable_index = max(0, self.purchasable_index - 1)

	def on_mount(self):
		def update_counter(counter_value : int):
			counter_value_fmt = "$" + str(counter_value)
			self.query_one(TuxbuxCounter).update(value=counter_value_fmt)
		self.watch(self, "tuxbuxAmount", update_counter)

	def on_tux_logo_clicked(self, message: TuxLogo.Clicked) -> None:
		self.tuxbuxAmount += 1
		self.log(message)

if __name__ == "__main__":
	app = TuxbuxIdleGameApp()
	app.run()
