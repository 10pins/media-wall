const SCALE = 1;
const OFFSET = 5;
const GAP = 25;
const SEP = 10;
const TEXT_H = 25;

function genLines(coords, id) {
    let lines = `<g id="${id}">\n`;

    const LINE_STRING = '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n';
    for (const line of coords) {
        lines += LINE_STRING.replace('{}', line[0]).replace('{}', line[1]).replace('{}', line[2]).replace('{}', line[3]);
    }

    lines += '</g>\n';
    return lines;
}

function adjustCoords(coords) {
    for (const line of coords) {
        for (let i = 0; i < line.length; i++) {
            line[i] = line[i] * SCALE + OFFSET + GAP + SEP + TEXT_H;
        }
    }
}


function genSvg(width,height,thickness,tv_width,tv_height){
    const padding = 2 * (OFFSET + GAP + SEP + TEXT_H);
    var svg = `<svg height="${height + padding}" width="${width + padding}" xmlns="http://www.w3.org/2000/svg">\n`

    svg += `<style>		
            #lines{stroke:black;stroke-width:3}
            #m-lines{stroke:gray;stroke-width:2;stroke-dasharray:5,5;}     
            #s-lines{stroke:gray;stroke-width:3;}
            text{text-anchor:middle;stroke:red;fill:red;font-size:35;}        
            </style>\n`;

    //wall lines
    const w1 = (width - tv_width) / 2;
    const w2 = tv_width / 2;

    const h1 = ((height - tv_height) / 2);
    const h2 = (tv_height / 2.0);

    
    const full_hor = [0,thickness,
                h1 - thickness,h1,
                height - h1, height - h1 + thickness,
                height - thickness,height];

    const full_vert = [0,thickness,
                    w1 - thickness,w1,
                    width - w1, width - w1 + thickness,
                    width - thickness,width];

    const part_hor = [h1 + thickness,
                h1 + h2 - thickness,h1 + h2,h1 + h2 + thickness,
                height - h1 - thickness];

    const part_vert = [w1 + thickness,
                    w1 + w2 - thickness,w1 + w2, w1 + w2 + thickness,
                    width - w1 - thickness];

    let coords = [];
    coords.push(...full_hor.map(h => [0, h, width, h]));
    coords.push(...full_vert.map(w => [w, 0, w, height]));
    coords.push(...part_hor.map(h => [0, h, w1, h]));
    coords.push(...part_hor.map(h => [width - w1, h, width, h]));
    coords.push(...part_vert.map(w => [w, 0, w, h1]));
    coords.push(...part_vert.map(w => [w, height - h1, w, height]));

    adjustCoords(coords);
    svg += genLines(coords,'lines');

    //measurment lines
    
    const coordsM = [[0,- GAP,width,- GAP],
                [width + GAP,0,width + GAP,height],
                [- GAP,h1 + h2,- GAP,height - h1],
                [- GAP,height - h1,- GAP,height],
                [0,height + GAP,w1,height + GAP],
                [w1,height + GAP,w1 + w2,height + GAP],
                [width - w1 - thickness, height + GAP, width - w1 + thickness, height + GAP]];

    adjustCoords(coordsM);
    svg += genLines(coordsM,'m-lines');

    //seperator lines
    
    const coordsS = [[0,- GAP - SEP,0,- GAP + SEP],
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
                [width - w1 + thickness,height + GAP - SEP,width - w1 + thickness,height + GAP + SEP]];
    
    adjustCoords(coordsS);
    svg += genLines(coordsS,'s-lines');

    //text

    let coordsT = [
        [w1 + w2, -GAP - SEP],
        [w1 / 2.0, height + GAP + SEP + TEXT_H],
        [w1 + (w2 / 2.0), height + GAP + SEP + TEXT_H],
        [width - w1, height + GAP + SEP + TEXT_H]
    ];
    let mes = [width, w1, w2, thickness * 2];
    
    adjustCoords(coordsT);
    for (let i = 0; i < coordsT.length; i++) {
        let t = coordsT[i];
        let m = mes[i];
        svg += ` <text x="${t[0]}" y="${t[1]}" font-size="25">${m}mm</text>\n`;
    }
    
    coordsT = [
        [width + GAP + SEP, h1 + h2],
        [-GAP - SEP - TEXT_H, height - (h1 / 2.0)],
        [-GAP - SEP - TEXT_H, height - h1 - (h2 / 2.0)]
    ];
    mes = [height, h1, h2];
    
    adjustCoords(coordsT);
    for (let i = 0; i < coordsT.length; i++) {
        let t = coordsT[i];
        let m = mes[i];
        svg += ` <text x="${t[0]}" y="${t[1]}" font-size="25" transform="rotate(90,${t[0]},${t[1]})">${m}mm</text>\n`;
    }

    console.log(svg);
    console.log(full_hor.toString());
    return svg;
}

const DEFAULT_HEIGHT = 1600;
const DEFAULT_WIDTH = 2400;
const DEFAULT_THICKNESS = 18;
const DEFAULT_TV_HEIGHT = 800;
const DEFAULT_TV_WIDTH = 1200;

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

var height = urlParams.has('height') ? Number(urlParams.get('height')) : DEFAULT_HEIGHT;
var width = urlParams.has('width') ? Number(urlParams.get('width')): DEFAULT_WIDTH;
var thickness = urlParams.has('thickness') ? Number(urlParams.get('thickness')) : DEFAULT_THICKNESS;
var tv_height = urlParams.has('tv_height') ? Number(urlParams.get('tv_height')) : DEFAULT_TV_HEIGHT;
var tv_width = urlParams.has('tv_width') ? Number(urlParams.get('tv_width')) : DEFAULT_TV_WIDTH;



document.getElementById('drawing-parent').innerHTML = genSvg(width,height,thickness,tv_width,tv_height);

urlParams.set('height',height);
urlParams.set('width',width);
urlParams.set('thickness',thickness);
urlParams.set('tv_height',tv_height);
urlParams.set('tv_width',tv_width);
history.replaceState(null, null, "?"+urlParams.toString());