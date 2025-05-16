
import tkinter as tk
import math

class NipkowDiskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disco de Nipkow")
        self.root.configure(bg='yellow')

        # Canvas
        self.canvas_size = 400
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg='yellow')
        self.canvas.pack(padx=20, pady=20)

        self.center = self.canvas_size // 2
        self.radius = self.canvas_size // 2 - 30
        self.num_holes = 13
        self.angle_offset = 0
        self.current_index = 0

        # Iniciar animação
        self.animate()

    def draw_disk(self):
        self.canvas.delete("all")
        z=0
        # Desenhar disco principal
        self.canvas.create_oval(
            self.center - self.radius, self.center - self.radius,
            self.center + self.radius, self.center + self.radius,
            outline="black", width=2
        )
        self.canvas.create_line(self.center, self.center, self.center + math.cos(math.radians(36*7)) * (self.radius), self.center + math.sin(math.radians(36*7)) * (self.radius), width=2)
        self.canvas.create_line(self.center, self.center, self.center + math.cos(math.radians(36*8)) * (self.radius), self.center + math.sin(math.radians(36*8)) * (self.radius), width=2)

        for i in range(self.num_holes):
            z=z+7
            
            angle_deg = (360 / self.num_holes) * (self.num_holes-i) + self.angle_offset
            if angle_deg>360.00:
                angle_deg=angle_deg-360.00
            angle_rad = math.radians(angle_deg)

            
            
            # Coordenadas do final da linha (na borda do disco)
            
            x = self.center + math.cos(angle_rad) * (self.radius- z - 10)
            y = self.center + math.sin(angle_rad) * (self.radius -z- 10)

            # Linha do centro até o ponto
            
            # Círculo no final da linha (ponto)
            r = 6
            
             
            color = "red" 
            if angle_deg>(36*7) and angle_deg<(36*8):
                self.canvas.create_oval(x - r, y - r, x + r, y + r,fill=color)

    def animate(self):
        self.angle_offset = (self.angle_offset + 5) % 360
        self.current_index = (self.current_index + 1) % self.num_holes
        self.draw_disk()
        self.root.after(15, self.animate)

# Rodar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = NipkowDiskApp(root)
    root.mainloop()
