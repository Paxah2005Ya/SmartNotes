#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QApplication, QWidget, QInputDialog
from json import *
key = ''
tag = ''
isSearch = False
dictNotes = {
    'Приветствие': {
        'Текст': 'Привет!',
        'Теги': ['Привет']
    }
}
def loadFromFile():
    global dictNotes
    with open('notes.json', 'r', encoding='utf-8') as file:
        dictNotes = load(file)
    showNotes()    
    disableButtons()

def showNotes():
    teNote.clear()
    lwNotes.clear()
    lwTags.clear()
    leTags.clear()
    lwNotes.addItems(dictNotes) 

def setNote():
    lwTags.clear()
    global key
    key = lwNotes.selectedItems()[0].text()
    teNote.setText(dictNotes[key]['Текст'])
    lwTags.addItems(dictNotes[key]['Теги'])
    enableButtons()
    btnDelTag.setDisabled(True)
def disableButtons():
    btnDelNote.setDisabled(True)
    btnSaveNote.setDisabled(True)
    btnAddTag.setDisabled(True)
    btnDelTag.setDisabled(True)
def enableButtons():
    if isSearch:
        return
    btnDelNote.setDisabled(False)
    btnSaveNote.setDisabled(False)
    btnAddTag.setDisabled(False)
    #btnDelTag.setDisabled(False)
def saveNote():
    dictNotes[key]['Текст'] = teNote.toPlainText()
    itemsList = list()
    for i in range(lwTags.count()):
        item = lwTags.item(i)
        itemsList.append(item.text())
    dictNotes[key]['Теги'] = itemsList
    writeToFile()
def writeToFile():
    with open('notes.json', 'w', encoding='utf-8') as file:
        dump(dictNotes, file, sort_keys=True)
def delNote():
    del dictNotes[key]
    writeToFile()
    loadFromFile()
def addNote():
    noteName, result = QInputDialog.getText(mw, 'Добавить заметку', 'Введите название:')
    noteName = noteName.strip().lower()
    if result and (len(noteName)) and (not (noteName in dictNotes)):
        dictNotes[noteName] = {
            'Текст': '',
            'Теги': []
        }
        writeToFile()
        loadFromFile()
def addTag():
    tagName = leTags.text().strip().lower()
    if len(tagName) and (not (tagName in dictNotes[key]['Теги'])):
        dictNotes[key]['Теги'].append(tagName)
        writeToFile()
        setNote()
def setTag():
    global tag
    tag = lwTags.selectedItems()[0].text()
    btnDelTag.setDisabled(False)
def delTag():
    dictNotes[key]['Теги'].remove(tag)
    writeToFile()
    setNote()
def srchTag():
    global isSearch
    if btnSrchTag.text() == 'Искать заметки по тегу':
        tagName = leTags.text().strip().lower()
        if len(tagName):
            #ищем по тегу и меняем текст на кнопке
            btnSrchTag.setText('Сбросить поиск')
            disableButtons()
            btnAddNote.setDisabled(True)
            isSearch = True
            dictNotes2 = dictNotes.copy()
            for keyName in dictNotes2:
                if (not (tagName in dictNotes2[keyName]['Теги'])):
                    del dictNotes[keyName]
            showNotes()
    else:
        #сбрасываем поиск
        btnSrchTag.setText('Искать заметки по тегу')
        isSearch = False
        loadFromFile()
App = QApplication([])
mw  = QWidget()
hl  = QHBoxLayout()
vl  = QVBoxLayout()
hlNotes     = QHBoxLayout()
hlTags      = QHBoxLayout()
teNote      = QTextEdit()
lblNotes    = QLabel('Список заметок')
lwNotes     = QListWidget()
btnAddNote  = QPushButton('Создать заметку')
btnDelNote  = QPushButton('Удалить заметку')
btnSaveNote = QPushButton('Сохранить заметку')
lblTags     = QLabel('Список тегов')
lwTags      = QListWidget()
leTags      = QLineEdit()
btnAddTag   = QPushButton('Добавить к заметке')
btnDelTag   = QPushButton('Открепить от заметки')
btnSrchTag  = QPushButton('Искать заметки по тегу')
hl.addWidget(teNote)
hl.addLayout(vl)
vl.addWidget(lblNotes)
vl.addWidget(lwNotes)
vl.addLayout(hlNotes)
vl.addWidget(btnSaveNote)
vl.addWidget(lblTags)
vl.addWidget(lwTags)
vl.addWidget(leTags)
vl.addLayout(hlTags)
vl.addWidget(btnSrchTag)
hlNotes.addWidget(btnAddNote)
hlNotes.addWidget(btnDelNote)
hlTags.addWidget(btnAddTag)
hlTags.addWidget(btnDelTag)

mw.setLayout(hl)
loadFromFile()
lwNotes.itemClicked.connect(setNote)
btnSaveNote.clicked.connect(saveNote)
btnDelNote.clicked.connect(delNote)
btnAddNote.clicked.connect(addNote)
btnAddTag.clicked.connect(addTag)
lwTags.itemClicked.connect(setTag)
btnDelTag.clicked.connect(delTag)
btnSrchTag.clicked.connect(srchTag)
#отключаем "ненужные" кнопки
disableButtons()
mw.show()
App.exec_()