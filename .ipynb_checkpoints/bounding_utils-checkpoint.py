import cv2
DEBUG = True

def organise_data(texts, path):
    if DEBUG:
        original = cv2.imread(path)
        copy = original.copy()

    grouped_data = []
    final_groupings = []
    max_horizontal_gap = 0
    max_vertical_gap = 0
    current_gap = 90

    if texts[0] != None:
        max_horizontal_gap = texts[0].bounding_poly.vertices[1].x - texts[0].bounding_poly.vertices[0].x
        max_vertical_gap = texts[0].bounding_poly.vertices[1].y - texts[0].bounding_poly.vertices[0].y

    texts.pop(0)

    for text in texts:
        if DEBUG:
            print('\n"{}"'.format(text.description))
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                       for vertex in text.bounding_poly.vertices])
            print('bounds: {}'.format(','.join(vertices)))

        start_x = text.bounding_poly.vertices[0].x
        start_y = text.bounding_poly.vertices[0].y

        end_x = text.bounding_poly.vertices[2].x
        end_y = text.bounding_poly.vertices[2].y

        if DEBUG:
            cv2.rectangle(copy, (start_x, start_y), (end_x, end_y), (16, 16, 255), 1)

        if len(grouped_data) == 0:
            grouped_data.append(text)
        else:
            last_element = grouped_data[len(grouped_data) - 1]
            if abs(last_element.bounding_poly.vertices[1].y - start_y) < 10:
                if last_element.bounding_poly.vertices[1].x <= start_x and start_x - last_element.bounding_poly.vertices[1].x <= current_gap + 25:
                    grouped_data.append(text)
                    current_gap = start_x - last_element.bounding_poly.vertices[1].x
                else:
                    final_groupings.append(grouped_data)
                    grouped_data = [text]
                    current_gap = 90
            else:
                final_groupings.append(grouped_data)
                grouped_data = [text]
                current_gap = 90

    # Layer 2 grouping
    y_based_groupings = []
    current_group = [final_groupings[0]]
    final_groupings.pop(0)

    i = 0
    marked_indexes = []

    while (i < len(final_groupings)):
        for j in range(i, i + 15 if i + 15 < len(final_groupings) else len(final_groupings)):
            if j not in marked_indexes and abs(current_group[len(current_group) - 1][0].bounding_poly.vertices[0].y - final_groupings[j][0].bounding_poly.vertices[0].y) <= 2:
                current_group.append(final_groupings[j])
                marked_indexes.append(j)

        if i not in marked_indexes:
            if abs(current_group[len(current_group) - 1][0].bounding_poly.vertices[0].y - final_groupings[i][0].bounding_poly.vertices[0].y) <= 2:
                current_group.append(final_groupings[i])
            else:
                y_based_groupings.append(current_group)
                current_group = [final_groupings[i]]
        i += 1

    # Sorting by x
    for data in y_based_groupings:
        data.sort(key=lambda x: x[0].bounding_poly.vertices[0].x)

    # Figuring out the table column names
    # i = len(y_based_groupings) - 1
    # max_grouping_count = 0
    # while i >= 0:
    #     if len(y_based_groupings[i]) > max_grouping_count:
    #         max_grouping_count = len(y_based_groupings[i])

    for data in y_based_groupings:
        for l in data:
            print([d.description for d in l])
        print('\n')
    
    
    if DEBUG:
        cv2.imshow("Bounding Boxes", copy)
        cv2.waitKey(0)
        return y_based_groupings
    
    