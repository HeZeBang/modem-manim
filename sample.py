from manim import *

class SineCurveUnitCircle(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6,0,0])
        x_end = np.array([6,0,0])

        y_start = np.array([-4,-2,0])
        y_end = np.array([-4,2,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4,0,0])
        self.curve_start = np.array([-3,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex(r"\pi"), MathTex(r"2 \pi"),
            MathTex(r"3 \pi"), MathTex(r"4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x,y,0]), color=YELLOW_A, stroke_width=2 )


        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)

class Embedding(Scene):
    def construct(self):
        self.wait(1)

        weiBin = "0101 0101 1000 0010"

        (txt1Bin, txt2Bin, txt3Bin) = [Text(weiBin, color=color) for color in [RED, GREEN, BLUE]]
        txt1Bin.next_to(txt2Bin, UP)
        txt3Bin.next_to(txt2Bin, DOWN)

        txtLWrap = Text("“").next_to(txt1Bin, LEFT)
        txtRWrap = Text("”").next_to(txt3Bin, RIGHT)

        self.play(
            FadeIn(txtLWrap), FadeIn(txtRWrap), 
            LaggedStart(
                Write(txt1Bin), 
                Write(txt2Bin), 
                Write(txt3Bin), 
                lag_ratio=0.05
            )
        )

        self.wait(0.5)

        (txt1, txt2, txt3) = [Text("喂", color=color) for color in [RED, GREEN, BLUE]]
        txt1.next_to(txt2, LEFT)
        txt3.next_to(txt2, RIGHT)
        # txtSound = Text("声音").next_to(txt2, DOWN)

        self.play(
            txtLWrap.animate.next_to(txt1, LEFT),
            txtRWrap.animate.next_to(txt3, RIGHT),
            LaggedStart(
                Transform(txt1Bin, txt1),
                Transform(txt2Bin, txt2),
                Transform(txt3Bin, txt3),
                lag_ratio=0.2
            )
        )

        self.wait(0.1)
        self.wait(1)

class Combine(Scene):
    def construct(self):
        self.wait(1)


class SlidingSineWaves(Scene):
    """Draw two sine waves (long & short period) that continuously slide left
    by increasing their common phase. The axes remain fixed.
    """
    def construct(self):
        a1 = DecimalNumber(
            2,
            show_ellipsis=False,
            num_decimal_places=1,
            include_sign=True,
        ).shift(3 * UP + RIGHT * 3) 
        a1L = MathTex(r"y = \sin (").next_to(a1, LEFT, buff=0.1)
        a1R = MathTex(r"\cdot \; x)").next_to(a1, RIGHT, buff=0.25)
        # a1.shift(UP*0.04)

        a1T = ValueTracker(2)
        a1.add_updater(lambda l:l.set_value(a1T.get_value()))

        def get_line():
            ax = Axes(
                x_range=[0, 5],
                y_range=[-5, 5],
                tips=True,
                x_length=5
            )
            line = ax.plot(lambda x: np.sin(a1T.get_value() * x), color=BLUE)
            return line
        
        ax = always_redraw(get_line)

        # self.add(ax)
        self.play(FadeIn(ax))
        self.wait(0.1)
        self.play(Write(a1L), Write(a1), Write(a1R))
        self.play(a1T.animate.set_value(5), run_time=5)
        self.wait(1)