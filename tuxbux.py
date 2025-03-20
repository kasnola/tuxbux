import math
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
		yield ShopEntry("Low-tier VPS", color="red", description="You scroll through lowendbox.com and decide to humor yourself. Surely, a gigabyte of ram should do the trick.", price=20, priceMod=1, cps=1, isVisible=True)
		yield ShopEntry("Mid-range VPS", color="orange", description="Hey, this one's got multiple cpu's!", price=250, priceMod=1, cps=8)
		yield ShopEntry("High-end VPS", color="yellow", description="Tux's penguin wings give this VM a few extra TeraFLOPS.", price=1000, priceMod=1, cps=48)
		yield ShopEntry("Dedicated Server Box", color="green", description="Nothing like a bare metal box to call home.", price=2500, priceMod=1, cps=256)
		yield ShopEntry("Herd of Linux Boxen", color="blue", description="After much contemplation, a scrupulous graybeard had found you worthy to inherit his commendable fleet. With a hefty right price, of course.", price=69420, priceMod=1, cps=1234)
		yield ShopEntry("Cloud Compute Cluster", color="indigo", description="Your data centers put Google and Amazon to shame.", price=250000, priceMod=1, cps=42069)
		yield ShopEntry("Hyperhypervisor", color="darkviolet", description="A 25th century chip with simulated reality bubble included. An entire universe finely tuned and programmed to one purpose: to synthesize and output more Tuxbux.", price=1234567, priceMod=1, cps=99999)

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

		

# class ShopEntries:
# 	name="Low-end VPS", classes="purchasable", id="tuxminer"
# 	# 1x vCPU, 768MB RAM
# 	name="Mid-range VPS", classes="purchasable", id="tuxminer2"
# 	# 4x vCPU, 4096MB RAM
# 	name="High-end VPS", classes="purchasable"
# 	# 8x vCPU, 8192MB RAM, 1x vGPU
# 	name="Dedicated Server Box", classes="purchasable"
# 	name="Herd of Linux Boxen", classes="purchasable"
# 	# you paid a graybeard some serious cash to inherit one of his herds
# 	name="Cloud Compute Cluster", classes="purchasable"
# 	# let's make this like 100x pricier than CCC
# 	name="Hyperhypervisor", classes="purchasable"

# shop related stuffs
priceIncrease = 1.35
ShopEntries = {}
ShopEntriesOwned = {}
	
class ShopEntry(Static):
	def __init__(self, title, color="white", description="", price=0, cps=0, priceMod=1, buyFunction=False, isVisible=False):
		global ShopEntries

		self.price = reactive(0)
		self.color = color
		self.priceMod = priceMod
		self.title = title
		self.description = description
		if (buyFunction):
			self.buyFunction = buyFunction
		else:
			self.buyFunction = False
		self.basePrice = price
		self.baseCps = cps

		self.price = self.basePrice
		self.cps = self.baseCps
		self.cost = 0
		self.amount = 0
		self.isVisible = isVisible

		ShopEntries[self.title] = self
		ShopEntriesOwned.update({self.title : 0})
		super().__init__()

	# @property
	def getPrice(self):
		price = self.basePrice * (priceIncrease ** max(0, self.amount) * self.priceMod)
		return math.ceil(price)

	class Bought(Message):
		def __init__(self, cost: int, cps: int, entry: str) -> None:
			self.cost = cost
			self.entry = entry
			self.cps = cps
			super().__init__()

	def buy(self, money):
		price = self.getPrice()
		if (money >= price):
			self.post_message(self.Bought(price, self.cps, self.title))
			self.amount += 1
			price = self.getPrice()
			self.price = price
			if (self.buyFunction): self.buyFunction()
	
	def on_mount(self):
		# def update_label(price : int):
		# 	self.query_one(Button).label = f"Buy (${price})"
		def make_visible():
			if (app.tuxbuxAmount >= self.basePrice):
				self.isVisible = True
				self.styles.visibility = "visible"
		self.styles.border = ("outer", self.color)
		self.classes=F"purchasable"
		self.border_title = self.title
		if (self.isVisible):
			self.styles.visibility = "visible"
		else:
			self.styles.visibility = "hidden"
		
		self.log("basePrice is " + str(self.basePrice))
		self.watch(app, "tuxbuxAmount", make_visible)
		self.query_one(Button).label = f"Buy (${self.price})"



	def compose(self) -> ComposeResult:
		with HorizontalGroup():
			yield Label(self.description, classes="label")
			yield Button("Buy", classes="button buy")

	def on_button_pressed(self, event: Button.Pressed) -> None:
		"""Event handler called when a button is pressed."""
		button_id = event.button.id
		# self.log(self)
		self.log("price is " + str(self.getPrice()))
		# self.log(app.tuxbuxAmount)
		self.buy(app.tuxbuxAmount)
		self.query_one(Button).label = f"Buy (${self.price})"
		# self.log("button pressed @ " + str(button_id))

class TuxbuxIdleGameApp(App):

	start_time = reactive(monotonic)
	current_time = reactive(0.0)

	# see Cookie Clicker
	tuxbuxAmount = reactive(0)
	tuxbuxEarned : int # all tuxbux earned during gameplay
	tuxbuxDisplay : int # tuxbux display
	tuxbuxPerSecond : int = 0 # recalculate w/ every new purchase
	tuxbuxPerSecondRaw : int # this doesn't do anything atm
	tuxbuxClicks : int = 0 # +1 for each click
	

	#main.js:3331 compute cookies earned while game was closed
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
# credits to https://www.asciiart.eu/computers/computers
	COMPUTER_ASCII = """
|-----------------------------------------|
|  _____________________________________  |
| |  CD-ROM   16X                       | |
| |______________________________.______| |
|       .oO                         ^     |
|   O  =====                {O} {#######} |
|--+--+---------------------+---+---------|
|  |  |####"""""""""""""####|   |   __    |
|  |  |#"                 "#|   | .' _`.  |
|  |   'q                 p'    | |=(_)|  |  Removable
|  |    'q_______________p'     | `.__.'  |  Hard Drive
|  |                            |         |
|  |----------------------------|    O    |
|--+------------------------+---+---------|
| ______,----------,______  |    Power    |
||______            ______| |   ,''''',   |  Floppy Disk
|       |__________|        |  d ~~~~~ b  |        Power Switch
|  {#}                ####  |  q ~~~~~ p  |
|---------------------------|   "wwwww"   |
|                           |             |
|                           |             |  Blank 3.5" Bay
|                           |    Reset    |
|                           |   ,''''',   |  Reset Button
|---------------------------+  d~~~~~~~b  |
| +-----+                      q~~~~~~~p  |
| | P   |             ON   O    "wwwww"   |       On Light
| |   C |                          |      |
| +-----+             HDD  O       |      |      Hard Disk Light
|                                  |      |
|  o   o   o   o   o   o   o       |      |   }
|                                  |      |   }
|  o   o   o   o   o   o   o       |      |   }
|                                  |      |   }
|  o   o   o   o   o   o   o       |      |   }
|                                  |      |   }
|  o   o   o   o   o   o   o       |      |   }  CASE PATTERN
|                                  |      |   }
|  o   o   o   o   o   o   o       |      |   }
|                                  |      |   }
|  o   o   o   o   o   o   o       |      |   }
|                                  |      |   }
|  o   o   o   o   o   o   o       |      |   }
|                                  |      |   }
|  o   o   o   o   o   o   o       |      |   }
|                                  |      |
|_________________________________________|
   [CA]                            [CA]       FEET
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
		yield Static(self.COMPUTER_ASCII, classes="box display")
		with VerticalGroup(classes="box shop"):
			yield Label(self.SHOPHEADER, id="label")
			yield Rule(line_style="thick", id="rule")
			yield Shop(id="shop")

	def tuxbux_earn(self, howmuch) -> None:
		self.tuxbuxAmount += howmuch
		self.tuxbuxEarned += howmuch 
	
	def tuxbux_spend(self, howmuch) -> None:
		self.tuxbuxAmount -= howmuch
	
	def tuxbux_calculate_gains(self) -> None:
		self.tuxbuxPerSecond = 0

	# def action_add_purchasable(self) -> None:
	# 	purchasable_name = "Product " + str(self.purchasable_index).zfill(2)
	# 	new_purchasable = Purchasable(name=purchasable_name,classes="purchasable")
	# 	self.query_one("#shop").mount(new_purchasable)
	# 	new_purchasable.scroll_visible()
	# 	self.purchasable_index += 1

	# def action_remove_purchasable(self) -> None:
	# 	purchasables = self.query("Purchasable")
	# 	if purchasables:
	# 		purchasables.last().remove()
	# 		self.purchasable_index = max(0, self.purchasable_index - 1)

	def on_mount(self):
		def update_counter(counter_value : int):
			counter_value_fmt = "$" + str(counter_value)
			self.query_one(TuxbuxCounter).update(value=counter_value_fmt)
		self.watch(self, "tuxbuxAmount", update_counter)
		self.set_interval(1, self.handle_cps)

	def handle_cps(self) -> None:
		app.tuxbuxAmount += app.tuxbuxPerSecond
		self.current_time = monotonic() - self.start_time
		self.log(app.tuxbuxPerSecond) 
		self.log(self.current_time) 

	def on_tux_logo_clicked(self, message: TuxLogo.Clicked) -> None:
		self.tuxbuxAmount += 1
		self.tuxbuxClicks += 1
		self.log(message)

	def on_shop_entry_bought(self, message: ShopEntry.Bought) -> None:
		self.tuxbuxAmount -= max(0, message.cost)
		self.log(message.entry)
		self.log(ShopEntries)
		ShopEntriesOwned[message.entry] += 1
		app.tuxbuxPerSecond += message.cps
		self.log(ShopEntriesOwned[message.entry])

if __name__ == "__main__":
	app = TuxbuxIdleGameApp()
	app.run()
