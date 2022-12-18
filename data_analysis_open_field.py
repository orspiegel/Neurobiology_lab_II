import scipy.io
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from tabulate import tabulate

BATCH_1 = 0
BATCH_2 = 150
BATCH_3 = 300
BATCH_4 = 450

BATCH_SIZE = 150


def load_mat_data(file):
    mat = scipy.io.loadmat(file)
    # print(len(mat))
    crossing_times = mat['crossing_times']
    grooming_start_stop = mat['grooming_start_stop']
    periphery_times = mat['periphery_times']
    mouse_data = {'crossing_times': crossing_times,
                  'grooming': grooming_start_stop,
                  'priphery_times': periphery_times}
    return mouse_data


def all_year_data_crossing(trails_per_year, mouses):
    """
    @input - all mat files from: curr year or from last year
    @output - list of all crossing vectors for that given year,
    the 1st in the mat file for each mat file.
    """
    m_no_suff = [m.split('.')[0] for m in mouses]
    union_cross_data = [load_mat_data(trail)['crossing_times'][0] for trail in trails_per_year]
    cross_curr_data_dict = dict(zip(m_no_suff, union_cross_data))
    return cross_curr_data_dict


def all_year_data_grooming(trails_per_year, mouses):
    """
    @input - all mat files from: curr year or from last year
    @output - list of all grooming vectors for that given year,
    the 2nd in the mat file for each mat file.
    """
    # union_grooming_data = [load_mat_data(trail)['periphery_times'] for trail in trails_per_year]
    # return union_grooming_data

    m_no_suff = [m.split('.')[0] for m in mouses]
    union_groom_data = [load_mat_data(trail)['grooming'] for trail in trails_per_year]
    groom_curr_data_dict = dict(zip(m_no_suff, union_groom_data))
    # print(groom_curr_data_dict)
    return groom_curr_data_dict


def all_year_data_periphery_crossing(trails_per_year, mouses):
    """
    @input - all mat files from: curr year or from last year
    @output - list of all periphery crossing vectors for that given year,
    the 3rd in the mat file for each mat file.
    """
    # union_priph_data = [load_mat_data(trail)['grooming_start_stop'] for trail in trails_per_year]
    # return union_priph_data
    m_no_suff = [m.split('.')[0] for m in mouses]
    union_priph_data = [load_mat_data(trail)['priphery_times'][0] for trail in trails_per_year]
    peri_curr_data_dict = dict(zip(m_no_suff, union_priph_data))
    return peri_curr_data_dict


def get_i_batch_n_variable(BATCH_START_TIME, all_data):
    """
    Get i of (1,2,3,4) batch for n of (cross, periphery, groom) param
    For all mice in a given year
    """
    mice_batch = {}
    treshold = BATCH_START_TIME + BATCH_SIZE
    for key in all_data:
        mice_batch.update({key: ((BATCH_START_TIME < all_data[key]) & (all_data[key] < treshold)).sum()})
    return mice_batch


def get_i_batch_n_variable_grooming(BATCH_START_TIME, all_data):
    """
    Get i of (1,2,3,4) batch for n of (cross, periphery, groom) param
    For all mice in a given year
    """
    treshold = BATCH_START_TIME + BATCH_SIZE
    mice_batch = {}
    for m in all_data:
        d = list(zip(*(all_data[m])))
        mice_batch.update({m: d})

    groom_lens_for_batch = []
    for m in mice_batch:
        for groom in mice_batch[m]:
            if groom[0] >= BATCH_START_TIME and groom[1] <= treshold:
                groom_lens_for_batch.append(groom[1] - groom[0])

    return groom_lens_for_batch


def box_plot(batch_i, param):
    # Creating plot
    plt.boxplot(batch_i)
    plt.title(f"{param} param for each bin")
    if param == "Grooming":
        plt.ylabel(f'{param} length per bin (sec)')
    else:
        plt.ylabel(f'{param} amount per bin')
    plt.xlabel('Bin number')

    # show plot
    plt.show()


def descriptive_stats_per_batch(bin1, bin2, bin3, bin4):
    data = [[1, 5, batch_std(bin1), batch_mean(bin1), batch_min_max(bin1, 'max'), batch_min_max(bin1, 'min')],
            [2, 5, batch_std(bin2), batch_mean(bin2), batch_min_max(bin2, 'max'), batch_min_max(bin2, 'min')],
            [3, 5, batch_std(bin3), batch_mean(bin3), batch_min_max(bin3, 'max'), batch_min_max(bin3, 'min')],
            [4, 5, batch_std(bin4), batch_mean(bin4), batch_min_max(bin4, 'max'), batch_min_max(bin4, 'min')]]
    print(tabulate(data, headers=["Bin", "N", "std", "mean", "max", "min"]))


def batch_mean(batch_dict):
    mean = np.mean(list(batch_dict.values()))
    return mean

def batch_std(batch_dict):
    std = np.std(list(batch_dict.values()))
    return std

def batch_min_max(batch_dict, extrema):
    min = np.min(list(batch_dict.values()))
    max = np.max(list(batch_dict.values()))
    ret_val = min if extrema == 'min' else max
    return ret_val

if __name__ == '__main__':
    # list of all curr year trails
    path_curr_year = "raw_data_package"
    curr_year_trails = os.listdir(path_curr_year)
    curr_paths = [os.path.join(path_curr_year, x) for x in curr_year_trails]
    # list of all last year trails
    path_former_year = "raw_data_former_year"
    former_year_trails = os.listdir(path_former_year)
    former_paths = [os.path.join(path_former_year, x) for x in former_year_trails]
    # all of 2022 trails in one set
    # mouse1: array([[cross1 time, cross2 time, ..., crossn time]]) data[mouse1]
    cross_curr_data_union = all_year_data_crossing(curr_paths, curr_year_trails)
    periphery_curr_data_union = all_year_data_periphery_crossing(curr_paths, curr_year_trails)
    groom_curr_data_union = all_year_data_grooming(curr_paths, curr_year_trails)

    # batch 1 for all params:
    batch_1_cross_2022 = get_i_batch_n_variable(BATCH_1, cross_curr_data_union)  
    batch_1_periphery_2022 = get_i_batch_n_variable(BATCH_1,
                                                    periphery_curr_data_union)  
    batch_1_groom_2022 = get_i_batch_n_variable_grooming(BATCH_1,
                                                         groom_curr_data_union)  


    batch_2_cross_2022 = get_i_batch_n_variable(BATCH_2, cross_curr_data_union)  
    batch_2_periphery_2022 = get_i_batch_n_variable(BATCH_2,
                                                    periphery_curr_data_union)  
    batch_2_groom_2022 = get_i_batch_n_variable_grooming(BATCH_2,
                                                         groom_curr_data_union)  

    batch_3_cross_2022 = get_i_batch_n_variable(BATCH_3, cross_curr_data_union)  
    batch_3_periphery_2022 = get_i_batch_n_variable(BATCH_3,
                                                    periphery_curr_data_union)  
    batch_3_groom_2022 = get_i_batch_n_variable_grooming(BATCH_3,
                                                         groom_curr_data_union)  

    batch_4_cross_2022 = get_i_batch_n_variable(BATCH_4, cross_curr_data_union)  
    batch_4_periphery_2022 = get_i_batch_n_variable(BATCH_4,
                                                    periphery_curr_data_union)  
    batch_4_groom_2022 = get_i_batch_n_variable_grooming(BATCH_4,
                                                         groom_curr_data_union)  

    # box_plot([list(batch_1_cross_2022.values()), list(batch_2_cross_2022.values()),
    #          list(batch_3_cross_2022.values()), list(batch_4_cross_2022.values())], "Crossing")
    #
    # box_plot([list(batch_1_periphery_2022.values()), list(batch_2_periphery_2022.values()),
    #          list(batch_3_periphery_2022.values()), list(batch_4_periphery_2022.values())], "Periphery crossing")
    #
    # box_plot([list(batch_1_groom_2022), list(batch_2_groom_2022),list(batch_3_groom_2022), list(batch_4_groom_2022)], "Grooming")
    # print(batch_1_cross_2022)
    # print(batch_2_groom_2022)
    # print(batch_3_groom_2022)
    # print(batch_4_groom_2022)

    ##############################################################################################################################
    # Last year
    cross_last_data_union = all_year_data_crossing(former_paths, former_year_trails)
    periphery_last_data_union = all_year_data_periphery_crossing(former_paths, former_year_trails)
    groom_last_data_union = all_year_data_grooming(former_paths, former_year_trails)

    batch_1_cross_2021 = get_i_batch_n_variable(BATCH_1, cross_last_data_union)
    batch_1_periphery_2021 = get_i_batch_n_variable(BATCH_1, periphery_last_data_union)
    batch_1_groom_2021 = get_i_batch_n_variable_grooming(BATCH_1, groom_last_data_union)

    batch_2_cross_2021 = get_i_batch_n_variable(BATCH_2, cross_last_data_union)
    batch_2_periphery_2021 = get_i_batch_n_variable(BATCH_2, periphery_last_data_union)
    batch_2_groom_2021 = get_i_batch_n_variable_grooming(BATCH_2, groom_last_data_union)

    batch_3_cross_2021 = get_i_batch_n_variable(BATCH_3, cross_last_data_union)
    batch_3_periphery_2021 = get_i_batch_n_variable(BATCH_3, periphery_last_data_union)
    batch_3_groom_2021 = get_i_batch_n_variable_grooming(BATCH_3, groom_last_data_union)

    batch_4_cross_2021 = get_i_batch_n_variable(BATCH_4, cross_last_data_union)
    batch_4_periphery_2021 = get_i_batch_n_variable(BATCH_4,
                                                    periphery_last_data_union)
    batch_4_groom_2021 = get_i_batch_n_variable_grooming(BATCH_4, groom_last_data_union)

    # box_plot([list(batch_1_cross_2021.values()), list(batch_2_cross_2021.values()),
    #          list(batch_3_cross_2021.values()), list(batch_4_cross_2021.values())], "Crossing")
    #
    # box_plot([list(batch_1_periphery_2021.values()), list(batch_2_periphery_2021.values()),
    #           list(batch_3_periphery_2021.values()), list(batch_4_periphery_2021.values())], "Periphery crossing")
    #
    # box_plot([list(batch_1_groom_2021), list(batch_2_groom_2021),
    #           list(batch_3_groom_2021), list(batch_4_groom_2021)], "Grooming")
    #
    ##############################################################################################################################
    """
    Descriptive stats for cross
    """
    print("2022 descriptive statistics for crossing:")
    print(descriptive_stats_per_batch(batch_1_cross_2022, batch_2_cross_2022, batch_3_cross_2022, batch_4_cross_2022))
    print("2021 descriptive statistics for crossing:")
    print(descriptive_stats_per_batch(batch_1_cross_2021, batch_2_cross_2021, batch_3_cross_2021, batch_4_cross_2021))
    """
    Descriptive stats for periphery cross
    """
    print("2022 descriptive statistics for periphery crossing:")
    print(descriptive_stats_per_batch(batch_1_periphery_2022, batch_2_periphery_2022, batch_3_periphery_2022, batch_4_periphery_2022))
    print("2021 descriptive statistics for periphery crossing:")
    print(descriptive_stats_per_batch(batch_1_periphery_2021, batch_2_periphery_2021, batch_3_periphery_2021, batch_4_periphery_2021))
