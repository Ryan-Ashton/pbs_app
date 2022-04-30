import pandas as pd
import numpy as np


class Scraper():


    def get_data(self):

        items = self.root.ids.item_codes.text.replace(" ", "").split(',')
        print(items)


        insert_items = 'itemlst=' +  '%27' + '%27%2C%27'.join(items) + '%27&ITEMCNT=' + str(len(items)) +'&LIST=' + '%2C'.join(items)


        df = pd.read_html("http://medicarestatistics.humanservices.gov.au/statistics/do.jsp?_PROGRAM=%2Fstatistics%2Fpbs_item_standard_report&" + insert_items + "&VAR=SERVICES&RPT_FMT=2&start_dt=199201&end_dt=202106")
        df = df[1]

        df.columns = df.columns.droplevel(2)
        df.columns = df.columns.droplevel(0)

        df=df.rename(columns = {'Unnamed: 0_level_1':'item_codes',
                                'Unnamed: 1_level_1':'criteria',
                                'Unnamed: 2_level_1':'date'})

        df = df[df["item_codes"].isin(items)]

        df = df[(df["criteria"] != "Scheme") & (df["criteria"] != "Total")]

        df = df[(df["date"] != "Total") & (df["date"] != "Month")]

        df = df.drop('Total', 1)


        state_list = [x for x in df.columns if x not in ['item_codes','criteria', 'date']]

        for x in state_list:
            df[x] = df[x].astype('int32')
            
            
        df = pd.pivot_table(df, values=state_list, index=['item_codes', 'criteria', 'date'])


        df = df.stack()

        df = df.to_frame()

        df = df.reset_index()

        df=df.rename(columns = {'level_3':'state',
                                0:'services'})



        df["date"] = pd.to_datetime(df["date"], dayfirst=True)
        df["date"] = pd.offsets.MonthEnd(1) + df["date"]
        df["date"] = df["date"].dt.strftime('%d-%m-%Y')

        return df


    def row_tuples(self):

        df = self.get_data()

        row_tuples = [tuple(x) for x in df.values]

        return row_tuples

    def column_tuples(self):

        df = self.get_data()

        column_tuples = []

        for x in df.columns:
            x = (x,) + "dp(20)"
            column_tuples.append(x)

        return column_tuples

    def download_csv(self):

        df = self.get_data()

        df.to_csv(self.root.ids.file_path.text, index=False)