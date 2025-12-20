import schemdraw
import schemdraw.elements as elm
import schemdraw.flow as flow
from manim import *

from xml.etree.ElementTree import Element, ElementTree, fromstring, register_namespace
import cairo

def render_text_to_path_cairo(text, x, y, font_family="Sans", font_size=14, font_style="normal", font_weight="normal",
                              fill_color='black'):
    """
    svg with text elements -> svg with path elements. 
    
    font_style options: normal, italic, oblique
    font_weight options: normal, bold
    """
    surface = cairo.SVGSurface(None, 1000, 1000)
    context = cairo.Context(surface)

    slant = {
        'normal': cairo.FONT_SLANT_NORMAL,
        'italic': cairo.FONT_SLANT_ITALIC,
        'oblique': cairo.FONT_SLANT_OBLIQUE
    }.get(font_style.lower(), cairo.FONT_SLANT_NORMAL)

    weight = {
        'normal': cairo.FONT_WEIGHT_NORMAL,
        'bold': cairo.FONT_WEIGHT_BOLD
    }.get(font_weight.lower(), cairo.FONT_WEIGHT_NORMAL)

    # Try requested font family, fallback to Sans if not available
    try:
        context.select_font_face(font_family, slant, weight)
    except:
        context.select_font_face("Sans", slant, weight)

    context.set_font_size(font_size)

    context.move_to(x, y)
    context.text_path(text)
    path_data = []

    for type_, points in context.copy_path():
        if type_ == cairo.PATH_MOVE_TO:
            path_data.append(f"M {points[0]} {points[1]}")
        elif type_ == cairo.PATH_LINE_TO:
            path_data.append(f"L {points[0]} {points[1]}")
        elif type_ == cairo.PATH_CURVE_TO:
            path_data.append(
                f"C {points[0]} {points[1]} {points[2]} {points[3]} {points[4]} {points[5]}"
            )
        elif type_ == cairo.PATH_CLOSE_PATH:
            path_data.append("Z")

    surface.finish()
    return " ".join(path_data), fill_color


def convert_text_to_paths(svg_root):
    """
    Saves text as path with original-text as an attribute.
    """

    SVG_NS = "http://www.w3.org/2000/svg"
    register_namespace('', SVG_NS)

    for text_elem in svg_root.iter(f'{{{SVG_NS}}}text'):
        x = float(text_elem.get('x', 0))
        y = float(text_elem.get('y', 0))
        text = text_elem.text
        fill = text_elem.get('fill', '#000000')

        font_family = text_elem.get('font-family', 'Sans').split(',')[0].strip("'\"") 
        font_size = float(text_elem.get('font-size', '14px').replace('px', ''))
        font_style = text_elem.get('font-style', 'normal')
        font_weight = text_elem.get('font-weight', 'normal')

        path_data, _ = render_text_to_path_cairo(
            text, x, y,
            font_family=font_family,
            font_size=font_size,
            font_style=font_style,
            font_weight=font_weight,
            fill_color=fill
        )

        path_elem = Element(f'{{{SVG_NS}}}path', {
            'd': path_data,
            'fill': fill,
            'original-text': text
        })

        parent = svg_root.find(f'.//{{{SVG_NS}}}g')
        if parent is not None:
            idx = list(parent).index(text_elem)
            parent.remove(text_elem)
            parent.insert(idx, path_elem)

    return svg_root


def convert_text(svg_path, output_path):
    with open(svg_path, 'r') as f:
        content = f.read()
        svg_root = fromstring(content)

    new_svg_root = convert_text_to_paths(svg_root)

    tree = ElementTree(new_svg_root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=13, unit=1, color=WHITE, lw=2)
    
    v_s = elm.SourceSin().label('$V_s$')
    end_pos = v_s.start
    elm.Line().up()

    elm.Line().right()
    # elm.Oscilloscope().anchor('in1').right().label('Measurement Device')
    elm.Line().right(2)


    elm.Line().right()

    box_w = 3
    box_h = 1.5
    
    d.push()
    elm.Line().up(box_h / 2)
    elm.Line().right()
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().right()
    elm.Line().down(box_h * 2)

    d.pop()
    elm.Line().down(box_h)
    elm.Line().right()
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().right()
    elm.Line().down(box_h)

    
    elm.Line().tox(end_pos)
    elm.Line().toy(end_pos)

d.save('circuit1.svg')
# convert_text('circuit.svg', 'ok_circuit.svg')

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=13, unit=1, color=WHITE, lw=2)
    
    v_s = elm.SourceSin().label('$V_s$')
    end_pos = v_s.start
    elm.Line().up()

    elm.Line().right()
    elm.Oscilloscope(signal='sine', signal_lw=1).anchor('in1').right().label('Measurement Device')
    elm.Line().right(2)


    elm.Line().right()

    box_w = 3
    box_h = 1.5
    
    d.push()
    elm.Line().up(box_h / 2)
    elm.Line().right()
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().right()
    elm.Line().down(box_h * 2)

    d.pop()
    elm.Line().down(box_h)
    elm.Line().right()
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().right()
    elm.Line().down(box_h)

    
    elm.Line().tox(end_pos)
    elm.Line().toy(end_pos)

d.save('circuit2.svg')

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=13, unit=1, color=WHITE, lw=2)
    
    v_s = elm.SourceSin().label('$V_s$')
    end_pos = v_s.start
    elm.Line().up()

    elm.Line().right()
    # elm.Oscilloscope().anchor('in1').right().label('Measurement Device')
    elm.Line().right(2)


    elm.Line().right()

    box_w = 3
    box_h = 1.5
    
    d.push()
    elm.Line().up(box_h / 2)
    elm.Line().right()
    elm.Oscilloscope(signal='sine', signal_lw=1).anchor('in1').right().label('Measurement Device')
    elm.Line().right()
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().right()
    elm.Line().toy(end_pos)
    node = elm.Line().down()
    branch_end = node.end

    d.pop()
    elm.Line().down(box_h)
    elm.Line().right(box_w / 2)
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().right().tox(branch_end)
    
    elm.Line().down(1.5)
    elm.Line().tox(end_pos)
    elm.Line().toy(end_pos)

d.save('circuit3.svg')

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=13, unit=1, color=WHITE, lw=2)
    
    v_s = elm.SourceSin().label('$V_s$')
    end_pos = v_s.start
    elm.Line().up()

    elm.Line().right()
    # elm.Oscilloscope().anchor('in1').right().label('Measurement Device')
    elm.Line().right(2)


    elm.Line().right()

    box_w = 3
    box_h = 1.5
    
    d.push()
    elm.Line().down(box_h)
    elm.Line().right()
    elm.Oscilloscope(signal='sine', signal_lw=1).anchor('in1').right().label('Measurement Device')
    elm.Line().right(box_w / 2)
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().right()
    elm.Line().toy(end_pos)
    node = elm.Line().down()
    branch_end = node.end

    d.pop()
    elm.Line().up(box_h / 2)
    elm.Line().right()
    flow.RoundBox(w=box_w, h=box_h).label('Appliance A')
    elm.Line().tox(branch_end)
    elm.Line().toy(branch_end)
    
    elm.Line().tox(end_pos)
    elm.Line().toy(end_pos)

d.save('circuit4.svg')

def display_submobject_indices(mobject):
    colors = [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, TEAL, MAROON, GOLD]
    mobject_indices_texts = []
    for i, mobj in enumerate(mobject.submobjects):
        
        mobj.set_color(colors[i % 10])
        mobject_indices_texts.append(Text(f"submobject #{i}", font_size=10.0, color=colors[i % 10]).next_to(mobj, DOWN))

    return mobject_indices_texts

class CircuitScene(Scene):
    def construct(self):
        circ1 = SVGMobject('circuit1.svg').scale(2)
        circ2 = SVGMobject('circuit2.svg').scale(2)
        circ3 = SVGMobject('circuit3.svg').scale(2)
        circ4 = SVGMobject('circuit4.svg').scale(2)

        # mobject_indices_texts1 = display_submobject_indices(circ1)
        # mobject_indices_texts2 = display_submobject_indices(circ2)
        # mobject_indices_texts3 = mobject_indices_texts2
        
        app_a_texts = []
        app_b_texts = []
        app_texts = [app_a_texts, app_b_texts]
        
        app_a_texts.append(Text("Appliance A", font_size=28).move_to(circ1.submobjects[1]))
        app_b_texts.append(Text("Appliance B", font_size=28).move_to(circ1.submobjects[2]))
        app_a_texts.append(Text("Appliance A", font_size=28).move_to(circ2.submobjects[3]))
        app_b_texts.append(Text("Appliance B", font_size=28).move_to(circ2.submobjects[4]))
        app_a_texts.append(Text("Appliance A", font_size=28).move_to(circ3.submobjects[3]))
        app_b_texts.append(Text("Appliance B", font_size=28).move_to(circ3.submobjects[4]))
        app_a_texts.append(Text("Appliance A", font_size=28).move_to(circ4.submobjects[4]))
        app_b_texts.append(Text("Appliance B", font_size=28).move_to(circ4.submobjects[3]))

        self.play(
            LaggedStart(
                Create(circ1),
                AnimationGroup(*[Write(text[0]) for text in app_texts], lag_ratio=1.5),
                lag_ratio=1.20
            )
         )
        self.wait(2.5)
        self.play(TransformMatchingShapes(circ1, circ2), *[Transform(text[0], text[1]) for text in app_texts])
        self.wait(2.5)
        self.remove(*[text[0] for text in app_texts])
        self.play(TransformMatchingShapes(circ2, circ3), *[Transform(text[1], text[2]) for text in app_texts])
        self.wait(2.5)
        self.remove(*[text[1] for text in app_texts])
        self.play(TransformMatchingShapes(circ3, circ4), *[Transform(text[2], text[3]) for text in app_texts])
        self.wait(5)

class Vectors(Scene):
    def construct(self):
        d1, d2 = Dot(color=BLUE), Dot(color=GREEN)
        dg = VGroup(d1,d2).arrange(RIGHT,buff=1)
        arrow = Arrow(d1.get_center(), d2.get_center(), buff=0).set_color(RED)
        x = ValueTracker(0)
        y = ValueTracker(0)
        d1.add_updater(lambda z: z.set_x(x.get_value()))
        d2.add_updater(lambda z: z.set_y(y.get_value()))
        arrow.add_updater(lambda z: z.become(Line(d1.get_center(),d2.get_center())))
        self.add(d1, d2, arrow)
        self.play(x.animate.set_value(5))
        self.play(y.animate.set_value(4))
        self.wait()
