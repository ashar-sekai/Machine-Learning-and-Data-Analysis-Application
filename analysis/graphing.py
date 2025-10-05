import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def plot_histogram(dataframe, column):
    """Creates an animated histogram with smooth growing bars"""
    try:
        # Set style safely
        if 'seaborn' in plt.style.available:
            plt.style.use('seaborn')
        else:
            plt.style.use('default')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title(f"Histogram: {column}")
        
        # Prepare data
        data = dataframe[column].dropna()
        if len(data) == 0:
            plt.close()
            raise ValueError(f"No valid data in column '{column}'")
        
        # Calculate bins and histogram values
        bin_edges = np.histogram_bin_edges(data, bins='auto')
        hist_vals, _ = np.histogram(data, bins=bin_edges)
        bin_count = len(bin_edges) - 1
        
        # Setup plot
        ax.set_title(f"Distribution of {column}", fontsize=14)
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Create empty bars
        bars = ax.bar(bin_edges[:-1], [0]*bin_count, 
                     width=np.diff(bin_edges), 
                     align='edge',
                     color='skyblue',
                     edgecolor='navy',
                     alpha=0)
        
        # Convert bars to list for animation
        bar_list = list(bars)
        
        # Create KDE line
        line, = ax.plot([], [], 'r-', linewidth=2, alpha=0)
        
        def init():
            return bar_list + [line]
        
        def update(frame):
            # Animate bars
            for i, bar in enumerate(bar_list):
                progress = min(1, (frame - i*2) / 30)
                bar.set_height(hist_vals[i] * progress)
                bar.set_alpha(0.7 * progress)
            
            # Animate KDE line after bars are done
            if frame > bin_count + 10 and len(data) > 1:
                line_progress = min(1, (frame - bin_count - 10) / 20)
                line.set_alpha(line_progress)
                if line_progress == 1 and len(line.get_data()[0]) == 0:
                    x_kde = np.linspace(min(data), max(data), 200)
                    kde = sns.kdeplot(data, ax=ax, color='red', linewidth=2)
                    y_kde = kde.get_lines()[-1].get_ydata()
                    line.set_data(x_kde, y_kde)
                    kde.get_lines()[-1].remove()
            
            return bar_list + [line]
        
        # Create animation with blit=True for smoothness
        ani = FuncAnimation(fig, update, frames=bin_count+40,
                          init_func=init, interval=50, blit=True)
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        if 'fig' in locals():
            plt.close(fig)
        raise RuntimeError(f"Failed to create histogram: {str(e)}")

def plot_heatmap(dataframe):
    """Creates an animated correlation heatmap"""
    try:
        if 'seaborn' in plt.style.available:
            plt.style.use('seaborn')
        else:
            plt.style.use('default')
            
        corr = dataframe.corr()
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.canvas.manager.set_window_title("Correlation Heatmap")
        
        # Create custom colormap
        cmap = LinearSegmentedColormap.from_list('custom_cmap', 
                                               ['#2E86AB', '#F6F5AE', '#F24236'])
        
        # Initialize empty heatmap
        sns.heatmap(np.zeros_like(corr), mask=np.ones_like(corr),
                   annot=True, fmt=".2f", cmap=cmap,
                   cbar=False, ax=ax, vmin=-1, vmax=1)
        
        def update(frame):
            progress = min(1, frame / 30)
            current_corr = corr * progress
            mask = np.triu(np.ones_like(corr, dtype=bool)) if frame < 15 else None
            
            ax.clear()
            sns.heatmap(current_corr, mask=mask,
                       annot=True, fmt=".2f", cmap=cmap,
                       cbar=True, ax=ax, vmin=-1, vmax=1)
            ax.set_title(f"Correlation Matrix ({int(progress*100)}%)", fontsize=14)
            
        ani = FuncAnimation(fig, update, frames=40, interval=50)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        if 'fig' in locals():
            plt.close(fig)
        raise RuntimeError(f"Failed to create heatmap: {str(e)}")

def plot_scatter(dataframe, x_col, y_col):
    """Creates an animated scatter plot"""
    try:
        if 'seaborn' in plt.style.available:
            plt.style.use('seaborn')
        else:
            plt.style.use('default')
            
        data = dataframe[[x_col, y_col]].dropna()
        if len(data) == 0:
            raise ValueError("No valid data for scatter plot")
            
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title(f"Scatter: {x_col} vs {y_col}")
        
        # Initialize empty scatter
        sc = ax.scatter([], [], alpha=0.7)
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Set axis limits
        ax.set_xlim(data[x_col].min() * 0.9, data[x_col].max() * 1.1)
        ax.set_ylim(data[y_col].min() * 0.9, data[y_col].max() * 1.1)
        
        def update(frame):
            show_points = min(frame + 1, len(data))
            x = data[x_col].iloc[:show_points]
            y = data[y_col].iloc[:show_points]
            
            sc.set_offsets(np.column_stack([x, y]))
            sc.set_alpha([0.7] * show_points)
            sc.set_array(np.linspace(0, 1, show_points))
            sc.set_cmap('viridis')
            
            ax.set_title(f"{x_col} vs {y_col} ({show_points}/{len(data)} points)", fontsize=14)
            return [sc]
        
        ani = FuncAnimation(fig, update, frames=len(data)+10,
                          interval=50, blit=True)
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        if 'fig' in locals():
            plt.close(fig)
        raise RuntimeError(f"Failed to create scatter plot: {str(e)}")
