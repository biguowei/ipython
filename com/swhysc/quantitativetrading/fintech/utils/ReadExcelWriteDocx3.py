# -*- coding: utf-8 -*-
import time

import win32com.client
import os


class RemoteExcel:
    """对excel表格的操作
    """

    def __init__(self, filename=None):
        """初始化函数
        Args:
            filename: 要进行操作的文件名，如果存在此文件则打开，不存在则新建此文件名一般包含路径
        """
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        self.xlApp.Visible = 0
        self.xlApp.DisplayAlerts = 0  # 后台运行，不显示，不警告
        if filename:
            self.filename = filename
            if os.path.exists(self.filename):
                self.xlBook = self.xlApp.Workbooks.Open(filename)
            else:
                self.xlBook = self.xlApp.Workbooks.Add()  # 创建新的Excel文件
                self.xlBook.SaveAs(self.filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''

    def get_cell(self, row, col, sheet=None):
        """读取单元格的内容
        Args:
            row: 行
            col: 列
            sheet: 表格名（不是文件名）
        """
        if sheet:
            sht = self.xlBook.Worksheets(sheet)
        else:
            sht = self.xlApp.ActiveSheet
        return sht.Cells(row, col).Value

    def set_cell(self, sheet, row, col, value):
        """向表格单元格写入
        Args:
            sheet: 表格名（不是文件名）
            row: 行
            col: 列
            value: 定入内容
        """
        try:
            sht = self.xlBook.Worksheets(sheet)
        except:
            self.new_sheet(sheet)
            sht = self.xlBook.Worksheets(sheet)
        sht.Cells(row, col).Value = value

    def save(self, newfilename=None):
        """保存表格"""
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(self.filename)
        else:
            self.xlBook.Save()

    def close(self):
        """保存表格、关闭表格，结束操作"""
        self.save()
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def new_sheet(self, newSheetName):
        """新建一个新表格"""
        sheet = self.xlBook.Worksheets.Add()
        sheet.Name = newSheetName
        sheet.Activate()

    def active_sheet(self):
        return self.xlApp.ActiveSheet


class RemoteWord:
    def __init__(self, filename=None):
        self.xlApp = win32com.client.DispatchEx('Word.Application')
        self.xlApp.Visible = 0
        self.xlApp.DisplayAlerts = 0  # 后台运行，不显示，不警告
        if filename:
            self.filename = filename
            if os.path.exists(self.filename):
                self.doc = self.xlApp.Documents.Open(filename)
            else:
                self.doc = self.xlApp.Documents.Add()  # 创建新的文档
                self.doc.SaveAs(filename)
        else:
            self.doc = self.xlApp.Documents.Add()
            self.filename = ''

    def add_doc_end(self, string):
        """在文档末尾添加内容"""
        rangee = self.doc.Range()
        rangee.InsertAfter('\n' + string)

    def add_doc_start(self, string):
        """在文档开头添加内容"""
        rangee = self.doc.Range(0, 0)
        rangee.InsertBefore(string + '\n')

    def insert_doc(self, insertPos, string):
        """在文档insertPos位置添加内容"""
        rangee = self.doc.Range(0, insertPos)
        if insertPos == 0:
            rangee.InsertAfter(string)
        else:
            rangee.InsertAfter('\n' + string)

    def save(self):
        """保存文档"""
        self.doc.Save()

    def save_as(self, filename):
        """文档另存为"""
        self.doc.SaveAs(filename)

    def close(self):
        """保存文件、关闭文件"""
        self.save()
        self.xlApp.Documents.Close()
        self.xlApp.Quit()


if __name__ == '__main__':
    # example1

    # TODAY = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    excel = RemoteExcel('F:\\PythonPro\\com\\swhysc\\test.xlsx')
    excel.set_cell('old', 1, 1, time.time())
    print(excel.get_cell(1, 1, 'new'))
    excel.close()

    # example2
    '''
    doc = RemoteWord(r'F:\\PythonPro\\com\\swhysc\\test.docx')
    doc.insert_doc(0, '0123456789')
    doc.add_doc_end('9876543210')
    doc.add_doc_start('asdfghjklm')
    doc.insert_doc(10, 'qwertyuiop')
    doc.close()
    '''
