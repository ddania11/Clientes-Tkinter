from tkinter import ttk
from tkinter import *
import sqlite3

class Client:
    db = 'basedatos.db'

    def __init__(self, window):
        self.window = window
        self.window.title('Administrador de Clientes')
        
        

        #Creacion del Frame contenedor 
        frame = LabelFrame(self.window, text='Registrar Nuevo Cliente')
        frame.grid(row=0, columnspan=8)
        #Nombre, Apellido, Cedula, Factura, Formula, Total, Abono, Resto

        #1ra fila, Labels Datos
        Label(frame, text='Nombre').grid(row=1, column=0, columnspan=2)
        Label(frame, text='Cédula').grid(row=1, column=2)
        Label(frame, text='Factura').grid(row=1, column=3)

        #2da fila, Entry Datos
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=2,column=0, columnspan=2, sticky=W+E)

        self.cedula = Entry(frame)
        self.cedula.grid(row=2,column=2)
        
        self.factura= Entry(frame)
        self.factura.grid(row=2,column=3)

        Label(frame, text='Formula').grid(row=3, column=0)
        Label(frame, text='Total').grid(row=3, column=1)
        Label(frame, text='Abono').grid(row=3, column=2)
        Label(frame, text='Resto').grid(row=3, column=3)

        #2da fila, Entry Datos
        self.formula=Entry(frame)
        self.formula.grid(row=4,column=0)

        self.total=Entry(frame)
        self.total.grid(row=4,column=1)

        self.abono=Entry(frame)
        self.abono.grid(row=4,column=2)

        self.resto=Entry(frame)
        self.resto.grid(row=4,column=3)

        #Boton Guardar datos base de datos
        self.boton =ttk.Button(frame, text='Registrar Cliente', command=self.add_client)
        self.boton.grid(row=5, columnspan=4, sticky=W+E)

        #Notificación

        self.message = Label(frame, text='', fg='red')
        self.message.grid(row=6, columnspan=4, sticky=W+E)

        #Creacion del Treeview (Table)
        self.tree = ttk.Treeview(height=25, columns=(' #1, #2, #3, #4, #5, #6, #7, #8'))
        self.tree.grid(row=7, column=0, columnspan=7)
        self.tree.heading('#0', text='', anchor=CENTER)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.heading('#1', text='ID', anchor=CENTER)
        self.tree.column('#1', stretch=NO, minwidth=0, width=20, anchor=CENTER)
        self.tree.heading('#2', text='Nombre', anchor=CENTER)
        self.tree.column('#2', stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.tree.heading('#3', text='Cedula', anchor=CENTER)
        self.tree.column('#3', stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.tree.heading('#4', text='Factura', anchor=CENTER)
        self.tree.column('#4', stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.tree.heading('#5', text='Formula', anchor=CENTER)
        self.tree.column('#5', stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.tree.heading('#6', text='Total', anchor=CENTER)
        self.tree.column('#6', stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.tree.heading('#7', text='Abono', anchor=CENTER)
        self.tree.column('#7', stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.tree.heading('#8', text='Resto', anchor=CENTER)
        self.tree.column('#8', stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.get_client()

        Button(text='BORRAR', command=self.delete).grid(row=8, column=2, sticky = W+E)
        Button(text='EDITAR', command=self.edit).grid(row=8, column=3, sticky= W+E)
        Button(text='BUSCAR', command=self.search).grid(row=8, column=4,sticky= W+E)
        

    #Funcion que se encarga de ejecutar la conexión
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    def get_client(self, where=''):
        #Limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Boton buscar
        if len(where) > 0:
            query = ('SELECT id, nombre, cedula, factura, formula, total, abono, resto FROM cliente' + where)
        else:
            query = 'SELECT id, nombre, cedula, factura, formula, total, abono, resto FROM cliente ORDER BY id DESC'
        #select column1, column2 from tables_name
        table_rows = self.run_query(query)
        for row in table_rows:
            self.tree.insert('', 0, text= str(row[0]), values=row[0:8])
    
    def validation(self): 
        return len(self.nombre.get())!=0 and len(self.cedula.get())!=0 and len(self.factura.get())!=0
    
    def add_client(self): 
        if self.validation():
            query = 'INSERT INTO cliente VALUES (NULL, ?,?,?,?,?,?,?)'

            parameters = (self.nombre.get(), self.cedula.get(), self.factura.get(), self.formula.get(), self.total.get(), self.abono.get(), self.abono.get())

            self.run_query(query, parameters)
            self.message['text'] = f'Cliente "{self.nombre.get()}" , agregado exitosamente en la base de datos.'
            self.nombre.delete(0,END)
            self.cedula.delete(0,END)
            self.factura.delete(0,END)
            self.formula.delete(0,END)
            self.total.delete(0,END)
            self.abono.delete(0,END)
            self.resto.delete(0,END)
        else: 
            self.message['text'] = 'Los campos: Nombre, cedula y factura son obligatorios, por favor llene dichos campos.'
        self.get_client()  
    
    def delete(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor seleccione el cliente que quiere eliminar'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM cliente WHERE id  = ?'
        self.run_query(query, (name,))
        self.message['text'] = f"El cliente {self.tree.item(self.tree.selection())['values'][1]} ha sido eliminado"
        self.get_client()
    
    def edit(self): 
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor seleccione el cliente que quiere editar'
            return
        self.old_id = self.tree.item(self.tree.selection())['values'][0]
        self.old_nombre = self.tree.item(self.tree.selection())['values'][1]
        self.old_cedula = self.tree.item(self.tree.selection())['values'][2]
        self.old_factura = self.tree.item(self.tree.selection())['values'][3]
        self.old_formula = self.tree.item(self.tree.selection())['values'][4]
        self.old_total = self.tree.item(self.tree.selection())['values'][5]
        self.old_abono = self.tree.item(self.tree.selection())['values'][6]
        self.old_resto = self.tree.item(self.tree.selection())['values'][7]
        self.edit_wind = Toplevel()
        self.edit_wind.resizable(0,0)

        self.edit_wind.title = 'Editar cliente'

        #ID
        Label(self.edit_wind, text='ID').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=self.old_id), state='readonly').grid(row=0, column=2)
        
        #Nombre Actual
        Label(self.edit_wind, text='Nombre Actual').grid(row=0, column=3)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=self.old_nombre), state='readonly').grid(row=0, column=4)

        #Nombre nuevo
        Label(self.edit_wind, text='Nuevo Nombre').grid(row=1, column=3)
        new_nombre = Entry(self.edit_wind)
        new_nombre.grid(row=1, column=4)

        #Cedula Actual
        Label(self.edit_wind, text='Cedula Actual').grid(row=0, column=5)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=self.old_cedula), state='readonly').grid(row=0, column=6)

        #Cedula nueva
        Label(self.edit_wind, text='Nueva cedula').grid(row=1, column=5)
        new_cedula = Entry(self.edit_wind)
        new_cedula.grid(row=1, column=6)

        #Factura actual
        Label(self.edit_wind, text='Factura Actual').grid(row=0, column=7)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=self.old_factura), state='readonly').grid(row=0, column=8)

        #Factura nueva
        Label(self.edit_wind, text='Nueva Factura').grid(row=1, column=7)
        new_factura = Entry(self.edit_wind)
        new_factura.grid(row=1, column=8)

        #Formula Actual
        Label(self.edit_wind, text='Formula Actual').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=self.old_factura), state='readonly').grid(row=2, column=2)

        #Formula Nueva
        Label(self.edit_wind, text='Nueva Formula').grid(row=3, column=1)
        new_formula = Entry(self.edit_wind)
        new_formula.grid(row=3, column=2)

        #Total Actual
        Label(self.edit_wind, text='Total Actual').grid(row=2, column=3)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=self.old_total), state='readonly').grid(row=2, column=4)

        #Total Nuevo
        Label(self.edit_wind, text='Nuevo Total').grid(row=3, column=3)
        new_total = Entry(self.edit_wind)
        new_total.grid(row=3, column=4)

        #Abono Actual
        Label(self.edit_wind, text='Abono Actual').grid(row=2, column=5)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=self.old_abono), state='readonly').grid(row=2, column=6)

        #Nuevo Abono
        Label(self.edit_wind, text='Nuevo Abono').grid(row=3, column=5)
        new_abono = Entry(self.edit_wind)
        new_abono.grid(row=3, column=6)

        #Resto Actual
        Label(self.edit_wind, text='Resto Actual').grid(row=2, column=7)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=self.old_resto), state='readonly').grid(row=2, column=8)

        #Nuevo Resto
        Label(self.edit_wind, text='Nuevo Resto').grid(row=3, column=7)
        new_resto = Entry(self.edit_wind)
        new_resto.grid(row=3, column=8)

        guardar = Button(self.edit_wind, text='Aplicar Cambios', command=lambda:self.edit_clients(new_nombre.get(), new_cedula.get(), new_factura.get(), new_formula.get(), new_total.get(), new_abono.get(), new_resto.get(), self.old_id))
        guardar.grid(row=5, column=3, columnspan=4, sticky=W+E)

    def edit_clients(self, new_nombre, new_cedula, new_factura, new_formula, new_total, new_abono, new_resto, old_id):

        if len(new_nombre) == 0:
            new_nombre = self.old_nombre
        
        if len(new_cedula) == 0:
            new_cedula = self.old_cedula
        
        if len(new_factura) == 0:
            new_factura = self.old_factura
        
        if len(new_formula) == 0:
            new_formula = self.old_formula
        
        if len(new_total) == 0:
            new_total = self.old_total
        
        if len(new_abono) == 0:
            new_abono = self.old_abono
        
        if len(new_resto) == 0:
            new_resto = self.old_resto

        query = 'UPDATE cliente SET nombre = ?, cedula = ?, factura=?, formula=?, total=?, abono=?, resto=?  WHERE id =?'
        parameters = (new_nombre, new_cedula, new_factura, new_formula, new_total, new_abono, new_resto, old_id)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'El cliente {} ha sido modificado'.format(new_nombre)
        self.get_client()

    def search(self):
        self.search_client = Toplevel()
        self.search_client.resizable(0,0)

        '''Label(self.search_client, text='Llene un campo para obtener la información').grid(row=0, column=1)
        self.busqueda = Entry(self.search_client)
        self.busqueda.grid(row=1, column=1)

        botonbuscar= Button(self.search_client, text='Buscar', command= self.buscarRegistro)

        botonbuscar.grid(row=2, column=1)
        '''
        Label(self.search_client, text='Buscar id').grid(row=0, column=1)
        Label(self.search_client, text='Buscar Nombre').grid(row=1, column=1)
        Label(self.search_client, text='Buscar Cedula').grid(row=2, column=1)
        Label(self.search_client, text='Buscar Factura').grid(row=3, column=1)

        self.searchId = Entry(self.search_client)
        self.searchId.grid(row=0, column=2)

        self.searchNombre = Entry(self.search_client)
        self.searchNombre.grid(row=1, column=2)

        self.searchCedula = Entry(self.search_client)
        self.searchCedula.grid(row=2, column=2)

        self.searchFactura = Entry(self.search_client)
        self.searchFactura.grid(row=3, column=2)

        Button(self.search_client, text='Buscar', command=self.buscarRegistro).grid(row=4, column=1, columnspan = 2, sticky= W+E)


    def buscarRegistro(self):
        where=" where 1=1 "
        if len(self.searchId.get())>0 :
            where=where+" and id ='"+self.searchId.get()+"' "
        if len(self.searchNombre.get())>0 :
            where=where+" and nombre like'"+self.searchNombre.get()+"' "
        if len(self.searchCedula.get())>0 :
            where=where+" and cedula like'"+self.searchCedula.get()+"' "
        if len(self.searchFactura.get())>0 :
            where=where+" and factura like'"+self.searchFactura.get()+"' "
        
        Button(text='VOLVER A LA LISTA', command=self.get_client).grid(row=8, column=5,sticky= W+E)
        

        
        
        self.get_client(where)


if __name__ == '__main__':
    window = Tk()
    application = Client(window)
    window.mainloop()