
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

def gen_svg(width : float, height : float, thickness : float, tv_width : float, tv_height : float):
    w1 = (width - tv_width) / 2.0
    w2 = tv_width / 2.0

    h1 = ((height - tv_height) / 2.0)
    h2 = (tv_height / 2.0)

  
    full_hor = [0,thickness,
                h1 - thickness,h1,
                height - h1, height - h1 + thickness,
                height - thickness,height]

    full_vert = [0,thickness,
                 w1 - thickness,w1,
                 width - w1, width - w1 + thickness,
                 width - thickness,width]

    part_hor = [h1 + thickness,
                h1 + h2 - thickness,h1 + h2,h1 + h2 + thickness,
                height - h1 - thickness]

    part_vert = [w1 + thickness,
                 w1 + w2 - thickness,w1 + w2, w1 + w2 + thickness,
                 width - w1 - thickness]
    
    coords = []
    coords.extend([[0,h,width,h] for h in full_hor])
    coords.extend([[w,0,w,height] for w in full_vert])
    coords.extend([[0,h,w1,h] for h in part_hor])
    coords.extend([[width - w1,h,width,h] for h in part_hor])
    coords.extend([[w,0,w,h1] for w in part_vert])
    coords.extend([[w,height - h1,w,height] for w in part_vert])

    SCALE = 1.0
    OFFSET = 5.0

    for line in coords:
        for i in range(4):
            line[i] = line[i] * SCALE + OFFSET

    LINE_STRING = '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'

    svg = ''
    for line in coords:
        svg += LINE_STRING.format(*line)

    print(svg)


#get_dimensions(2400,2400,500,17.5,1200,1200)
gen_svg(2400,1600,18,1200,800)
    