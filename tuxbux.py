from time import monotonic

from textual import log
from textual.app import App, ComposeResult
from textual.content import Content
from textual.containers import Middle, HorizontalGroup, VerticalGroup, VerticalScroll, Center
from textual.reactive import reactive
from textual.widgets import Button, Digits, Footer, Header, Static, Label

class Shop(VerticalScroll):
	"""The shop."""

	def compose(self) -> ComposeResult:
		"""Create child purchasables."""
		yield Purchasable(name="Product 00", classes="purchasable", id="tuxminer")
		yield Purchasable(name="Product 01", classes="purchasable", id="tuxminer2")
		yield Purchasable(name="Product 02", classes="purchasable", id="tuxminer3")
		yield Purchasable(name="Product 03", classes="purchasable", id="tuxminer4")
		yield Purchasable(name="Product 04", classes="purchasable", id="tuxminer5")
		yield Purchasable(name="Product 05", classes="purchasable", id="tuxminer6")

class Purchasable(HorizontalGroup):
	"""A purchasable widget."""

	def on_mount(self) -> None:
		self.border_title = self.name

	def on_button_pressed(self, event: Button.Pressed) -> None:
		"""Event handler called when a button is pressed."""
		button_id = event.button.id
		self.log("button pressed @ " + str(button_id))

	def compose(self) -> ComposeResult:
		"""Create child widgets of a purchasable."""
		yield VerticalGroup(
			Label(
				Content.from_markup("[bold]$name[/bold]", name=self.name),
				id=self.id
				),
			classes="label"
		)
		yield Middle(Button("Buy", classes="button buy", id=self.id))

class TuxbuxIdleGameApp(App):
	"""An idle game made with Textual."""

	CSS_PATH = "tuxbux.tcss"
	TITLE = "Tuxbux"
	SUB_TITLE = "An idle game in your terminal"

	BINDINGS = [
		("d", "toggle_dark", "Toggle dark mode"),
	]

	def compose(self) -> ComposeResult:
		"""Create child widgets for the app."""
		yield Header()
		yield Footer()
		yield Static("Tuxbux", classes="box")
		yield Static("Hax0r Display", classes="box")
		yield Shop(classes="box", id="shop")

	def action_toggle_dark(self) -> None:
		"""An action to toggle dark mode."""
		self.theme = (
			"textual-dark" if self.theme == "textual-light" else "textual-light"
		)

if __name__ == "__main__":
	app = TuxbuxIdleGameApp()
	app.run()
