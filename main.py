import PySimpleGUI as sg
import pandas as pd
import sys
from tax_calc import optimize


def get_precision(values: dict):
    if values[1]:
        return 1
    elif values[2]:
        return 10
    elif values[3]:
        return 100
    else:
        return 1000


if __name__ == '__main__':
    radios = [
        sg.Radio("1", "group1", default=False),
        sg.Radio("10", "group1", default=False),
        sg.Radio("100", "group1", default=False),
        sg.Radio("1000", "group1", default=True),
              ]
    layout = [[sg.Text('选择xlsx文件')], [sg.Input(), sg.FileBrowse(file_types=[('表格', 'xlsx')])], [sg.Text("选择精确度")], radios, [sg.OK("确认"), sg.Cancel("取消")]]
    event, values = sg.Window(title='选择xlsx文件', layout=layout).read(
        close=True)

    if event in ["取消", None] or values[0] == values["Browse"] == "":
        sys.exit()

    if values[0] != values["Browse"]:
        sg.popup_ok("请重新运行程序，并确保在选择文件后不要手动修改其路径")
        sys.exit()

    precision = get_precision(values)
    path = values["Browse"]
    file_name = path.split("/")[-1]
    df = pd.read_excel(path)
    try:
        money_sums = df["总计"]
    except KeyError:
        raise KeyError('请确保输入的xlsx文件中存在一列名称为"总计"')
    incomes = []
    bonuses = []
    min_taxes = []
    for i, money_sum in enumerate(money_sums):
        sg.one_line_progress_meter("进度", i + 1, len(money_sums), orientation='h')
        try:
            money_sum = int(money_sum)
        except Exception:
            raise ValueError(f"无法处理第{i + 1}行数据{money_sum}")
        combination, min_tax = optimize(money_sum, precision)
        incomes.append(combination["income"])
        bonuses.append(combination["bonus"])
        min_taxes.append(min_tax)
    df["最优工资"] = incomes
    df["最优奖金"] = bonuses
    df["最优税额"] = min_taxes
    df.to_excel(f"最优方案_{file_name}")
    sg.popup_ok(f"输出文件位置与本程序位置相同，名为：最优方案_{file_name}", title="完成")
