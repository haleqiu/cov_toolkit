import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import pandas as pd

def sparsification_plot(var, mse):
    '''
    Steps:
    1:sort each pixel's variance from large to small and get the index
    2:remove 10 pixels each time and calculate the remaining pixels' mean mse
    3:plot the mean mse with the percentage of removed pixels
    '''
    var = var.flatten()
    mse = mse.flatten()
    sorted_indices = np.argsort(var)[::-1]
    sorted_indices_mse = np.argsort(mse)[::-1]
    mean_mses = []
    mean_mses_mse = []
    for i in range(0, var.shape[0], var.shape[0] // 1000):
        remain_indices = sorted_indices[i:]
        remain_indices_mse = sorted_indices_mse[i:]
        if remain_indices.shape[0] == 0:
            mean_mses.append(0)
            mean_mses_mse.append(0)
            break
        mean_mses.append(np.mean(mse[remain_indices]))
        mean_mses_mse.append(np.mean(mse[remain_indices_mse]))
    mean_mses = np.array(mean_mses)
    mean_mses_mse = np.array(mean_mses_mse)
    return mean_mses, mean_mses_mse

def area_under_curve(list):
    '''
    calculate the area under the curve
    '''
    return np.sum(list) / list.shape[0]

mse = np.load('mse.npy')
cov = np.load('cov.npy')

cc_mse_cov = spearmanr(mse.flatten(), cov.flatten())[0]

# plot the sparsification curve
estimated_var , oracle = sparsification_plot(cov, mse)

#normalize the result
oracle = (oracle - np.min(oracle)) / \
        (np.max(oracle) - np.min(oracle))
factor = oracle[0] / estimated_var[0]
estimated_var = estimated_var * factor

#calculate the spearman correlation coefficient curve
cc = spearmanr(estimated_var, oracle)[0]

#calculate the area under the curve
auc = area_under_curve(estimated_var)

#calculate Cov_AUC/Oracle_AUC
dauc = area_under_curve(estimated_var) / area_under_curve(oracle)

#plot the result
x = np.linspace(0, 1, 1001)
plt.plot(x,estimated_var, label='Estimated Variance')
plt.plot(x,oracle, label='Oracle')
plt.title('Sparsification Curve')
plt.legend()
plt.xlabel('Percentage of Removed Pixels')
plt.ylabel('AEPE')
plt.savefig('sparsification_plot.png')
plt.show()

#save the result
data = {'cc_mse_cov':cc_mse_cov, 'cc':cc, 'auc':auc, 'dauc':dauc}
df = pd.DataFrame(data, index=[0])
df.to_csv('result.csv', index=False)


