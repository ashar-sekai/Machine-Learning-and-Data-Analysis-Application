import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, ttest_1samp
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import IsolationForest
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import matplotlib


plt.style.use('dark_background')
matplotlib.rcParams['axes.facecolor'] = '#1e1e1e'
matplotlib.rcParams['figure.facecolor'] = '#1e1e1e'
matplotlib.rcParams['axes.edgecolor'] = '#a855f7'
matplotlib.rcParams['text.color'] = 'white'
matplotlib.rcParams['axes.labelcolor'] = '#a855f7'
matplotlib.rcParams['xtick.color'] = '#a855f7'
matplotlib.rcParams['ytick.color'] = '#a855f7'

dataframe = None  


def plot_histogram(dataframe, column):
    """Interactive histogram with Desmos-like zoom/pan and animated bars/KDE."""
    try:
        
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title(f"Histogram: {column} (Drag to Pan | Scroll to Zoom)")
        
        
        data = dataframe[column].dropna()
        if len(data) == 0:
            plt.close()
            raise ValueError("No valid data to plot")

        
        bin_edges = np.histogram_bin_edges(data, bins='auto')
        hist_vals, _ = np.histogram(data, bins=bin_edges)
        bin_count = len(bin_edges) - 1
        xlim_original = (bin_edges[0], bin_edges[-1])
        ylim_original = (0, max(hist_vals) * 1.1)

        
        bars = ax.bar(bin_edges[:-1], [0]*bin_count, 
                     width=np.diff(bin_edges), 
                     align='edge',
                     color='#a855f7',
                     edgecolor='white',
                     alpha=0.7)
        line, = ax.plot([], [], color='#f472b6', linewidth=2, alpha=0)

        
        ax.set_title(f"Distribution of {column}\n(Pan: Left-click+Drag | Zoom: Scroll | Reset: Right-click)", 
                    color='white', pad=20)
        ax.set_xlabel(column, color='#a855f7')
        ax.set_ylabel("Frequency", color='#a855f7')
        ax.grid(True, alpha=0.2, color='#a855f7')
        ax.set_xlim(*xlim_original)
        ax.set_ylim(*ylim_original)

        
        class ZoomPan:
            def __init__(self):
                self.press = None
                self.zoom_factor = 1.2
            
            def on_press(self, event):
                if event.button == 1:  # Left mouse button
                    self.press = (event.xdata, event.ydata)
            
            def on_motion(self, event):
                if self.press is None: return
                xpress, ypress = self.press
                dx = event.xdata - xpress
                dy = event.ydata - ypress
                ax.set_xlim(ax.get_xlim() - dx)
                ax.set_ylim(ax.get_ylim() - dy)
                fig.canvas.draw()
                self.press = (event.xdata, event.ydata)
            
            def on_release(self, event):
                self.press = None
            
            def on_scroll(self, event):
                zoom_factor = self.zoom_factor if event.button == 'up' else 1/self.zoom_factor
                x, y = event.xdata, event.ydata
                
                if x is None or y is None: 
                    x = np.mean(ax.get_xlim())
                    y = np.mean(ax.get_ylim())
                
                
                ax.set_xlim([x - (x - ax.get_xlim()[0]) * zoom_factor,
                             x + (ax.get_xlim()[1] - x) * zoom_factor])
                ax.set_ylim([y - (y - ax.get_ylim()[0]) * zoom_factor,
                             y + (ax.get_ylim()[1] - y) * zoom_factor])
                fig.canvas.draw()
            
            def on_right_click(self, event):
                if event.button == 3:  
                    ax.set_xlim(*xlim_original)
                    ax.set_ylim(*ylim_original)
                    fig.canvas.draw()

        
        zp = ZoomPan()
        fig.canvas.mpl_connect('button_press_event', zp.on_press)
        fig.canvas.mpl_connect('motion_notify_event', zp.on_motion)
        fig.canvas.mpl_connect('button_release_event', zp.on_release)
        fig.canvas.mpl_connect('scroll_event', zp.on_scroll)
        fig.canvas.mpl_connect('button_press_event', zp.on_right_click)

        
        def init():
            return bars.patches + [line]
        
        def update(frame):
           
            for i, bar in enumerate(bars.patches):
                progress = min(1, frame / (bin_count * 2))
                if i <= frame:
                    bar.set_height(hist_vals[i] * min(1, (frame - i) * 0.1))
            
            
            if frame > bin_count * 0.6 and len(data) > 1:
                line_progress = min(1, (frame - bin_count * 0.6) / (bin_count * 0.4))
                line.set_alpha(line_progress)
                if line_progress > 0.5 and len(line.get_data()[0]) == 0:
                    x_kde = np.linspace(min(data), max(data), 200)
                    kde = sns.kdeplot(data, ax=ax, color='#f472b6', linewidth=2)
                    y_kde = kde.get_lines()[-1].get_ydata()
                    line.set_data(x_kde, y_kde)
                    kde.get_lines()[-1].remove()
            
            return bars.patches + [line]

        
        ani = FuncAnimation(fig, update, frames=int(bin_count*2.5),
                          init_func=init, interval=50, blit=True, repeat=False)
        
        plt.tight_layout()
        plt.show()

    except Exception as e:
        if 'fig' in locals():
            plt.close(fig)
        raise RuntimeError(f"Failed to create histogram: {str(e)}")

def plot_heatmap(dataframe):
    """Fixed heatmap plotting function with limited animation"""
    try:
        corr = dataframe.select_dtypes(include=[np.number]).corr()
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.canvas.manager.set_window_title("Correlation Heatmap")
        
        
        cmap = LinearSegmentedColormap.from_list('purple_cmap', ['#1e1e1e', '#4c1d95', '#a855f7', '#f472b6'])
        
        
        animation_complete = False
        
        def update(frame):
            nonlocal animation_complete
            if animation_complete:
                return
            
            progress = min(1, frame / 30)
            current_corr = corr * progress
            mask = np.triu(np.ones_like(corr, dtype=bool)) if frame < 15 else None
            
            ax.clear()
            sns.heatmap(current_corr, mask=mask,
                       annot=True, fmt=".2f", cmap=cmap,
                       cbar=True, ax=ax, vmin=-1, vmax=1)
            ax.set_title(f"Correlation Matrix ({int(progress*100)}%)", color='white')
            
            
            if progress >= 1:
                animation_complete = True
                plt.close(fig)  
        
        ani = FuncAnimation(fig, update, frames=30, interval=50, repeat=False)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        if 'fig' in locals():
            plt.close(fig)
        raise RuntimeError(f"Failed to create heatmap: {str(e)}")

def plot_scatter(dataframe, x_col, y_col):
   
    try:
        data = dataframe[[x_col, y_col]].dropna()
        if len(data) == 0:
            raise ValueError("No valid data for scatter plot")
            
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title(f"Scatter: {x_col} vs {y_col}")
        
        
        sc = ax.scatter([], [], alpha=0.7, cmap='Purples_r')
        ax.set_xlabel(x_col, color='#a855f7')
        ax.set_ylabel(y_col, color='#a855f7')
        ax.grid(True, alpha=0.2, color='#a855f7')
        
        
        ax.set_xlim(data[x_col].min() * 0.9, data[x_col].max() * 1.1)
        ax.set_ylim(data[y_col].min() * 0.9, data[y_col].max() * 1.1)
        
        def update(frame):
            show_points = min(frame + 1, len(data))
            x = data[x_col].iloc[:show_points]
            y = data[y_col].iloc[:show_points]
            
            sc.set_offsets(np.column_stack([x, y]))
            sc.set_alpha([0.7] * show_points)
            sc.set_array(np.linspace(0, 1, show_points))
            
            ax.set_title(f"{x_col} vs {y_col} ({show_points}/{len(data)} points)", color='white')
            
            
            if show_points >= len(data):
                ani.event_source.stop()
            
            return [sc]
        
        ani = FuncAnimation(fig, update, frames=len(data), interval=50, blit=True, repeat=False)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        if 'fig' in locals():
            plt.close(fig)
        raise RuntimeError(f"Failed to create scatter plot: {str(e)}")

def launch_gui():
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_file():
        global dataframe
        file_path = filedialog.askopenfilename(
            title="Select CSV or Excel File",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    dataframe = pd.read_csv(file_path)
                elif file_path.endswith((".xlsx", ".xls")):
                    dataframe = pd.read_excel(file_path)
                else:
                    raise ValueError("Unsupported file format")
                
                display_dataframe(treeview, dataframe)
                messagebox.showinfo("Done hogaya!", "File loaded successfully bhai!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def save_csv():
        global dataframe
        if dataframe is None or dataframe.empty:
            messagebox.showerror("Error", "No data to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
            title="Save Data As..."
        )

        if file_path:
            try:
                if file_path.endswith(".csv"):
                    dataframe.to_csv(file_path, index=False)
                elif file_path.endswith((".xlsx", ".xls")):
                    dataframe.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Data saved successfully NIGGA! to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def load_saved_csv():
        global dataframe
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    dataframe = pd.read_csv(file_path)
                elif file_path.endswith((".xlsx", ".xls")):
                    dataframe = pd.read_excel(file_path)
                display_dataframe(treeview, dataframe)
                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def display_dataframe(tree, df):
        tree.delete(*tree.get_children())
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        
        
        for col in df.columns:
            tree.heading(col, text=col)
            max_width = max(
                df[col].astype(str).apply(len).max(),  # Content width
                len(str(col)) * 8  # Header width
            )
            tree.column(col, width=min(200, max_width + 10), anchor='center')
            
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    def show_datatypes():
        if dataframe is not None:
            top = tk.Toplevel()
            top.title("Data Types Information")
            top.geometry("600x400")
            
            frame = ttk.Frame(top)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = ttk.Treeview(frame, columns=("Column", "Data Type", "Non-Null Count"), 
                              yscrollcommand=scrollbar.set, show='headings')
            
            tree.heading("Column", text="Column")
            tree.heading("Data Type", text="Data Type")
            tree.heading("Non-Null Count", text="Non-Null Count")
            
            for col in dataframe.columns:
                tree.insert("", tk.END, values=(
                    col, 
                    str(dataframe[col].dtype),
                    dataframe[col].count() 
                ))
            
            tree.pack(fill='both', expand=True)
            scrollbar.config(command=tree.yview)

    def show_missing_values():
        if dataframe is not None:
            missing = dataframe.isnull().sum()
            total = len(dataframe)
            missing_pct = (missing / total) * 100
            
            top = tk.Toplevel()
            top.title("Missing Values Analysis")
            top.geometry("600x400")
            
            frame = ttk.Frame(top)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = ttk.Treeview(frame, columns=("Column", "Missing Count", "Percentage"), 
                              yscrollcommand=scrollbar.set, show='headings')
            
            tree.heading("Column", text="Column")
            tree.heading("Missing Count", text="Missing Count")
            tree.heading("Percentage", text="Percentage (%)")
            
            for col in missing.index:
                if missing[col] > 0:
                    tree.insert("", tk.END, values=(
                        col, 
                        missing[col],
                        f"{missing_pct[col]:.2f}%"
                    ))
            
            if len(tree.get_children()) == 0:
                tree.insert("", tk.END, values=("No missing values found", "", ""))
            
            tree.pack(fill='both', expand=True)
            scrollbar.config(command=tree.yview)

    def show_standard_deviation_outliers():
        if dataframe is not None:
            numeric_df = dataframe.select_dtypes(include=[np.number])
            if numeric_df.empty:
                messagebox.showwarning("No Numeric Columns", "No numeric columns to analyze")
                return
                
            outliers = {}
            for col in numeric_df.columns:
                mean, std = numeric_df[col].mean(), numeric_df[col].std()
                if std > 0: 
                    count = numeric_df[(numeric_df[col] < mean - 3 * std) | (numeric_df[col] > mean + 3 * std)].shape[0]
                    outliers[col] = count
                else:
                    outliers[col] = 0
            
            top = tk.Toplevel()
            top.title("Outlier Detection (3σ)")
            top.geometry("500x300")
            
            frame = ttk.Frame(top)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = ttk.Treeview(frame, columns=("Column", "# Outliers"), 
                              yscrollcommand=scrollbar.set, show='headings')
            
            tree.heading("Column", text="Column")
            tree.heading("# Outliers", text="# Outliers (3σ)")
            
            for col in outliers:
                tree.insert("", tk.END, values=(col, outliers[col]))
            
            tree.pack(fill='both', expand=True)
            scrollbar.config(command=tree.yview)

    def show_skew_kurtosis():
        if dataframe is not None:
            numeric_df = dataframe.select_dtypes(include=[np.number])
            if numeric_df.empty:
                messagebox.showwarning("No Numeric Columns", "No numeric columns to analyze")
                return
                
            skewness = numeric_df.apply(skew)
            kurt_vals = numeric_df.apply(kurtosis)
            
            top = tk.Toplevel()
            top.title("Distribution Statistics")
            top.geometry("600x400")
            
            frame = ttk.Frame(top)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')
            
            tree = ttk.Treeview(frame, columns=("Column", "Skewness", "Kurtosis"), 
                              yscrollcommand=scrollbar.set, show='headings')
            
            tree.heading("Column", text="Column")
            tree.heading("Skewness", text="Skewness")
            tree.heading("Kurtosis", text="Kurtosis")
            
            for col in numeric_df.columns:
                tree.insert("", tk.END, values=(
                    col, 
                    f"{skewness[col]:.4f}",
                    f"{kurt_vals[col]:.4f}"
                ))
            
            tree.pack(fill='both', expand=True)
            scrollbar.config(command=tree.yview)

    def show_correlation_matrix():
        if dataframe is not None:
            numeric_df = dataframe.select_dtypes(include=[np.number])
            if numeric_df.empty:
                messagebox.showwarning("No Numeric Columns", "No numeric columns to correlate")
                return
                
            try:
                corr = numeric_df.corr()
                plt.figure(figsize=(12, 10))
                sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", 
                           center=0, vmin=-1, vmax=1, linewidths=0.5)
                plt.title("Feature Correlation Matrix", pad=20)
                plt.xticks(rotation=45, ha='right')
                plt.yticks(rotation=0)
                plt.tight_layout()
                plt.show()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create correlation matrix:\n{str(e)}")

    def show_histogram():
        if dataframe is not None:
            numeric_cols = dataframe.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_cols:
                messagebox.showwarning("No Numeric Columns", "No numeric columns available for histogram")
                return
                
            
            if len(numeric_cols) > 1:
                col = select_column_dialog(numeric_cols, "Select column for histogram")
                if col is None:
                    return
            else:
                col = numeric_cols[0]
                
            try:
                plot_histogram(dataframe, col)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create histogram:\n{str(e)}")

    def show_heatmap():
        if dataframe is not None:
            numeric_df = dataframe.select_dtypes(include=[np.number])
            if numeric_df.empty:
                messagebox.showwarning("No Numeric Columns", "No numeric columns available for heatmap")
                return
                
            try:
                plot_heatmap(dataframe)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create heatmap:\n{str(e)}")

    def show_scatter():
        if dataframe is not None:
            numeric_cols = dataframe.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) < 2:
                messagebox.showwarning("Insufficient Columns", "Need at least 2 numeric columns for scatter plot")
                return
                
           
            cols = select_columns_dialog(numeric_cols, 2, "Select columns for scatter plot")
            if cols is None or len(cols) != 2:
                return
                
            try:
                plot_scatter(dataframe, cols[0], cols[1])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create scatter plot:\n{str(e)}")

    def select_column_dialog(columns, title):
        top = tk.Toplevel()
        top.title(title)
        top.geometry("300x200")
        
        selected = tk.StringVar(value=columns[0])
        
        label = ttk.Label(top, text="Select column:")
        label.pack(pady=10)
        
        listbox = tk.Listbox(top, selectmode=tk.SINGLE)
        for col in columns:
            listbox.insert(tk.END, col)
        listbox.pack(fill='both', expand=True, padx=10, pady=5)
        listbox.selection_set(0)
        
        def on_select():
            selected.set(listbox.get(listbox.curselection()))
            top.destroy()
            
        def on_cancel():
            selected.set(None)
            top.destroy()
            
        button_frame = ttk.Frame(top)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Select", command=on_select).pack(side='left', expand=True)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side='left', expand=True)
        
        top.wait_window()
        return selected.get()

    def select_columns_dialog(columns, num_required, title):
        top = tk.Toplevel()
        top.title(title)
        top.geometry("400x300")
        
        selected = []
        
        label = ttk.Label(top, text=f"Select {num_required} columns:")
        label.pack(pady=10)
        
        listbox = tk.Listbox(top, selectmode=tk.MULTIPLE)
        for col in columns:
            listbox.insert(tk.END, col)
        listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        def on_select():
            selected.extend([listbox.get(i) for i in listbox.curselection()])
            if len(selected) != num_required:
                messagebox.showwarning("Selection Error", 
                                     f"Please select exactly {num_required} columns")
                selected.clear()
                return
            top.destroy()
            
        def on_cancel():
            selected.clear()
            top.destroy()
            
        button_frame = ttk.Frame(top)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Select", command=on_select).pack(side='left', expand=True)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side='left', expand=True)
        
        top.wait_window()
        return selected if len(selected) == num_required else None

    def train_model():
        global dataframe
        if dataframe is None or 'is_anomaly' not in dataframe.columns:
            messagebox.showerror("Error", "Please load data with 'is_anomaly' label column")
            return
            
        try:
            X = dataframe.drop(columns=["is_anomaly"]).select_dtypes(include=["number"])
            y = dataframe["is_anomaly"]
            
            if len(X.columns) == 0:
                messagebox.showerror("Error", "No numeric features available for training")
                return
                
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)
            
            train_acc = accuracy_score(y_train, model.predict(X_train))
            test_acc = accuracy_score(y_test, model.predict(X_test))
            
            messagebox.showinfo("Model Results", 
                              f"Training Accuracy: {train_acc:.2%}\n"
                              f"Test Accuracy: {test_acc:.2%}")
        except Exception as e:
            messagebox.showerror("Error", f"Model training failed:\n{str(e)}")

    def run_unsupervised_model():
        global dataframe
        if dataframe is None:
            messagebox.showerror("Error", "Please load data first")
            return
            
        try:
            X = dataframe.select_dtypes(include=["number"])
            if len(X.columns) == 0:
                messagebox.showerror("Error", "No numeric columns available for analysis")
                return
                
            model = IsolationForest(contamination=0.1, random_state=42)
            preds = model.fit_predict(X)
            
            if "unsupervised_anomaly" in dataframe.columns:
                dataframe = dataframe.drop(columns=["unsupervised_anomaly"])
                
            dataframe["unsupervised_anomaly"] = (preds == -1).astype(int)
            display_dataframe(treeview, dataframe)
            
            anomaly_count = (preds == -1).sum()
            messagebox.showinfo("Results", 
                              f"Anomaly detection complete\n"
                              f"Found {anomaly_count} anomalies ({anomaly_count/len(dataframe):.2%})")
        except Exception as e:
            messagebox.showerror("Error", f"Anomaly detection failed:\n{str(e)}")

    def gui_train_model():
        global dataframe
        if dataframe is None or 'is_anomaly' not in dataframe.columns:
            messagebox.showerror("Error", "Please load data with 'is_anomaly' label column")
            return
            
        try:
            X = dataframe.drop(columns=["is_anomaly"]).select_dtypes(include=["number"])
            y = dataframe["is_anomaly"]
            
            if len(X.columns) == 0:
                messagebox.showerror("Error", "No numeric features available for training")
                return
                
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = train_supervised_model(X_train, y_train)
            
            train_acc = accuracy_score(y_train, model.predict(X_train))
            test_acc = accuracy_score(y_test, model.predict(X_test))
            
            messagebox.showinfo("Model Results", 
                              f"Training Accuracy: {train_acc:.2%}\n"
                              f"Test Accuracy: {test_acc:.2%}")
        except Exception as e:
            messagebox.showerror("Error", f"Model training failed:\n{str(e)}")
            
    def show_basic_statistics():
        if dataframe is not None:
            numeric_df = dataframe.select_dtypes(include=[np.number])
            if numeric_df.empty:
                messagebox.showwarning("No Numeric Columns", "No numeric columns to analyze")
                return
                
            stats = pd.DataFrame({
                'Mean': numeric_df.mean(),
                'Median': numeric_df.median(),
                'Mode': numeric_df.mode().iloc[0],
                'Std Dev': numeric_df.std(),
                'Variance': numeric_df.var(),
                'Min': numeric_df.min(),
                'Max': numeric_df.max(),
                'Range': numeric_df.max() - numeric_df.min(),
                'IQR': numeric_df.quantile(0.75) - numeric_df.quantile(0.25)
            }).transpose()
            
            top = tk.Toplevel()
            top.title("Descriptive Statistics")
            top.geometry("800x500")
            
            frame = ttk.Frame(top)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            scroll_x = ttk.Scrollbar(frame, orient='horizontal')
            scroll_y = ttk.Scrollbar(frame)
            
            tree = ttk.Treeview(frame, 
                              columns=["Statistic"] + list(numeric_df.columns),
                              xscrollcommand=scroll_x.set,
                              yscrollcommand=scroll_y.set,
                              show='headings')
            
            tree.heading("Statistic", text="Statistic")
            for col in numeric_df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='center')
            
            for stat in stats.index:
                values = [f"{x:.4f}" if isinstance(x, (float, np.floating)) else str(x) 
                         for x in stats.loc[stat]]
                tree.insert("", tk.END, values=[stat] + values)
            
            scroll_x.config(command=tree.xview)
            scroll_y.config(command=tree.yview)
            
            scroll_x.pack(side='bottom', fill='x')
            scroll_y.pack(side='right', fill='y')
            tree.pack(fill='both', expand=True)

    def show_significance_tests():
        if dataframe is not None:
            numeric_df = dataframe.select_dtypes(include=[np.number])
            if numeric_df.empty:
                messagebox.showwarning("No Numeric Columns", "No numeric columns to analyze")
                return
                
            results = []
            for col in numeric_df.columns:
                col_data = numeric_df[col].dropna()
                if len(col_data) > 1:
                    t_stat, p_val = ttest_1samp(col_data, 0)
                    results.append({
                        'Column': col,
                        'T-statistic': t_stat,
                        'P-value': p_val,
                        'Significant (p<0.05)': p_val < 0.05
                    })
            
            if not results:
                messagebox.showwarning("No Valid Tests", "No columns with sufficient data for testing")
                return
                
            results_df = pd.DataFrame(results)
            
            top = tk.Toplevel()
            top.title("Statistical Significance Tests")
            top.geometry("700x400")
            
            frame = ttk.Frame(top)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            scroll_y = ttk.Scrollbar(frame)
            tree = ttk.Treeview(frame, columns=list(results_df.columns),
                              yscrollcommand=scroll_y.set,
                              show='headings')
            
            for col in results_df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')
            
            for _, row in results_df.iterrows():
                tree.insert("", tk.END, values=[
                    row['Column'],
                    f"{row['T-statistic']:.4f}",
                    f"{row['P-value']:.4f}",
                    "Yes" if row['Significant (p<0.05)'] else "No"
                ])
            
            scroll_y.config(command=tree.yview)
            scroll_y.pack(side='right', fill='y')
            tree.pack(fill='both', expand=True)

    
    root = tk.Tk()
    root.title("Advanced Data Analysis Dashboard")
    root.geometry("1000x700")
    center_window(root)
    
    
    root.tk_setPalette(background='#1e1e1e', foreground='white',
                      activeBackground='#4c1d95', activeForeground='white')
    
    style = ttk.Style()
    style.theme_use('clam')
    
    
    style.configure('.', background='#1e1e1e', foreground='white')
    style.configure('TFrame', background='#1e1e1e')
    style.configure('TLabel', background='#1e1e1e', foreground='white')
    style.configure('TButton', background='#4c1d95', foreground='white',
                  borderwidth=1, focusthickness=3, focuscolor='none')
    style.map('TButton', background=[('active', '#a855f7')])
    style.configure('Treeview', background='#2d2d2d', fieldbackground='#2d2d2d',
                  foreground='white', rowheight=25)
    style.configure('Treeview.Heading', background='#4c1d95', foreground='white')
    style.map('Treeview', background=[('selected', '#a855f7')])
    style.configure('TLabelframe', background='#1e1e1e', foreground='white')
    style.configure('TLabelframe.Label', background='#1e1e1e', foreground='#a855f7')
    style.configure('TScrollbar', background='#4c1d95')
    
    
    control_frame = ttk.Frame(root, padding="10")
    control_frame.pack(fill='x')
    
    display_frame = ttk.Frame(root)
    display_frame.pack(fill='both', expand=True, padx=10, pady=5)
    
    
    data_btn_frame = ttk.LabelFrame(control_frame, text="Data Operations", padding=10)
    data_btn_frame.pack(side='left', fill='y', padx=5)
    
    ttk.Button(data_btn_frame, text="📁 Load Dataset", command=load_file).pack(fill='x', pady=2)
    ttk.Button(data_btn_frame, text="📂 Load Saved File", command=load_saved_csv).pack(fill='x', pady=2)
    ttk.Button(data_btn_frame, text="💾 Save Current Data", command=save_csv).pack(fill='x', pady=2)
    
    
    analysis_btn_frame = ttk.LabelFrame(control_frame, text="Data Analysis", padding=10)
    analysis_btn_frame.pack(side='left', fill='y', padx=5)
    
    ttk.Button(analysis_btn_frame, text="Data Types", command=show_datatypes).pack(fill='x', pady=2)
    ttk.Button(analysis_btn_frame, text="Missing Values", command=show_missing_values).pack(fill='x', pady=2)
    ttk.Button(analysis_btn_frame, text="Basic Statistics", command=show_basic_statistics).pack(fill='x', pady=2)
    ttk.Button(analysis_btn_frame, text="Significance Tests", command=show_significance_tests).pack(fill='x', pady=2)
    ttk.Button(analysis_btn_frame, text="Outlier Detection", command=show_standard_deviation_outliers).pack(fill='x', pady=2)
    ttk.Button(analysis_btn_frame, text="Skewness & Kurtosis", command=show_skew_kurtosis).pack(fill='x', pady=2)
    
    
    viz_btn_frame = ttk.LabelFrame(control_frame, text="Visualizations", padding=10)
    viz_btn_frame.pack(side='left', fill='y', padx=5)
    
    ttk.Button(viz_btn_frame, text="Histogram", command=show_histogram).pack(fill='x', pady=2)
    ttk.Button(viz_btn_frame, text="Heatmap", command=show_heatmap).pack(fill='x', pady=2)
    ttk.Button(viz_btn_frame, text="Scatter Plot", command=show_scatter).pack(fill='x', pady=2)
    ttk.Button(viz_btn_frame, text="Correlation Matrix", command=show_correlation_matrix).pack(fill='x', pady=2)
    
    
    model_btn_frame = ttk.LabelFrame(control_frame, text="Modeling", padding=10)
    model_btn_frame.pack(side='left', fill='y', padx=5)
    
    ttk.Button(model_btn_frame, text="Train Model (Supervised)", command=train_model).pack(fill='x', pady=2)
    ttk.Button(model_btn_frame, text="Anomaly Detection (Unsupervised)", command=run_unsupervised_model).pack(fill='x', pady=2)
    ttk.Button(model_btn_frame, text="Train with Persistence", command=gui_train_model).pack(fill='x', pady=2)
    
    
    treeview = ttk.Treeview(display_frame)
    scroll_y = ttk.Scrollbar(display_frame, orient='vertical', command=treeview.yview)
    scroll_x = ttk.Scrollbar(display_frame, orient='horizontal', command=treeview.xview)
    treeview.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    
    scroll_x.pack(side='bottom', fill='x')
    scroll_y.pack(side='right', fill='y')
    treeview.pack(fill='both', expand=True)
    
    
    status_bar = ttk.Label(root, text="Ready", relief='sunken')
    status_bar.pack(fill='x', side='bottom')
    
    root.mainloop()

