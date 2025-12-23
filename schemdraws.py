import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='circ3.svg') as d:
    d += elm.SourceSin()
    d += elm.Resistor().right()
    # d += elm.Line().right()
    # d += elm.Line().right()
    # d += elm.Inductor()
    d += elm.Capacitor()
    d += elm.Line().down()
    d += elm.Line().left()
    d += elm.Line().left()
