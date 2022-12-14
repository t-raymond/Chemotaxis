import matplotlib.pyplot as plt
from matplotlib import animation, rc
import numpy as np

def SA_1D(x, y, labels, xlabel, ylabel, title):
    """
    Plot 1D sensitivity analysis
    """
    fig = plt.figure()
    for i, label in enumerate(labels):
        plt.loglog(x[i], y[i], label = label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()

    return fig

# Initialization function
def init():
    """
    
    """
    line_B.set_data([], [])
    line_BL.set_data([], [])
    line_Ads.set_data([], [])

    return (line_B, line_BL, line_Ads)

def animate(i):
    """
    
    """
    
    X = x
    Y_B = y_B[i]
    Y_BL = y_BL[i]
    Y_Ads = y_Ads[i]

    # Bulk
    line_B.set_data(X, Y_B)
    line_B.set_label('Bulk')

    # Boundary Layer
    line_BL.set_data(X, Y_BL)
    line_BL.set_label('Boundary Layer')

    # Adsorbed
    line_Ads.set_data(X, Y_Ads)
    line_Ads.set_label('Adsorbed')

    # Set figure attributes
    ax.legend()
    ax.set_title('Spatiotemporal Diffusion')
    ax.set_xlabel('$\lambda = \\frac{x}{L}$')
    ax.set_ylabel('$\\theta = \\frac{C}{C_0}$')

    # Remove any existing text on figure
    for T in ax.texts:
        T.remove()

    # Update text
    ax.text(1.1, 0.9, "$\\frac{Dt}{L^{2}}$ = " + str(m.time[i].round(2)))
    ax.text(1.1, 0.8, "$\\frac{kL^{2}}{D}$ = " + str(alpha))
    ax.text(1.1, 0.7, "$\phi~\sqrt[n]{\\frac{S_0}{C_0}}$ = " + str(beta))
    ax.text(1.1, 0.6, "$n$ = " + str(n))

    fig.subplots_adjust(right = 0.7)

    return(line_B, line_BL, line_Ads)

def MakeAnimation(x, t, y_B, y_BL, y_Ads):
    """
    
    """

    # Initialize figure
    rc('animation', html = 'html5')

    fig, ax = plt.subplots()

    ax.set_xlim((0, 1))
    ax.set_ylim((0, 1))

    line_B, = ax.plot([], [], lw = 2)
    line_BL, = ax.plot([], [], lw = 2)
    line_Ads, = ax.plot([], [], lw = 2)

    # Create animation
    anim = animation.FuncAnimation(fig, animate, init_func = init, frames = len(t), interval = 100, blit = True)
    return anim

    # Save animation
    # anim.save('Diffusion.mp4', fps = 10)
