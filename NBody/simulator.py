"""
Author: Miles Lucas
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from system import Particle, System
import sys as Sys
import getopt

#-------------------------------------------------------------------------------
#Command Line interaction

#set default
# Number of bodies to be generated
N = 50
#Choose length of animation and determine parameters from that
time = 5 # in seconds
# interval = 20 # in ms
save = False

try:
    opts, args = getopt.getopt(Sys.argv[1:],'hn:t:s:')
except getopt.GetoptError:
    print('simulator.py\n\t-h: help\n\t-n <int>: Number of Objects\n\t-t <int>: \
        Time of animation (s) \n\t-i <int>: Time interval for animation (ms)\n\t\
        -s <filename>: Save animation in file')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('\t-h: help\n\t-n <int>: Number of Objects\n\t-t <int>: Time of \
        animation (s)\n\t-i <int>: Time interval for animation (ms)\n\t \
        -s <filename>: Save animation in file')
        Sys.exit()
    if opt == '-n':
        N = int(arg)
    if opt == '-t':
        time = int(arg)
    if opt == '-s':
        save = True
        filename = str(arg)

n_frames = int(time *60)
time_step = 1

#-------------------------------------------------------------------------------
#Setup

# Generate random particles with the following parameters and put them into a system
# -100 < x,y,z < 100
# -1 < vx, vy, vz < 1
# 0 < m < 10
p = []
for i in range(N):
    pos = (np.random.rand(3)-0.5)*400
    vel = (np.random.rand(3)-0.5)*2
    m = np.random.rand(1)*10
    # vel = np.zeros(3)
    p.append(Particle(pos, vel, m))

sys = System(p)

# The following can be used to simulate a massive central particle as in a galaxy or planetary system

# center = Particle([0, 0, 0], [0, 0, 0], 50)
# sys.add(center)

# The following creates an array with a snapshot of every body's position for each discrete time step
rt = []
for t in range(n_frames):
    rt.append(sys.unpack())
    sys.update(time_step)
    Sys.stdout.write('\rComputing frame '+str(t+1)+'/'+str(n_frames)+'     '+str((t+1)*100/n_frames)+'%')
    Sys.stdout.flush()
rt = np.asarray(rt)

#-------------------------------------------------------------------------------
# Animation

#Set up plot
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
plt.style.use('ggplot')

# All for setting up axis
ax.set_xlim(-200, 200)
ax.set_xlabel('X')
ax.set_ylim(-200, 200)
ax.set_ylabel('Y')
ax.set_zlim(-200, 200)
ax.set_zlabel('Z')
ax.tick_params(axis='both', bottom='off', top='off', right='off', left='off',
    labelbottom='off', labeltop='off', labelright='off', labelleft='off')
ax.xaxis._axinfo['tick']['inward_factor'] = 0
ax.xaxis._axinfo['tick']['outward_factor'] = 0
ax.yaxis._axinfo['tick']['inward_factor'] = 0
ax.yaxis._axinfo['tick']['outward_factor'] = 0
ax.zaxis._axinfo['tick']['inward_factor'] = 0
ax.zaxis._axinfo['tick']['outward_factor'] = 0
ax.zaxis._axinfo['tick']['outward_factor'] = 0
ax.grid(False)
ax.xaxis.pane.set_edgecolor('black')
ax.yaxis.pane.set_edgecolor('black')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
# plt.axis('off')

# Set up empty points for each body with variable markersize
pts = sum([ax.plot([], [], [], 'bo', ms=b.m/5) for b in sys.bodies], [])

# This function is called as part of the animation function and serves to empty out the canvas each iteration
def init():
    for pt in pts:
        pt.set_data([], [])
        pt.set_3d_properties([])
    return pts

# This function is called at each frame and represents one time step for the system
def animate(i):
    for r, pt in zip(rt[i], pts):
        pt.set_data(r[0], r[1])
        pt.set_3d_properties(r[2])
    ax.view_init(30, .3 * i)
    fig.canvas.draw()
    return pts

# This is the animation function from matplotlib
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=n_frames, blit=True)

# Save as mp4. This requires mplayer or ffmpeg to be installed
if save:
    print('\nWriting to '+filename+'.mp4')
    Writer = animation.writers['ffmpeg']
    anim.save(filename+'.mp4', fps=60, bitrate=3200)
else:
    plt.show()
