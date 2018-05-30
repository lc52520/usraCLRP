#!/usr/bin/env
# author: Joseph Lucero
# created on: 25 May 2018 11:33:46
# purpose: plotting 3ddose files

from __future__ import division

from sys import argv, exit
from os import getcwd

from numpy import linspace, histogram, arange, meshgrid, array, empty, around
from py3ddose import DoseFile

from matplotlib.cm import get_cmap
from matplotlib.style import use
use('seaborn-paper')
from matplotlib.pyplot import subplots, figure, close
from mpl_toolkits.mplot3d import Axes3D

def dose_position_plots():
    """
    Description:
    Takes any number of .3ddose files and plots a plethora of diagnostic plots 
    from the data

    Inputs:
    :name list_file: a list of file names that are to be loaded
    :type list_file: list
    """

    pwd = getcwd()

    # target_dir = '/Users/JLucero/MPhysProj/results_not_to_git' for home
    target_dir = '/Users/student/research/results_not_to_git'  # for work

    file_list = [
        target_dir +
        '/mlwa_0shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_90shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_180shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_270shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
    ]

    shield_type_lst = [
        'Unshielded',
        '90 degree shield',
        '180 degree shield',
        '270 degree shield'
    ]

    vox_size_lst = [
        # '0.5mm',
        '1mm',
        '2mm'
    ]
    vox_size_txt_lst = [
        # '0.5mm',
        '1pt0mm',
        '2pt0mm'
    ]

    title_list = [
        'X - axis',
        'Y - axis',
        'Z - axis'
    ]

    for fig_index in xrange(len(vox_size_lst)):

        fig, ax = subplots(
            3, len(shield_type_lst), figsize=(15, 15),
            sharex='col', sharey='all'
        )

        for index2 in xrange(len(shield_type_lst)):  # iterate through shield types

            full_data = DoseFile(
                file_list[index2].format(vox_size_txt_lst[fig_index])
            )

            Nx, Ny, Nz = full_data.shape

            # scale to maximum individual dwell time
            full_data.dose *= 8.2573429808917e13  

            x_min, x_max = full_data.x_extent
            y_min, y_max = full_data.y_extent
            z_min, z_max = full_data.z_extent

            for index1 in xrange(3):  # iterate through axes

                if index1 == 0:
                    ax[index1, index2].plot(
                        linspace(x_min, x_max,
                                 Nx), full_data.dose[:, Ny // 2, Nz // 2],
                        # yerr=full_data.uncertainty[Nz // 2, Ny // 2, :],
                        lw=3.0
                    )
                elif index1 == 1:
                    ax[index1, index2].plot(
                        linspace(y_min, y_max,
                                 Ny), full_data.dose[Nx // 2, :, Nz // 2],
                        # yerr=full_data.uncertainty[Nz // 2, :, Nx // 2],
                        lw=3.0
                    )
                else:
                    ax[index1, index2].plot(
                        linspace(z_min, z_max,
                                 Nz), full_data.dose[Nx // 2, Ny // 2, :],
                        # yerr=full_data.uncertainty[:, Ny // 2, Nx // 2],
                        lw=3.0
                    )
        for n in xrange(len(title_list)):
            for m in xrange(len(shield_type_lst)):
                ax[n, m].grid(True)
                if n == 0:
                    ax[n, m].set_title(shield_type_lst[m], fontsize=20)
                if m == len(shield_type_lst) - 1:
                    ax[n, m].set_ylabel(title_list[n],fontsize=20)
                    ax[n, m].yaxis.set_label_position("right")
                ax[n, m].xaxis.set_tick_params(labelsize=14)
                ax[n, m].yaxis.set_tick_params(labelsize=14)
                ax[n, m].set_xticks(arange(z_min, z_max + 1, 5))

        fig.text(
            0.01, 0.51, 'Dose (Gy)',
            fontsize=27, rotation='vertical', va='center'
        )
        fig.text(
            0.43, 0.03, 'Position (cm)', fontsize=27, va='center'
        )
        fig.text(
            0.52, 0.95,
            'Absolute Dose vs. Position \n With Volume Correction; ncase = 5E9',
            fontsize=27, va='center', ha='center'
        )
        fig.tight_layout()

        left = 0.125  # the left side of the subplots of the figure
        right = 0.95    # the right side of the subplots of the figure
        bottom = 0.09   # the bottom of the subplots of the figure
        top = 0.87     # the top of the subplots of the figure
        # wspace = 0.2  # the amount of width reserved for blank space between subplots
        # hspace = 0.2  # the amount of height reserved for white space between subplotss

        fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top)

        fig.savefig(pwd + '/dosage_comparison_' + vox_size_lst[fig_index] + '.pdf')

def dose_inv_position_plots():
    """
    Description:
    Takes any number of .3ddose files and plots a plethora of diagnostic plots 
    from the data

    Inputs:
    :name list_file: a list of file names that are to be loaded
    :type list_file: list
    """

    pwd = getcwd()

    # target_dir = '/Users/JLucero/MPhysProj/results_not_to_git' for home
    target_dir = '/Users/student/research/results_not_to_git'  # for work

    file_list = [
        target_dir +
        '/mlwa_0shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_90shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_180shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_270shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
    ]

    shield_type_lst = [
        'Unshielded',
        '90 degree shield',
        '180 degree shield',
        '270 degree shield'
    ]

    vox_size_lst = [
        # '0.5mm',
        '1mm',
        '2mm'
    ]
    vox_size_txt_lst = [
        # '0.5mm',
        '1pt0mm',
        '2pt0mm'
    ]

    title_list = [
        'y-cuts (|x| = {0}, z = {1})',
        'z-cuts (|x| = {0}, y = {1})'
    ]

    for x_pos in around(arange(1.6, 2.2, 0.2), 1):
        for z_pos in around(arange(-2.0, 2.2, 0.2), 1):
            for fig_index in xrange(len(vox_size_lst)):

                fig, ax = subplots(
                    1, len(shield_type_lst), figsize=(15, 10),
                    sharex='col', sharey='all'
                )

                for index2 in xrange(len(shield_type_lst)):  # iterate through shield types

                    full_data = DoseFile(
                        file_list[index2].format(vox_size_txt_lst[fig_index])
                    )

                    Nx, Ny, Nz = full_data.shape

                    x_position_to_index = {
                        x_position: x_index
                        for x_index, x_position in enumerate(full_data.positions[1])
                    }
                    y_position_to_index = {
                        y_position: y_index
                        for y_index, y_position in enumerate(full_data.positions[1])
                    }
                    z_position_to_index = {
                        z_position: z_index
                        for z_index, z_position in enumerate(full_data.positions[2])
                    }

                    # scale to maximum individual dwell time
                    full_data.dose *= 8.2573429808917e13  

                    x_min, x_max = full_data.x_extent
                    y_min, y_max = full_data.y_extent
                    z_min, z_max = full_data.z_extent

                    # x_pos, y_pos, z_pos = 1.5, 0.0, 0.0

                    y_depths = empty(Ny)
                    
                    for y_depth_index in xrange(Nz):
                        y_depths[y_depth_index] = (
                            full_data.dose.transpose()[
                                x_position_to_index[-x_pos], 
                                y_depth_index, 
                                z_position_to_index[z_pos]
                                ] / full_data.dose.transpose()[
                                    x_position_to_index[x_pos], 
                                    y_depth_index, 
                                    z_position_to_index[z_pos]
                                ]
                            )

                    ax[index2].plot(
                        linspace(y_min, y_max, Ny), 
                        y_depths,
                        # yerr=full_data.uncertainty[Nz // 2, Ny // 2, :],
                        lw=3.0
                    )

                for m in xrange(len(shield_type_lst)):
                    ax[m].grid(True)
                    ax[m].set_title(shield_type_lst[m], fontsize=20)
                    if m == len(shield_type_lst) - 1:
                        ax[m].set_ylabel(
                            title_list[0].format(x_pos, z_pos),
                            fontsize=20
                        )
                        ax[m].yaxis.set_label_position("right")
                    ax[m].xaxis.set_tick_params(labelsize=14)
                    ax[m].yaxis.set_tick_params(labelsize=14)
                    ax[m].set_xticks(arange(z_min, z_max + 1, 5))
                    ax[m].set_ylim([0.8, 1.10])

                fig.text(
                    0.01, 0.51, 'Ratio at depths',
                    fontsize=27, rotation='vertical', va='center'
                )
                fig.text(
                    0.43, 0.03, 'Depth of cut (cm)', fontsize=27, va='center'
                )
                fig.text(
                    0.52, 0.95,
                    'Absolute Dose vs. Position \n With Volume Correction; ncase = 1E9',
                    fontsize=27, va='center', ha='center'
                )
                fig.tight_layout()

                left = 0.125  # the left side of the subplots of the figure
                right = 0.95    # the right side of the subplots of the figure
                bottom = 0.09   # the bottom of the subplots of the figure
                top = 0.87     # the top of the subplots of the figure
                # wspace = 0.2  # the amount of width for blank space between subplots
                # hspace = 0.2  # the amount of height for white space between subplots

                fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top)

                fig.savefig(
                    pwd + '/dosage_inv_comparison_' + vox_size_lst[fig_index] 
                    + '_x' + str(x_pos) + '_z' + str(z_pos) 
                    + '.pdf'
                )

                close(fig)

    for x_pos in around(arange(1.6, 2.2, 0.2), 1):
        for y_pos in around(arange(-2.0, 2.2, 0.2), 1):
            for fig_index in xrange(len(vox_size_lst)):

                fig, ax = subplots(
                    1, len(shield_type_lst), figsize=(15, 10),
                    sharex='col', sharey='all'
                )

                for index2 in xrange(len(shield_type_lst)):  # iterate through shield types

                    full_data = DoseFile(
                        file_list[index2].format(vox_size_txt_lst[fig_index])
                    )

                    Nx, Ny, Nz = full_data.shape

                    x_position_to_index = {
                        x_position: x_index
                        for x_index, x_position in enumerate(full_data.positions[1])
                    }
                    y_position_to_index = {
                        y_position: y_index
                        for y_index, y_position in enumerate(full_data.positions[1])
                    }
                    z_position_to_index = {
                        z_position: z_index
                        for z_index, z_position in enumerate(full_data.positions[2])
                    }

                    # scale to maximum individual dwell time
                    full_data.dose *= 8.2573429808917e13  

                    x_min, x_max = full_data.x_extent
                    y_min, y_max = full_data.y_extent
                    z_min, z_max = full_data.z_extent

                    z_depths = empty(Nz)
                    
                    for z_depth_index in xrange(Nz):
                        z_depths[z_depth_index] = (
                            full_data.dose.transpose()[
                                x_position_to_index[-x_pos], 
                                y_position_to_index[y_pos], 
                                z_depth_index
                                ] / full_data.dose.transpose()[
                                    x_position_to_index[x_pos], 
                                    y_position_to_index[y_pos],
                                    z_depth_index
                                ]
                            )

                    ax[index2].plot(
                        linspace(z_min, z_max, Nz), 
                        z_depths,
                        # yerr=full_data.uncertainty[:, Ny // 2, Nx // 2],
                        lw=3.0
                    )
                for m in xrange(len(shield_type_lst)):
                    ax[m].grid(True)
                    ax[m].set_title(shield_type_lst[m], fontsize=20)
                    if m == len(shield_type_lst) - 1:
                        ax[m].set_ylabel(
                            title_list[1].format(x_pos, y_pos),
                            fontsize=20
                        )
                        ax[m].yaxis.set_label_position("right")
                    ax[m].xaxis.set_tick_params(labelsize=14)
                    ax[m].yaxis.set_tick_params(labelsize=14)
                    ax[m].set_xticks(arange(z_min, z_max + 1, 5))

                fig.text(
                    0.01, 0.51, 'Ratio at depths',
                    fontsize=27, rotation='vertical', va='center'
                )
                fig.text(
                    0.43, 0.03, 'Depth of cut (cm)', fontsize=27, va='center'
                )
                fig.text(
                    0.52, 0.95,
                    'Absolute Dose vs. Position \n With Volume Correction; ncase = 1E9',
                    fontsize=27, va='center', ha='center'
                )
                fig.tight_layout()

                left = 0.125  # the left side of the subplots of the figure
                right = 0.95    # the right side of the subplots of the figure
                bottom = 0.09   # the bottom of the subplots of the figure
                top = 0.87     # the top of the subplots of the figure
                # wspace = 0.2  # the amount of width for blank space between subplots
                # hspace = 0.2  # the amount of height for white space between subplots

                fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top)

                fig.savefig(
                    pwd + '/dosage_inv_comparison_' + vox_size_lst[fig_index] 
                    + '_x' + str(x_pos) + '_y' + str(y_pos) + '.pdf'
                    )

                close(fig)
    
def isodose_plot():
    """
    Description:
    Takes any number of .3ddose files and plots a plethora of diagnostic plots 
    from the data

    Inputs:
    :name list_file: a list of file names that are to be loaded
    :type list_file: list
    """

    pwd = getcwd()

    # target_dir = '/Users/JLucero/MPhysProj/results_not_to_git' # for home
    target_dir = '/Users/student/research/results_not_to_git'  # for work

    file_list = [
        # target_dir +
        # '/mlwa_0shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        # target_dir +
        # '/mlwa_90shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        # target_dir +
        # '/mlwa_180shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        # target_dir +
        # '/mlwa_270shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_0shield_{0}_sim.phantom_wo_applicator.3ddose',
        target_dir +
        '/mlwa_90shield_{0}_sim.phantom_wo_applicator.3ddose',
        target_dir +
        '/mlwa_180shield_{0}_sim.phantom_wo_applicator.3ddose',
        target_dir +
        '/mlwa_270shield_{0}_sim.phantom_wo_applicator.3ddose',
    ]

    shield_type_lst = [
        'Unshielded',
        r'$90^{\circ}$ shield',
        r'$180^{\circ}$ shield',
        r'$270^{\circ}$ shield'
    ]

    vox_size_lst = [
        '1mm',
        '2mm'
    ]

    vox_size_txt_lst = [
        '1pt0mm',
        '2pt0mm'
    ]

    for fig_index in xrange(len(vox_size_lst)):

        fig, ax = subplots(
            2, 2, figsize=(12, 12),
            sharex='all', sharey='all'
        )
        fig2, ax2 = subplots(
            2, 2, figsize=(12, 12),
            sharex='all', sharey='all'
        )

        for file_index, file in enumerate(file_list):

            full_data = DoseFile(file.format(vox_size_txt_lst[fig_index]))

            y_position_to_index = {
                position:index 
                for index, position in enumerate(full_data.positions[1])
            }
            z_position_to_index = {
                position:index 
                for index, position in enumerate(full_data.positions[2])
            }

            if file_index == 0:
                ax_x, ax_y = 0, 0
            elif file_index == 1:
                ax_x, ax_y = 0, 1
            elif file_index == 2:
                ax_x, ax_y = 1, 0
            else:
                ax_x, ax_y = 1, 1

            Nx, Ny, Nz = full_data.shape

            full_data.dose *= 8.2573429808917e13  # scale to maximum individual dwell time

            full_data.dose /= 5  # normalize to desired dose of 5 Gy
            full_data.dose *= 100  # express in percent. Should see 100% at x=-2cm

            x_min, x_max = full_data.x_extent
            y_min, y_max = full_data.y_extent
            z_min, z_max = full_data.z_extent

            xy_contour = ax[ax_x, ax_y].contourf(
                linspace(x_min, x_max, Nx), linspace(y_min, y_max, Ny),
                # matplotlib plots column by row (instead of row by column)
                # so transpose data array to account for this
                full_data.dose[:, :, z_position_to_index[0.0]].transpose(),
                arange(0, 110, 10),
                # [5, 10, 20, 50, 100],
                # cmap=get_cmap('gnuplot')
            )
            ax[ax_x, ax_y].set_title(shield_type_lst[file_index], fontsize=15)

            xz_contour = ax2[ax_x, ax_y].contourf(
                linspace(x_min, x_max, Nx), linspace(z_min, z_max, Nz),
                # matplotlib plots column by row (instead of row by column)
                # so transpose data array to account for this
                full_data.dose[:, y_position_to_index[0.0], :].transpose(),
                arange(0, 110, 10),
                # [5, 10, 20, 50, 100],
                # cmap=get_cmap('gnuplot')
            )
            ax2[ax_x, ax_y].set_title(shield_type_lst[file_index], fontsize=15)

        for n in xrange(2):
            for m in xrange(2):

                # ax[n, m].grid(True)
                ax[n, m].xaxis.set_tick_params(
                    labelsize=14, top=True, direction='in'
                    )
                ax[n, m].yaxis.set_tick_params(
                    labelsize=14, right=True, direction='in'
                    )
                ax[n, m].set_xticks(arange(x_min, x_max + 1, 2))
                ax[n, m].set_yticks(arange(y_min, y_max + 1, 2))
            
                ax[n, m].vlines([-2, 2], -10, 10, linestyles='dashed', lw=2.0)
                ax[n, m].hlines([-2, 2], -10, 10, linestyles='dashed', lw=2.0)

                # ax2[n, m].grid(True)
                ax2[n, m].xaxis.set_tick_params(
                    labelsize=14, top=True, direction='in'
                    )
                ax2[n, m].yaxis.set_tick_params(
                    labelsize=14, right=True, direction='in'
                    )
                ax2[n, m].set_xticks(arange(x_min, x_max + 1, 2))
                ax2[n, m].set_yticks(arange(y_min, y_max + 1, 2))

                ax2[n, m].vlines([-2, 2], -10, 10, linestyles='dashed', lw=2.0)
                

        fig.text(
            0.01, 0.51, 'y-axis (cm)',
            fontsize=27, rotation='vertical', va='center'
        )
        fig.text(
            0.43, 0.03, 'x-axis (cm)', fontsize=27, va='center'
        )
        fig.text(
            0.52, 0.95,
            'Isodose Contours \n With Volume Correction; ncase = 5E9',
            fontsize=27, va='center', ha='center'
        )

        cax = fig.add_axes([0.91, 0.13, 0.01, 0.7])
        cbar1 = fig.colorbar(
            xy_contour, cax=cax, orientation='vertical',
            ax=ax
        )
        cbar1.set_label('Percentage Isodose (%)', fontsize=24)
        cbar1.ax.tick_params(labelsize=14)
        fig.tight_layout()

        left = 0.1  # the left side of the subplots of the figure
        right = 0.89    # the right side of the subplots of the figure
        bottom = 0.09   # the bottom of the subplots of the figure
        top = 0.88     # the top of the subplots of the figure
        # wspace = 0.2  # the amount of width reserved for blank space between subplots
        # hspace = 0.2  # the amount of height reserved for white space between subplotss

        fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top)

        fig.savefig(
            pwd + '/xy_isodose_profile_' + vox_size_lst[fig_index] + '.pdf'
        )

        fig2.text(
            0.01, 0.51, 'z-axis (cm)',
            fontsize=27, rotation='vertical', va='center'
        )
        fig2.text(
            0.43, 0.03, 'x-axis (cm)', fontsize=27, va='center'
        )
        fig2.text(
            0.52, 0.95,
            'Isodose Contours \n With Volume Correction; ncase = 1E9',
            fontsize=27, va='center', ha='center'
        )
        cax2 = fig2.add_axes([0.91, 0.13, 0.01, 0.7])
        cbar2 = fig2.colorbar(
            xz_contour, cax=cax2, orientation='vertical',
            ax=ax
        )
        cbar2.set_label('Percentage Isodose (%)', fontsize=24)
        cbar2.set_clim([0, 100])
        cbar2.ax.tick_params(labelsize=14)

        fig2.tight_layout()

        left = 0.1  # the left side of the subplots of the figure
        right = 0.89    # the right side of the subplots of the figure
        bottom = 0.09   # the bottom of the subplots of the figure
        top = 0.88     # the top of the subplots of the figure
        # wspace = 0.2  # the amount of width reserved for blank space between subplots
        # hspace = 0.2  # the amount of height reserved for white space between subplotss

        fig2.subplots_adjust(left=left, bottom=bottom, right=right, top=top)

        fig2.savefig(
            pwd + '/xz_isodose_profile_' + vox_size_lst[fig_index] + '.pdf'
        )

def inverse_isodose_plot():
    """
    Description:
    Takes any number of .3ddose files and plots a plethora of diagnostic plots 
    from the data

    Inputs:
    :name list_file: a list of file names that are to be loaded
    :type list_file: list
    """

    pwd = getcwd()

    # target_dir = '/Users/JLucero/MPhysProj/results_not_to_git' # for home
    target_dir = '/Users/student/research/results_not_to_git'  # for work

    file_list = [
        target_dir +
        '/mlwa_0shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_90shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_180shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
        target_dir +
        '/mlwa_270shield_{0}_sim.phantom_wo_applicator_wo_box.3ddose',
    ]

    shield_type_lst = [
        'Unshielded',
        r'$90^{\circ}$ shield',
        r'$180^{\circ}$ shield',
        r'$270^{\circ}$ shield'
    ]

    vox_size_lst = [
        '1mm',
        '2mm'
    ]

    vox_size_txt_lst = [
        '1pt0mm',
        '2pt0mm'
    ]

    for fig_index in xrange(len(vox_size_lst)):

        fig, ax = subplots(
            2, 2, figsize=(12, 12),
            sharex='all', sharey='all'
        )
        fig2, ax2 = subplots(
            2, 2, figsize=(12, 12),
            sharex='all', sharey='all'
        )

        for file_index, file in enumerate(file_list):

            full_data = DoseFile(file.format(vox_size_txt_lst[fig_index]))

            y_position_to_index = {
                position:index 
                for index, position in enumerate(full_data.positions[1])
            }
            z_position_to_index = {
                position:index 
                for index, position in enumerate(full_data.positions[2])
            }

            if file_index == 0:
                ax_x, ax_y = 0, 0
            elif file_index == 1:
                ax_x, ax_y = 0, 1
            elif file_index == 2:
                ax_x, ax_y = 1, 0
            else:
                ax_x, ax_y = 1, 1

            Nx, Ny, Nz = full_data.shape

            full_data.dose *= 8.2573429808917e13  # scale to maximum individual dwell time

            full_data.dose /= 5  # normalize to desired dose of 5 Gy
            full_data.dose *= 100  # express in percent. Should see 100% at x=-2cm

            x_min, x_max = full_data.x_extent
            y_min, y_max = full_data.y_extent
            z_min, z_max = full_data.z_extent

            xy_contour = ax[ax_x, ax_y].contourf(
                linspace(x_min, x_max, Nx), linspace(y_min, y_max, Ny),
                # matplotlib plots column by row (instead of row by column)
                # so transpose data array to account for this
                full_data.dose[:, :, z_position_to_index[0.0]].transpose(),
                arange(0, 110, 10),
                # [5, 10, 20, 50, 100],
                # cmap=get_cmap('gnuplot')
            )
            ax[ax_x, ax_y].set_title(shield_type_lst[file_index], fontsize=15)

            xz_contour = ax2[ax_x, ax_y].contourf(
                linspace(x_min, x_max, Nx), linspace(z_min, z_max, Nz),
                # matplotlib plots column by row (instead of row by column)
                # so transpose data array to account for this
                full_data.dose[:, y_position_to_index[0.0], :].transpose(),
                arange(0, 110, 10),
                # [5, 10, 20, 50, 100],
                # cmap=get_cmap('gnuplot')
            )
            ax2[ax_x, ax_y].set_title(shield_type_lst[file_index], fontsize=15)

        for n in xrange(2):
            for m in xrange(2):

                # ax[n, m].grid(True)
                ax[n, m].xaxis.set_tick_params(
                    labelsize=14, top=True, direction='in'
                    )
                ax[n, m].yaxis.set_tick_params(
                    labelsize=14, right=True, direction='in'
                    )
                ax[n, m].set_xticks(arange(x_min, x_max + 1, 2))
                ax[n, m].set_yticks(arange(y_min, y_max + 1, 2))
            
                ax[n, m].vlines([-2, 2], -10, 10, linestyles='dashed', lw=2.0)
                ax[n, m].hlines([-2, 2], -10, 10, linestyles='dashed', lw=2.0)

                # ax2[n, m].grid(True)
                ax2[n, m].xaxis.set_tick_params(
                    labelsize=14, top=True, direction='in'
                    )
                ax2[n, m].yaxis.set_tick_params(
                    labelsize=14, right=True, direction='in'
                    )
                ax2[n, m].set_xticks(arange(x_min, x_max + 1, 2))
                ax2[n, m].set_yticks(arange(y_min, y_max + 1, 2))

                ax2[n, m].vlines([-2, 2], -10, 10, linestyles='dashed', lw=2.0)
                

        fig.text(
            0.01, 0.51, 'y-axis (cm)',
            fontsize=27, rotation='vertical', va='center'
        )
        fig.text(
            0.43, 0.03, 'x-axis (cm)', fontsize=27, va='center'
        )
        fig.text(
            0.52, 0.95,
            'Isodose Contours \n With Volume Correction; ncase = 5E9',
            fontsize=27, va='center', ha='center'
        )

        cax = fig.add_axes([0.91, 0.13, 0.01, 0.7])
        cbar1 = fig.colorbar(
            xy_contour, cax=cax, orientation='vertical',
            ax=ax
        )
        cbar1.set_label('Percentage Isodose (%)', fontsize=24)
        cbar1.ax.tick_params(labelsize=14)
        fig.tight_layout()

        left = 0.1  # the left side of the subplots of the figure
        right = 0.89    # the right side of the subplots of the figure
        bottom = 0.09   # the bottom of the subplots of the figure
        top = 0.88     # the top of the subplots of the figure
        # wspace = 0.2  # the amount of width reserved for blank space between subplots
        # hspace = 0.2  # the amount of height reserved for white space between subplotss

        fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top)

        fig.savefig(
            pwd + '/xy_isodose_profile_' + vox_size_lst[fig_index] + '.pdf'
        )

        fig2.text(
            0.01, 0.51, 'z-axis (cm)',
            fontsize=27, rotation='vertical', va='center'
        )
        fig2.text(
            0.43, 0.03, 'x-axis (cm)', fontsize=27, va='center'
        )
        fig2.text(
            0.52, 0.95,
            'Isodose Contours \n With Volume Correction; ncase = 1E9',
            fontsize=27, va='center', ha='center'
        )
        cax2 = fig2.add_axes([0.91, 0.13, 0.01, 0.7])
        cbar2 = fig2.colorbar(
            xz_contour, cax=cax2, orientation='vertical',
            ax=ax
        )
        cbar2.set_label('Percentage Isodose (%)', fontsize=24)
        cbar2.set_clim([0, 100])
        cbar2.ax.tick_params(labelsize=14)

        fig2.tight_layout()

        left = 0.1  # the left side of the subplots of the figure
        right = 0.89    # the right side of the subplots of the figure
        bottom = 0.09   # the bottom of the subplots of the figure
        top = 0.88     # the top of the subplots of the figure
        # wspace = 0.2  # the amount of width reserved for blank space between subplots
        # hspace = 0.2  # the amount of height reserved for white space between subplotss

        fig2.subplots_adjust(left=left, bottom=bottom, right=right, top=top)

        fig2.savefig(
            pwd + '/xz_isodose_profile_' + vox_size_lst[fig_index] + '.pdf'
        )

if __name__ == "__main__":
    # dose_position_plots()
    # dose_inv_position_plots()
    isodose_plot()
    # inverse_isodose_plot()