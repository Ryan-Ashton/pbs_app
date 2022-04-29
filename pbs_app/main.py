from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.scrollview import ScrollView

from kivy.factory import Factory

from file_manager import GrabFile

from kivy.core.window import Window
Window.size = (800, 850)

from scraper import Scraper


class MDBoxLayout(MDBoxLayout):
    pass

class MDGridLayout(MDGridLayout):
    pass

class ScrollView(ScrollView):
    pass


class Data(MDApp, MDDataTable, Scraper):

    def table_build(self):
        self.data_table = MDDataTable(
            size_hint=(.9, 1),
            pos_hint={'center_x': .5, 'center_y': .5},
            use_pagination=False,
            check=False,
            column_data=[
                ("item_codes", dp(50)),
                ("criteria", dp(20)),
                ("date", dp(20)),
                ("state", dp(20)),
                ("value", dp(20)),
            ],
            row_data=Scraper.row_tuples(self),
            sorted_on="date",
            sorted_order="ASC",
            elevation=2,
        )

        return self.data_table

class MainApp(MDApp, Scraper):
    
    def tab_build(self):
        return self.root.ids.table.add_widget(Data.table_build(self))

    def build(self):
        # return Builder.load_file('main.kv')
        return self.load_all_kv_files()

    def load_all_kv_files(self):
        Builder.load_file('main.kv')
        




MainApp().run()