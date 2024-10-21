
def get_dimensions(width : float, height : float, depth : float, thickness : float, tv_width : float, tv_height : float):
    w1 = (width - tv_width) / 2.0
    w2 = tv_width / 2.0

    h1 = ((height - tv_height) / 2.0) - 2 * thickness
    h2 = (tv_height / 2.0) - 2 * thickness

    total_area = (16 * w1 * depth) + (8 * w2 * depth) + (16 * h1 * depth) + 8 * h2 * depth

    if width == tv_width * 2:
        print('24 pieces of {} x {} x {} mm'.format(w1,depth,thickness))
    else:
        print('16 pieces of {} x {} x {} mm'.format(w1,depth,thickness))
        print('8 pieces of {} x {} x {} mm'.format(w2,depth,thickness))

    if height == tv_height * 2:
        print('24 pieces of {} x {} x {} mm'.format(h1,depth,thickness))
    else:
        print('16 pieces of {} x {} x {} mm'.format(h1,depth,thickness))
        print('8 pieces of {} x {} x {} mm'.format(h2,depth,thickness))


    print('Total Area: {:,}mm²'.format(total_area))

def gen_svg(width : float, height : float, depth : float, thickness : float, tv_width : float, tv_height : float):
    pass

get_dimensions(2400,2400,500,17.5,1200,1200)

    