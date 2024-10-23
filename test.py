pattern = [[4, 1, 1, [0, 0], [0.1275, 0], 0]]

if len(pattern) > 0:  # There is some pattern
    for p in range(0, len(pattern)):
        if pattern[p][2] == 1:  # grating
            print(f"Grating: Layer=Layer{pattern[p][0]}, Material=Mat{pattern[p][1]}, "
                  f"Center=({pattern[p][3][0]}, {pattern[p][3][1]}), "
                  f"Angle=0, Halfwidths=({pattern[p][4][0] / 2}, {pattern[p][4][0] / 2})")
        elif pattern[p][2] == 2:  # circular
            print(f"Circular: Layer=Layer{pattern[p][0]}, Material=Mat{pattern[p][1]}, "
                  f"Center=({pattern[p][3][0]}, {pattern[p][3][1]}), "
                  f"Halfwidth={pattern[p][4][0] / 2}")
        elif pattern[p][2] == 3:  # rectangular
            print(f"Rectangular: Layer=Layer{pattern[p][0]}, Material=Mat{pattern[p][1]}, "
                  f"Center=({pattern[p][3][0]}, {pattern[p][3][1]}), "
                  f"Angle={pattern[p][5]}, Halfwidths=({pattern[p][4][0] / 2}, {pattern[p][4][0] / 2})")
        elif pattern[p][2] == 4:  # ellipse
            print(f"Ellipse: Layer=Layer{pattern[p][0]}, Material=Mat{pattern[p][1]}, "
                  f"Center=({pattern[p][3][0]}, {pattern[p][3][1]}), "
                  f"Angle={pattern[p][5]}, Halfwidths=({pattern[p][4][0] / 2}, {pattern[p][4][0] / 2})")
        else:
            print("PATTERN DEFINITION: invalid pattern form")
