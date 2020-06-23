

import numpy as np
# from networkx.drawing.nx_agraph import to_agraph
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import corner
from cycler import cycler
import os
from IPython.display import Image, display

from .selection import dots_w_bars_evidence, dots_wo_bars_likelihood_max, dots_wo_bars_bic, dots_wo_bars_evidence_from_bic
import warnings
# NOTE: mark as comment for cluster computations
# import graphviz

# dynesty plotting utilities
from dynesty import plotting as dyplot

__all__ = ["net_main_plot", "net_hidden_plot",
            "sim_counts_plot", "sim_mean_plot", "sim_variance_plot", "sim_covariance_plot",
            "data_mean_plot", "data_variance_plot", "data_covariance_plot",
            "data_hist_variables_plot", "data_hist_waiting_times_plot", "data_variable_scatter_plot",
            "selection_plot", "est_runplot", "est_traceplot",
            "est_parameter_plot", "est_corner_plot", "est_corner_kernel_plot",
            "est_corner_weight_plot", "est_corner_bounds_plot", "est_chains_plot",
            "est_bestfit_mean_plot", "est_bestfit_variance_plot", "est_bestfit_covariance_plot"]

###############################
### MAIN PLOTTING FUNCTIONS ###
###############################

def net_main_plot(net, node_settings=None, edge_settings=None,
                                            layout=None, show=True, save=None):
    """docstring for ."""

    # if not given, create some default node settings
    if node_settings==None:
        nodes = list(net.net_nodes_identifier.values())
        colors = sns.color_palette('Set2', n_colors=len(nodes)).as_hex()
        node_settings = dict()

        for i, node in enumerate(nodes):
            node_settings[node] = {'label': node, 'color': colors[i]}

    # if not given, create some default edge settings
    if edge_settings==None:
        edge_settings = dict()
        for rate in net.net_rates_identifier.values():
            edge_settings[rate] = {'label': rate, 'color': 'black'}

    # create net object with plotting info for graphviz
    net_graphviz, layout_engine = net.draw_main_network_graph(node_settings, edge_settings)
    pdot = nx.drawing.nx_pydot.to_pydot(net_graphviz)

    # overwrite default layout_engine if specified
    if layout!=None:
        layout_engine = layout

    # save/show figure
    if save!=None:
        pdot.write_pdf(save, prog=layout_engine)

    if show:
        display(Image(pdot.create_png(prog=layout_engine)))


def net_hidden_plot(net, node_settings=None, edge_settings=None,
                                            layout=None, show=True, save=None):
    """docstring for ."""

    # if not given, create some default node settings
    if node_settings==None:
        nodes = list(net.net_nodes_identifier.values())
        colors = sns.color_palette('Set2', n_colors=len(nodes)).as_hex()
        node_settings = dict()

        for i, node in enumerate(nodes):
            node_settings[node] = {'label': node, 'color': colors[i]}

    # if not given, create some default edge settings
    if edge_settings==None:
        edge_settings = dict()
        for rate in net.net_rates_identifier.values():
            edge_settings[rate] = {'label': rate, 'color': 'black'}

    # create net object with plotting info for graphviz
    net_graphviz, layout_engine = net.draw_hidden_network_graph(node_settings, edge_settings)
    pdot = nx.drawing.nx_pydot.to_pydot(net_graphviz)

    # overwrite default layout_engine if specified
    if layout!=None:
        layout_engine = layout

    # save/show figure
    if save!=None:
        pdot.write_pdf(save, prog=layout_engine)

    if show:
        display(Image(pdot.create_png(prog=layout_engine)))


def sim_counts_plot(sim, settings=None,
                    x_label='Time', x_lim=None, x_log=False,
                    y_label='Counts', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [sim.sim_variables_identifier[var[0]][0] for var in sim.sim_variables_order[0]]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': var, 'color': colors[i]}

    # create plotting information from simulation
    x_arr, y_arr, attributes = sim.line_evolv_counts(settings)

    # plot by line_evolv utility plotting function
    line_evolv(x_arr, y_arr, attributes,
                    x_label=x_label, x_lim=x_lim, x_log=x_log,
                    y_label=y_label, y_lim=y_lim, y_log=y_log,
                    show=show, save=save)

    pass


def sim_mean_plot(sim, settings=None,
                    x_label='Time', x_lim=None, x_log=False,
                    y_label='Mean', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [sim.sim_variables_identifier[var[0]][0] for var in sim.sim_variables_order[0]]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'E({var})', 'color': colors[i]}

    # create plotting information from simulation
    x_arr, y_arr, attributes = sim.line_evolv_mean(settings)

    # plot by line_evolv utility plotting function
    line_evolv(x_arr, y_arr, attributes,
                    x_label=x_label, x_lim=x_lim, x_log=x_log,
                    y_label=y_label, y_lim=y_lim, y_log=y_log,
                    show=show, save=save)


def sim_variance_plot(sim, settings=None,
                    x_label='Time', x_lim=None, x_log=False,
                    y_label='Variance', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [(sim.sim_variables_identifier[var[0]][0], sim.sim_variables_identifier[var[1]][0])
                    for var in sim.sim_variables_order[1] if var[0]==var[1]]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'Var({var[0]})', 'color': colors[i]}

    # create plotting information from simulation
    x_arr, y_arr, attributes = sim.line_evolv_variance(settings)

    # plot by line_evolv utility plotting function
    line_evolv(x_arr, y_arr, attributes,
                    x_label=x_label, x_lim=x_lim, x_log=x_log,
                    y_label=y_label, y_lim=y_lim, y_log=y_log,
                    show=show, save=save)


def sim_covariance_plot(sim, settings=None,
                    x_label='Time', x_lim=None, x_log=False,
                    y_label='Covariance', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [(sim.sim_variables_identifier[var[0]][0], sim.sim_variables_identifier[var[1]][0])
                    for var in sim.sim_variables_order[1] if var[0]!=var[1]]
        colors = sns.color_palette('muted', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'Cov({var[0]}, {var[1]})', 'color': colors[i]}

    # create plotting information from simulation
    x_arr, y_arr, attributes = sim.line_evolv_covariance(settings)

    # plot by line_evolv utility plotting function
    line_evolv(x_arr, y_arr, attributes,
                    x_label=x_label, x_lim=x_lim, x_log=x_log,
                    y_label=y_label, y_lim=y_lim, y_log=y_log,
                    show=show, save=save)


def data_mean_plot(data, settings=None,
                    x_label='Time', x_lim=None, x_log=False,
                    y_label='Mean', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [d['variables'] for d in data.data_mean_order]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'E({var})', 'color': colors[i]}

    # create plotting information from data
    x_arr, y_arr, attributes = data.dots_w_bars_evolv_mean(settings)

    # plot by dots_w_bars_evolv utility plotting function
    dots_w_bars_evolv(x_arr, y_arr, attributes,
                    x_label=x_label, x_lim=x_lim, x_log=x_log,
                    y_label=y_label, y_lim=y_lim, y_log=y_log,
                    show=show, save=save)


def data_variance_plot(data, settings=None,
                    x_label='Time', x_lim=None, x_log=False,
                    y_label='Variance', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [d['variables'] for d in data.data_variance_order]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'Var({var[0]})', 'color': colors[i]}

    # create plotting information from data
    x_arr, y_arr, attributes = data.dots_w_bars_evolv_variance(settings)

    # plot by dots_w_bars_evolv utility plotting function
    dots_w_bars_evolv(x_arr, y_arr, attributes,
                    x_label=x_label, x_lim=x_lim, x_log=x_log,
                    y_label=y_label, y_lim=y_lim, y_log=y_log,
                    show=show, save=save)


def data_covariance_plot(data, settings=None,
                    x_label='Time', x_lim=None, x_log=False,
                    y_label='Covariance', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [d['variables'] for d in data.data_covariance_order]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'Cov({var[0]}, {var[1]})', 'color': colors[i]}

    # create plotting information from data
    x_arr, y_arr, attributes = data.dots_w_bars_evolv_covariance(settings)

    # plot by dots_w_bars_evolv utility plotting function
    dots_w_bars_evolv(x_arr, y_arr, attributes,
                    x_label=x_label, x_lim=x_lim, x_log=x_log,
                    y_label=y_label, y_lim=y_lim, y_log=y_log,
                    show=show, save=save)


def data_hist_variables_plot(data, time_ind, settings=None, normalised=False,
                            x_label='Variable counts', x_lim=None, x_log=False,
                            y_label='Frequency', y_lim=None, y_log=False,
                            show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [d for d in data.data_variables]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': var, 'color': colors[i], 'opacity': 0.5}

    # create plotting information from data
    bar_arr, bar_attributes = data.histogram_discrete_cell_counts_at_time_point(time_ind, settings)

    # plot by histogram_discrete utility plotting function
    histogram_discrete(bar_arr, bar_attributes, normalised=normalised,
                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                            show=show, save=save)


def data_hist_waiting_times_plot(data, data_events, settings=None,
                            normalised=True, gamma_fit=True,
                            x_label='Waiting time', x_lim=None, x_log=False,
                            y_label='Frequency', y_lim=None, y_log=False,
                            show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = {'label': 'Event waiting times', 'opacity': 1.0,
                    'color': 'orange', 'gamma_color': 'darkorange'}

    # create plotting information from data and
    # plot by respective continuous histogram utility plotting functions
    if gamma_fit:
        normalised = True # overwrite normalised, gamma fit currently only as pdf
        bar_arr, bar_attributes, gamma_fit_func = data.histogram_continuous_event_waiting_times_w_gamma_fit(data_events, settings)
        histogram_continuous_w_line(bar_arr, bar_attributes, gamma_fit_func, normalised=normalised,
                                x_label=x_label, x_lim=x_lim, x_log=x_log,
                                y_label=y_label, y_lim=y_lim, y_log=y_log,
                                show=show, save=save)
    else:
        bar_arr, bar_attributes = data.histogram_continuous_event_waiting_times(data_events, settings)
        histogram_continuous(bar_arr, bar_attributes, normalised=normalised,
                                x_label=x_label, x_lim=x_lim, x_log=x_log,
                                y_label=y_label, y_lim=y_lim, y_log=y_log,
                                show=show, save=save)


def data_variable_scatter_plot(data, time_ind, variable1, variable2, settings=None,
                                x_label=None, x_lim=None, x_log=False,
                                y_label=None, y_lim=None, y_log=False,
                                show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = {'color': 'orange', 'opacity': 0.5, 'label': None}

    # create plotting information from data
    x_arr, y_arr, attributes = data.scatter_at_time_point(variable1, variable2, time_ind, settings)

    # plot by scatter utility plotting function
    scatter(x_arr, y_arr, attributes,
                                x_label=x_label, x_lim=x_lim, x_log=x_log,
                                y_label=y_label, y_lim=y_lim, y_log=y_log,
                                show=show, save=save)


def selection_plot(estimation_instances, est_type='evidence',
                    settings=None, show_errorbar=True,
                    x_label=None, x_lim=None, x_log=False,
                    y_label=None, y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        est_names = [est.est_name for est in estimation_instances]
        settings = dict()

        for i, est_name in enumerate(est_names):
            settings[est_name] = {'label': est_name, 'color': 'orange'}

    # create plotting information from estimation_instances
    if est_type=='evidence':
        y_label = 'Log(Evidence)'
        y_arr_err, x_ticks, attributes = dots_w_bars_evidence(estimation_instances, settings)
    elif est_type=='likelihood':
        y_label = 'Max. Log(Likelihood)'
        y_arr_err, x_ticks, attributes = dots_wo_bars_likelihood_max(estimation_instances, settings)
    elif est_type=='bic':
        y_label = 'BIC'
        y_arr_err, x_ticks, attributes = dots_wo_bars_bic(estimation_instances, settings)
    elif est_type=='evidence_from_bic':
        y_label = 'Log(Evidence) [approx. from BIC]'
        y_arr_err, x_ticks, attributes = dots_wo_bars_evidence_from_bic(estimation_instances, settings)
    else:
        warnings.warn('Unknown est_type for model selection plot; default est_type will be used')
        y_label = 'Log(Evidence)'
        y_arr_err, x_ticks, attributes = dots_w_bars_evidence(estimation_instances, settings)

    # plot by dots_w_bars utility plotting function
    dots_w_bars(y_arr_err, x_ticks, attributes, show_errorbar=show_errorbar,
                x_label=x_label, x_lim=x_lim, x_log=x_log,
                y_label=y_label, y_lim=y_lim, y_log=y_log,
                show=show, save=save)


def est_runplot(estimation, color='limegreen', show=True, save=None):
    """docstring for ."""

    # get plotting information from estimation instance
    sampler_result = estimation.bay_nested_sampler_res

    # generate plot by dynesty plotting methods
    fig, ax = dyplot.runplot(sampler_result, color=color)

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def est_traceplot(estimation, settings=None, show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = dict()
        for theta_id in estimation.net.net_theta_symbolic:
            param = estimation.net.net_rates_identifier[theta_id]
            settings[param] = {'label': param}

    # get plotting information from estimation instance
    sampler_result, params_labels = estimation.sampling_res_and_labels(settings)

    # generate plot by dynesty plotting methods
    fig, axes = dyplot.traceplot(sampler_result,
                         show_titles=True,
                         post_color='dodgerblue',
                         connect_color='darkorange',
                         trace_cmap='magma',
                         connect=True,
                         connect_highlight=range(5),
                         labels=params_labels #, title_fmt='.4f'
                         )

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def est_parameter_plot(estimation, settings=None, show_errorbar=True,
            x_label=None, x_lim=None,
            y_label="Parameter values", y_lim=None, y_log=False,
            show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = dict()
        for theta_id in estimation.net.net_theta_symbolic:
            param = estimation.net.net_rates_identifier[theta_id]
            settings[param] = {'label': param, 'color': 'dodgerblue'}

    # create plotting information from estimation instance
    y_arr_err, x_ticks, attributes = estimation.dots_w_bars_parameters(settings)

    # plot by dots_w_bars utility plotting function
    dots_w_bars(y_arr_err, x_ticks, attributes, show_errorbar=show_errorbar,
                x_label=x_label, x_lim=x_lim, x_log=False,
                y_label=y_label, y_lim=y_lim, y_log=y_log,
                show=show, save=save)


def est_corner_plot(estimation, settings=None, show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = dict()
        for theta_id in estimation.net.net_theta_symbolic:
            param = estimation.net.net_rates_identifier[theta_id]
            settings[param] = {'label': param}

    # get plotting information from estimation instance
    samples, labels = estimation.samples_corner_parameters(settings)

    # use corner package for this plot
    fig = corner.corner(samples, labels=labels)

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def est_corner_kernel_plot(estimation, settings=None, show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = dict()
        for theta_id in estimation.net.net_theta_symbolic:
            param = estimation.net.net_rates_identifier[theta_id]
            settings[param] = {'label': param}

    # get plotting information from estimation instance
    sampler_result, params_labels = estimation.sampling_res_and_labels(settings)

    # generate plot by dynesty plotting methods
    fig, axes = dyplot.cornerplot(sampler_result,
                            color='dodgerblue',
                            show_titles=True,
                            labels=params_labels,
                            title_fmt='.4f')
    fig.tight_layout()

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def est_corner_weight_plot(estimation, settings=None, show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = dict()
        for theta_id in estimation.net.net_theta_symbolic:
            param = estimation.net.net_rates_identifier[theta_id]
            settings[param] = {'label': param}

    # get plotting information from estimation instance
    sampler_result, params_labels = estimation.sampling_res_and_labels(settings)

    # generate plot by dynesty plotting methods
    fig, axes = dyplot.cornerpoints(sampler_result,
                         cmap='magma',
                         labels=params_labels)

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def est_corner_bounds_plot(estimation, num_iter=14, settings=None, show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        settings = dict()
        for theta_id in estimation.net.net_theta_symbolic:
            param = estimation.net.net_rates_identifier[theta_id]
            settings[param] = {'label': param}

    # get plotting information from estimation instance
    sampler_result, params_labels, prior_transform = estimation.sampling_res_and_labels_and_priortransform(settings)

    # create subplots
    num_it_segs = num_iter
    num_it_total = sampler_result.niter
    num_subplot_rows = int(np.ceil(num_it_segs/3.0))
    fig, axes = plt.subplots(num_subplot_rows, 3, figsize=(num_subplot_rows*3, 3*3))

    # make square
    for ax in axes.flatten():
        ax.set(aspect='equal')

    # turn excess subplots off
    for i in range(num_it_segs, num_subplot_rows*3):
        axes.flatten()[i].set_axis_off()

    # actual plotting
    for it_plot in range(num_it_segs):
        it_num = int(it_plot * num_it_total / float(num_it_segs - 1))
        it_num = min(num_it_total, it_num)

        dyplot.cornerbound(sampler_result,
                    it=it_num,
                    prior_transform=prior_transform,
                    color='lightgrey',
                    show_live=True,
                    live_color='darkorange',
                    labels=params_labels,
                    fig=(fig, axes.flatten()[it_plot]))

    plt.tight_layout()

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig)


def est_chains_plot(estimation, weighted=True,
                    x_label='Sample iteration', x_lim=None, x_log=False,
                    y_label='Parameter values', y_lim=None, y_log=False,
                    show=True, save=None):
    """docstring for ."""

    # get plotting information from estimation instance
    if weighted:
        samples, num_params = estimation.samples_weighted_chains_parameters()
    else:
        samples, num_params = estimation.samples_chains_parameters()

    # generate plot
    fig = plt.figure()
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # set a color cycle for the different params
    colormap = plt.cm.viridis
    plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 1, num_params)]))

    plt.plot(samples, alpha=0.75)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def est_bestfit_mean_plot(estimation, settings=None, data=True, conf=True,
                            x_label='Time', x_lim=None, x_log=False,
                            y_label='Mean', y_lim=None, y_log=False,
                            show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [estimation.net_simulation.sim_variables_identifier[var[0]][0] for var in estimation.net_simulation.sim_variables_order[0]]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'E({var})', 'color': colors[i]}

    # create plotting information from estimation instance and
    # plot by respective utility plotting function
    if data:
        if conf:
            x_arr_dots, x_arr_line, y_dots_err, y_line, y_lower, y_upper, attributes = estimation.dots_w_bars_and_line_w_band_evolv_mean_confidence(settings)

            dots_w_bars_and_line_w_band_evolv(x_arr_dots, x_arr_line, y_dots_err,
                                            y_line, y_lower, y_upper, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)
        else:
            x_arr_dots, x_arr_line, y_dots_err, y_line, attributes = estimation.dots_w_bars_and_line_evolv_bestfit_mean_data(settings)

            dots_w_bars_and_line_evolv(x_arr_dots, x_arr_line, y_dots_err, y_line, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)

    else:
        if conf:
            x_arr, y_line, y_lower, y_upper, attributes = estimation.line_w_band_evolv_mean_confidence(settings)

            line_w_band_evolv(x_arr, y_line, y_lower, y_upper, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)
        else:
            x_arr, y_arr, attributes = estimation.line_evolv_bestfit_mean(settings)

            line_evolv(x_arr, y_arr, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)


def est_bestfit_variance_plot(estimation, settings=None, data=True, conf=True,
                            x_label='Time', x_lim=None, x_log=False,
                            y_label='Variance', y_lim=None, y_log=False,
                            show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [(estimation.net_simulation.sim_variables_identifier[var[0]][0], estimation.net_simulation.sim_variables_identifier[var[1]][0])
                    for var in estimation.net_simulation.sim_variables_order[1] if var[0]==var[1]]
        colors = sns.color_palette('Set2', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'Var({var[0]})', 'color': colors[i]}

    # create plotting information from estimation instance and
    # plot by respective utility plotting function
    if data:
        if conf:
            x_arr_dots, x_arr_line, y_dots_err, y_line, y_lower, y_upper, attributes = estimation.dots_w_bars_and_line_w_band_evolv_variance_confidence(settings)

            dots_w_bars_and_line_w_band_evolv(x_arr_dots, x_arr_line, y_dots_err,
                                            y_line, y_lower, y_upper, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)
        else:
            x_arr_dots, x_arr_line, y_dots_err, y_line, attributes = estimation.dots_w_bars_and_line_evolv_bestfit_variance_data(settings)

            dots_w_bars_and_line_evolv(x_arr_dots, x_arr_line, y_dots_err, y_line, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)

    else:
        if conf:
            x_arr, y_line, y_lower, y_upper, attributes = estimation.line_w_band_evolv_variance_confidence(settings)

            line_w_band_evolv(x_arr, y_line, y_lower, y_upper, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)
        else:
            x_arr, y_arr, attributes = estimation.line_evolv_bestfit_variance(settings)

            line_evolv(x_arr, y_arr, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)


def est_bestfit_covariance_plot(estimation, settings=None, data=True, conf=True,
                            x_label='Time', x_lim=None, x_log=False,
                            y_label='Covariance', y_lim=None, y_log=False,
                            show=True, save=None):
    """docstring for ."""

    # if not given, create some default settings
    if settings==None:
        vars = [(estimation.net_simulation.sim_variables_identifier[var[0]][0], estimation.net_simulation.sim_variables_identifier[var[1]][0])
                    for var in estimation.net_simulation.sim_variables_order[1] if var[0]!=var[1]]
        colors = sns.color_palette('muted', n_colors=len(vars)).as_hex()
        settings = dict()

        for i, var in enumerate(vars):
            settings[var] = {'label': f'Cov({var[0]}, {var[1]})', 'color': colors[i]}

    # create plotting information from estimation instance and
    # plot by respective utility plotting function
    if data:
        if conf:
            x_arr_dots, x_arr_line, y_dots_err, y_line, y_lower, y_upper, attributes = estimation.dots_w_bars_and_line_w_band_evolv_covariance_confidence(settings)

            dots_w_bars_and_line_w_band_evolv(x_arr_dots, x_arr_line, y_dots_err,
                                            y_line, y_lower, y_upper, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)
        else:
            x_arr_dots, x_arr_line, y_dots_err, y_line, attributes = estimation.dots_w_bars_and_line_evolv_bestfit_covariance_data(settings)

            dots_w_bars_and_line_evolv(x_arr_dots, x_arr_line, y_dots_err, y_line, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)

    else:
        if conf:
            x_arr, y_line, y_lower, y_upper, attributes = estimation.line_w_band_evolv_covariance_confidence(settings)

            line_w_band_evolv(x_arr, y_line, y_lower, y_upper, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)
        else:
            x_arr, y_arr, attributes = estimation.line_evolv_bestfit_covariance(settings)

            line_evolv(x_arr, y_arr, attributes,
                                            x_label=x_label, x_lim=x_lim, x_log=x_log,
                                            y_label=y_label, y_lim=y_lim, y_log=y_log,
                                            show=show, save=save)


##################################
### PLOTTING UTILITY FUNCTIONS ###
##################################

def dots_w_bars(y_arr_err, x_ticks, attributes, show_errorbar=True,
                x_label=None, x_lim=None, x_log=False,
                y_label=None, y_lim=None, y_log=False,
                show=True, save=None):
    """
    Plot dots with error bars (values in y axis, iteration over x axis).

    parameters
    ----------
    y_arr_err
        numpy array with shape (# dots, 2); errors are given in the second
        dimension
    attributes
        dictionary specifying the keys 'color'
    x_ticks (set None to ignore)
        list of labels for dots which are plotted below x axis.
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'


    example
    -------
    y_arr_err = np.array([
    [1, 0.2],
    [2, 0.8],
    [3, 0.3]
    ])

    x_ticks = ['a', 'b', 'c']

    attributes = {'color': 'dodgerblue'}

    output = {'output_folder': './test_figures',
            'plot_name': 'fig_test_dots_bars'}
    """

    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # actual plotting
    for dot_ind in range(y_arr_err.shape[0]):
        plt.errorbar(dot_ind + 1, y_arr_err[dot_ind, 0],
                    yerr=np.array([y_arr_err[dot_ind, 1], y_arr_err[dot_ind, 2]]).reshape(2,1) if show_errorbar else None,
                    fmt='o', capsize=4, elinewidth=2.5, markeredgewidth=2.5,
                    markersize=5, markeredgecolor=attributes[dot_ind][1],
                    color=attributes[dot_ind][1], ecolor='lightgrey')

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    if x_ticks != None:
        plt.xticks([i + 1 for i in range(y_arr_err.shape[0])],
                    [x_ticks[i] for i in range(y_arr_err.shape[0])], rotation=55)

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def dots_w_bars_evolv(x_arr, y_arr_err, var_attributes,
                        x_label=None, x_lim=None, x_log=False,
                        y_label=None, y_lim=None, y_log=False,
                        show=True, save=None):
    """
    Plot multiple evolving (e.g. over time) dots with error bars.

    parameters
    ----------
    x_arr
        numpy array with shape (# time points, )
    y_arr_err
        numpy array with shape (# variables, # time points, 2); third
        dimension includes [value, error value]
    var_attributes
        dictionary specifying the keys 0, 1, ..., # variables - 1
        with tuples (string for legend label, plt color code for variable)
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    x_arr = np.linspace(0, 2, num=3, endpoint=True)
    y_arr_err = np.array([
                        [[1, 0.1], [2, 0.2], [3, 0.3]],
                        [[2, 0.4], [1, 0.1], [4, 0.5]]
                        ])

    # use var_ind as specified in var_order
    var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
                    0: ('$B_t$ (OFF gene)', 'tomato')}
    output = {'output_folder': './test_figures',
            'plot_name': 'fig_test_dots_time'}
    """
    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # actual plotting
    for var_ind in range(y_arr_err.shape[0]):
        var_name = var_attributes[var_ind][0]
        var_color = var_attributes[var_ind][1]

        plt.errorbar(x_arr, y_arr_err[var_ind, :, 0], yerr=y_arr_err[var_ind, :, 1],
                    label=var_name, markeredgecolor=var_color, color=var_color, fmt='o',
                    capsize=4.0, elinewidth=2.5, markeredgewidth=2.5, markersize=4.5)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def line_evolv(x_arr, y_line, var_attributes,
                x_label=None, x_lim=None, x_log=False,
                y_label=None, y_lim=None, y_log=False,
                show=True, save=None):
    """
    Plot multiple evolving (e.g. over time) lines.

    parameters
    ----------
    x_arr
        numpy array with shape (# time points, )
    y_line
        numpy array setting the multiple lines with shape (# variables, # time points)
    var_attributes
        dictionary specifying the keys 0, 1, ..., # variables - 1
        with tuples (string for legend label, plt color code for variable)
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    x_arr = np.linspace(0, 2, num=3, endpoint=True)

    y_line = np.array([
    [1, 2, 3],
    [2, 1, 4]
    ])

    var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
                    0: ('$B_t$ (OFF gene)', 'tomato')}
    output = {'output_folder': './test_figures',
            'plot_name': 'fig_test_line_evolv'}
    """
    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # actual plotting
    for var_ind in range(y_line.shape[0]):
        var_name = var_attributes[var_ind][0]
        var_color = var_attributes[var_ind][1]

        plt.plot(x_arr, y_line[var_ind, :], label=var_name,
                        color=var_color, linewidth=2.5, zorder=2000)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def line_w_band_evolv(x_arr, y_line, y_lower, y_upper, var_attributes,
                                    x_label=None, x_lim=None, x_log=False,
                                    y_label=None, y_lim=None, y_log=False,
                                    show=True, save=None):
    """
    Plot multiple evolving (e.g. over time) lines with error/prediction bands.

    parameters
    ----------
    x_arr
        numpy array with shape (# time points, )
    y_line
        numpy array setting the multiple lines with shape (# variables, # time points)
    y_lower
        numpy array setting the lower bounds of the band
        with shape (# variables, # time points)
    y_upper
        numpy array setting the upper bounds of the band
        with shape (# variables, # time points)
    var_attributes
        dictionary specifying the keys 0, 1, ..., # variables - 1
        with tuples (string for legend label, plt color code for variable)
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    x_arr = np.linspace(0, 2, num=3, endpoint=True)

    y_line = np.array([
    [1, 2, 3],
    [2, 1, 4]
    ])

    y_lower = np.array([
    [0.5, 1, 2],
    [1.8, 0.8, 3.5]
    ])

    y_upper = np.array([
    [1.4, 2.7, 3.1],
    [2.1, 1.3, 4.4]
    ])

    var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
                    0: ('$B_t$ (OFF gene)', 'tomato')}
    output = {'output_folder': './test_figures',
            'plot_name': 'fig_test_line_band'}
    """
    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # actual plotting
    for var_ind in range(y_line.shape[0]):
        var_name = var_attributes[var_ind][0]
        var_color = var_attributes[var_ind][1]

        ax.fill_between(x_arr, y_lower[var_ind, :], y_upper[var_ind, :],
                        color=var_color, alpha=0.5, linewidth=0.0, zorder=1000)
        plt.plot(x_arr, y_line[var_ind, :], label=var_name,
                        color=var_color, linewidth=2.5, zorder=2000)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def dots_w_bars_and_line_evolv(x_arr_dots, x_arr_line,
                                            y_dots_err, y_line, var_attributes,
                                            x_label=None, x_lim=None, x_log=False,
                                            y_label=None, y_lim=None, y_log=False,
                                            show=True, save=None):
    """
    Plot multiple evolving (e.g. over time) lines with error/prediction bands.

    parameters
    ----------
    x_arr_dots
        numpy array with shape (# time points, ); used for aligment with
        y_dots_err
    x_arr_line
        numpy array with shape (# time points, ); used for aligment with
        y_line, y_lower and y_upper
    y_dots_err
        numpy array with shape (# variables, # time points, 2); third
        dimension includes [value, error value]
    y_line
        numpy array setting the multiple lines with shape (# variables, # time points)
    var_attributes
        dictionary specifying the keys 0, 1, ..., # variables - 1
        with tuples (string for legend label, plt color code for variable)
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    x_arr_dots = np.linspace(0, 1, num=2, endpoint=True)
    x_arr_line = np.linspace(0, 2, num=3, endpoint=True)
    y_dots_err = np.array([
                        [[1, 0.1], [2, 0.3]],
                        [[2, 0.4], [1, 0.5]]
                        ])
    y_line = np.array([
    [1, 2, 3],
    [2, 1, 4]
    ])
    var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
                    0: ('$B_t$ (OFF gene)', 'tomato')}
    output = {'output_folder': './test_figures',
            'plot_name': 'fig_test_line_band_dots_bars'}
    """
    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # actual plotting
    for var_ind in range(y_line.shape[0]):
        var_name = var_attributes[var_ind][0]
        var_color = var_attributes[var_ind][1]

        # ax.fill_between(x_arr_line, y_lower[var_ind, :], y_upper[var_ind, :],
        #                 color=var_color, alpha=0.5, linewidth=0.0, zorder=1000)

        # # normal version
        # plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
        #                 color=var_color, linewidth=3, zorder=3000)
        # plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
        #             fmt='o', capsize=4.0, elinewidth=2.5, #label='data' if var_ind==0 else '',
        #             markeredgewidth=2.5, markersize=4.5, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)
        # poster version
        # plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
        #                 color=var_color, linewidth=2, zorder=3000)
        # plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
        #             fmt='o', capsize=2, elinewidth=2, #label='data' if var_ind==0 else '',
        #             markeredgewidth=2, markersize=3, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)
        # paper version
        plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
                        color=var_color, linewidth=2.5, zorder=3000)
        plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
                    fmt='o', capsize=4.0, elinewidth=2.5, #label='data' if var_ind==0 else '',
                    markeredgewidth=2.5, markersize=4.5, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')
    plt.legend(frameon=False)

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def dots_w_bars_and_line_w_band_evolv(x_arr_dots, x_arr_line, y_dots_err, y_line,
                                        y_lower, y_upper, var_attributes,
                                        x_label=None, x_lim=None, x_log=False,
                                        y_label=None, y_lim=None, y_log=False,
                                        show=True, save=None):
    """
    Plot multiple evolving (e.g. over time) lines with error/prediction bands.

    parameters
    ----------
    x_arr_dots
        numpy array with shape (# time points, ); used for aligment with
        y_dots_err
    x_arr_line
        numpy array with shape (# time points, ); used for aligment with
        y_line, y_lower and y_upper
    y_dots_err
        numpy array with shape (# variables, # time points, 2); third
        dimension includes [value, error value]
    y_line
        numpy array setting the multiple lines with shape (# variables, # time points)
    y_lower
        numpy array setting the lower bounds of the band
        with shape (# variables, # time points)
    y_upper
        numpy array setting the upper bounds of the band
        with shape (# variables, # time points)
    var_attributes
        dictionary specifying the keys 0, 1, ..., # variables - 1
        with tuples (string for legend label, plt color code for variable)
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    x_arr_dots = np.linspace(0, 1, num=2, endpoint=True)
    x_arr_line = np.linspace(0, 2, num=3, endpoint=True)
    y_dots_err = np.array([
                        [[1, 0.1], [2, 0.3]],
                        [[2, 0.4], [1, 0.5]]
                        ])
    y_line = np.array([
    [1, 2, 3],
    [2, 1, 4]
    ])
    y_lower = np.array([
    [0.5, 1, 2],
    [1.8, 0.8, 3.5]
    ])
    y_upper = np.array([
    [1.4, 2.7, 3.1],
    [2.1, 1.3, 4.4]
    ])
    var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
                    0: ('$B_t$ (OFF gene)', 'tomato')}
    output = {'output_folder': './test_figures',
            'plot_name': 'fig_test_line_band_dots_bars'}
    """
    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # actual plotting
    for var_ind in range(y_line.shape[0]):
        var_name = var_attributes[var_ind][0]
        var_color = var_attributes[var_ind][1]

        ax.fill_between(x_arr_line, y_lower[var_ind, :], y_upper[var_ind, :],
                        color=var_color, alpha=0.5, linewidth=0.0, zorder=1000)
        plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
                        color=var_color, linewidth=2.5, zorder=3000)
        plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
                    fmt='o', capsize=4.0, elinewidth=2.5, #label='data' if var_ind==0 else '',
                    markeredgewidth=2.5, markersize=4.5, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def histogram_discrete(bar_arr, bar_attributes, normalised=False,
                        x_label=None, x_lim=None, x_log=False,
                        y_label=None, y_lim=None, y_log=False,
                        show=True, save=None):
    """
    Plot a histogram for discrete values.

    parameters
    ----------
    bar_arr
        numpy array of discrete values with shape (#realisations, #variables),
        histograms are computed over all realisations for each variable

    bar_attributes
        dictionary with keys specifying a general bin 'label' and bin 'color'
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    bar_arr = np.random.poisson(10, size=10).reshape(10, 1)

    bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}

    output = {'output_folder': './test_figures',
            'plot_name': 'hist_disc_test'}
    """

    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # plotting of a histogram
    try:
        bar_min = min(np.amin(bar_arr), x_lim[0])
    except:
        bar_min = np.amin(bar_arr)

    try:
        bar_max = max(np.amax(bar_arr), x_lim[1])
    except:
        bar_max = np.amax(bar_arr)

    hist_bins = np.linspace(bar_min - 0.5, bar_max + 0.5, num=int(bar_max - bar_min + 2))

    for var_ind in range(bar_arr.shape[1]):
        plt.hist(bar_arr[:, var_ind], bins=hist_bins,
            density=normalised,
            histtype='stepfilled', # step, stepfilled
            linewidth=2.0,
            align='mid', color=bar_attributes[var_ind]['color'],
            label=bar_attributes[var_ind]['label'],
            alpha=bar_attributes[var_ind]['opacity'], zorder=1-var_ind)

    # ax.set_xticks(bins + 0.5)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')
    plt.legend(frameon=False)

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def histogram_discrete_w_line(bar_arr, bar_attributes, line_function, normalised=False,
                            x_label=None, x_lim=None, x_log=False,
                            y_label=None, y_lim=None, y_log=False,
                            show=True, save=None):
    """
    Plot a histogram for discrete values with line.

    parameters
    ----------
    bar_arr
        numpy array of discrete values with shape (#realisations, #variables),
        histograms are computed over all realisations for each variable

    bar_attributes
        dictionary with keys specifying a general bin 'label' and bin 'color'
    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    bar_arr = np.random.poisson(10, size=10).reshape(10, 1)

    bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}

    output = {'output_folder': './test_figures',
            'plot_name': 'hist_disc_test'}
    """

    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # plotting of a histogram
    try:
        bar_min = min(np.amin(bar_arr), x_lim[0])
    except:
        bar_min = np.amin(bar_arr)

    try:
        bar_max = max(np.amax(bar_arr), x_lim[1])
    except:
        bar_max = np.amax(bar_arr)

    x_line_arr = np.linspace(bar_min, bar_max, num=1000, endpoint=True)
    hist_bins = np.linspace(bar_min - 0.5, bar_max + 0.5, num=bar_max - bar_min + 2)

    for var_ind in range(bar_arr.shape[1]):
        plt.hist(bar_arr[:, var_ind], bins=hist_bins,
            density=normalised,
            histtype='stepfilled', # step, stepfilled
            linewidth=2.0,
            align='mid', color=bar_attributes[var_ind]['color'],
            label=bar_attributes[var_ind]['label'],
            alpha=bar_attributes[var_ind]['opacity'])

        x_line, y_line, line_label, line_color = line_function(x_line_arr, bar_arr[:, var_ind])
        plt.plot(x_line, y_line, label=line_label, color=line_color, linewidth=2.5)

    # ax.set_xticks(bins + 0.5)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def histogram_continuous(bar_arr, bar_attributes, normalised=False,
                        x_label=None, x_lim=None, x_log=False,
                        y_label=None, y_lim=None, y_log=False,
                        show=True, save=None):
    """
    Plot a histogram for continuous values.

    parameters
    ----------
    bar_arr
        numpy array of continuous values with shape (#realisations, #variables),
        histograms are computed over all realisations for each variable

    bar_attributes
        dictionary with keys specifying a general bin 'label', bin 'color',
        bin 'edges' and bin edges 'interval_type' ('[)' (default) or '(]')

    normalised
        True or False

    interval

    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    bar_arr = np.random.poisson(10, size=10).reshape(10, 1)

    bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}

    output = {'output_folder': './test_figures',
            'plot_name': 'hist_disc_test'}
    """

    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # plotting of a histogram
    for var_ind in range(bar_arr.shape[1]):
        # read out interval type, default plt.hist() behavior are
        # half-open interval [.., ..), small epsilon shift mimicks (.., ..]
        if bar_attributes[var_ind]['interval_type']=='(]':
            epsilon = 1e-06
        else:
            epsilon = 0.0

        plt.hist(bar_arr[:, var_ind] - epsilon,
            bins=bar_attributes[var_ind]['edges'],
            density=normalised,
            histtype='stepfilled', # step, stepfilled
            linewidth=2.0,
            color=bar_attributes[var_ind]['color'],
            label=bar_attributes[var_ind]['label'],
            alpha=bar_attributes[var_ind]['opacity'])

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def histogram_continuous_w_line(bar_arr, bar_attributes, line_function, normalised=False,
                                x_label=None, x_lim=None, x_log=False,
                                y_label=None, y_lim=None, y_log=False,
                                show=True, save=None):
    """
    Plot a histogram for continuous values with line.

    parameters
    ----------
    bar_arr
        numpy array of continuous values with shape (#realisations, #variables),
        histograms are computed over all realisations for each variable

    bar_attributes
        dictionary with keys specifying a general bin 'label', bin 'color',
        bin 'edges' and bin edges 'interval_type' ('[)' (default) or '(]')

    normalised
        True or False

    interval

    output
        dictionary specifying the keys 'output_folder' and 'plot_name'

    example
    -------
    bar_arr = np.random.poisson(10, size=10).reshape(10, 1)

    bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}

    output = {'output_folder': './test_figures',
            'plot_name': 'hist_disc_test'}
    """

    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # plotting of a histogram
    for var_ind in range(bar_arr.shape[1]):
        # read out interval type, default plt.hist() behavior are
        # half-open interval [.., ..), small epsilon shift mimicks (.., ..]
        if bar_attributes[var_ind]['interval_type']=='(]':
            epsilon = 1e-06
        else:
            epsilon = 0.0

        plt.hist(bar_arr[:, var_ind] - epsilon,
            bins=bar_attributes[var_ind]['edges'],
            density=normalised,
            histtype='stepfilled', # step, stepfilled
            linewidth=2.0,
            color=bar_attributes[var_ind]['color'],
            label=bar_attributes[var_ind]['label'],
            alpha=bar_attributes[var_ind]['opacity'])

        x_line_arr = np.linspace(np.amin(bar_attributes[var_ind]['edges']),
                                np.amax(bar_attributes[var_ind]['edges']),
                                num=1000, endpoint=True)
        x_line, y_line, line_label, line_color = line_function(x_line_arr, bar_arr[:, var_ind])
        plt.plot(x_line, y_line, label=line_label, color=line_color, linewidth=2.5)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    legend = ax.legend(loc=0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


def scatter(x_arr, y_arr, attributes, x_label=None, x_lim=None, x_log=False,
                                    y_label=None, y_lim=None, y_log=False,
                                    show=True, save=None):
    """docstring for ."""

    # initialise figure and axis settings
    fig = plt.figure()

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # plotting of a histogram
    plt.scatter(x_arr, y_arr,
                color=attributes['color'],
                alpha=attributes['opacity'],
                label=attributes['label'])

    # ax.set_xticks(bins + 0.5)

    # final axis setting
    ax.set_xlim(x_lim)
    ax.set_xlabel(x_label, color="black")
    ax.set_xscale('log' if x_log==True else 'linear')
    ax.set_ylim(y_lim)
    ax.set_ylabel(y_label, color="black")
    ax.set_yscale('log' if y_log==True else 'linear')

    # add legend
    if not attributes['label']==None:
        legend = ax.legend(loc=0)
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('lightgrey')

    # save/show figure
    if save!=None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show(fig, block=False)


### class version (for reference) uncommented June 2020
### (might still contain some more code snippets for later use)
### new version above

# class Plots(object):
#     """
#     Class with multiple methods for plotting.
#
#     methods
#     -------
#     network_graph
#     samples_corner
#     samples_chains
#     dots_w_bars_evolv
#     line_evolv
#     line_w_band_evolv
#     dots_w_bars_and_line_evolv
#     dots_w_bars_and_line_w_band_evolv
#     dots_w_bars
#
#     attributes
#     ----------
#     x_axis
#         dictionary with keys specifying x axis 'label', lower and upper axis
#         'limits' and 'log' scale
#     y_axis
#         dictionary with keys specifying y axis 'label', lower and upper axis
#         'limits' and 'log' scale
#     show=False (default)
#         set to True to show plot
#
#     example
#     -------
#     x_axis = {'label': 'time',
#             'limits': (None, None),
#             'log': False}
#     y_axis = {'label': 'counts',
#             'limits': (None, None),
#             'log': False}
#     """
#     def __init__(self, x_axis, y_axis, show=True, save=False):
#         # initialise basic information
#         try:
#             self.x_label = x_axis['label']
#             self.x_lim = x_axis['limits']
#             self.x_log = x_axis['log']
#
#             self.y_label = y_axis['label']
#             self.y_lim = y_axis['limits']
#             self.y_log = y_axis['log']
#         except:
#             self.x_label = None
#             self.x_lim = None
#             self.x_log = None
#
#             self.y_label = None
#             self.y_lim = None
#             self.y_log = None
#
#         self.plot_show = show
#         self.plot_save = save
#
#         # update or set basic figure settings
#         # NOTE: Helvetica Neue has to be installed, otherwise default font is used
#         # plt.rcParams.update({'figure.autolayout': True}) # replaced with , bbox_inches='tight'
#         # plt.rcParams.update({'figure.figsize': (8, 5)})
#         # plt.rcParams.update({'font.size': 14})
#         # plt.rcParams['font.family'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['font.weight'] = 'medium'
#         # plt.rcParams['mathtext.fontset'] = 'custom' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:italic' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue:medium'
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:medium:italic'
#         # plt.rcParams['axes.labelweight'] = 'medium'
#         # plt.rcParams['axes.labelsize'] = 16
#         # plt.rcParams['axes.linewidth'] = 1.2
#
#
#     def network_graph(self, net_graphviz, layout_engine, output):
#         """docstring for ."""
#
#         ### plotting via networkx
#         # fig = plt.figure(figsize=figsize)
#         # ax = fig.gca()
#         # ax.spines['top'].set_visible(False)
#         # ax.spines['right'].set_visible(False)
#         # ax.spines['bottom'].set_visible(False)
#         # ax.spines['left'].set_visible(False)
#         #
#         # pos = nx.nx_agraph.graphviz_layout(net_graphviz, prog=layout_engine)
#         # nx.draw_networkx_nodes(net_graphviz, pos, node_color=node_colors,
#         #                     node_size=node_sizes)
#         #
#         # nx.draw_networkx_labels(net_graphviz, pos,
#         #               labels=node_labels, font_color='black') # , font_size=0.5
#         #
#         # # draw network edges
#         # # (node_size is given otherwise arrowheads are displaced)
#         # nx.draw_networkx_edges(net_graphviz, pos, edge_color=edge_colors,
#         #                 arrowstyle='-|>') #, connectionstyle='arc3,rad=-0.3', arrowsize=6) # , node_size=node_size, alpha=edge_alpha)
#         #
#         # # possible arrow styles that look nice
#         # # '-|>' (default)
#         # # '->'
#         #
#         # nx.draw_networkx_edge_labels(net_graphviz, pos, edge_labels=edge_labels,
#         #                 label_pos=0.4)
#         ###
#
#         pdot = nx.drawing.nx_pydot.to_pydot(net_graphviz)
#
#         # save/show figure
#         if self.plot_save:
#             # plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight') # networkx
#             pdot.write_pdf(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), prog=layout_engine)
#
#         if self.plot_show:
#             # plt.show() # networkx
#             display(Image(pdot.create_png(prog=layout_engine)))
#
#         # # graphviz version
#         # A = to_agraph(net_graphviz)
#         # A.layout(layout_engine)
#         # A.draw(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']))
#         #
#         # if self.plot_show:
#         #     graphviz.Source(A).view()
#
#         # NOTE: use this somehow (arrow option for directed graphs in networkx)
#         # nx.draw_networkx(G, arrows=True, **options)
#         # options = {
#         #     'node_color': 'blue',
#         #     'node_size': 100,
#         #     'width': 3,
#         #     'arrowstyle': '-|>',
#         #     'arrowsize': 12,
#         # }
#
#
#     def samples_corner(self, samples, labels, output):
#         """docstring for ."""
#         # initialise figure
#         # plt.rcParams.update({'figure.autolayout': True})
#         # plt.rcParams.update({'font.size': 16})
#         # plt.rcParams['font.family'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['font.weight'] = 'medium'
#         # plt.rcParams['mathtext.fontset'] = 'custom' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:italic' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue:medium'
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:medium:italic'
#
#         # use corner package for this plot
#         fig = corner.corner(samples, labels=labels)
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def samples_cornerkernel(self, sampler_result, params_labels, output):
#         """docstring for ."""
#
#         # plt.rcParams.update({'figure.autolayout': True})
#         # plt.rcParams.update({'font.size': 16})
#         # plt.rcParams['font.family'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['font.weight'] = 'medium'
#         # plt.rcParams['mathtext.fontset'] = 'custom' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:italic' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue:medium'
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:medium:italic'
#
#         # fig = plt.figure()
#         # ax = fig.gca()
#
#         fig, axes = dyplot.cornerplot(sampler_result,
#                                 color='dodgerblue',
#                                 show_titles=True,
#                                 labels=params_labels,
#                                 title_fmt='.4f')
#         fig.tight_layout()
#
#         # save/show figure
#         if self.plot_save:
#             name = output['plot_name']
#             plt.savefig(output['output_folder'] + f'/{name}.pdf', bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def samples_cornerpoints(self, sampler_result, params_labels, output):
#         """docstring for ."""
#
#         # plt.rcParams.update({'figure.autolayout': True})
#         # plt.rcParams.update({'font.size': 16})
#         # plt.rcParams['font.family'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['font.weight'] = 'medium'
#         # plt.rcParams['mathtext.fontset'] = 'custom' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:italic' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue:medium'
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:medium:italic'
#
#         # fig = plt.figure()
#         # ax = fig.gca()
#
#         fig, axes = dyplot.cornerpoints(sampler_result,
#                              cmap='magma',
#                              labels=params_labels)
#
#         # save/show figure
#         if self.plot_save:
#             name = output['plot_name']
#             plt.savefig(output['output_folder'] + f'/{name}.pdf', bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def samples_cornerbounds(self, sampler_result, params_labels, prior_transform, output):
#         """docstring for ."""
#
#         # plt.rcParams.update({'figure.autolayout': True})
#         # plt.rcParams.update({'font.size': 16})
#         # plt.rcParams['font.family'] = 'Helvetica Neue' # uncommented 2020
#         # plt.rcParams['font.weight'] = 'medium' # uncommented 2020
#         # plt.rcParams['mathtext.fontset'] = 'custom' # uncommented 2020
#         # plt.rcParams['mathtext.rm'] = 'Helvetica Neue:medium' # uncommented 2020
#         # plt.rcParams['mathtext.it'] = 'Helvetica Neue:medium:italic' # uncommented 2020
#
#         num_it_segs = 14 # num_it_segs+1 plots will be plotted
#         num_it_total = sampler_result.niter
#
#         for it_plot in range(num_it_segs):
#
#             it_num = int( it_plot * num_it_total / float(num_it_segs - 1))
#             it_num = min(num_it_total, it_num)
#
#             # fig = plt.figure()
#             # ax = fig.gca()
#
#             fig, axes = dyplot.cornerbound(sampler_result,
#                                     it=it_num,
#                                     prior_transform=prior_transform,
#                                     color='lightgrey',
#                                     show_live=True,
#                                     live_color='darkorange',
#                                     labels=params_labels)
#
#             # save/show figure
#             if self.plot_save:
#                 name = output['plot_name']
#                 plt.savefig(output['output_folder'] + f'/{name}_it{it_num}.pdf', bbox_inches='tight')
#             if self.plot_show:
#                 plt.show(fig, block=False)
#             plt.close(fig)
#             plt.close('all')
#
#
#     def sampling_runplot(self, sampler_result, output):
#         """docstring for ."""
#
#         # plt.rcParams['axes.titleweight'] = 'medium'
#         # plt.rcParams['axes.titlesize'] = 14
#
#         # fig = plt.figure()
#         # ax = fig.gca()
#         # ax.spines['top'].set_visible(False)
#         # ax.spines['right'].set_visible(False)
#         # ax.spines['bottom'].set_visible(True)
#         # ax.spines['left'].set_visible(True)
#
#         fig, ax = dyplot.runplot(sampler_result,
#                                 color='limegreen') # fig, axes =
#
#         # save/show figure
#         if self.plot_save:
#             name = output['plot_name']
#             plt.savefig(output['output_folder'] + f'/{name}.pdf', bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def sampling_traceplot(self, sampler_result, params_labels, output):
#         """docstring for ."""
#
#         # plt.rcParams['axes.titleweight'] = 'medium'
#         # plt.rcParams['axes.titlesize'] = 14
#
#         # fig = plt.figure()
#         # ax = fig.gca()
#         # ax.spines['top'].set_visible(False)
#         # ax.spines['right'].set_visible(False)
#         # ax.spines['bottom'].set_visible(True)
#         # ax.spines['left'].set_visible(True)
#
#         fig, axes = dyplot.traceplot(sampler_result,
#                              show_titles=True,
#                              post_color='dodgerblue',
#                              connect_color='darkorange',
#                              trace_cmap='magma',
#                              connect=True,
#                              connect_highlight=range(5),
#                              labels=params_labels #, title_fmt='.4f'
#                              )
#
#         # save/show figure
#         if self.plot_save:
#             name = output['plot_name']
#             plt.savefig(output['output_folder'] + f'/{name}.pdf', bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def samples_chains(self, samples, num_params, output):
#         """docstring for ."""
#
#         # plt.rcParams['axes.titleweight'] = 'medium'
#         # plt.rcParams['axes.titlesize'] = 14
#
#         fig = plt.figure()
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # set a color cycle for the different params
#         colormap = plt.cm.viridis
#         plt.gca().set_prop_cycle(cycler('color', [colormap(i) for i in np.linspace(0, 1, num_params)]))
#
#         plt.plot(samples, alpha=0.75)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         plt.xlabel('sample iteration')
#         plt.ylabel('parameter value')
#
#         # save/show figure
#         if self.plot_save:
#             name = output['plot_name']
#             plt.savefig(output['output_folder'] + f'/{name}.pdf', bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     # def fig_step_evolv(self, x_arr, y_arr, var_attributes, output):
#     #     """
#     #     Plot an evolving (e.g. over time) step function of multiple variables.
#     #
#     #     parameters
#     #     ----------
#     #     x_arr
#     #         numpy array with shape (# time points, )
#     #     y_arr
#     #         numpy array with shape (# variables, # time points)
#     #     var_attributes
#     #         dictionary specifying the keys 0, 1, ..., # variables - 1
#     #         with tuples (string for legend label, plt color code for variable)
#     #     output
#     #         dictionary specifying the keys 'output_folder' and 'plot_name'
#     #
#     #     example
#     #     -------
#     #     x_arr = np.linspace(0, 10, num=11, endpoint=True)
#     #     y_arr = np.array([
#     #                         [1, 1, 2, 2, 1, 2, 3, 4, 3, 3, 3],
#     #                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     #                         ])
#     #     var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
#     #                     0: ('$B_t$ (OFF gene)', 'tomato')}
#     #     output = {'output_folder': './test_figures',
#     #             'plot_name': 'fig_test_step'}
#     #     """
#     #     # initialise figure and axis settings
#     #     plt.figure()
#     #     ax = plt.gca()
#     #     ax.spines['top'].set_visible(False)
#     #     ax.spines['right'].set_visible(False)
#     #     ax.spines['bottom'].set_visible(True)
#     #     ax.spines['left'].set_visible(True)
#     #
#     #     # actual plotting
#     #     for var_ind in range(y_arr.shape[0]):
#     #         var_name = var_attributes[var_ind][0]
#     #         var_color = var_attributes[var_ind][1]
#     #
#     #         plt.step(x_arr, y_arr[var_ind, :], label='{0}'.format(var_name),
#     #                     where='mid', linewidth=2.75, color=var_color, alpha=0.75)
#     #         #         plt.plot(time_arr, var_arr[var_ind, :], marker='o',
#     #         #                     label='{0}'.format(var_name),
#     #         #                     linewidth=2.5, markersize=6, markeredgecolor=var_color,
#     #         #                     color=var_color, alpha=0.75)
#     #
#     #     # final axis setting
#     #     ax.set_xlim(self.x_lim)
#     #     ax.set_xlabel(self.x_label, color="black")
#     #     ax.set_xscale('log' if self.x_log==True else 'linear')
#     #     ax.set_ylim(self.y_lim)
#     #     ax.set_ylabel(self.y_label, color="black")
#     #     ax.set_yscale('log' if self.y_log==True else 'linear')
#     #
#     #     # add legend
#     #     legend = ax.legend(loc=0)
#     #     legend.get_frame().set_facecolor('white')
#     #     legend.get_frame().set_edgecolor('lightgrey')
#     #
#     #     # save figure
#     #     plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']))
#     #     if self.plot_show:
#     #         plt.show()
#     #     plt.close()
#
#     def line_evolv(self, x_arr, y_line, var_attributes,
#                     x_label=None, x_lim=None, x_log=False,
#                     y_label=None, y_lim=None, y_log=False,
#                     show=True, save=None):
#         """
#         Plot multiple evolving (e.g. over time) lines.
#
#         parameters
#         ----------
#         x_arr
#             numpy array with shape (# time points, )
#         y_line
#             numpy array setting the multiple lines with shape (# variables, # time points)
#         var_attributes
#             dictionary specifying the keys 0, 1, ..., # variables - 1
#             with tuples (string for legend label, plt color code for variable)
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         x_arr = np.linspace(0, 2, num=3, endpoint=True)
#
#         y_line = np.array([
#         [1, 2, 3],
#         [2, 1, 4]
#         ])
#
#         var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
#                         0: ('$B_t$ (OFF gene)', 'tomato')}
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'fig_test_line_evolv'}
#         """
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # actual plotting
#         for var_ind in range(y_line.shape[0]):
#             var_name = var_attributes[var_ind][0]
#             var_color = var_attributes[var_ind][1]
#
#             plt.plot(x_arr, y_line[var_ind, :], label=var_name,
#                             color=var_color, linewidth=2.5, zorder=2000)
#
#         # final axis setting
#         ax.set_xlim(x_lim)
#         ax.set_xlabel(x_label, color="black")
#         ax.set_xscale('log' if x_log==True else 'linear')
#         ax.set_ylim(y_lim)
#         ax.set_ylabel(y_label, color="black")
#         ax.set_yscale('log' if y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#
#         # save/show figure
#         if save!=None:
#             plt.savefig(save, bbox_inches='tight')
#         if show:
#             plt.show(fig, block=False)
#
#
#     def dots_w_bars_evolv(self, x_arr, y_arr_err, var_attributes, output):
#         """
#         Plot multiple evolving (e.g. over time) dots with error bars.
#
#         parameters
#         ----------
#         x_arr
#             numpy array with shape (# time points, )
#         y_arr_err
#             numpy array with shape (# variables, # time points, 2); third
#             dimension includes [value, error value]
#         var_attributes
#             dictionary specifying the keys 0, 1, ..., # variables - 1
#             with tuples (string for legend label, plt color code for variable)
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         x_arr = np.linspace(0, 2, num=3, endpoint=True)
#         y_arr_err = np.array([
#                             [[1, 0.1], [2, 0.2], [3, 0.3]],
#                             [[2, 0.4], [1, 0.1], [4, 0.5]]
#                             ])
#
#         # use var_ind as specified in var_order
#         var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
#                         0: ('$B_t$ (OFF gene)', 'tomato')}
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'fig_test_dots_time'}
#         """
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # actual plotting
#         for var_ind in range(y_arr_err.shape[0]):
#             var_name = var_attributes[var_ind][0]
#             var_color = var_attributes[var_ind][1]
#
#             plt.errorbar(x_arr, y_arr_err[var_ind, :, 0], yerr=y_arr_err[var_ind, :, 1],
#                         label=var_name, markeredgecolor=var_color, color=var_color, fmt='o',
#                         capsize=4.0, elinewidth=2.5, markeredgewidth=2.5, markersize=4.5)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def line_w_band_evolv(self, x_arr, y_line, y_lower, y_upper, var_attributes, output):
#         """
#         Plot multiple evolving (e.g. over time) lines with error/prediction bands.
#
#         parameters
#         ----------
#         x_arr
#             numpy array with shape (# time points, )
#         y_line
#             numpy array setting the multiple lines with shape (# variables, # time points)
#         y_lower
#             numpy array setting the lower bounds of the band
#             with shape (# variables, # time points)
#         y_upper
#             numpy array setting the upper bounds of the band
#             with shape (# variables, # time points)
#         var_attributes
#             dictionary specifying the keys 0, 1, ..., # variables - 1
#             with tuples (string for legend label, plt color code for variable)
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         x_arr = np.linspace(0, 2, num=3, endpoint=True)
#
#         y_line = np.array([
#         [1, 2, 3],
#         [2, 1, 4]
#         ])
#
#         y_lower = np.array([
#         [0.5, 1, 2],
#         [1.8, 0.8, 3.5]
#         ])
#
#         y_upper = np.array([
#         [1.4, 2.7, 3.1],
#         [2.1, 1.3, 4.4]
#         ])
#
#         var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
#                         0: ('$B_t$ (OFF gene)', 'tomato')}
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'fig_test_line_band'}
#         """
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # actual plotting
#         for var_ind in range(y_line.shape[0]):
#             var_name = var_attributes[var_ind][0]
#             var_color = var_attributes[var_ind][1]
#
#             ax.fill_between(x_arr, y_lower[var_ind, :], y_upper[var_ind, :],
#                             color=var_color, alpha=0.5, linewidth=0.0, zorder=1000)
#             plt.plot(x_arr, y_line[var_ind, :], label=var_name,
#                             color=var_color, linewidth=2.5, zorder=2000)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def dots_w_bars_and_line_evolv(self, x_arr_dots, x_arr_line, y_dots_err, y_line, var_attributes, output):
#         """
#         Plot multiple evolving (e.g. over time) lines with error/prediction bands.
#
#         parameters
#         ----------
#         x_arr_dots
#             numpy array with shape (# time points, ); used for aligment with
#             y_dots_err
#         x_arr_line
#             numpy array with shape (# time points, ); used for aligment with
#             y_line, y_lower and y_upper
#         y_dots_err
#             numpy array with shape (# variables, # time points, 2); third
#             dimension includes [value, error value]
#         y_line
#             numpy array setting the multiple lines with shape (# variables, # time points)
#         var_attributes
#             dictionary specifying the keys 0, 1, ..., # variables - 1
#             with tuples (string for legend label, plt color code for variable)
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         x_arr_dots = np.linspace(0, 1, num=2, endpoint=True)
#         x_arr_line = np.linspace(0, 2, num=3, endpoint=True)
#         y_dots_err = np.array([
#                             [[1, 0.1], [2, 0.3]],
#                             [[2, 0.4], [1, 0.5]]
#                             ])
#         y_line = np.array([
#         [1, 2, 3],
#         [2, 1, 4]
#         ])
#         var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
#                         0: ('$B_t$ (OFF gene)', 'tomato')}
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'fig_test_line_band_dots_bars'}
#         """
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # actual plotting
#         for var_ind in range(y_line.shape[0]):
#             var_name = var_attributes[var_ind][0]
#             var_color = var_attributes[var_ind][1]
#
#             # ax.fill_between(x_arr_line, y_lower[var_ind, :], y_upper[var_ind, :],
#             #                 color=var_color, alpha=0.5, linewidth=0.0, zorder=1000)
#
#             # # normal version
#             # plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
#             #                 color=var_color, linewidth=3, zorder=3000)
#             # plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
#             #             fmt='o', capsize=4.0, elinewidth=2.5, #label='data' if var_ind==0 else '',
#             #             markeredgewidth=2.5, markersize=4.5, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)
#             # poster version
#             # plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
#             #                 color=var_color, linewidth=2, zorder=3000)
#             # plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
#             #             fmt='o', capsize=2, elinewidth=2, #label='data' if var_ind==0 else '',
#             #             markeredgewidth=2, markersize=3, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)
#             # paper version
#             plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
#                             color=var_color, linewidth=2.5, zorder=3000)
#             plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
#                         fmt='o', capsize=4.0, elinewidth=2.5, #label='data' if var_ind==0 else '',
#                         markeredgewidth=2.5, markersize=4.5, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#         plt.legend(frameon=False)
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def dots_w_bars_and_line_w_band_evolv(self, x_arr_dots, x_arr_line, y_dots_err, y_line, y_lower, y_upper, var_attributes, output):
#         """
#         Plot multiple evolving (e.g. over time) lines with error/prediction bands.
#
#         parameters
#         ----------
#         x_arr_dots
#             numpy array with shape (# time points, ); used for aligment with
#             y_dots_err
#         x_arr_line
#             numpy array with shape (# time points, ); used for aligment with
#             y_line, y_lower and y_upper
#         y_dots_err
#             numpy array with shape (# variables, # time points, 2); third
#             dimension includes [value, error value]
#         y_line
#             numpy array setting the multiple lines with shape (# variables, # time points)
#         y_lower
#             numpy array setting the lower bounds of the band
#             with shape (# variables, # time points)
#         y_upper
#             numpy array setting the upper bounds of the band
#             with shape (# variables, # time points)
#         var_attributes
#             dictionary specifying the keys 0, 1, ..., # variables - 1
#             with tuples (string for legend label, plt color code for variable)
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         x_arr_dots = np.linspace(0, 1, num=2, endpoint=True)
#         x_arr_line = np.linspace(0, 2, num=3, endpoint=True)
#         y_dots_err = np.array([
#                             [[1, 0.1], [2, 0.3]],
#                             [[2, 0.4], [1, 0.5]]
#                             ])
#         y_line = np.array([
#         [1, 2, 3],
#         [2, 1, 4]
#         ])
#         y_lower = np.array([
#         [0.5, 1, 2],
#         [1.8, 0.8, 3.5]
#         ])
#         y_upper = np.array([
#         [1.4, 2.7, 3.1],
#         [2.1, 1.3, 4.4]
#         ])
#         var_attributes = {1: ('$A_t$ (ON gene)', 'limegreen'),
#                         0: ('$B_t$ (OFF gene)', 'tomato')}
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'fig_test_line_band_dots_bars'}
#         """
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # actual plotting
#         for var_ind in range(y_line.shape[0]):
#             var_name = var_attributes[var_ind][0]
#             var_color = var_attributes[var_ind][1]
#
#             ax.fill_between(x_arr_line, y_lower[var_ind, :], y_upper[var_ind, :],
#                             color=var_color, alpha=0.5, linewidth=0.0, zorder=1000)
#             plt.plot(x_arr_line, y_line[var_ind, :], label=var_name,
#                             color=var_color, linewidth=2.5, zorder=3000)
#             plt.errorbar(x_arr_dots, y_dots_err[var_ind, :, 0], yerr=y_dots_err[var_ind, :, 1],
#                         fmt='o', capsize=4.0, elinewidth=2.5, #label='data' if var_ind==0 else '',
#                         markeredgewidth=2.5, markersize=4.5, markeredgecolor='lightgrey', color='lightgrey', zorder=2000)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     # # TODO: steady state plots / volume plots?
#     # def fig_dots_w_bars(self, y_arr_err, attributes, output, x_ticks=None):
#     #     """
#     #     Plot dots with error bars (values in y axis, iteration over x axis).
#     #
#     #     parameters
#     #     ----------
#     #     y_arr_err
#     #         numpy array with shape (# dots, 2); errors are given in the second
#     #         dimension
#     #     attributes
#     #         dictionary specifying the keys 'color'
#     #     output
#     #         dictionary specifying the keys 'output_folder' and 'plot_name'
#     #     x_ticks (optional)
#     #         list of labels for dots which are plotted below x axis.
#     #
#     #     example
#     #     -------
#     #     y_arr_err = np.array([
#     #     [1, 0.2],
#     #     [2, 0.8],
#     #     [3, 0.3]
#     #     ])
#     #
#     #     x_ticks = ['a', 'b', 'c']
#     #
#     #     attributes = {'color': 'dodgerblue'}
#     #
#     #     output = {'output_folder': './test_figures',
#     #             'plot_name': 'fig_test_dots_bars'}
#     #     """
#     #     # initialise figure and axis settings
#     #     plt.figure()
#     #
#     #     ax = plt.gca()
#     #     ax.spines['top'].set_visible(False)
#     #     ax.spines['right'].set_visible(False)
#     #     ax.spines['bottom'].set_visible(True)
#     #     ax.spines['left'].set_visible(True)
#     #
#     #     # actual plotting
#     #     dot_color = attributes['color']
#     #     for dot_ind in range(y_arr_err.shape[0]):
#     #         plt.errorbar(dot_ind + 1, y_arr_err[dot_ind, 0], yerr=y_arr_err[dot_ind, 1],
#     #                     fmt='o', capsize=4, elinewidth=2.5, markeredgewidth=2.5,
#     #                     markersize=5, markeredgecolor=dot_color, color=dot_color, ecolor='lightgrey')
#     #
#     #     # final axis setting
#     #     ax.set_xlim(self.x_lim)
#     #     ax.set_xlabel(self.x_label, color="black")
#     #     ax.set_xscale('log' if self.x_log==True else 'linear')
#     #     ax.set_ylim(self.y_lim)
#     #     ax.set_ylabel(self.y_label, color="black")
#     #     ax.set_yscale('log' if self.y_log==True else 'linear')
#     #
#     #     if x_ticks != None:
#     #         plt.xticks([i + 1 for i in range(y_arr_err.shape[0])],
#     #                     [x_ticks[i] for i in range(y_arr_err.shape[0])], rotation=55)
#     #
#     #     # save figure
#     #     plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']))
#     #     if self.plot_show:
#     #         plt.show()
#     #     plt.close()
#
#
#     def dots_w_bars(self, y_arr_err, x_ticks, attributes, output, show_errorbar=True):
#         """
#         Plot dots with error bars (values in y axis, iteration over x axis).
#
#         parameters
#         ----------
#         y_arr_err
#             numpy array with shape (# dots, 2); errors are given in the second
#             dimension
#         attributes
#             dictionary specifying the keys 'color'
#         x_ticks (set None to ignore)
#             list of labels for dots which are plotted below x axis.
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#
#         example
#         -------
#         y_arr_err = np.array([
#         [1, 0.2],
#         [2, 0.8],
#         [3, 0.3]
#         ])
#
#         x_ticks = ['a', 'b', 'c']
#
#         attributes = {'color': 'dodgerblue'}
#
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'fig_test_dots_bars'}
#         """
#
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # actual plotting
#         for dot_ind in range(y_arr_err.shape[0]):
#             plt.errorbar(dot_ind + 1, y_arr_err[dot_ind, 0],
#                         yerr=np.array([y_arr_err[dot_ind, 1], y_arr_err[dot_ind, 2]]).reshape(2,1) if show_errorbar else None,
#                         fmt='o', capsize=4, elinewidth=2.5, markeredgewidth=2.5,
#                         markersize=5, markeredgecolor=attributes[dot_ind][1],
#                         color=attributes[dot_ind][1], ecolor='lightgrey')
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         if x_ticks != None:
#             plt.xticks([i + 1 for i in range(y_arr_err.shape[0])],
#                         [x_ticks[i] for i in range(y_arr_err.shape[0])], rotation=55)
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def histogram_discrete(self, bar_arr, bar_attributes, output, normalised=False):
#         """
#         Plot a histogram for discrete values.
#
#         parameters
#         ----------
#         bar_arr
#             numpy array of discrete values with shape (#realisations, #variables),
#             histograms are computed over all realisations for each variable
#
#         bar_attributes
#             dictionary with keys specifying a general bin 'label' and bin 'color'
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         bar_arr = np.random.poisson(10, size=10).reshape(10, 1)
#
#         bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}
#
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'hist_disc_test'}
#         """
#
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # plotting of a histogram
#         try:
#             bar_min = min(np.amin(bar_arr), self.x_lim[0])
#         except:
#             bar_min = np.amin(bar_arr)
#
#         try:
#             bar_max = max(np.amax(bar_arr), self.x_lim[1])
#         except:
#             bar_max = np.amax(bar_arr)
#
#         hist_bins = np.linspace(bar_min - 0.5, bar_max + 0.5, num=bar_max - bar_min + 2)
#
#         for var_ind in range(bar_arr.shape[1]):
#             plt.hist(bar_arr[:, var_ind], bins=hist_bins,
#                 density=normalised,
#                 histtype='stepfilled', # step, stepfilled
#                 linewidth=2.0,
#                 align='mid', color=bar_attributes[var_ind]['color'],
#                 label=bar_attributes[var_ind]['label'],
#                 alpha=bar_attributes[var_ind]['opacity'], zorder=1-var_ind)
#
#         # ax.set_xticks(bins + 0.5)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#         plt.legend(frameon=False)
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def histogram_discrete_w_line(self, bar_arr, bar_attributes, line_function, output, normalised=False):
#         """
#         Plot a histogram for discrete values with line.
#
#         parameters
#         ----------
#         bar_arr
#             numpy array of discrete values with shape (#realisations, #variables),
#             histograms are computed over all realisations for each variable
#
#         bar_attributes
#             dictionary with keys specifying a general bin 'label' and bin 'color'
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         bar_arr = np.random.poisson(10, size=10).reshape(10, 1)
#
#         bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}
#
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'hist_disc_test'}
#         """
#
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # plotting of a histogram
#         try:
#             bar_min = min(np.amin(bar_arr), self.x_lim[0])
#         except:
#             bar_min = np.amin(bar_arr)
#
#         try:
#             bar_max = max(np.amax(bar_arr), self.x_lim[1])
#         except:
#             bar_max = np.amax(bar_arr)
#
#         x_line_arr = np.linspace(bar_min, bar_max, num=1000, endpoint=True)
#         hist_bins = np.linspace(bar_min - 0.5, bar_max + 0.5, num=bar_max - bar_min + 2)
#
#         for var_ind in range(bar_arr.shape[1]):
#             plt.hist(bar_arr[:, var_ind], bins=hist_bins,
#                 density=normalised,
#                 histtype='stepfilled', # step, stepfilled
#                 linewidth=2.0,
#                 align='mid', color=bar_attributes[var_ind]['color'],
#                 label=bar_attributes[var_ind]['label'],
#                 alpha=bar_attributes[var_ind]['opacity'])
#
#             x_line, y_line, line_label, line_color = line_function(x_line_arr, bar_arr[:, var_ind])
#             plt.plot(x_line, y_line, label=line_label, color=line_color, linewidth=2.5)
#
#         # ax.set_xticks(bins + 0.5)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def histogram_continuous(self, bar_arr, bar_attributes, output, normalised=False):
#         """
#         Plot a histogram for continuous values.
#
#         parameters
#         ----------
#         bar_arr
#             numpy array of continuous values with shape (#realisations, #variables),
#             histograms are computed over all realisations for each variable
#
#         bar_attributes
#             dictionary with keys specifying a general bin 'label', bin 'color',
#             bin 'edges' and bin edges 'interval_type' ('[)' (default) or '(]')
#
#         normalised
#             True or False
#
#         interval
#
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         bar_arr = np.random.poisson(10, size=10).reshape(10, 1)
#
#         bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}
#
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'hist_disc_test'}
#         """
#
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # plotting of a histogram
#         for var_ind in range(bar_arr.shape[1]):
#             # read out interval type, default plt.hist() behavior are
#             # half-open interval [.., ..), small epsilon shift mimicks (.., ..]
#             if bar_attributes[var_ind]['interval_type']=='(]':
#                 epsilon = 1e-06
#             else:
#                 epsilon = 0.0
#
#             plt.hist(bar_arr[:, var_ind] - epsilon,
#                 bins=bar_attributes[var_ind]['edges'],
#                 density=normalised,
#                 histtype='stepfilled', # step, stepfilled
#                 linewidth=2.0,
#                 color=bar_attributes[var_ind]['color'],
#                 label=bar_attributes[var_ind]['label'],
#                 alpha=bar_attributes[var_ind]['opacity'])
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def histogram_continuous_w_line(self, bar_arr, bar_attributes, line_function, output, normalised=False):
#         """
#         Plot a histogram for continuous values with line.
#
#         parameters
#         ----------
#         bar_arr
#             numpy array of continuous values with shape (#realisations, #variables),
#             histograms are computed over all realisations for each variable
#
#         bar_attributes
#             dictionary with keys specifying a general bin 'label', bin 'color',
#             bin 'edges' and bin edges 'interval_type' ('[)' (default) or '(]')
#
#         normalised
#             True or False
#
#         interval
#
#         output
#             dictionary specifying the keys 'output_folder' and 'plot_name'
#
#         example
#         -------
#         bar_arr = np.random.poisson(10, size=10).reshape(10, 1)
#
#         bar_attributes = {0 : {'label': 'some bins', 'color': 'dodgerblue', 'opacity': 1.0}}
#
#         output = {'output_folder': './test_figures',
#                 'plot_name': 'hist_disc_test'}
#         """
#
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # plotting of a histogram
#         for var_ind in range(bar_arr.shape[1]):
#             # read out interval type, default plt.hist() behavior are
#             # half-open interval [.., ..), small epsilon shift mimicks (.., ..]
#             if bar_attributes[var_ind]['interval_type']=='(]':
#                 epsilon = 1e-06
#             else:
#                 epsilon = 0.0
#
#             plt.hist(bar_arr[:, var_ind] - epsilon,
#                 bins=bar_attributes[var_ind]['edges'],
#                 density=normalised,
#                 histtype='stepfilled', # step, stepfilled
#                 linewidth=2.0,
#                 color=bar_attributes[var_ind]['color'],
#                 label=bar_attributes[var_ind]['label'],
#                 alpha=bar_attributes[var_ind]['opacity'])
#
#             x_line_arr = np.linspace(np.amin(bar_attributes[var_ind]['edges']),
#                                     np.amax(bar_attributes[var_ind]['edges']),
#                                     num=1000, endpoint=True)
#             x_line, y_line, line_label, line_color = line_function(x_line_arr, bar_arr[:, var_ind])
#             plt.plot(x_line, y_line, label=line_label, color=line_color, linewidth=2.5)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         legend = ax.legend(loc=0)
#         legend.get_frame().set_facecolor('white')
#         legend.get_frame().set_edgecolor('lightgrey')
#
#         # save/show figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#
#     def scatter(self, x_arr, y_arr, attributes, output, normalised=False):
#         """docstring for ."""
#
#         # initialise figure and axis settings
#         fig = plt.figure()
#
#         ax = plt.gca()
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(True)
#         ax.spines['left'].set_visible(True)
#
#         # plotting of a histogram
#         plt.scatter(    x_arr, y_arr,
#                         color=attributes['color'],
#                         alpha=attributes['opacity'])
#
#         # ax.set_xticks(bins + 0.5)
#
#         # final axis setting
#         ax.set_xlim(self.x_lim)
#         ax.set_xlabel(self.x_label, color="black")
#         ax.set_xscale('log' if self.x_log==True else 'linear')
#         ax.set_ylim(self.y_lim)
#         ax.set_ylabel(self.y_label, color="black")
#         ax.set_yscale('log' if self.y_log==True else 'linear')
#
#         # add legend
#         if not attributes['label']==None:
#             legend = ax.legend(loc=0)
#             legend.get_frame().set_facecolor('white')
#             legend.get_frame().set_edgecolor('lightgrey')
#
#         # save figure
#         if self.plot_save:
#             plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']), bbox_inches='tight')
#         if self.plot_show:
#             plt.show(fig, block=False)
#         plt.close(fig)
#         plt.close('all')
#
#     # def fig_dots_w_mult_bars(self, val_obj, attributes, legend_attr, output):
#     #     """
#     #
#     #     parameters
#     #     ----------
#     #
#     #     example
#     #     -------
#     #     x_axis = {'label': ' ',
#     #     'limits': (0, 5),
#     #     'log': False}
#     #     y_axis = {'label': 'mRNA counts',
#     #             'limits': (None, None),
#     #             'log': False}
#     #
#     #     val_obj = np.array([
#     #             np.array([[0.5, 0.45, 0.7]]),
#     #             np.array([[0.8, 0.7, 0.95], [0.4, 0.35, 0.44]]),
#     #             np.array([[0.8, 0.7, 0.95], [0.4, 0.35, 0.44], [0.4, 0.35, 0.44]]),
#     #             np.array([[0.5, 0.45, 0.7]])
#     #             ], dtype=object)
#     #
#     #     attributes = {0: ('a', ['blue']),
#     #                 1: ('b', ['limegreen', 'red']),
#     #                   2: ('b', ['blue', 'limegreen', 'red']),
#     #                 3: ('c', ['blue'])}
#     #
#     #     legend_attr = [('blue', 'x'), ('limegreen', 'y'), ('red', 'z')]
#     #
#     #     output = {'output_folder': './output',
#     #             'plot_name': 'fig_test_dots_mult_bars'}
#     #
#     #     im = pl(x_axis, y_axis, show=True)
#     #     im.fig_dots_w_mult_bars(val_obj, attributes, legend_attr, output)
#     #     """
#     #     # initialise figure and axis settings
#     #     plt.figure()
#     #
#     #     ax = plt.gca()
#     #     ax.spines['top'].set_visible(False)
#     #     ax.spines['right'].set_visible(False)
#     #     ax.spines['bottom'].set_visible(True)
#     #     ax.spines['left'].set_visible(True)
#     #
#     #     # actual plotting
#     #     for val_ind in range(val_obj.shape[0]):
#     #         color_list = attributes[val_ind][1]
#     #         dots_per_categ = val_obj[val_ind].shape[0]
#     #
#     #         if dots_per_categ == 1:
#     #             x_pos = [val_ind + 1]
#     #         elif dots_per_categ == 2:
#     #             x_pos = [val_ind + 1 - 0.2, val_ind + 1 + 0.2]
#     #         elif dots_per_categ == 3:
#     #             x_pos = [val_ind + 1 - 0.2, val_ind + 1, val_ind + 1 + 0.2]
#     #
#     #         for dot_ind in range(dots_per_categ):
#     #             plt.errorbar(x_pos[dot_ind], val_obj[val_ind][dot_ind, 0],
#     #                         yerr=val_obj[val_ind][dot_ind, 1:].reshape(2,1),
#     #                         fmt='o', capsize=4, elinewidth=2.5, markeredgewidth=2.5,
#     #                         markersize=5, markeredgecolor=color_list[dot_ind],
#     #                         color=color_list[dot_ind], ecolor='lightgrey', zorder=1000)
#     #     # comment/uncomment for grey line at zero
#     #     # plt.axhline(0, color='grey')
#     #
#     #     # final axis setting
#     #     ax.set_xlim(self.x_lim)
#     #     ax.set_xlabel(self.x_label, color="black")
#     #     ax.set_xscale('log' if self.x_log==True else 'linear')
#     #     ax.set_ylim(self.y_lim)
#     #     ax.set_ylabel(self.y_label, color="black")
#     #     ax.set_yscale('log' if self.y_log==True else 'linear')
#     #
#     #     # add x axis ticks
#     #     plt.xticks([val_ind + 1 for val_ind in range(val_obj.shape[0])],
#     #                     [attributes[val_ind][0] for val_ind in range(val_obj.shape[0])], rotation=55)
#     #
#     #     # add legend manually
#     #     plt.legend(handles=[mpatches.Patch(color=leg[0], label=leg[1]) for leg in legend_attr])
#     #
#     #     # save figure
#     #     plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']))
#     #     if self.plot_show:
#     #         plt.show()
#     #     plt.close()
#
#
#     # def fig_hist(self, bar_arr, bins, bar_attributes, output, normalised=True):
#     #     # NOTE: this function (bin alignmight) expects float binning and looks
#     #     # weird so far in case of discrete integer binning
#     #     """
#     #     Plot a histogram for continuous values.
#     #
#     #     parameters
#     #     ----------
#     #     bar_arr
#     #         numpy array of continuous values
#     #     bins
#     #         integer, number of bins of the histogram
#     #     bar_attributes
#     #         dictionary with keys specifying a general bin 'label', bin 'color'
#     #         and how to 'align' the bins (default 'mid')
#     #     output
#     #         dictionary specifying the keys 'output_folder' and 'plot_name'
#     #
#     #     example
#     #     -------
#     #     bar_arr = np.array([1.1, 1.6, 2.1, 2.0, 0.9, 2.5, 3.3, 4.1, 3.9, 3.5, 3.6])
#     #     bins = 4
#     #     bar_attributes = {'label': 'some bins',
#     #                         'color': 'dodgerblue',
#     #                         'align': 'mid'}
#     #     output = {'output_folder': './test_figures',
#     #             'plot_name': 'fig_test_hist'}
#     #     """
#     #     # initialise figure and axis settings
#     #     plt.figure()
#     #
#     #     ax = plt.gca()
#     #     ax.spines['top'].set_visible(False)
#     #     ax.spines['right'].set_visible(False)
#     #     ax.spines['bottom'].set_visible(True)
#     #     ax.spines['left'].set_visible(True)
#     #
#     #     # plotting of a histogram
#     #     plt.hist(bar_arr, bins=bins,
#     #         normed=normalised, histtype='stepfilled',
#     #         align=bar_attributes['align'], color=bar_attributes['color'],
#     #         label=bar_attributes['label'])
#     #
#     #     # final axis setting
#     #     ax.set_xlim(self.x_lim)
#     #     ax.set_xlabel(self.x_label, color="black")
#     #     ax.set_xscale('log' if self.x_log==True else 'linear')
#     #     ax.set_ylim(self.y_lim)
#     #     ax.set_ylabel(self.y_label, color="black")
#     #     ax.set_yscale('log' if self.y_log==True else 'linear')
#     #
#     #     # add legend
#     #     legend = ax.legend(loc=0)
#     #     legend.get_frame().set_facecolor('white')
#     #     legend.get_frame().set_edgecolor('lightgrey')
#     #
#     #     # save figure
#     #     plt.savefig(output['output_folder'] + '/{0}.pdf'.format(output['plot_name']))
#     #     if self.plot_show:
#     #         plt.show()
#     #     plt.close()
