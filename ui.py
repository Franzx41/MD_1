# -*- coding: utf-8 -*-

import wx
import pandas as pd
from ranking import ranking

class Ui(wx.Frame):    
    def __init__(self, parent, title):
        super(Ui, self).__init__(parent, title=title, size=(500, 400))

        panel = wx.Panel(self)
        mainBox = wx.BoxSizer(wx.VERTICAL)

        self.heroForm = wx.TextCtrl(panel , 0 ,style = wx.TE_PROCESS_ENTER)
        self.heroForm.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)
        mainBox.Add(self.heroForm, 0, wx.ALL | wx.EXPAND, 5)

        self.list_ctrl = wx.ListCtrl(
            panel, size=(-1, -1), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onListClick, self.list_ctrl)
        mainBox.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        self.sbox = wx.StaticBox(panel, -1, 'Busca de heróis por atributos similares:') 
        self.sboxSizer = wx.StaticBoxSizer(self.sbox, wx.VERTICAL) 

        metricas = ['hamming', 'jaccard', 'simpson'] 
        self.combo = wx.ComboBox(panel, value=metricas[0], choices = metricas)
        self.sboxSizer.Add(self.combo, 0, wx.ALL | wx.RIGHT, 5)

        self.ckboxList = wx.CheckListBox(parent=panel, id=wx.ID_ANY, size=(-1, 80))
        self.sboxSizer.Add(self.ckboxList, 1, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL) 

        cancelButton = wx.Button(panel, label='Cancelar', size=(70, 30))
        cancelButton.Bind(wx.EVT_BUTTON, self.onBackBtnClick) 
        hbox.Add(cancelButton, 0, wx.ALL|wx.LEFT, 5)

        # = wx.Button(panel, label='Selecionar Tudo', size=(70, 30))
        #selectAllButton.Bind(wx.EVT_BUTTON, self.onSelectAllBtnClick) 
        #hbox.Add(selectAllButton, 0, wx.ALL|wx.LEFT, 5)  

        searchButton = wx.Button(panel, label='Buscar', size=(70, 30))
        searchButton.Bind(wx.EVT_BUTTON, self.onSearchBtnClick) 
        hbox.Add(searchButton, 0, wx.ALL|wx.LEFT, 5) 

        self.sboxSizer.Add(hbox, 0, wx.ALL|wx.LEFT, 0)
        mainBox.Add(self.sboxSizer, 0, wx.ALL | wx.EXPAND, 5)

        #self.sboxSizer.ShowItems(show=False)

        panel.SetSizer(mainBox)

        self.selectedHero = None


    #def onSelectAllBtnClick(self, event):
        #for i in self.ckboxList.GetChecked
        #for i in range(0, ):
            #print self.ckboxList.GetItem

    def OnEnterPressed(self,event): 
        self.list_ctrl.DeleteAllItems()
        if (event.GetString() == ''):
            self.__show_dataset(self.dataset)
        else:
            # Add columns
            for i in range(len(self.dataset.columns)):
                self.list_ctrl.InsertColumn(i, self.dataset.columns[i], width=80)
            # Add rows
            size = self.dataset.shape[0]
            for i in range(size): # FIXME
                h = self.dataset.iloc[i]['hero_names']
                if h.lower().startswith(str(event.GetString()).lower()):
                    self.list_ctrl.Append(self.dataset.iloc[i])

    def onBackBtnClick(self, event):
        self.selectedHero = None
        self.list_ctrl.DeleteAllItems()
        self.list_ctrl.DeleteAllColumns()
        self.__show_dataset(self.dataset)
        self.SetTitle('Analisador de Heróis')

    def onSearchBtnClick(self, event):
        if self.selectedHero is None:
            print ("Heroi não selecionado")
            return
        features = [self.dataset.columns[i + 1] for i in range(self.ckboxList.GetCount()) if self.ckboxList.IsChecked(i)]
        if len(features) == 0:
            print ("Features não selecionadas")
            return
        #index = self.list_ctrl.GetFirstSelected()
        self.list_ctrl.DeleteAllItems()
        #hero_name = self.dataset.copy().iloc[index]['hero_names']
        #features = ["Agility", "Accelerated Healing", "Lantern Power Ring", "Dimensional Awareness"]
        print("Buscando por " + "'" + str(self.selectedHero) + "'")
        print("Features: ")
        print (features)
        result = ranking(self.dataset.copy(), features, str(self.selectedHero), metodo=self.combo.GetValue())
        result = result[0:10]
        result = result.iloc[:, ::-1]
        #print result
        self.list_ctrl.DeleteAllColumns()
        self.list_ctrl.InsertColumn(0, 'Score', width=80)
        self.list_ctrl.InsertColumn(1, 'Super-herói', width=80)
        self.__addItems(result[0:10]) #top 10
        self.heroForm.SetValue('') 

    def onListClick(self, event):
        #print('Clicked')
        self.ckboxList.Set(self.dataset.columns[1:len(self.dataset.columns)]) # Mostra atributos
        self.selectedHero = self.list_ctrl.GetItemText(self.list_ctrl.GetFirstSelected())
        self.SetTitle('Analisador de Heróis @ ' + '"' + str(self.selectedHero) + '"')
        #self.sboxSizer.ShowItems(show=True)

    def __addItems(self, dataset):
        # Add linhas do dataset
        size = dataset.shape[0]
        for i in range(size):
            self.list_ctrl.Append(dataset.iloc[i])

    def open_dataset(self):
        pd.set_option('display.max_columns', 200)
        self.dataset = pd.read_csv('data/superpoderes.csv')
        self.__show_dataset(self.dataset)
        
    def __show_dataset(self, dataset):
        # Add colunas do dataset
        for i in range(len(dataset.columns)):
            self.list_ctrl.InsertColumn(i, dataset.columns[i], width=80)
            
        self.__addItems(dataset.head(20))

if __name__ == '__main__':
    app = wx.App()
    ui = Ui(None, title='Analisador de Heróis')
    ui.open_dataset()
    ui.Show()
    app.MainLoop()
