import cPickle
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

plt.switch_backend('Agg')

sw = 20

def runningMeanFast(x, sw):
    return np.convolve(x, np.ones((sw,))/sw, mode="valid")


# ANALYSIS
def main(log_dir, config):

    print log_dir, config
    
    # 
    # if xp_name == "xp1" or xp_name == "xp2":
    #     env_type = 1
    #     log_dir = '/home/sforesti/scm/Flowers/explaupoppydiva/logs/2015-11-06_12-31-26-Tools-' + xp_name + '/'
    # elif xp_name == "xp3":
    #     env_type = 2
    #     log_dir = '/home/sforesti/scm/Flowers/explaupoppydiva/logs/2015-11-09_13-46-41-Tools-xp3/'
    # else:
    #     raise NotImplementedError
    
    
    trials = range(9, 10)
    n_logs = 1
    
    n = 100000
    p = 100
    
    gss = [0, 10, 100, 20, 10, 6, 5, 4, 3, 3]
    
    
    x = np.array(np.linspace(0,n,n/p+1), dtype=int)
    
    def mean_std(d):
        v = np.zeros((n/p,len(d)))
        for i,l in zip(range(len(d)), d.values()):
            for j,lj in zip(range(len(l)), l):
                v[j,i] = lj
        mean = np.mean(v, axis=1)
        std = np.std(v, axis=1) / np.sqrt(len(d))
        return mean, std
    
    
    
    def compute_explo(data, mins, maxs, checkpoints=None):
        if checkpoints is None:
            checkpoints = [len(data)]
        n = len(mins)
        assert len(data[0]) == n
        gs = gss[n]
        epss = (maxs - mins) / gs
        grid = np.zeros([gs] * n)
        #print np.size(grid), mins, maxs
        res = [0]
        for c in range(1, len(checkpoints)):
            for i in range(checkpoints[c-1], checkpoints[c]):
                idxs = np.array((data[i] - mins) / epss, dtype=int)
                #print c, i, idxs
                idxs[idxs>=gs] = gs-1
                idxs[idxs<0] = 0
                #print idxs
                grid[tuple(idxs)] = grid[tuple(idxs)] + 1
            grid[grid > 1] = 1
            res.append(np.sum(grid))
        return np.array(res)
    
    
    
    
    explo = {}
    explo['hand'] = {}
    explo['stick_1'] = {}
    explo['stick_2'] = {}
    explo['obj'] = {}
    explo['box'] = {}
    

    
    explo['hand'][config] = {}
    explo['stick_1'][config] = {}
    explo['obj'][config] = {}
    explo['box'][config] = {}
    explo['stick_2'][config] = {}
        
    for trial in trials:
        print trial
                
        try:
            data = {}
            
            def get_data_topic(topic):
                data[topic] = []
                for i in range(n_logs):
                    with open(log_dir + config + "/log{}-".format(trial) + topic + "-{}.pickle".format(i), 'r') as f:
                        log = cPickle.load(f)
                        f.close()
                    data[topic] = data[topic] + log
            
            get_data_topic('agentS')
            
            
        
            data = np.array(data['agentS'])
            
            
        
            dims = dict(
                        hand=[2,5],
                        stick_1=[11, 14],
                        stick_2=[17, 20],
                        obj=[21, 22],
                        box=[23])
            
            mins = np.array([-2.] * (7 * 3) + [-2., -2., 1., 0.])
            maxs = np.array([2.] * (7 * 3) + [2., 2., 11., 2.])
            
        
        
            for s_space in dims.keys():
                explo[s_space][config][trial] = compute_explo(data[:,np.array(dims[s_space])], mins[dims[s_space]], maxs[dims[s_space]], x)
            
            #print explo
             
            if True:
#                 fig, ax = plt.subplots()
#                 fig.canvas.set_window_title('Exploration')
#                 for s_space in dims.keys():
#                     ax.plot(x, explo[s_space][config][trial], label=s_space)
#                 handles, labels = ax.get_legend_handles_labels()
#                 ax.legend(handles, labels)
#                      
#                 plt.savefig(log_dir + "img/" + config + '-log{}-explo.pdf'.format(trial), format='pdf', dpi=1000, bbox_inches='tight')
#                 plt.close(fig)
                
                
                #Object exploration
                fig, ax = plt.subplots()
                fig.canvas.set_window_title('Object exploration')            
                sx = data[:,dims['obj'][0]]
                sy = data[:,dims['obj'][1]]            
#                 plt.xlabel('X', fontsize = 16)
#                 plt.ylabel('Y', fontsize = 16)   
                #ax.add_patch(plt.Rectangle((-0.1, 1.1), 0.1, 0.1, fc='y', alpha=0.5))
                ax.add_patch(plt.Rectangle((-1.5, -0.1), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((-1.2, 1.), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((-0.1, 1.3), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((1., 1.), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((1.3, -0.1), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((-1., -0.1), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((-0.7, 0.5), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((-0.1, 0.8), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((0.5, 0.5), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                ax.add_patch(plt.Rectangle((0.8, -0.1), 0.2, 0.2, fc="none", alpha=0.5, lw=4))
                
                color=matplotlib.colors.ColorConverter().to_rgba('b', alpha=0.1)
                ax.scatter(sx, sy, s=3, color=color, rasterized=True)
                ax.set_xticklabels([])
                ax.set_yticklabels([])
                plt.gca().xaxis.set_major_locator(plt.NullLocator())
                plt.gca().yaxis.set_major_locator(plt.NullLocator())
                plt.xlim(-1.7, 1.7)
                plt.ylim(-0.8, 1.7)
                ax.set_aspect('equal')            
                plt.savefig("/home/sforesti/scm/PhD/cogsci2016/include/obj-explo.pdf", format='pdf', dpi=100, bbox_inches='tight')
                #plt.savefig(log_dir + "img/" + config + '-log{}-obj-explo.pdf'.format(trial), format='pdf', dpi=100, bbox_inches='tight')
                plt.close(fig)
        
        except IOError:
            print "File not found for trial", trial
            
    with open(log_dir + config + '/analysis_explo.pickle', 'wb') as f:
        cPickle.dump(explo, f)

if __name__ == "__main__":
    
    log_dir = sys.argv[1]
    config = sys.argv[2]
    main(log_dir, config)
# 