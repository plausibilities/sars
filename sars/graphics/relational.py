import matplotlib.pyplot as plt


class Relational:
    """
    Class Relational
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def figure(width: float, height: float):
        """

        :param width: The width of the graph
        :param height: The height of the graph
        :return:
        """

        fig = plt.figure(figsize=(width, height))
        handle = fig.gca()
        handle.tick_params(axis='both', labelsize='small')

        return handle

    @staticmethod
    def annotation(handle, labels):
        """

        :param handle: The handle of the graph that will be annotated
        :param labels: collections.namedtuple(
                            typename='RelationalGraphLabels',
                            field_names=['title', 'xlabel', 'ylabel'])
        :return:
        """
        handle.set_title(labels.title, fontsize='medium')
        handle.set_xlabel(labels.xlabel, fontsize='medium')
        handle.set_ylabel(labels.ylabel, fontsize='medium')
