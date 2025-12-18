import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TiendaApp:
    def __init__(self, root):
        self.window = root
        self.window.title("Gestor de Tienda Completo")
        
        self.db_name = 'database.db'
        self.run_query("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, precio REAL)")

        # --- Interfaz ---
        frame = tk.LabelFrame(self.window, text="Registrar nuevo producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        tk.Label(frame, text="Nombre: ").grid(row=1, column=0)
        self.nombre = tk.Entry(frame)
        self.nombre.grid(row=1, column=1)

        tk.Label(frame, text="Precio: ").grid(row=2, column=0)
        self.precio = tk.Entry(frame)
        self.precio.grid(row=2, column=1)

        tk.Button(frame, text="Guardar Producto", command=self.add_product).grid(row=3, columnspan=2, sticky=tk.W + tk.E)

        # Botones de Acción (NUEVO)
        tk.Button(text="ELIMINAR", command=self.delete_product, bg="red", fg="white").grid(row=5, column=0, sticky=tk.W + tk.E)
        tk.Button(text="EDITAR", command=self.edit_product, bg="blue", fg="white").grid(row=5, column=1, sticky=tk.W + tk.E)

        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=tk.CENTER)
        self.tree.heading('#1', text='Precio', anchor=tk.CENTER)
        
        self.get_products()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM productos ORDER BY id DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def add_product(self):
        if self.nombre.get() != '' and self.precio.get() != '':
            query = 'INSERT INTO productos VALUES(NULL, ?, ?)'
            parameters = (self.nombre.get(), self.precio.get())
            self.run_query(query, parameters)
            self.nombre.delete(0, tk.END)
            self.precio.delete(0, tk.END)
            self.get_products()
        else:
            messagebox.showwarning("Error", "Nombre y precio son requeridos")

    # --- NUEVAS FUNCIONES ---
    def delete_product(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            messagebox.showerror("Error", "Selecciona un producto primero")
            return
        nombre = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM productos WHERE nombre = ?'
        self.run_query(query, (nombre, ))
        self.get_products()

    def edit_product(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            messagebox.showerror("Error", "Selecciona un producto primero")
            return
        
        nombre_antiguo = self.tree.item(self.tree.selection())['text']
        precio_antiguo = self.tree.item(self.tree.selection())['values'][0]

        # Ventana emergente para editar
        self.edit_wind = tk.Toplevel()
        self.edit_wind.title = 'Editar Producto'
        
        tk.Label(self.edit_wind, text='Nombre Antiguo:').grid(row=0, column=1)
        tk.Entry(self.edit_wind, textvariable=tk.StringVar(self.edit_wind, value=nombre_antiguo), state='readonly').grid(row=0, column=2)
        
        tk.Label(self.edit_wind, text='Nombre Nuevo:').grid(row=1, column=1)
        new_name = tk.Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        tk.Label(self.edit_wind, text='Precio Antiguo:').grid(row=2, column=1)
        tk.Entry(self.edit_wind, textvariable=tk.StringVar(self.edit_wind, value=precio_antiguo), state='readonly').grid(row=2, column=2)

        tk.Label(self.edit_wind, text='Precio Nuevo:').grid(row=3, column=1)
        new_price = tk.Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        tk.Button(self.edit_wind, text='Actualizar', command=lambda: self.edit_records(new_name.get(), nombre_antiguo, new_price.get(), precio_antiguo)).grid(row=4, column=2, sticky=tk.W)

    def edit_records(self, new_name, old_name, new_price, old_price):
        query = 'UPDATE productos SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        parameters = (new_name, new_price, old_name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.get_products()

if __name__ == '__main__':
    window = tk.Tk()
    application = TiendaApp(window)
    window.mainloop()