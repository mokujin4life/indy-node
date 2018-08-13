from matplotlib import pyplot as plt
import pandas as pd
import argparse


def build_graph():
    parser = argparse.ArgumentParser(description='Gets file path and graph name to build a graph')
    parser.add_argument('filepath', type=str, help='the csv file absolute path')
    args = parser.parse_args()
    file_path = args.filepath
    try:
        file = pd.read_csv(file_path)
    except IOError:
        assert False, "Could not find a path!"
    subplot_value = 411
    for i in ["Throughput", "Latency", "Queues"]:
            multi_line_plot(i, file, subplot_value)
            subplot_value += 1
    separate_single_line_plots(file)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.gca().grid(True)
    plt.subplots_adjust(left=0.05, right=0.85)
    plt.suptitle(file_path)
    plt.show()


def multi_line_plot(graph_name, file, subplot_value):
    graph_data_dict = {"Throughput": ["client_stack_messages_processed_per_sec", "master_ordered_requests_count_per_sec"]
                       , "Latency": ["avg_master_monitor_avg_latency", "avg_monitor_avg_latency"]
                       , "Queues": ["avg_node_stack_messages_processed", "avg_client_stack_messages_processed"]
                       }
    timestamp = list(map(lambda x: x.replace("2018-", ""), file.timestamp))
    numbers = range(len(timestamp))
    looper_list = graph_data_dict[graph_name]
    ax = plt.subplot(subplot_value)
    for i in looper_list:
        data_y_axis = file[i]
        plt.plot(numbers, data_y_axis, label=i.upper())
        plt.xticks(numbers, timestamp)
        for label in ax.xaxis.get_ticklabels():
            label.set_visible(False)
        for label in list(filter(lambda x: ax.xaxis.get_major_ticks().index(x) % 10 != 0, ax.xaxis.get_major_ticks())):
            label.set_visible(False)
        plt.legend(bbox_to_anchor=(1, 1), loc=2, prop={'size': 8}, borderaxespad=0.)
        plt.title(graph_name)
        plt.gca().grid(True)


def separate_single_line_plots(file):
    timestamp = list(map(lambda x: x.replace("2018-", ""), file.timestamp))
    numbers = range(len(timestamp))
    looper_list = ["AVG_NODE_PROD_TIME", "AVG_SERVICE_REPLICAS_TIME", "AVG_SERVICE_NODE_MSGS_TIME",
                   "AVG_SERVICE_ACTIONS_TIME", "AVG_SERVICE_ACTIONS_TIME", "AVG_SERVICE_VIEW_CHANGER_TIME"]
    ax = plt.subplot(414)
    ax.set_yscale("log")
    for i in looper_list:
        data_y_axis = file[i]
        plt.plot(numbers, data_y_axis, label=i)
        plt.xticks(numbers, timestamp)
        plt.legend(bbox_to_anchor=(1, 1), loc=2, prop={'size': 8}, borderaxespad=0.)
        for label in list(filter(lambda x: ax.xaxis.get_ticklabels().index(x) % 10 != 0, ax.xaxis.get_ticklabels())):
            label.set_visible(False)
        for label in list(filter(lambda x: ax.xaxis.get_major_ticks().index(x) % 10 != 0, ax.xaxis.get_major_ticks())):
            label.set_visible(False)
        plt.xticks(rotation=15)
        plt.tick_params(axis='x', which='minor')
        plt.title("Looper")


if __name__ == '__main__':
    build_graph()
