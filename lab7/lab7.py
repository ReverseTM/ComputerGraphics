import tkinter as tk
from math import comb, sqrt


class BezierCurveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bezier Curve Editor")

        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.points = [(100, 400), (200, 100), (300, 400), (400, 200), (500, 400)]  # Initial control points
        self.tensions = [1, 1, 1, 1]  # Initial tensions for each control point

        self.curve_id = None
        self.control_point_ids = []
        self.tangent_ids = []
        self.selected_point = None

        self.draw_curve()
        self.draw_control_points()
        self.draw_point_connections()

        self.canvas.bind("<B1-Motion>", self.drag_point)
        self.canvas.bind("<ButtonRelease-1>", self.release_point)
        self.canvas.bind("<Button-1>", self.select_point)

    def draw_curve(self):
        if self.curve_id:
            self.canvas.delete(self.curve_id)
        if self.tangent_ids:
            self.canvas.delete(*self.tangent_ids)

        steps = 100
        curve_points = []
        for t in range(steps + 1):
            x = sum(comb(4, i) * ((1 - t / steps) ** (4 - i)) * (t / steps) ** i * self.points[i][0] for i in range(5))
            y = sum(comb(4, i) * ((1 - t / steps) ** (4 - i)) * (t / steps) ** i * self.points[i][1] for i in range(5))
            curve_points.append((x, y))

        self.curve_id = self.canvas.create_line(curve_points, fill="blue")

        for i in range(1, 4):
            tangent_vector = (
                (self.points[i + 1][0] - self.points[i - 1][0]) * self.tensions[i - 1],
                (self.points[i + 1][1] - self.points[i - 1][1]) * self.tensions[i - 1]
            )
            normalized_tangent = (
                tangent_vector[0] / sqrt(tangent_vector[0] ** 2 + tangent_vector[1] ** 2),
                tangent_vector[1] / sqrt(tangent_vector[0] ** 2 + tangent_vector[1] ** 2)
            )
            tangent_point = (
                self.points[i][0] + normalized_tangent[0] * 50,
                self.points[i][1] + normalized_tangent[1] * 50
            )

            tangent_id = self.canvas.create_line(self.points[i], tangent_point, fill="green", arrow=tk.LAST)
            self.tangent_ids.append(tangent_id)

    def draw_control_points(self):
        for point in self.points:
            point_id = \
               self.canvas.create_oval(point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5, fill="red", tags="point")
            self.control_point_ids.append(point_id)

    def draw_point_connections(self):
        for i in range(len(self.points) - 1):
            connection_id = self.canvas.create_line(self.points[i], self.points[i + 1], fill="black", dash=(2, 2))
            self.tangent_ids.append(connection_id)
        # Соединяем последнюю точку с первой
        connection_id = self.canvas.create_line(self.points[-1], self.points[0], fill="black", dash=(2, 2))
        self.tangent_ids.append(connection_id)

    def drag_point(self, event):
        if self.selected_point is not None:
            self.points[self.selected_point] = (event.x, event.y)
            self.canvas.coords(
                self.control_point_ids[self.selected_point], event.x - 5, event.y - 5, event.x + 5, event.y + 5)
            self.draw_curve()
            self.draw_point_connections()

    def release_point(self, event):
        self.selected_point = None

    def select_point(self, event):
        for i, point_id in enumerate(self.control_point_ids):
            if self.canvas.coords(point_id)[0] < event.x < self.canvas.coords(point_id)[2] and \
               self.canvas.coords(point_id)[1] < event.y < self.canvas.coords(point_id)[3]:
                self.selected_point = i
                break


if __name__ == '__main__':
    root = tk.Tk()
    app = BezierCurveApp(root)
    root.mainloop()
    