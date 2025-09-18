import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# ---------- Colors / config ----------
BORDER_COLOR = "#0e466b"
PRIMARY_BLUE = "#2b7be9"
PRIMARY_RED = "#e24b4b"
PRIMARY_GREEN = "#26a653"
SIDEBAR_BG = "#2c3e50"
BUTTON_BG = "#0e466b"
SOLUTION_BLUE = "#1e5aa8"
HOVER_BG = "#4a6fa5"
ENTRY_BG = "#f8f9fa"

# ---------- App ----------
class VectorLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vector Learning App - Interactive 3D Visualizer")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configure style
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Initialize lessons
        self.init_lessons()
        
        # Show first lesson
        self.show_lesson("Vector Basics")
        
        # Bind window resize event for responsive centering
        self.root.bind("<Configure>", self.on_window_resize)
    
    def setup_styles(self):
        """Configure ttk styles for better appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure("Sidebar.TButton",
                       background="#34495e",
                       foreground="white",
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 8))
        style.map("Sidebar.TButton",
                 background=[('active', HOVER_BG)])
    
    def create_widgets(self):
        """Create main UI structure"""
        # Sidebar
        self.sidebar = tk.Frame(self.root, width=240, bg=SIDEBAR_BG)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Add title to sidebar
        title_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        title_frame.pack(fill="x", pady=(15, 20))
        tk.Label(title_frame, text="📚 LESSONS", fg="white", bg=SIDEBAR_BG,
                font=("Arial", 14, "bold")).pack()
        
        # Main area container
        self.main_container = tk.Frame(self.root, bg="white")
        self.main_container.pack(side="right", expand=True, fill="both")
        
        # Create canvas and scrollbar for main area
        self.main_canvas = tk.Canvas(self.main_container, bg="white", highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", 
                                           command=self.main_canvas.yview)
        self.main_canvas.config(yscrollcommand=self.main_scrollbar.set)
        
        # Pack scrollbar and canvas
        self.main_scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        # Create the scrollable main area
        self.main_area = tk.Frame(self.main_canvas, bg="white")
        self.main_canvas_window = self.main_canvas.create_window(0, 0, anchor="nw", window=self.main_area)
        
        # Bind mousewheel for scrolling
        self.bind_mousewheel()
    
    def bind_mousewheel(self):
        """Enable mousewheel scrolling"""
        def on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.main_canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows
        self.main_canvas.bind_all("<Button-4>", lambda e: self.main_canvas.yview_scroll(-1, "units"))  # Linux
        self.main_canvas.bind_all("<Button-5>", lambda e: self.main_canvas.yview_scroll(1, "units"))  # Linux
    
    def update_main_scroll(self):
        """Update scroll region"""
        self.main_area.update_idletasks()
        self.main_canvas.config(scrollregion=self.main_canvas.bbox("all"))
        
        # Center the content horizontally when window is wider than content
        canvas_width = self.main_canvas.winfo_width()
        content_width = self.main_area.winfo_reqwidth()
        
        if canvas_width > content_width:
            x_offset = (canvas_width - content_width) // 2
            self.main_canvas.coords(self.main_canvas_window, x_offset, 0)
        else:
            self.main_canvas.coords(self.main_canvas_window, 0, 0)
    
    def on_window_resize(self, event=None):
        """Handle window resize for responsive centering"""
        self.update_main_scroll()
    
    def init_lessons(self):
        """Initialize lesson structure"""
        self.lesson_frames = {}
        self.lessons = [
            "Vector Basics",
            "Vector Addition & Subtraction",
            "Vector Scaling",
            "Vector Magnitude & Direction"
        ]
        
        # Create sidebar buttons with icons
        icons = ["🎯", "➕", "📏", "🧭"]
        for lesson, icon in zip(self.lessons, icons):
            btn_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
            btn_frame.pack(fill="x", padx=8, pady=3)
            
            btn = tk.Button(btn_frame, text=f"{icon} {lesson}", 
                           fg="white", bg="#34495e",
                           font=("Arial", 11), relief="flat",
                           activebackground=HOVER_BG, activeforeground="white",
                           cursor="hand2", pady=10,
                           command=lambda l=lesson: self.show_lesson(l))
            btn.pack(fill="x")
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=HOVER_BG))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))
        
        # Add reset button at bottom
        tk.Frame(self.sidebar, bg=SIDEBAR_BG).pack(expand=True, fill="both")
        reset_btn = tk.Button(self.sidebar, text="🔄 Reset All", 
                             fg="white", bg="#c0392b",
                             font=("Arial", 10, "bold"), relief="flat",
                             activebackground="#e74c3c", cursor="hand2",
                             command=self.reset_all)
        reset_btn.pack(fill="x", padx=8, pady=10)
    
    def show_lesson(self, name):
        """Show selected lesson"""
        for f in self.lesson_frames.values():
            f.pack_forget()
        
        # Create frame if it doesn't exist
        if name not in self.lesson_frames:
            f = tk.Frame(self.main_area, bg="white")
            self.lesson_frames[name] = f
            
            if name == "Vector Basics":
                VectorBasicsLesson(f, self)
            elif name == "Vector Addition & Subtraction":
                VectorAddSubLesson(f, self)
            elif name == "Vector Scaling":
                VectorScalingLesson(f, self)
            elif name == "Vector Magnitude & Direction":
                VectorMagnitudeLesson(f, self)
        
        self.lesson_frames[name].pack(fill="both", expand=True)
        self.update_main_scroll()
    
    def reset_all(self):
        """Reset all lessons"""
        if messagebox.askyesno("Reset", "Reset all vector inputs and plots?"):
            for frame in self.lesson_frames.values():
                frame.destroy()
            self.lesson_frames.clear()
            self.show_lesson(self.lessons[0])

# ------------- Helper Classes and Functions -------------

class VectorInput(tk.Frame):
    """Reusable vector input widget with validation"""
    def __init__(self, parent, label="Vector", default_values=(0, 0, 0), **kwargs):
        super().__init__(parent, **kwargs)
        self.entries = []
        self.create_widgets(label, default_values)
    
    def create_widgets(self, label, defaults):
        tk.Label(self, text=f"{label}:", font=("Arial", 11, "bold"),
                bg=self.cget("bg"), fg="white").grid(row=0, column=0, pady=5, sticky="w")
        
        for i, (comp, val) in enumerate(zip(["X", "Y", "Z"], defaults)):
            tk.Label(self, text=f"{comp}:", bg=self.cget("bg"), fg="white",
                    font=("Arial", 10)).grid(row=1, column=2*i, padx=(10, 5), pady=3)
            
            e = tk.Entry(self, width=8, font=("Arial", 10), bg=ENTRY_BG,
                        relief="solid", bd=1)
            e.insert(0, str(val))
            e.grid(row=1, column=2*i+1, padx=(0, 10), pady=3)
            
            # Add validation
            e.bind("<KeyRelease>", self.validate_input)
            self.entries.append(e)
    
    def validate_input(self, event):
        """Validate numeric input"""
        entry = event.widget
        value = entry.get()
        if value and value != "-":
            try:
                float(value)
                entry.config(bg=ENTRY_BG)
            except ValueError:
                entry.config(bg="#ffcccc")
    
    def get_vector(self):
        """Get vector as numpy array with validation"""
        vec = []
        for e in self.entries:
            v = e.get().strip()
            if v == "" or v == "-":
                vec.append(0.0)
            else:
                try:
                    vec.append(float(v))
                except ValueError:
                    vec.append(0.0)
        return np.array(vec)
    
    def reset(self):
        """Reset to zero vector"""
        for e in self.entries:
            e.delete(0, tk.END)
            e.insert(0, "0")

class PlotManager:
    """Manages plot creation and updates with better centering"""
    @staticmethod
    def plot_vectors(tab, vectors, colors, labels, title, limits=10, show_toolbar=True):
        """Create centered vector plot with optional toolbar"""
        # Clear previous plot elements
        PlotManager.clear_plot(tab)
        
        # Create centered plot frame
        plot_container = tk.Frame(tab, bg="white")
        plot_container.pack(expand=True, fill="both", padx=20, pady=15)
        tab.plot_container = plot_container
        
        # Create inner frame for centering
        plot_frame = tk.Frame(plot_container, bg="white", relief="solid", bd=2)
        plot_frame.pack(expand=True)  # This centers the frame
        tab.plot_frame = plot_frame
        
        # Determine plot dimensions and type
        needs_3d = any(abs(vec[2]) > 1e-10 for vec in vectors if len(vec) >= 3)
        
        # Create figure with appropriate size
        fig_width = 8 if needs_3d else 7
        fig_height = 6 if needs_3d else 5
        
        fig = plt.figure(figsize=(fig_width, fig_height), facecolor='white', dpi=100)
        
        # Create plot
        if needs_3d:
            ax = fig.add_subplot(111, projection='3d')
            PlotManager.setup_3d_plot(ax, vectors, colors, labels, limits)
        else:
            ax = fig.add_subplot(111)
            PlotManager.setup_2d_plot(ax, vectors, colors, labels, limits)
        
        ax.set_title(title, fontsize=14, weight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add legend if multiple vectors
        if len(vectors) > 1:
            ax.legend(loc='upper right', framealpha=0.9)
        
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        
        # Add navigation toolbar if requested
        if show_toolbar:
            toolbar_frame = tk.Frame(plot_frame, bg="white")
            toolbar_frame.pack(fill="x")
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            tab.toolbar = toolbar
        
        tab.canvas_widget = canvas
        
        # Update scroll region after adding plot
        if hasattr(tab, 'master') and hasattr(tab.master, 'update_main_scroll'):
            tab.master.update_main_scroll()
    
    @staticmethod
    def setup_3d_plot(ax, vectors, colors, labels, limits):
        """Setup 3D plot with vectors"""
        ax.set_xlim(-limits, limits)
        ax.set_ylim(-limits, limits)
        ax.set_zlim(-limits, limits)
        ax.set_xlabel("X", fontsize=12, labelpad=10)
        ax.set_ylabel("Y", fontsize=12, labelpad=10)
        ax.set_zlabel("Z", fontsize=12, labelpad=10)
        
        # Add origin point
        ax.scatter([0], [0], [0], color='black', s=100, alpha=0.8, label='Origin')
        
        # Plot vectors
        offset = limits * 0.05
        for vec, color, label in zip(vectors, colors, labels):
            if np.linalg.norm(vec) > 1e-10:
                ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], 
                         color=color, linewidth=2.5, arrow_length_ratio=0.15,
                         label=label, alpha=0.8)
                
                # Add text label at vector tip
                ax.text(vec[0] + offset, vec[1] + offset, vec[2] + offset,
                       f"{label}\n({vec[0]:.2f}, {vec[1]:.2f}, {vec[2]:.2f})",
                       color=color, fontsize=9, weight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))
        
        # Set better viewing angle
        ax.view_init(elev=20, azim=45)
    
    @staticmethod
    def setup_2d_plot(ax, vectors, colors, labels, limits):
        """Setup 2D plot with vectors"""
        ax.set_xlim(-limits, limits)
        ax.set_ylim(-limits, limits)
        ax.set_xlabel("X", fontsize=12)
        ax.set_ylabel("Y", fontsize=12)
        ax.set_aspect('equal')
        
        # Add origin point
        ax.scatter([0], [0], color='black', s=100, alpha=0.8, label='Origin', zorder=5)
        
        # Add coordinate axes
        ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
        ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
        
        # Plot vectors
        offset = limits * 0.05
        for vec, color, label in zip(vectors, colors, labels):
            if np.linalg.norm(vec[:2]) > 1e-10:
                ax.quiver(0, 0, vec[0], vec[1], angles='xy', scale_units='xy', 
                         scale=1, color=color, linewidth=2.5, width=0.008,
                         label=label, alpha=0.8, zorder=3)
                
                # Add text label at vector tip
                ax.text(vec[0] + offset, vec[1] + offset,
                       f"{label}\n({vec[0]:.2f}, {vec[1]:.2f})",
                       color=color, fontsize=9, weight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))
    
    @staticmethod
    def clear_plot(tab):
        """Clear previous plot elements"""
        for attr in ['canvas_widget', 'toolbar', 'plot_frame', 'plot_container']:
            if hasattr(tab, attr):
                widget = getattr(tab, attr)
                if widget and hasattr(widget, 'destroy'):
                    try:
                        widget.destroy()
                    except:
                        pass

class FormulaRenderer:
    """Handles LaTeX formula rendering"""
    @staticmethod
    def render(parent_frame, latex_text, fontsize=12):
        """Render LaTeX formula in a frame"""
        lines = max(1, latex_text.count("\n") + 1)
        height = min(3.0, 1.2 + 0.3 * (lines - 1))
        
        fig = plt.figure(figsize=(10, height), facecolor='#f0f8ff', dpi=80)
        ax = fig.add_subplot(111)
        ax.axis("off")
        ax.text(0.02, 0.5, latex_text, fontsize=fontsize, va='center', ha='left',
               color=SOLUTION_BLUE, weight='bold', transform=ax.transAxes)
        plt.tight_layout(pad=0.5)
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=6)
        return canvas

# ------------- Lesson Classes -------------

class VectorBasicsLesson:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_ui()
    
    def create_ui(self):
        # Title
        title = tk.Label(self.parent, text="Vector Basics - Visualization & Magnitude",
                        font=("Arial", 16, "bold"), bg="white", fg=BORDER_COLOR)
        title.pack(pady=(10, 20))
        
        # Input frame
        input_frame = tk.Frame(self.parent, bg=BUTTON_BG, bd=2, relief="raised")
        input_frame.pack(pady=10, padx=20)
        
        self.vector_input = VectorInput(input_frame, "Enter Vector", 
                                       default_values=(3, 4, 2), bg=BUTTON_BG)
        self.vector_input.pack(pady=10, padx=10)
        
        # Buttons frame
        btn_frame = tk.Frame(input_frame, bg=BUTTON_BG)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📊 Plot Vector", command=self.plot,
                 bg="#1a5490", fg="white", font=("Arial", 11, "bold"),
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Reset", command=self.reset,
                 bg="#7f8c8d", fg="white", font=("Arial", 11),
                 cursor="hand2", padx=15, pady=8).pack(side="left", padx=5)
        
        # Info text
        info = tk.Label(self.parent, 
                       text="💡 Tip: Enter X, Y, and Z components to visualize a vector in 3D space",
                       font=("Arial", 10, "italic"), bg="white", fg="#666")
        info.pack(pady=10)
    
    def plot(self):
        vec = self.vector_input.get_vector()
        PlotManager.plot_vectors(self.parent, [vec], [PRIMARY_BLUE], ["V"], 
                                "Vector Visualization", show_toolbar=True)
        
        # Calculate and display info
        mag = np.linalg.norm(vec)
        self.show_info(vec, mag)
    
    def show_info(self, vec, mag):
        # Clear previous info
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        
        # Create info panel
        self.info_frame = tk.Frame(self.parent, bg="#f5f5f5", bd=2, relief="groove")
        self.info_frame.pack(fill="x", padx=20, pady=20)
        
        # Title
        tk.Label(self.info_frame, text="📐 Vector Analysis",
                font=("Arial", 13, "bold"), bg="#f5f5f5", fg=BORDER_COLOR).pack(pady=10)
        
        # Components
        comp_frame = tk.Frame(self.info_frame, bg="white", bd=1, relief="solid")
        comp_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(comp_frame, text=f"Components: ({vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f})",
                font=("Arial", 11), bg="white", fg=PRIMARY_BLUE).pack(pady=8)
        
        tk.Label(comp_frame, text=f"Magnitude: |V| = {mag:.4f}",
                font=("Arial", 11, "bold"), bg="white", fg=PRIMARY_GREEN).pack(pady=8)
        
        # Formula
        formula_frame = tk.Frame(self.info_frame, bg="#f0f8ff", bd=1, relief="solid")
        formula_frame.pack(fill="x", padx=20, pady=10)
        
        formula = (r"$|\vec{V}| = \sqrt{X^2 + Y^2 + Z^2}$" + "\n" +
                  r"$= \sqrt{" + f"{vec[0]:.3f}^2 + {vec[1]:.3f}^2 + {vec[2]:.3f}^2" + r"}$" + "\n" +
                  r"$= " + f"{mag:.4f}" + r"$")
        
        FormulaRenderer.render(formula_frame, formula, fontsize=13)
    
    def reset(self):
        self.vector_input.reset()
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        PlotManager.clear_plot(self.parent)

class VectorAddSubLesson:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_ui()
    
    def create_ui(self):
        # Title
        title = tk.Label(self.parent, text="Vector Addition & Subtraction",
                        font=("Arial", 16, "bold"), bg="white", fg=BORDER_COLOR)
        title.pack(pady=(10, 20))
        
        # Input frame
        input_frame = tk.Frame(self.parent, bg=BUTTON_BG, bd=2, relief="raised")
        input_frame.pack(pady=10, padx=20)
        
        self.vector_a = VectorInput(input_frame, "Vector A", 
                                   default_values=(3, 2, 1), bg=BUTTON_BG)
        self.vector_a.pack(pady=5, padx=10)
        
        self.vector_b = VectorInput(input_frame, "Vector B",
                                   default_values=(1, 3, -1), bg=BUTTON_BG)
        self.vector_b.pack(pady=5, padx=10)
        
        # Operation selection
        op_frame = tk.Frame(input_frame, bg=BUTTON_BG)
        op_frame.pack(pady=10)
        
        tk.Label(op_frame, text="Operation:", bg=BUTTON_BG, fg="white",
                font=("Arial", 11)).pack(side="left", padx=5)
        
        self.op_var = tk.StringVar(value="Add")
        for op in ["Add", "Subtract"]:
            tk.Radiobutton(op_frame, text=op, variable=self.op_var, value=op,
                          bg=BUTTON_BG, fg="white", selectcolor=BUTTON_BG,
                          font=("Arial", 10), cursor="hand2").pack(side="left", padx=10)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg=BUTTON_BG)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📊 Compute & Plot", command=self.compute,
                 bg="#1a5490", fg="white", font=("Arial", 11, "bold"),
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Reset", command=self.reset,
                 bg="#7f8c8d", fg="white", font=("Arial", 11),
                 cursor="hand2", padx=15, pady=8).pack(side="left", padx=5)
    
    def compute(self):
        vec_a = self.vector_a.get_vector()
        vec_b = self.vector_b.get_vector()
        op = self.op_var.get()
        
        result = vec_a + vec_b if op == "Add" else vec_a - vec_b
        
        PlotManager.plot_vectors(self.parent, [vec_a, vec_b, result],
                                [PRIMARY_BLUE, PRIMARY_RED, PRIMARY_GREEN],
                                ["A", "B", "Result"],
                                f"Vector {op}ition", limits=12)
        
        self.show_info(vec_a, vec_b, result, op)
    
    def show_info(self, vec_a, vec_b, result, op):
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        
        self.info_frame = tk.Frame(self.parent, bg="#f5f5f5", bd=2, relief="groove")
        self.info_frame.pack(fill="x", padx=20, pady=20)
        
        sign = '+' if op == "Add" else '-'
        
        # Title
        tk.Label(self.info_frame, text=f"📐 {op}ition Result",
                font=("Arial", 13, "bold"), bg="#f5f5f5", fg=BORDER_COLOR).pack(pady=10)
        
        # Result
        res_frame = tk.Frame(self.info_frame, bg="white", bd=1, relief="solid")
        res_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(res_frame, text=f"A = ({vec_a[0]:.3f}, {vec_a[1]:.3f}, {vec_a[2]:.3f})",
                font=("Arial", 10), bg="white", fg=PRIMARY_BLUE).pack(pady=3)
        tk.Label(res_frame, text=f"B = ({vec_b[0]:.3f}, {vec_b[1]:.3f}, {vec_b[2]:.3f})",
                font=("Arial", 10), bg="white", fg=PRIMARY_RED).pack(pady=3)
        tk.Label(res_frame, text=f"Result = ({result[0]:.3f}, {result[1]:.3f}, {result[2]:.3f})",
                font=("Arial", 11, "bold"), bg="white", fg=PRIMARY_GREEN).pack(pady=5)
        
        # Formula
        formula_frame = tk.Frame(self.info_frame, bg="#f0f8ff", bd=1, relief="solid")
        formula_frame.pack(fill="x", padx=20, pady=10)
        
        formula = (r"$\vec{R} = \vec{A} " + (r"+ \vec{B}$" if op == "Add" else r"- \vec{B}$") + "\n" +
                  r"$R_x = " + f"{vec_a[0]:.2f} {sign} {vec_b[0]:.2f} = {result[0]:.2f}$" + "\n" +
                  r"$R_y = " + f"{vec_a[1]:.2f} {sign} {vec_b[1]:.2f} = {result[1]:.2f}$" + "\n" +
                  r"$R_z = " + f"{vec_a[2]:.2f} {sign} {vec_b[2]:.2f} = {result[2]:.2f}$")
        
        FormulaRenderer.render(formula_frame, formula, fontsize=12)
    
    def reset(self):
        self.vector_a.reset()
        self.vector_b.reset()
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        PlotManager.clear_plot(self.parent)

class VectorScalingLesson:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_ui()
    
    def create_ui(self):
        # Title
        title = tk.Label(self.parent, text="Vector Scaling (Scalar Multiplication)",
                        font=("Arial", 16, "bold"), bg="white", fg=BORDER_COLOR)
        title.pack(pady=(10, 20))
        
        # Input frame
        input_frame = tk.Frame(self.parent, bg=BUTTON_BG, bd=2, relief="raised")
        input_frame.pack(pady=10, padx=20)
        
        self.vector_input = VectorInput(input_frame, "Vector V",
                                       default_values=(2, 3, 1), bg=BUTTON_BG)
        self.vector_input.pack(pady=5, padx=10)
        
                # Scalar input
        scalar_frame = tk.Frame(input_frame, bg=BUTTON_BG)
        scalar_frame.pack(pady=10)
        
        tk.Label(scalar_frame, text="Scalar (k):", bg=BUTTON_BG, fg="white",
                 font=("Arial", 11)).pack(side="left", padx=5)
        self.scalar_entry = tk.Entry(scalar_frame, width=8, font=("Arial", 10),
                                     bg=ENTRY_BG, relief="solid", bd=1)
        self.scalar_entry.insert(0, "2")
        self.scalar_entry.pack(side="left", padx=5)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg=BUTTON_BG)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📊 Compute & Plot", command=self.compute,
                 bg="#1a5490", fg="white", font=("Arial", 11, "bold"),
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Reset", command=self.reset,
                 bg="#7f8c8d", fg="white", font=("Arial", 11),
                 cursor="hand2", padx=15, pady=8).pack(side="left", padx=5)
    
    def compute(self):
        vec = self.vector_input.get_vector()
        try:
            k = float(self.scalar_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid scalar.")
            return
        
        scaled_vec = k * vec
        
        PlotManager.plot_vectors(self.parent, [vec, scaled_vec],
                                [PRIMARY_BLUE, PRIMARY_GREEN],
                                ["V", f"{k}·V"], f"Vector Scaling (k={k})", limits=12)
        
        self.show_info(vec, k, scaled_vec)
    
    def show_info(self, vec, k, scaled_vec):
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        
        self.info_frame = tk.Frame(self.parent, bg="#f5f5f5", bd=2, relief="groove")
        self.info_frame.pack(fill="x", padx=20, pady=20)
        
        # Title
        tk.Label(self.info_frame, text="📐 Scalar Multiplication Result",
                font=("Arial", 13, "bold"), bg="#f5f5f5", fg=BORDER_COLOR).pack(pady=10)
        
        # Result
        res_frame = tk.Frame(self.info_frame, bg="white", bd=1, relief="solid")
        res_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(res_frame, text=f"Original Vector V = ({vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f})",
                font=("Arial", 10), bg="white", fg=PRIMARY_BLUE).pack(pady=3)
        tk.Label(res_frame, text=f"Scalar k = {k}", font=("Arial", 10), bg="white", fg=PRIMARY_RED).pack(pady=3)
        tk.Label(res_frame, text=f"Scaled Vector k·V = ({scaled_vec[0]:.3f}, {scaled_vec[1]:.3f}, {scaled_vec[2]:.3f})",
                font=("Arial", 11, "bold"), bg="white", fg=PRIMARY_GREEN).pack(pady=5)
        
        # Formula
        formula_frame = tk.Frame(self.info_frame, bg="#f0f8ff", bd=1, relief="solid")
        formula_frame.pack(fill="x", padx=20, pady=10)
        
        formula = (r"$k \cdot \vec{V} = k \cdot (X, Y, Z)$" + "\n" +
                  r"$= (" + f"{k}·{vec[0]:.2f}, {k}·{vec[1]:.2f}, {k}·{vec[2]:.2f}" + r")$" + "\n" +
                  r"$= (" + f"{scaled_vec[0]:.2f}, {scaled_vec[1]:.2f}, {scaled_vec[2]:.2f}" + r")$")
        
        FormulaRenderer.render(formula_frame, formula, fontsize=12)
    
    def reset(self):
        self.vector_input.reset()
        self.scalar_entry.delete(0, tk.END)
        self.scalar_entry.insert(0, "1")
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        PlotManager.clear_plot(self.parent)

class VectorMagnitudeLesson:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_ui()
    
    def create_ui(self):
        # Title
        title = tk.Label(self.parent, text="Vector Magnitude & Direction",
                        font=("Arial", 16, "bold"), bg="white", fg=BORDER_COLOR)
        title.pack(pady=(10, 20))
        
        # Input frame
        input_frame = tk.Frame(self.parent, bg=BUTTON_BG, bd=2, relief="raised")
        input_frame.pack(pady=10, padx=20)
        
        self.vector_input = VectorInput(input_frame, "Vector V",
                                       default_values=(3, 4, 5), bg=BUTTON_BG)
        self.vector_input.pack(pady=10, padx=10)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg=BUTTON_BG)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📊 Compute Magnitude & Direction", command=self.compute,
                 bg="#1a5490", fg="white", font=("Arial", 11, "bold"),
                 cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🔄 Reset", command=self.reset,
                 bg="#7f8c8d", fg="white", font=("Arial", 11),
                 cursor="hand2", padx=15, pady=8).pack(side="left", padx=5)
    
    def compute(self):
        vec = self.vector_input.get_vector()
        mag = np.linalg.norm(vec)
        if mag > 1e-10:
            direction = vec / mag
        else:
            direction = np.zeros_like(vec)
        
        PlotManager.plot_vectors(self.parent, [vec], [PRIMARY_BLUE], ["V"], "Vector Magnitude & Direction", limits=12)
        self.show_info(vec, mag, direction)
    
    def show_info(self, vec, mag, direction):
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        
        self.info_frame = tk.Frame(self.parent, bg="#f5f5f5", bd=2, relief="groove")
        self.info_frame.pack(fill="x", padx=20, pady=20)
        
        # Title
        tk.Label(self.info_frame, text="📐 Vector Analysis",
                font=("Arial", 13, "bold"), bg="#f5f5f5", fg=BORDER_COLOR).pack(pady=10)
        
        # Result
        res_frame = tk.Frame(self.info_frame, bg="white", bd=1, relief="solid")
        res_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(res_frame, text=f"Vector V = ({vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f})",
                font=("Arial", 10), bg="white", fg=PRIMARY_BLUE).pack(pady=3)
        tk.Label(res_frame, text=f"Magnitude |V| = {mag:.4f}",
                font=("Arial", 11, "bold"), bg="white", fg=PRIMARY_GREEN).pack(pady=3)
        tk.Label(res_frame, text=f"Direction = ({direction[0]:.3f}, {direction[1]:.3f}, {direction[2]:.3f})",
                font=("Arial", 10), bg="white", fg=PRIMARY_RED).pack(pady=3)
        
        # Formula
        formula_frame = tk.Frame(self.info_frame, bg="#f0f8ff", bd=1, relief="solid")
        formula_frame.pack(fill="x", padx=20, pady=10)
        
        formula = (r"$|\vec{V}| = \sqrt{X^2 + Y^2 + Z^2} = " + f"{mag:.4f}$\n" +
                   r"$\hat{V} = \frac{\vec{V}}{|\vec{V}|} = (" +
                   f"{direction[0]:.3f}, {direction[1]:.3f}, {direction[2]:.3f})$")
        
        FormulaRenderer.render(formula_frame, formula, fontsize=12)
    
    def reset(self):
        self.vector_input.reset()
        if hasattr(self, 'info_frame'):
            self.info_frame.destroy()
        PlotManager.clear_plot(self.parent)

# ------------- Run App -------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VectorLearningApp(root)
    root.mainloop()
