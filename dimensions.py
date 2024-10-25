import os

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

SCALE = 1.0
OFFSET = 5.0
GAP = 25
SEP = 10
TEXT_H = 25

def gen_svg(width : float, height : float, thickness : float, tv_width : float, tv_height : float):
    padding = 2 * (OFFSET + GAP + SEP + TEXT_H)
    svg = '<svg height="{}" width="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(height + padding,width + padding)

    svg += '''<style>		
                #lines{stroke:black;stroke-width:3}
                #m-lines{stroke:gray;stroke-width:2;stroke-dasharray:5,5;}     
                #s-lines{stroke:gray;stroke-width:3;}
                text{text-anchor:middle;stroke:red;fill:red;font-size:35;}        
            </style>\n'''

    #wall lines
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

   
    adjust_coords(coords)
    svg += gen_lines(coords,'lines')

    #measurment lines
    
    coords_m = [[0,- GAP,width,- GAP],
                [width + GAP,0,width + GAP,height],
                [- GAP,h1 + h2,- GAP,height - h1],
                [- GAP,height - h1,- GAP,height],
                [0,height + GAP,w1,height + GAP],
                [w1,height + GAP,w1 + w2,height + GAP],
                [width - w1 - thickness, height + GAP, width - w1 + thickness, height + GAP]]

    adjust_coords(coords_m)
    svg += gen_lines(coords_m,'m-lines')

    #seperator lines
    
    coords_s = [[0,- GAP - SEP,0,- GAP + SEP],
                [width,- GAP - SEP,width,- GAP + SEP],
                [width + GAP - SEP,0,width + GAP + SEP,0],
                [width + GAP - SEP,height,width + GAP + SEP,height],
                [- GAP - SEP,h1 + h2,- GAP + SEP,h1 + h2],
                [- GAP - SEP,height - h1,- GAP + SEP,height - h1],
                [- GAP - SEP,height,- GAP + SEP,height],
                [0,height + GAP - SEP,0,height + GAP + SEP],
                [w1,height + GAP - SEP,w1,height + GAP + SEP],
                [w1 + w2,height + GAP - SEP,w1 + w2,height + GAP + SEP],
                [width - w1 - thickness,height + GAP - SEP,width - w1 - thickness,height + GAP + SEP],
                [width - w1 + thickness,height + GAP - SEP,width - w1 + thickness,height + GAP + SEP]]
    
    
    
    adjust_coords(coords_s)
    svg += gen_lines(coords_s,'s-lines')

    #text
    coords_t = [[w1 + w2,- GAP - SEP],
                [w1 / 2.0,height + GAP + SEP + TEXT_H],
                [w1 + (w2 / 2.0),height + GAP + SEP + TEXT_H],
                [width - w1,height + GAP + SEP + TEXT_H]]
    mes = [width,w1,w2,thickness * 2]

    adjust_coords(coords_t)
    for t,m in zip(coords_t,mes):
        svg += ' <text x="{}" y="{}" font-size="25">{}mm</text>\n'.format(t[0],t[1],m)

    coords_t = [[width + GAP + SEP,h1 + h2],
                [- GAP - SEP - TEXT_H,height - (h1 / 2.0)],
                [- GAP - SEP - TEXT_H,height - h1 - (h2 / 2.0)]]
    mes = [height,h1,h2]

    adjust_coords(coords_t)
    for t,m in zip(coords_t,mes):
        svg += ' <text x="{0}" y="{1}" font-size="25" transform="rotate(90,{0},{1})">{2}mm</text>\n'.format(t[0],t[1],m)

    svg += 'Sorry, your browser does not support inline SVG.\n</svg>'

    return svg

def gen_lines(coords: list[list[float]], id : str):
    lines = '<g id="{}">\n'.format(id)

    LINE_STRING = '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'
    for line in coords:
        lines += LINE_STRING.format(*line)

    lines += '</g>\n'
    return lines

def adjust_coords(coords: list[list[float]]):
    for line in coords:
        for i in range(len(line)):
            line[i] = line[i] * SCALE + OFFSET + GAP + SEP + TEXT_H


#get_dimensions(2400,2400,500,17.5,1200,1200)
#gen_svg(2400,1600,18,1200,800)

with open(os.path.join('comp','drawing.html'),'w') as f:
    f.write(gen_svg(2400,1600,18,1200,800))

with open(os.path.join('docs','drawing','index.html'),'w') as fw:
    for file in ['begin','drawing','end']:
        with open(os.path.join('comp','{}.html'.format(file))) as fr:
            fw.write(fr.read())
    