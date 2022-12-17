import scipy.io
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
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
    union_groom_data = [load_mat_data(trail)['grooming'][0] for trail in trails_per_year]
    groom_curr_data_dict = dict(zip(m_no_suff, union_groom_data))
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


def box_plot():
    

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
    batch_1_cross_2022 = get_i_batch_n_variable(BATCH_1, cross_curr_data_union) # map of mouse: amount of X in bach 1
    batch_1_periphery_2022 = get_i_batch_n_variable(BATCH_1, periphery_curr_data_union) # map of mouse: amount of X in bach 1
    batch_1_groom_2022 = get_i_batch_n_variable(BATCH_1, groom_curr_data_union) # map of mouse: amount of X in bach 1

    batch_2_cross_2022 = get_i_batch_n_variable(BATCH_2, cross_curr_data_union) # map of mouse: amount of X in bach 1
    batch_2_periphery_2022 = get_i_batch_n_variable(BATCH_2, periphery_curr_data_union) # map of mouse: amount of X in bach 1
    batch_2_groom_2022 = get_i_batch_n_variable(BATCH_2, groom_curr_data_union) # map of mouse: amount of X in bach 1

    batch_3_cross_2022 = get_i_batch_n_variable(BATCH_3, cross_curr_data_union) # map of mouse: amount of X in bach 1
    batch_3_periphery_2022 = get_i_batch_n_variable(BATCH_3, periphery_curr_data_union) # map of mouse: amount of X in bach 1
    batch_3_groom_2022 = get_i_batch_n_variable(BATCH_3, groom_curr_data_union) # map of mouse: amount of X in bach 1

    batch_4_cross_2022 = get_i_batch_n_variable(BATCH_4, cross_curr_data_union) # map of mouse: amount of X in bach 1
    batch_4_periphery_2022 = get_i_batch_n_variable(BATCH_4, periphery_curr_data_union) # map of mouse: amount of X in bach 1
    batch_4_groom_2022 = get_i_batch_n_variable(BATCH_4, groom_curr_data_union) # map of mouse: amount of X in bach 1


    print(batch_1_groom_2022, batch_1_periphery_2022, batch_1_groom_2022)
    #all of 2021 trails in one set
    cross_former_data_union = cross_curr_data_union
