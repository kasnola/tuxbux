from time import monotonic

from textual import log
from textual.app import App, ComposeResult
from textual.content import Content
from textual.containers import Middle, HorizontalGroup, VerticalGroup, VerticalScroll, Center
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Rule, Digits, Footer, Header, Static, Label

class Shop(VerticalScroll):
	"""The shop."""

	def compose(self) -> ComposeResult:
		"""Create child purchasables."""
		yield Purchasable(name="Product 00", classes="purchasable", id="tuxminer")
		yield Purchasable(name="Product 01", classes="purchasable", id="tuxminer2")

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
		with VerticalGroup(classes="label"):
			yield Label(self.description, id=self.id)
		with Middle():
			yield Button("Buy", classes="button buy", id=self.id)

class TuxbuxIdleGameApp(App):
	CSS_PATH = "tuxbux.tcss"
	TITLE = "Tuxbux"
	SUB_TITLE = "An idle game in your terminal"
	SHOPHEADER = """
   ▄▄▄▄    ▄▄    ▄▄    ▄▄▄▄    ▄▄▄▄▄▄   
 ▄█▀▀▀▀█   ██    ██   ██▀▀██   ██▀▀▀▀█▄ 
 ██▄       ██    ██  ██    ██  ██    ██ 
  ▀████▄   ████████  ██    ██  ██████▀  
      ▀██  ██    ██  ██    ██  ██       
 █▄▄▄▄▄█▀  ██    ██   ██▄▄██   ██       
  ▀▀▀▀▀    ▀▀    ▀▀    ▀▀▀▀    ▀▀       
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
		yield Static("Tuxbux", classes="box")
		yield Static("Hax0r Display", classes="box")
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

	def action_toggle_dark(self) -> None:
		"""An action to toggle dark mode."""
		self.theme = (
			"textual-dark" if self.theme == "textual-light" else "textual-light"
		)

if __name__ == "__main__":
	app = TuxbuxIdleGameApp()
	app.run()
