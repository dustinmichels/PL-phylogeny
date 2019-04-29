"""
See: https://medium.com/@bostjan_cigan/using-the-needleman-wunsch-algorithm-to-draw-evolutionary-trees-90d9db149413
"""


from scipy.cluster.hierarchy import linkage, dendrogram

# Calculate the distance scoring matrix


def scoring_distance_matrix(scoring_matrix):

    scoring_distance_matrix = create_matrix(
        len(scoring_matrix[0]), len(scoring_matrix[0]))
    maxR = get_matrix_max(scoring_matrix)

    for i in range(0, len(organisms_table)):
        for j in range(0, len(organisms_table)):
            scoring_distance_matrix[i][j] = abs(scoring_matrix[i][j] - maxR)

    return scoring_distance_matrix

# Return the max value in a matrix, used in
# scoring_distance_matrix method


def get_matrix_max(matrix):

    max_value = None

    for i in range(0, len(matrix[0])):
        for j in range(0, len(matrix[0])):
            if(max_value == None):
                max_value = matrix[i][j]
            if(matrix[i][j] >= max_value):
                max_value = matrix[i][j]

    return max_value


view raw


# scoring = scoring_matrix(organisms_table, d)
# scoring_distance_matrix = scoring_distance_matrix(scoring)
# average = linkage(scoring_distance_matrix, "average")
# dendrogram(average, labels=names, orientation="left", leaf_font_size=8)
# pylab.subplots_adjust(bottom=0.1, left=0.2, right=1.0, top=1.0)
# pylab.savefig("dendro.jpg")
