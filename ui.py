# -*- coding: utf-8 -*-

import wx
import pandas as pd
from ranking import ranking

class Ui(wx.Frame):    
    def __init__(self, parent, title):
        super(Ui, self).__init__(parent, title=title, size=(500, 400))

        panel = wx.Panel(self)
        mainBox = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = wx.ListCtrl(
            panel, size=(-1, -1), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onListClick, self.list_ctrl)
        mainBox.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        self.sbox = wx.StaticBox(panel, -1, 'Busca de heróis por atributos similares:') 
        self.sboxSizer = wx.StaticBoxSizer(self.sbox, wx.VERTICAL) 

        self.ckboxList = wx.CheckListBox(parent=panel, id=wx.ID_ANY, size=(-1, 80))
        self.sboxSizer.Add(self.ckboxList, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL) 

        cancelButton = wx.Button(panel, label='Cancelar', size=(70, 30))
        hbox.Add(cancelButton, 0, wx.ALL|wx.LEFT, 5) 

        searchButton = wx.Button(panel, label='Buscar', size=(70, 30))
        searchButton.Bind(wx.EVT_BUTTON, self.onBtnClick) 
        hbox.Add(searchButton, 0, wx.ALL|wx.LEFT, 5) 

        self.sboxSizer.Add(hbox, 0, wx.ALL|wx.LEFT, 0)
        mainBox.Add(self.sboxSizer, 0, wx.ALL | wx.EXPAND, 5)

        #self.sboxSizer.ShowItems(show=False)

        panel.SetSizer(mainBox)

    def onBtnClick(self, event):
        index = self.list_ctrl.GetFirstSelected()
        self.list_ctrl.DeleteAllItems()
        hero_name = self.dataset.iloc[index]['hero_names']
        #features = ["Agility", "Accelerated Healing", "Lantern Power Ring", "Dimensional Awareness"]
        features = [self.dataset.columns[i + 1] for i in range(self.ckboxList.GetCount()) if self.ckboxList.IsChecked(i)]
        result = ranking(self.dataset.copy(), features, hero_name, metodo='hamming')
        result = result[0:10]
        result = result.iloc[:, ::-1]
        #print result
        self.list_ctrl.DeleteAllColumns()
        self.list_ctrl.InsertColumn(0, 'similaridade', width=80)
        self.list_ctrl.InsertColumn(1, 'hero_names', width=80)
        self.addItems(result[0:10]) #top 10

    def onListClick(self, event):
        #print('Clicked')
        self.ckboxList.Set(self.dataset.columns[1:len(self.dataset.columns)]) # Mostra atributos
        #self.sboxSizer.ShowItems(show=True)

    def addItems(self, dataset):
        # Add linhas do dataset
        size = dataset.shape[0]
        for i in range(size):
            self.list_ctrl.Append(dataset.iloc[i])

    def open_dataset(self):
        pd.set_option('display.max_columns', 200)
        self.dataset = pd.read_csv('data/superpoderes.csv')
        
    def show_dataset(self):
        # Add colunas do dataset
        for i in range(len(self.dataset.columns)):
            self.list_ctrl.InsertColumn(i, self.dataset.columns[i], width=80)
            
        self.addItems(self.dataset)

if __name__ == '__main__':
    app = wx.App()
    ui = Ui(None, title='Analisador de Heróis')
    ui.open_dataset()
    ui.show_dataset()
    ui.Show()
    app.MainLoop()
