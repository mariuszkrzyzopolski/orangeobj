import numpy as np
import pandas as pd


class MergeOrangeData:
    def __init__(self, excel_name, sheet_name):
        self.df = pd.read_excel(excel_name, sheet_name=sheet_name)
        # round time,replace 0 to nan in some columns to proper read
        self.df['START TIME'] = self.df['START TIME'].dt.round("S")
        cols = ["A CAUSE", "B CAUSE"]
        self.df[cols] = self.df[cols].replace(0.0, np.nan)
        self.df["DURATION"] = self.df["DURATION"].fillna(0)
        # merge on fly
        self.result = self.merge_data_frame()

    def merge_pair(self, left, right):
        # only add non NaNs based on matrix
        return pd.Series(np.where(left.isnull(), right, left), index=self.df.columns)

    def merge_data_frame(self):
        # copy first record to maintain columns order
        dfr = pd.DataFrame([self.df.loc[0]])
        for x in range(0, len(self.df)):
            # group same values
            r = self.df.loc[(self.df['A NUMBER'] == self.df.loc[x]['A NUMBER']) & (
                    self.df['B NUMBER'] == self.df.loc[x]['B NUMBER']) & (
                                    self.df['DURATION'] == self.df.loc[x]['DURATION']) & (
                                    self.df['START TIME'] == self.df.loc[x]['START TIME'])]
            # if we more than 2 record = duplicates
            if len(r) >= 2:
                for y in range(0, len(r) - 1):
                    dfr = dfr.append((self.merge_pair(r.iloc[y], r.iloc[y + 1])), ignore_index=True)
            # uniq record, just add to result
            elif len(r) == 1:
                dfr = dfr.append(r.iloc[0])
        return dfr.drop_duplicates()

    # add styles to table and save to file, cannot use pandas to_html if use style
    def generate_html(self, name):
        cols = ["A NUMBER", "B NUMBER", "DURATION", "START TIME"]
        hart = self.result.style.set_properties(**{'background-color': 'green'}, subset=cols)
        hart.set_properties(**{'border-collapse': 'collapse', 'border-style': 'solid', 'border-width': '1px'})
        html_file = open(name, "w")
        html_file.write(hart.render())
        html_file.close()
