import random
import turtle
import argparse


def send_cursor(draw_tool, pos_x, pos_y):
    draw_tool.up()
    draw_tool.goto(pos_x, pos_y)
    draw_tool.down()


def send_cursor_home(draw_tool):
    draw_tool.up()
    draw_tool.home()
    draw_tool.down()


def draw_circle_chart(langs_from_user):
    if not isinstance(langs_from_user, list):
        print('Необходимо в функцию передать список с данными!')
        return None

    draw_tool = turtle.Turtle()
    draw_tool.screen.colormode(255)

    langs_details = {lang: {'count': langs_from_user.count(lang),
                            'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}
                     for lang in langs_from_user}
    one_piece = 360 / len(langs_from_user)
    last_position = 0
    step_for_legend = 0

    for lang, details in langs_details.items():
        angle_for_lang = one_piece * details.get('count')
        draw_tool.pencolor(details.get('color'))

        # сдвигаем курсор для написания текста
        draw_tool.up()
        draw_tool.left(last_position + angle_for_lang / 2)
        draw_tool.fd(225)
        draw_tool.down()

        align_for_text = 'left' if draw_tool.pos()[0] > 0 else 'right'
        draw_tool.write(lang, False, align=align_for_text, font=("Arial", 12, "bold"))
        send_cursor_home(draw_tool)

        draw_tool.fillcolor(details.get('color'))
        draw_tool.begin_fill()
        draw_tool.left(last_position)
        draw_tool.fd(200)
        last_position += angle_for_lang
        draw_tool.left(90)
        draw_tool.circle(200, angle_for_lang)
        draw_tool.home()
        draw_tool.end_fill()

        draw_legend(draw_tool, step_for_legend, lang, details.get("count"), details.get('color'), details.get('color'))
        step_for_legend += 25

    input()


def draw_legend(draw_tool, step, lang, lang_count, fill_color, pen_color):
    x = 350
    y = 400

    send_cursor(draw_tool, x, y - step)

    draw_tool.fillcolor(fill_color)
    draw_tool.pencolor(pen_color)

    draw_tool.begin_fill()
    for line_length in (30, 10, 30, 10):
        draw_tool.fd(line_length)
        draw_tool.right(90)
    draw_tool.end_fill()

    send_cursor(draw_tool, x + 50, y - 15 - step)
    draw_tool.write(f'{lang}: {lang_count}', font=("Arial", 12, "bold"))
    send_cursor_home(draw_tool)


def draw_line_chart(langs_from_user):
    if not isinstance(langs_from_user, list):
        print('Необходимо в функцию передать список с данными!')
        return None

    draw_tool = turtle.Turtle()
    draw_tool.screen.colormode(255)

    langs_details = {lang:
                         {'count': langs_from_user.count(lang),
                          'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}
                     for lang in langs_from_user}
    step_for_legend = 0

    # рисуем сетку с процентами
    for step in range(0, 810, 32):
        if step == 0 or step % 160 == 0:
            send_cursor(draw_tool, -600 + step, -70)
            draw_tool.write(f'{int(step * 100 / 800)}%')

            draw_tool.pensize(2)
        else:
            draw_tool.pensize(1)

        send_cursor(draw_tool, -600 + step, -40)
        draw_tool.left(90)
        draw_tool.fd(180)
        draw_tool.right(90)

    draw_tool.pensize(0)
    send_cursor_home(draw_tool)
    send_cursor(draw_tool, -600, 0)
    one_piece = 800 / len(langs_from_user)
    distance = 0

    # рисуем диаграмму
    for lang, details in langs_details.items():
        rectangle_length = one_piece * details.get('count')

        draw_tool.pencolor(details.get('color'))
        draw_tool.fillcolor(details.get('color'))
        draw_tool.begin_fill()

        for line_length in (rectangle_length, 100, rectangle_length, 100):
            draw_tool.fd(line_length)
            draw_tool.left(90)

        draw_tool.end_fill()
        distance += rectangle_length

        draw_legend(draw_tool, step_for_legend, lang, details.get("count"), details.get('color'), details.get('color'))
        step_for_legend += 25

        send_cursor(draw_tool, -600 + distance, 0)

    input()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Вывод графика на основании входных данных.')
    parser.add_argument('-t', '--type', choices=['1', '2'], dest='chart_type', default=1,
                        help='тип диаграммы: 1 - круговая, 2 - диаграмма в прямоугольной системе координат '
                             '(по-умолчанию type=1)')
    parser.add_argument('--lang', nargs='*',  required=True,
                        help='данные, по которым будет строиться график')

    args = parser.parse_args()

    if int(args.chart_type) == 1:
        draw_circle_chart(args.lang)
    else:
        draw_line_chart(args.lang)
