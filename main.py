# Kivy Dependencies
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.toast import toast
from kivy.factory import Factory

# Screens and Components
from components.file_manager import GrabFile
from components.scraper import Scraper
from screens.home import Home

# Additional Dependencies
import pandas as pd

#  Resize the Window when starting the App
from kivy.core.window import Window
Window.size = (800, 850)


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
        toast("Download has started, please wait :)")
        return self.sm.get_screen('Home').ids.table.add_widget(Data.table_build(self))

    def build(self):
        self.load_all_kv_files()
        self.sm = ScreenManager()
        screens = [Home(), GrabFile()]
        for screen in screens:
            self.sm.add_widget(screen)
        return self.sm

    def load_all_kv_files(self):
        Builder.load_file('screens/home.kv')
        Builder.load_file('components/file_manager.kv')

    def download_csv(self):
        if self.sm.get_screen('Home').ids.file_path.text == '':
            with open('components/path.txt') as f:
                path = f.read()
            df = Scraper.get_data(self)
            df.to_csv(path, index=False)

        elif self.sm.get_screen('Home').ids.file_path.text != '':
            df = Scraper.get_data(self)
            path = self.sm.get_screen('Home').ids.file_path.text
            df.to_csv(path, index=False)

        else:
            toast('Please select a file')

MainApp().run()

