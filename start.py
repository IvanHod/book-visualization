from manimlib import *


def discrete_func(x):
    if x < 1 or x > 6:
        return 0
    return 1 / 6


def draw_table(scene: Scene, border, n_cols, labels):
    top, right, bottom, left = border['top'], border['right'], border['bottom'], border['left']
    h_line = Line(left, right, stroke_width=1)
    print(left, right)

    v_lines = VGroup()
    col_width = (right[0] - left[0]) / n_cols
    for i in range(n_cols - 1):
        w = left[0] + col_width * (i + 1)

        v_lines.add(Line(np.array([w, top[1], 0]), np.array([w, bottom[1], 0]), stroke_width=1))
    scene.play(
        ShowCreation(h_line),
        ShowCreation(v_lines)
    )

    top_labels = VGroup()
    for i, label in enumerate(labels):
        w = left[0] + col_width * (i + 1) - col_width / 2
        pos_new = np.array([w, top[1], 0]) + DOWN / 5
        text = SingleStringTex(label, font_size=16).move_to(pos_new)
        top_labels.add(text)
    scene.play(ShowCreation(top_labels))


class RandomVariable(Scene):
    def construct(self):
        text1 = Text('2.1 Теорема Байеса')
        text1.get_center()

        text2 = Text('Теория вероятности')

        text3 = Text('\tДискретная\nслучайная величина', font_size=36).move_to(LEFT * 3)
        text4 = Text('\tНепрерывная\nслучайная величина', font_size=36).move_to(RIGHT * 3)

        self.add(text1)
        # self.wait(1)
        self.play(
            text1.animate.shift(UP * 2),
            FadeIn(text2),
        )
        self.wait()

        self.play(
            FadeOut(text1),
            text2.animate.shift(UP * 2),
            FadeIn(text3),
            FadeIn(text4),
        )

        framebox1 = SurroundingRectangle(text3, buff=.1)
        img = ImageMobject('play-cube.png', height=2).move_to(DOWN * 2)
        self.play(ShowCreation(framebox1))
        self.play(FadeIn(img))

        # Создали все надписи и добавили кубик

        self.remove(framebox1)
        self.play(
            img.animate.shift(LEFT * 5).scale(0.5),
            self.camera.frame.animate.scale(0.5).shift(LEFT * 3).shift(DOWN * 1.3)
        )
        formula = Tex(
            r'P_(\xi=x_k)=p_k=\frac{x_k}{K}',
            font_size=26
        )
        formula_desc = Text('где K - число исходов', font_size=20).shift(DOWN / 2)
        formula_group = VGroup(formula, formula_desc).shift(DOWN * 1.5).shift(LEFT * 2.2)
        self.play(FadeIn(formula_group))

        self.play(
            FadeOut(formula_desc),
            formula.animate.move_to(img).shift(UP),
        )

        center = self.camera.get_frame_center() + RIGHT + DOWN / 2
        border = {'top': center + UP / 3, 'right': center + RIGHT * 1.5,
                  'bottom': center + DOWN / 3, 'left': center + LEFT * 1.5}
        labels = ['x_k'] + list(map(lambda v: f'x_{v}', range(1, 7)))
        draw_table(self, border, n_cols=7, labels=labels)


class DiscreteRandomVariableFunction(Scene):
    CONFIG = {
        'x_min': -1,
        'x_max': 7,
        'y_min': -1,
        'y_max': 6
    }

    def construct(self):
        axes = Axes(x_range=(-1, 7, 1), y_range=(0, 6, 1),
                    axis_config={
                        "stroke_color": GREY_A,
                        # "stroke_width": 2,
                        "include_tip": True,
                    },
                    y_axis_config={
                        "include_tip": False,
                    })

        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
        self.add(axes)

        func_1_label = (
            Text('Hellow world!').next_to(axes, UP, buff=0.2)
        )
        self.add(func_1_label)

        dot_slice = Dot(axes.c2p(1, 1, 0))
        self.add(dot_slice)

        for i in range(2, 7):
            next_dot = Dot(axes.c2p(i, i - 1, 0))
            self.play(
                Transform(dot_slice, next_dot),
                ShowCreation(Line(dot_slice.get_center(), next_dot.get_center()))
            )
            self.wait()

            if i <= 6:
                dot_slice.move_to(axes.c2p(i, i, 0))
        self.remove(dot_slice)
