from manim import *


class SineCurveUnitCircle(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])

    def add_x_labels(self):
        x_labels = [
            MathTex(r"\pi"),
            MathTex(r"2 \pi"),
            MathTex(r"3 \pi"),
            MathTex(r"4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2 * i, 0, 0]), DOWN)
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
            self.t_offset += dt * rate
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(
                dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2
            )

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=YELLOW_D)
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

        (txt1Bin, txt2Bin, txt3Bin) = [
            Text(weiBin, color=color) for color in [RED, GREEN, BLUE]
        ]
        txt1Bin.next_to(txt2Bin, UP)
        txt3Bin.next_to(txt2Bin, DOWN)

        txtLWrap = Text("“").next_to(txt1Bin, LEFT)
        txtRWrap = Text("”").next_to(txt3Bin, RIGHT)

        self.play(
            FadeIn(txtLWrap),
            FadeIn(txtRWrap),
            LaggedStart(Write(txt1Bin), Write(txt2Bin), Write(txt3Bin), lag_ratio=0.05),
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
                lag_ratio=0.2,
            ),
        )

        self.wait(0.1)
        self.wait(1)


class Combine(Scene):
    def construct(self):
        self.wait(1)
        ax0 = Axes(
            x_range=[0, 2],
            y_range=[-1, 1],
            tips=True,
            x_length=5,
            y_length=1,
        ).shift(4 * LEFT)
        txt0 = Text("0").next_to(ax0, DOWN)
        line0 = ax0.plot(lambda x: np.sin(2 * np.pi * x), color=RED)

        ax1 = Axes(
            x_range=[0, 2],
            y_range=[-1, 1],
            tips=True,
            x_length=5,
            y_length=1,
        ).shift(4 * RIGHT)
        txt1 = Text("1").next_to(ax1, DOWN)
        line1 = ax1.plot(lambda x: np.sin(4 * np.pi * x), color=BLUE)

        self.play(Write(txt0), Write(txt1), Create(line0), Create(line1))
        self.wait(1)

        data = "0101"
        data_lines = [line0.copy() if i == "0" else line1.copy() for i in data]
        data_texts = [Text(i) for i in data]
        for line in data_lines:
            self.add(line)

        data_tip = Text("Data:").shift(5 * LEFT + 3 * UP)
        wave_tip = Text("Wave:").shift(5 * LEFT + 2 * UP)

        for idx in range(len(data_texts)):
            data_texts[idx].next_to(
                data_tip if idx == 0 else data_texts[idx - 1],
                RIGHT,
                buff=1.6 if idx == 0 else 2.15,
            )

        self.play(
            Write(wave_tip),
            Write(data_tip),
            LaggedStart(*[Write(data_text) for data_text in data_texts], lag_ratio=0.2),
        )

        for idx in range(len(data_lines)):
            line = data_lines[idx]
            self.play(
                line.animate.scale(0.5).next_to(
                    wave_tip if idx == 0 else data_lines[idx - 1],
                    RIGHT,
                    buff=0.3 if idx == 0 else 0,
                ),
                Indicate(data_texts[idx], color="red" if data[idx] == "0" else "blue"),
            )

        self.wait(1)

        play_line = Line(ORIGIN + 0.5 * UP, ORIGIN + 0.5 * DOWN).next_to(
            data_lines[0], LEFT, buff=0
        )
        self.play(Create(play_line))

        self.wait(0.1)

        for idx in range(len(data_lines)):
            self.play(
                play_line.animate.next_to(data_lines[idx], RIGHT, buff=0),
                Indicate(data_texts[idx], color="red" if data[idx] == "0" else "blue"),
            )

        self.wait(1)


class SlidingSineWaves(Scene):
    """Draw two sine waves (long & short period) that continuously slide left
    by increasing their common phase. The axes remain fixed.
    """

    def construct(self):
        # a1 = DecimalNumber(
        #     2,
        #     show_ellipsis=False,
        #     num_decimal_places=1,
        #     include_sign=True,
        # ).shift(3 * UP + RIGHT * 3)
        # a1L = MathTex(r"y = \sin (").next_to(a1, LEFT, buff=0.1)
        # a1R = MathTex(r"\cdot \; x)").next_to(a1, RIGHT, buff=0.25)
        # a1.shift(UP*0.04)

        a1T = ValueTracker(2)
        # a1.add_updater(lambda l: l.set_value(a1T.get_value()))
        def get_line():
            ax = Axes(x_range=[0, 5], y_range=[-5, 5], tips=True, x_length=5)
            line = ax.plot(lambda x: np.sin(
                (2 + 0.1 * (a1T.get_value() - 40) * (a1T.get_value() >= 40) - 0.1 * (a1T.get_value() - 80) * (a1T.get_value() >= 80))
                  * x + a1T.get_value()), color=BLUE)
            return line

        ax = always_redraw(get_line)

        self.add(ax)
        self.play(FadeIn(ax))
        # self.wait(0.1)
        # self.play(Write(a1L), Write(a1), Write(a1R))
        self.play(a1T.animate.set_value(120), run_time=20)
        self.wait(1)


class MovingSineWaves(Scene):
    """Draw two sine waves (long & short period) that continuously slide left
    by increasing their common phase. The axes remain fixed.
    """

    def construct(self):

        a1T = ValueTracker(2)
        offset = ValueTracker(-5)
        # a1.add_updater(lambda l: l.set_value(a1T.get_value()))
        def get_line():
            offset.set_value(offset.get_value() + 0.05)
            ax = Axes(x_range=[0, 5], y_range=[-5, 5], tips=True, x_length=5)
            line = ax.plot(lambda x: np.sin(a1T.get_value() * (x + offset.get_value())), color=BLUE)
            return line

        ax = always_redraw(get_line)

        self.add(ax)
        # self.play(FadeIn(ax))
        self.play(a1T.animate.set_value(2), run_time=5)
        self.play(a1T.animate.set_value(8), run_time=5)
        self.play(a1T.animate.set_value(8), run_time=5)


class SineFrequencyRamp(Scene):
    def construct(self):
        # Axes setup
        axes = Axes(
            x_range=[0, 0.01, 0.002],  # show 10 ms of waveform
            y_range=[-1.2, 1.2, 0.5],
            x_length=10,
            y_length=3,
            axis_config={"include_numbers": False},
        )

        self.add(axes)

        # Frequency parameters
        f_start = 500  # 0.5 kHz
        f_end = 1000  # 1 kHz
        duration_static = 5
        duration_ramp = 5

        # Define the sine function
        def sine_wave(x, freq):
            return np.sin(2 * np.pi * freq * x)

        # --- Part 1: static 0.5 kHz sine ---
        wave_static = always_redraw(
            lambda: axes.plot(
                lambda x: sine_wave(x, f_start), x_range=[0, 0.01], color=YELLOW
            )
        )

        self.play(Create(wave_static))
        self.wait(duration_static)

        # --- Part 2: frequency ramp 0.5kHz → 1kHz ---
        freq_tracker = ValueTracker(0.0)

        def ramp_wave():
            # Linear interpolation
            freq = f_start + (f_end - f_start) * freq_tracker.get_value()
            return axes.plot(
                lambda x: sine_wave(x, freq), x_range=[0, 0.01], color=YELLOW
            )

        wave_ramp = always_redraw(ramp_wave)

        # Replace static wave with animated one
        self.remove(wave_static)
        self.add(wave_ramp)

        self.play(
            freq_tracker.animate.set_value(1.0),
            run_time=duration_ramp,
            rate_func=linear,
        )

        self.wait(5)
